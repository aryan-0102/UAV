import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
# Calculate mass distances ---------

hub_coordinates = {
    'A': (30.724913, 76.787800),
    'B': (30.746120, 76.769660),
    'C': (30.727379, 76.725188),
    'D': (30.700463, 76.755896)
}


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

    distances_km = {name: distance for name, distance in distances_meters.items()}
    sorted_names = sorted(distances_km, key=lambda name: distances_km[name])
    nearest_hub_name = sorted_names[0]
    nearest_distance_km = distances_km[nearest_hub_name]

    return nearest_hub_name, nearest_distance_km, distances_km



customer_data = pd.read_csv('customer_data.csv')


graph = ox.graph_from_place('Chandigarh, India', network_type='drive')


names = []
longitudes = []
latitudes = []
order_values = []
nearest_hubs = []
shortest_distances = []
routes = []


for index, row in customer_data.iterrows():
    name = row['Location']
    longitude = row['Longitude']
    latitude = row['Latitude']


    try:
        order_value = row['OrderValue']
    except KeyError:
        print("Column 'OrderValue' does not exist. Setting to None.")
        order_value = None


    nearest_hub_name, nearest_distance_km, distances_km = calculate_nearest_hub(graph, (latitude, longitude))


    user_node = ox.distance.nearest_nodes(graph, longitude, latitude)
    hub_node = ox.distance.nearest_nodes(graph, hub_coordinates[nearest_hub_name][1],
                                         hub_coordinates[nearest_hub_name][0])

    try:
        shortest_path = nx.shortest_path(graph, user_node, hub_node, weight='length')
        route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]
        route_str = ';'.join(f"({lat},{lng})" for lat, lng in route_coords)
    except nx.NetworkXNoPath:
        route_str = None


    names.append(name)
    longitudes.append(longitude)
    latitudes.append(latitude)
    order_values.append(order_value)
    nearest_hubs.append(nearest_hub_name)
    shortest_distances.append(nearest_distance_km)
    routes.append(route_str)


results_df = pd.DataFrame({
    'Location': names,
    'Longitude': longitudes,
    'Latitude': latitudes,
    'OrderValue': order_values,
    'NearestHub': nearest_hubs,
    'ShortestDistance': shortest_distances,
    'Route': routes
})

results_df.to_csv('compute.csv', index=False)

print("Results saved to compute.csv")
