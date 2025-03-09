import osmnx as ox
import folium
import networkx as nx
import numpy as np
import pandas as pd

# Define the central hub coordinates with names
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

    return nearest_hub_name, nearest_distance_km


def plot_route(G, user_location, nearest_hub_name):
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
        folium.Marker(hub, popup=f"Hub {name}", icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(user_location, popup="User Location", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(hub_coordinates[nearest_hub_name], popup=f"Nearest Hub {nearest_hub_name}",
                  icon=folium.Icon(color="green")).add_to(m)

    if route:
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(route_coords, color="purple", weight=3).add_to(m)

    m.save("chandigarh_route_map.html")

    return route_coords


def save_to_csv(user_location, nearest_hub_name, distance_km):
    data = {
        'Latitude': [user_location[0]],
        'Longitude': [user_location[1]],
        'Nearest Hub': [nearest_hub_name],
        'Distance (km)': [distance_km]
    }
    df = pd.DataFrame(data)
    df.to_csv('nearest_hub_data.csv', index=False)


def main():
    user_lat, user_lon = get_user_input()
    user_location = (user_lat, user_lon)

    G = download_street_network()

    for u, v, data in G.edges(data=True):
        if 'length' not in data:
            data['length'] = 0  # Assign a default length if missing

    nearest_hub_name, nearest_distance_km = calculate_nearest_hub(G, user_location)

    print(f"Nearest Hub: {nearest_hub_name} - Distance: {nearest_distance_km} km")

    route_coords = plot_route(G, user_location, nearest_hub_name)

    save_to_csv(user_location, nearest_hub_name, nearest_distance_km)

    import webbrowser
    webbrowser.open("chandigarh_route_map.html")


if __name__ == "__main__":
    main()

    30.716166
    76.772845
