import osmnx as ox
import folium
import networkx as nx
import numpy as np
import pandas as pd

#mass plotter

hub_coordinates = {
    'A': (30.724913, 76.787800),
    'B': (30.746120, 76.769660),
    'C': (30.727379, 76.725188),
    'D': (30.700463, 76.755896)
}


def get_user_input():
    user_lat = float(input("Enter the latitude of your location: "))
    user_lon = float(input("Enter the longitude of your location: "))
    return user_lat, user_lon


def download_street_network():
    return ox.graph_from_place('Chandigarh, India', network_type='drive')


def calculate_nearest_hub(G, user_location):
    user_node = ox.distance.nearest_nodes(G, user_location[1], user_location[0])
    hub_nodes = {name: ox.distance.nearest_nodes(G, hub[1], hub[0]) for name, hub in hub_coordinates.items()}

    distances_meters = {}
    for name, hub_node in hub_nodes.items():
        try:
            distance_meters = nx.dijkstra_path_length(G, user_node, hub_node, weight='length')
            distances_meters[name] = distance_meters
        except nx.NetworkXNoPath:
            distances_meters[name] = np.inf

    distances_km = {name: distance / 1000 for name, distance in distances_meters.items()}
    sorted_names = sorted(distances_km, key=lambda name: distances_km[name])
    nearest_hub_name = sorted_names[0]
    nearest_distance_km = distances_km[nearest_hub_name]

    return nearest_hub_name, nearest_distance_km, distances_km


def plot_route(G, user_location, nearest_hub_name, nearest_distance_km, distances_km):
    user_node = ox.distance.nearest_nodes(G, user_location[1], user_location[0])
    nearest_hub_node = ox.distance.nearest_nodes(G, hub_coordinates[nearest_hub_name][1],
                                                 hub_coordinates[nearest_hub_name][0])

    try:
        route = nx.shortest_path(G, source=user_node, target=nearest_hub_node, weight="length")
    except nx.NetworkXNoPath:
        print("No path found.")
        route = []

    m = folium.Map(location=[30.7333, 76.7794], zoom_start=13)

    for name, hub in hub_coordinates.items():
        folium.Marker(hub, popup=f"Hub {name} - Distance: {distances_km[name]:.2f} km",
                      icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(user_location, popup="User Location", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(hub_coordinates[nearest_hub_name],
                  popup=f"Nearest Hub {nearest_hub_name} - Distance: {nearest_distance_km:.2f} km",
                  icon=folium.Icon(color="green")).add_to(m)

    if route:
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(route_coords, color="purple", weight=3).add_to(m)
        route_distance = sum([G[u][v][0]['length'] for u, v in zip(route[:-1], route[1:])])
        folium.Marker(route_coords[0], popup=f"Route Distance: {route_distance / 1000:.2f} km",
                      icon=folium.Icon(color="purple")).add_to(m)

    m.save("shortest_route_map_dijk.html")

    return route_coords3


def save_to_csv(user_location, nearest_hub_name, distance_km):
    data = {
        'Latitude': [user_location[0]],
        'Longitude': [user_location[1]],
        'Nearest Hub': [nearest_hub_name],
        'Distance (km)': [distance_km]
    }
    df = pd.DataFrame(data)
    df.to_csv('nearest_hub_data.csv', index=False)


def plot_all_routes(G, user_coordinates_list):
    # Create a single map centered on Chandigarh
    m = folium.Map(location=[30.7333, 76.7794], zoom_start=13)

    # Add all hub locations to the map
    for name, hub in hub_coordinates.items():
        folium.Marker(hub, popup=f"Hub {name}",
                      icon=folium.Icon(color="red")).add_to(m)

    # Process each user location
    route_colors = ['purple', 'blue', 'green', 'orange', 'darkred', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'pink']

    for i, user_location in enumerate(user_coordinates_list):
        # Get color for this route (cycle through colors if more routes than colors)
        color = route_colors[i % len(route_colors)]

        # Find nearest hub
        nearest_hub_name, nearest_distance_km, distances_km = calculate_nearest_hub(G, user_location)

        # Create detailed popup content with distances to all hubs
        popup_content = f"<b>User {i + 1}</b><br>"
        popup_content += f"<b>Nearest Hub:</b> {nearest_hub_name} ({nearest_distance_km:.2f} km)<br><br>"
        popup_content += "<b>Distances to all hubs:</b><br>"

        for hub_name, distance in sorted(distances_km.items(), key=lambda x: x[1]):
            popup_content += f"Hub {hub_name}: {distance:.2f} km<br>"

        # Add user marker with detailed distance information
        folium.Marker(
            user_location,
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"User {i + 1} - Nearest: Hub {nearest_hub_name} ({nearest_distance_km:.2f} km)",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        # Find route
        user_node = ox.distance.nearest_nodes(G, user_location[1], user_location[0])
        nearest_hub_node = ox.distance.nearest_nodes(G, hub_coordinates[nearest_hub_name][1],
                                                     hub_coordinates[nearest_hub_name][0])

        try:
            route = nx.shortest_path(G, source=user_node, target=nearest_hub_node, weight="length")
            route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

            # Calculate exact route distance
            route_distance = sum([G[u][v][0]['length'] for u, v in zip(route[:-1], route[1:])])
            route_distance_km = route_distance / 1000

            # Add route line with distance information
            folium.PolyLine(
                route_coords,
                color=color,
                weight=3,
                popup=f"User {i + 1} to Hub {nearest_hub_name}: {route_distance_km:.2f} km",
                tooltip=f"Route: {route_distance_km:.2f} km"
            ).add_to(m)

        except nx.NetworkXNoPath:
            print(f"No path found for user location {i + 1}")

    # Add a legend
    legend_html = '''
    <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 200px; height: 160px; 
         border:2px solid grey; z-index:9999; font-size:14px;
         background-color:white;
         padding: 10px;
         overflow-y: auto;
         ">
         <p><b>Legend:</b></p>
    '''

    for i in range(len(user_coordinates_list)):
        color = route_colors[i % len(route_colors)]
        legend_html += f'<p><span style="color:{color};">&#9473;&#9473;</span> User {i + 1}</p>'

    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save the map once with all routes
    m.save("all_routes_map.html")
    return m


def main():
    G = download_street_network()
    for u, v, data in G.edges(data=True):
        if 'length' not in data:
            data['length'] = 0

    df = pd.read_csv('customer_data.csv')
    user_coordinates = list(zip(df['Latitude'], df['Longitude']))

    # Create a single map with all routes
    map_with_all_routes = plot_all_routes(G, user_coordinates)

    # Process each location for data saving
    results = []
    for user_location in user_coordinates:
        nearest_hub_name, nearest_distance_km, distances_km = calculate_nearest_hub(G, user_location)
        print(f"User location: {user_location}")
        print(f"Nearest Hub: {nearest_hub_name} - Distance: {nearest_distance_km} km")

        # Save data for this user location
        results.append({
            'Latitude': user_location[0],
            'Longitude': user_location[1],
            'Nearest Hub': nearest_hub_name,
            'Distance (km)': nearest_distance_km
        })

    # Save all results at once
    df_results = pd.DataFrame(results)
    df_results.to_csv('nearest_hub_data.csv', index=False)

    # Open the map with all routes
    import webbrowser
    webbrowser.open("all_routes_map.html")


if __name__ == "__main__":
    main()