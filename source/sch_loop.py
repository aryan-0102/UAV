import pandas as pd
from datetime import datetime, timedelta
import itertools
import csv

def enhanced_scheduler(input_file, vehicles_config, speed=40):
    df = pd.read_csv(input_file)
    df['OrderDateTime'] = pd.to_datetime(df['Time'], format='%H:%M')

    hubs = {hub: [{'busy_until': None} for _ in range(vehicles_config.get(hub, 1))]
            for hub in ['A', 'B', 'C', 'D']}

    results = []
    speed_mps = speed * 1000 / 3600

    for hub in hubs:
        hub_orders = df[df['NearestHub'] == hub].sort_values('OrderDateTime')

        for _, order in hub_orders.iterrows():
            order_time = order['OrderDateTime']
            distance = order['Distance(meters)']

            best_vehicle = min(hubs[hub], key=lambda v: v['busy_until'] or datetime.min)

            wait_time = max(timedelta(0), (best_vehicle['busy_until'] or order_time) - order_time)
            travel_time = timedelta(seconds=distance / speed_mps)
            delivery_time = order_time + wait_time + travel_time

            best_vehicle['busy_until'] = delivery_time + travel_time

            results.append({
                'WaitMinutes': wait_time.total_seconds() / 60,
                'TravelMinutes': travel_time.total_seconds() / 60,
                'TotalMinutes': (delivery_time - order_time).total_seconds() / 60,
            })

    return pd.DataFrame(results)

def find_optimal_configuration():
    SPEED = 40
    best_abc = {'config': None, 'total_time': float('inf'), 'travel_time': float('inf')}
    worst_abc = {'config': None, 'total_time': 0, 'travel_time': 0}
    best_dij = {'config': None, 'total_time': float('inf'), 'travel_time': float('inf')}
    worst_dij = {'config': None, 'total_time': 0, 'travel_time': 0}

    csv_filename = 'configuration_results.csv'
    csv_header = ['Config_A', 'Config_B', 'Config_C', 'Config_D',
                  'ABC_Total_Time', 'ABC_Travel_Time',
                  'Dijkstra_Total_Time', 'Dijkstra_Travel_Time']

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_header)

        total_configs = 10000
        for i, config in enumerate(itertools.product(range(1, 11), repeat=4), 1):
            vehicles_config = dict(zip(['A', 'B', 'C', 'D'], config))

            abc_results = enhanced_scheduler('abc_distances1000_with_time.csv', vehicles_config, SPEED)
            abc_total = abc_results['TotalMinutes'].sum()
            abc_travel = abc_results['TravelMinutes'].sum()

            dij_results = enhanced_scheduler('dijkstra.csv', vehicles_config, SPEED)
            dij_total = dij_results['TotalMinutes'].sum()
            dij_travel = dij_results['TravelMinutes'].sum()

            csv_writer.writerow(list(config) + [abc_total, abc_travel, dij_total, dij_travel])

            # Update best and worst configurations
            if abc_total < best_abc['total_time']:
                best_abc = {'config': vehicles_config, 'total_time': abc_total, 'travel_time': abc_travel}
            if abc_total > worst_abc['total_time']:
                worst_abc = {'config': vehicles_config, 'total_time': abc_total, 'travel_time': abc_travel}

            if dij_total < best_dij['total_time']:
                best_dij = {'config': vehicles_config, 'total_time': dij_total, 'travel_time': dij_travel}
            if dij_total > worst_dij['total_time']:
                worst_dij = {'config': vehicles_config, 'total_time': dij_total, 'travel_time': dij_travel}

            # Print progress every 100 iterations
            if i % 100 == 0:
                print(f"Processed {i}/{total_configs} configurations")

    print(f"\nResults saved to {csv_filename}")
    return best_abc, worst_abc, best_dij, worst_dij

# Main execution
if __name__ == "__main__":
    best_abc, worst_abc, best_dij, worst_dij = find_optimal_configuration()

    print("\n=== ABC Algorithm ===")
    print("Best Configuration:")
    print(f"Vehicles: {best_abc['config']}")
    print(f"Total Delivery Time: {best_abc['total_time']:.2f} mins")
    print(f"Total Travel Time: {best_abc['travel_time']:.2f} mins")
    print("\nWorst Configuration:")
    print(f"Vehicles: {worst_abc['config']}")
    print(f"Total Delivery Time: {worst_abc['total_time']:.2f} mins")
    print(f"Total Travel Time: {worst_abc['travel_time']:.2f} mins")

    print("\n=== Dijkstra Algorithm ===")
    print("Best Configuration:")
    print(f"Vehicles: {best_dij['config']}")
    print(f"Total Delivery Time: {best_dij['total_time']:.2f} mins")
    print(f"Total Travel Time: {best_dij['travel_time']:.2f} mins")
    print("\nWorst Configuration:")
    print(f"Vehicles: {worst_dij['config']}")
    print(f"Total Delivery Time: {worst_dij['total_time']:.2f} mins")
    print(f"Total Travel Time: {worst_dij['travel_time']:.2f} mins")
