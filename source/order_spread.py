import osmnx as ox
import folium
import networkx as nx
import pandas as pd

G = ox.graph_from_place('Chandigarh, India', network_type='drive')


m = folium.Map(location=[G.nodes[list(G.nodes)[0]]['y'], G.nodes[list(G.nodes)[0]]['x']], zoom_start=12)


for u, v in G.edges():
    if 'geometry' in G[u][v]:
        geometry = G[u][v]['geometry']
        folium.PolyLine([(p.y, p.x) for p in geometry.coords], color='blue').add_to(m)

df = pd.read_csv('compute.csv', usecols=[1,2])



for index, row in df.iterrows():
    folium.Marker(
        location=[row[1], row[0]],
        popup=f"Latitude: {row[1]}, Longitude: {row[0]}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)


m.save('map_with_points.html')

print("Map saved as 'map_with_points.html'. Open it in a browser to view.")

import webbrowser
webbrowser.open("map_with_points.html")
