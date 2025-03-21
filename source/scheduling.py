import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def enhanced_scheduler(input_file, vehicles_config, speed=40):
    """Enhanced scheduling engine with multi-algorithm support"""
    df = pd.read_csv(input_file)
    df['OrderDateTime'] = pd.to_datetime(df['Time'], format='%H:%M')

    hubs = {hub: [{'busy_until': None} for _ in range(vehicles_config.get(hub, 1))]
            for hub in ['A', 'B', 'C', 'D']}

    results = []
    speed_mps = speed * 1000 / 3600  # Convert to m/s

    for hub in hubs:
        hub_orders = df[df['NearestHub'] == hub].sort_values('OrderDateTime')

        for _, order in hub_orders.iterrows():
            order_time = order['OrderDateTime']
            distance = order['Distance(meters)']

            # Find best available vehicle
            best_vehicle = min(
                hubs[hub],
                key=lambda v: v['busy_until'] or datetime.min
            )

            # Calculate timeline components
            wait_time = max(timedelta(0), (best_vehicle['busy_until'] or order_time) - order_time)
            travel_time = timedelta(seconds=distance / speed_mps)
            departure_time = order_time + wait_time
            delivery_time = departure_time + travel_time

            # Update vehicle status (round trip calculation)
            best_vehicle['busy_until'] = delivery_time + travel_time

            results.append({
                'Location': order['Location'],
                'Hub': hub,
                'OrderTime': order_time.strftime('%H:%M'),
                'WaitMinutes': wait_time.total_seconds() / 60,
                'TravelMinutes': travel_time.total_seconds() / 60,
                'TotalMinutes': (delivery_time - order_time).total_seconds() / 60,
                'VehicleUsed': hubs[hub].index(best_vehicle) + 1
            })

    return pd.DataFrame(results)


def analyze_results(abc_df, dij_df):
    """Comparative performance analysis with visualization"""
    metrics = {
        'ABC': {
            'avg_wait': abc_df['WaitMinutes'].mean(),
            'avg_total': abc_df['TotalMinutes'].mean(),
            'throughput': len(abc_df) / abc_df['TotalMinutes'].max()
        },
        'Dijkstra': {
            'avg_wait': dij_df['WaitMinutes'].mean(),
            'avg_total': dij_df['TotalMinutes'].mean(),
            'throughput': len(dij_df) / dij_df['TotalMinutes'].max()
        }
    }

    # Comparative visualization
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Wait time comparison
    ax[0].bar(metrics.keys(), [m['avg_wait'] for m in metrics.values()], color=['blue', 'green'])
    ax[0].set_title('Average Wait Time Comparison')
    ax[0].set_ylabel('Minutes')

    # Total time comparison
    ax[1].bar(metrics.keys(), [m['avg_total'] for m in metrics.values()], color=['orange', 'red'])
    ax[1].set_title('Average Total Delivery Time Comparison')
    ax[1].set_ylabel('Minutes')

    plt.tight_layout()
    plt.savefig('algorithm_comparison.png', dpi=300)
    plt.show()

    return metrics


# Main execution
if __name__ == "__main__":
    # Common configuration
    VEHICLE_CONFIG = {'A': 4, 'B': 2, 'C': 1, 'D': 1}
    SPEED = 40  # km/h

    # Process ABC data
    abc_results = enhanced_scheduler(
        'abc_distances1000_with_time.csv',
        VEHICLE_CONFIG,
        SPEED
    )
    abc_results.to_csv('optimized_schedule_abc.csv', index=False)

    # Process Dijkstra data
    dij_results = enhanced_scheduler(
        'dijkstra.csv',
        VEHICLE_CONFIG,
        SPEED
    )
    dij_results.to_csv('optimized_schedule_dij.csv', index=False)

    # Comparative analysis
    metrics = analyze_results(abc_results, dij_results)

    # Print summary
    print("Algorithm Performance Summary:\n")
    for algo, data in metrics.items():
        print(f"{algo}:")
        print(f"  Average Wait Time: {data['avg_wait']:.2f} mins")
        print(f"  Average Total Time: {data['avg_total']:.2f} mins")
        print(f"  Throughput: {data['throughput']:.2f} orders/min\n")
