import osmnx as ox
import networkx as nx
import folium
import os
import webbrowser
# Define hub coordinates and destination
hub_coordinates = {
    'A': (30.724913, 76.787800),
    'B': (30.746120, 76.769660),
    'C': (30.727379, 76.725188),
    'D': (30.700463, 76.755896)
}

destination = (30.737613, 76.742474)

# Fetch Chandigarh map using OSMnx
G = ox.graph_from_place('Chandigarh, India', network_type='drive')

# Function to find the nearest node on the graph given coordinates
def nearest_node(lat, lon):
    return ox.distance.nearest_nodes(G, lon, lat)

# Find nearest nodes for hubs and destination
hub_nodes = {hub: nearest_node(*coords) for hub, coords in hub_coordinates.items()}
destination_node = nearest_node(*destination)

# Calculate shortest distances from each hub to the destination
distances = {}
routes = {}
for hub, hub_node in hub_nodes.items():
    try:
        distance = nx.shortest_path_length(G, source=hub_node, target=destination_node, weight='length')
        route = nx.shortest_path(G, source=hub_node, target=destination_node, weight='length')
        distances[hub] = distance
        routes[hub] = route
    except nx.NetworkXNoPath:
        distances[hub] = float('inf')
        routes[hub] = []

# Find the hub with the shortest distance
shortest_hub = min(distances, key=distances.get)
shortest_distance = distances[shortest_hub]
shortest_route = routes[shortest_hub]

# Extract coordinates for the shortest route
shortest_route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_route]

# Initialize a Folium map centered around Chandigarh
m = folium.Map(location=[30.7333, 76.7794], zoom_start=13)

# Add the shortest route to the map
folium.PolyLine(shortest_route_coords, color='blue', weight=2.5, opacity=1).add_to(m)

# Add markers for the starting hub and destination
folium.Marker(location=shortest_route_coords[0], popup=f"Hub {shortest_hub}\nDistance: {shortest_distance:.2f} meters", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=shortest_route_coords[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)

# Save the map to an HTML file
map_filename = "shortest_route_map_abc.html"
m.save(map_filename)

webbrowser.open("shortest_route_map_abc.html")