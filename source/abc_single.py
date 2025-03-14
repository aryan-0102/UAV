import pandas as pd
import numpy as np
import osmnx as ox
import networkx as nx
import folium


hubs = {
    'A': (30.724913, 76.787800),
    'B': (30.746120, 76.769660),
    'C': (30.727379, 76.725188),
    'D': (30.700463, 76.755896)
}


user_lat, user_lon = 30.737613, 76.742474


print("Fetching Chandigarh map...")
G = ox.graph_from_place('Chandigarh, India', network_type='drive')


def nearest_node(lat, lon):
    return ox.distance.nearest_nodes(G, lon, lat)


hub_nodes = {hub: nearest_node(*coords) for hub, coords in hubs.items()}


user_node = nearest_node(user_lat, user_lon)


distances_to_hubs = {}

for hub_name, hub_node in hub_nodes.items():
    try:
        distance = nx.shortest_path_length(G, source=hub_node, target=user_node, weight='length')
    except nx.NetworkXNoPath:
        distance = float('inf')

    distances_to_hubs[hub_name] = distance


class ABCAlgorithm:
    def __init__(self, distances_to_hubs, n_bees=10, max_iter=100):
        self.distances_to_hubs = distances_to_hubs
        self.hubs = list(distances_to_hubs.keys())
        self.n_bees = n_bees
        self.max_iter = max_iter
        self.best_solution = None
        self.best_cost = float('inf')

    def initialize_population(self):
        return [np.random.choice(self.hubs) for _ in range(self.n_bees)]

    def evaluate_fitness(self, solution):
        return self.distances_to_hubs[solution]

    def run(self):
        print("Running ABC optimization...")
        population = self.initialize_population()

        for iteration in range(self.max_iter):
            fitness_values = [self.evaluate_fitness(sol) for sol in population]

            # Update best solution found so far
            min_idx = np.argmin(fitness_values)
            if fitness_values[min_idx] < self.best_cost:
                self.best_cost = fitness_values[min_idx]
                self.best_solution = population[min_idx]

            # Employed bees phase (local search)
            for i in range(self.n_bees):
                new_sol = np.random.choice(self.hubs)
                if self.evaluate_fitness(new_sol) < fitness_values[i]:
                    population[i] = new_sol

            # Onlooker bees phase (probabilistic selection based on fitness)
            fitness_inv = [1/f if f > 0 else 0 for f in fitness_values]
            probs_sum = np.sum(fitness_inv)
            probs = fitness_inv / probs_sum if probs_sum > 0 else np.ones(self.n_bees) / self.n_bees

            for i in range(self.n_bees):
                selected_idx = np.random.choice(range(self.n_bees), p=probs)
                new_sol = np.random.choice(self.hubs)
                if self.evaluate_fitness(new_sol) < fitness_values[selected_idx]:
                    population[selected_idx] = new_sol


            worst_idx = np.argmax(fitness_values)
            population[worst_idx] = np.random.choice(self.hubs)

        print("ABC optimization completed.")
        return self.best_solution

abc_solver = ABCAlgorithm(distances_to_hubs)
nearest_hub = abc_solver.run()


try:
    route = nx.shortest_path(G, source=hub_nodes[nearest_hub], target=user_node, weight='length')
except nx.NetworkXNoPath:
    route = []

route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]


distance_to_display = distances_to_hubs[nearest_hub]


m = folium.Map(location=[user_lat, user_lon], zoom_start=15)

folium.PolyLine(route_coords, color='blue').add_to(m)

folium.Marker([user_lat, user_lon], popup='User Location').add_to(m)
folium.Marker(hubs[nearest_hub], popup=f'Nearest Hub: {nearest_hub} - Distance: {distance_to_display:.2f} meters').add_to(m)


m.save('route_map.html')
import webbrowser

webbrowser.open('route_map.html')
