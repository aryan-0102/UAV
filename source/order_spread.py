#!/usr/bin/env python3
import pandas as pd
import folium
import osmnx as ox

# Load the CSV file
customer_data = pd.read_csv('customer_data.csv')

# Extract latitude and longitude
latitudes = customer_data['Latitude']
longitudes = customer_data['Longitude']

# Create a map centered on Chandigarh
m = folium.Map(location=[30.7333, 76.7794], zoom_start=12)

# Plot points
for lat, lon in zip(latitudes, longitudes):
    folium.Marker([lat, lon], radius=2).add_to(m)

# Save the map as an HTML file
m.save('customer_points_map.html')




import webbrowser
webbrowser.open("customer_points_map.html")
