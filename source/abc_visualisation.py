import pandas as pd
import folium
import webbrowser
import os

def plot_single_row(row_data):
    # Initialize a map centered around Chandigarh
    chandigarh_map = folium.Map(location=[30.7333, 76.7794], zoom_start=13)

    # Extract data from the input row
    location = row_data['Location']
    latitude = row_data['Latitude']
    longitude = row_data['Longitude']
    nearest_hub = row_data['NearestHub']
    distance_meters = row_data['Distance(meters)']
    route_nodes = eval(row_data['Route(nodes)'])  # Convert string representation of list to actual list

    # Add a marker for the location
    folium.Marker(
        location=[latitude, longitude],
        popup=f"{location}\nNearest Hub: {nearest_hub}\nDistance: {distance_meters} meters",
        icon=folium.Icon(color='blue')
    ).add_to(chandigarh_map)

    # Add a polyline for the route (mocking coordinates for simplicity)
    if nearest_hub == 'A':
        end_point = [30.724913, 76.787800]  # Hub A coordinates
    elif nearest_hub == 'B':
        end_point = [30.746120, 76.769660]  # Hub B coordinates
    else:
        end_point = [latitude, longitude]  # Default to start point if hub not recognized

    folium.PolyLine(
        locations=[[latitude, longitude], end_point],
        color='red',
        weight=2.5,
        opacity=1
    ).add_to(chandigarh_map)

    # Save the map to an HTML file
    filename = "single_row_map.html"
    chandigarh_map.save(filename)

    # Open the map in the default web browser
    webbrowser.open('file://' + os.path.realpath(filename))

    print(f"Map for single row saved as {filename} and launched in your browser.")

# Example usage
row_data = {
    'Location': 'Elante Mall - Point 1',
    'Latitude': 30.704418817895,
    'Longitude': 76.799736963917,
    'NearestHub': 'A',
    'Distance(meters)': 3939.3538228132807,
    'Route(nodes)': "[1429417889, 1429417907, 1429417931, 1429262258, 1429141632, 1429141626, 1429141599, 1429141579, 1429380154, 1429261749, 1429141509, 1429141504, 1429141482, 1429141468, 1429261128, 1429337192, 1429141395, 1429141387, 1429141384, 1429141383, 1429141353, 1429336893, 5513120081, 5513120080, 5513120086, 1429336699, 1429336740]"
}

plot_single_row(row_data)
