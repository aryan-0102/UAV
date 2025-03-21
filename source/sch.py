import pandas as pd
from datetime import datetime, timedelta


def enhanced_dynamic_scheduler():
    # Configuration
    input_files = {
        'ABC': 'abc_distances1000_with_time.csv',
        'Dijkstra': 'dijkstra.csv'
    }

    vehicles_config = {
        'A': 4,  # Industrial zone hub
        'B': 3,  # Commercial district hub
        'C': 1,  # Residential area hub
        'D': 1  # Special zone hub
    }

    speed_kmh = 40  # Standard delivery speed

    # Process both algorithms
    for algo, input_file in input_files.items():
        print(f"\nProcessing {algo} algorithm...")

        # Load and prepare data
        df = pd.read_csv(input_file)
        df['OrderDateTime'] = pd.to_datetime(df['Time'], format='%H:%M')

        # Initialize performance tracking
        performance_data = []
        hubs = {hub: [] for hub in vehicles_config}

        # Initialize vehicles
        for hub, count in vehicles_config.items():
            hubs[hub] = [{
                'id': f"{hub}-{i + 1}",
                'busy_until': None,
                'utilization': timedelta(0)
            } for i in range(count)]

        # Process orders chronologically
        df = df.sort_values('OrderDateTime')
        for _, row in df.iterrows():
            hub = row['NearestHub']
            order_time = row['OrderDateTime']
            distance = row['Distance(meters)']

            # Find best available vehicle
            vehicle = min(
                hubs[hub],
                key=lambda x: x['busy_until'] or datetime.min
            )

            # Calculate timeline
            wait_time = vehicle['busy_until'] - order_time if vehicle['busy_until'] else timedelta(0)
            travel_time = timedelta(seconds=distance / (speed_kmh * 1000 / 3600))

            departure_time = max(order_time, vehicle['busy_until'] or order_time)
            return_time = departure_time + 2 * travel_time  # Round trip

            # Update vehicle status
            vehicle['busy_until'] = return_time
            vehicle['utilization'] += 2 * travel_time  # Track both-way utilization

            # Record metrics
            performance_data.append({
                'Algorithm': algo,
                'Location': row['Location'],
                'Hub': hub,
                'OrderTime': order_time.strftime('%H:%M'),
                'WaitMinutes': wait_time.total_seconds() / 60,
                'TravelMinutes': travel_time.total_seconds() / 60,
                'TotalMinutes': (return_time - order_time).total_seconds() / 60,
                'VehicleID': vehicle['id']
            })

        # Save results
        output_file = f"optimized_schedule_{algo.lower()}_v{sum(vehicles_config.values())}.csv"
        pd.DataFrame(performance_data).to_csv(output_file, index=False)
        print(f"Saved {len(performance_data)} orders to {output_file}")

        # Print performance summary
        total_time = sum(item['TotalMinutes'] for item in performance_data)
        avg_time = total_time / len(performance_data)

        print(f"\n{algo} Performance Summary:")
        print(f"Total Delivery Time: {total_time:.2f} minutes")
        print(f"Average Delivery Time: {avg_time:.2f} minutes")
        print("Vehicle Utilization:")
        for hub in vehicles_config:
            util = sum((v['utilization'].total_seconds() / 3600) for v in hubs[hub])
            print(f"  {hub}: {util:.2f} hours")


# Execute the enhanced scheduler
if __name__ == "__main__":
    enhanced_dynamic_scheduler()
