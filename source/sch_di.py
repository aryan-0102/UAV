import pandas as pd
from datetime import datetime, timedelta


def process_deliveries(input_file, output_file):
    # Read CSV data
    df = pd.read_csv(input_file)

    # Convert order time to datetime
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time
    df['OrderDateTime'] = pd.to_datetime(df['Time'].astype(str))

    # Initialize hubs with availability times
    hubs = {
        'A': {'available_at': None},
        'B': {'available_at': None},
        'C': {'available_at': None},
        'D': {'available_at': None}
    }

    # Constants
    SPEED_MPS = 40000 / 3600  # 40 km/h to m/s
    results = []

    # Process orders hub-wise in FCFS order
    for hub in hubs:
        hub_orders = df[df['NearestHub'] == hub].sort_values('OrderDateTime')

        for _, order in hub_orders.iterrows():
            order_time = order['OrderDateTime']
            distance = order['ShortestDistance']

            # Calculate travel duration
            travel_seconds = distance / SPEED_MPS
            travel_time = timedelta(seconds=travel_seconds)

            # Calculate wait time
            if hubs[hub]['available_at'] is None or order_time > hubs[hub]['available_at']:
                wait_time = timedelta(0)
                departure_time = order_time
            else:
                wait_time = hubs[hub]['available_at'] - order_time
                departure_time = hubs[hub]['available_at']
    
            # Calculate delivery timeline
            arrival_time = departure_time + travel_time
            return_time = arrival_time + travel_time  # Return trip

            # Update hub availability
            hubs[hub]['available_at'] = return_time

            # Store results
            results.append({
                'Location': order['Location'],
                'NearestHub': hub,
                'Distance(meters)': distance,
                'OrderTime': order['Time'].strftime('%H:%M'),
                'WaitTimeMinutes': round(wait_time.total_seconds() / 60, 2),
                'DepartureTime': departure_time.strftime('%H:%M:%S'),
                'ArrivalTime': arrival_time.strftime('%H:%M:%S'),
                'DeliveryCompleteTime': arrival_time.strftime('%H:%M:%S')
            })

    # Create and save output
    result_df = pd.DataFrame(results)
    result_df = result_df[[
        'Location', 'NearestHub', 'Distance(meters)', 'OrderTime',
        'WaitTimeMinutes', 'DepartureTime', 'ArrivalTime', 'DeliveryCompleteTime'
    ]]

    # Calculate total delivery time and average
    result_df['OrderDateTime'] = pd.to_datetime(result_df['OrderTime'], format='%H:%M')
    result_df['DeliveryCompleteDateTime'] = pd.to_datetime(result_df['DeliveryCompleteTime'], format='%H:%M:%S')
    result_df['TotalDeliveryTimeMinutes'] = (result_df['DeliveryCompleteDateTime'] - result_df[
        'OrderDateTime']).dt.total_seconds() / 60

    total_delivery_time = result_df['TotalDeliveryTimeMinutes'].sum()
    average_delivery_time = result_df['TotalDeliveryTimeMinutes'].mean()

    result_df.to_csv(output_file, index=False)

    # Print total and average delivery times
    print(f"Total Delivery Time: {total_delivery_time:.2f} minutes")
    print(f"Average Delivery Time: {average_delivery_time:.2f} minutes")


# Run the processor with input and output files
if __name__ == "__main__":
    input_file = "dijkstra.csv"  # Replace with your input file name
    output_file = "delivery_schedule_dijkstra.csv"  # Replace with your desired output file name

    process_deliveries(input_file, output_file)
