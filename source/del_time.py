import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV files
file_dijkstra = 'optimized_schedule_dijkstra_v9.csv'
file_abc = 'optimized_schedule_abc_v9.csv'

# Read the CSV files
df_dijkstra = pd.read_csv(file_dijkstra)
df_abc = pd.read_csv(file_abc)

# Extract relevant columns (assuming the columns are named 'TotalMinutes' and 'TravelMinutes')
df_dijkstra = df_dijkstra[['TotalMinutes', 'TravelMinutes']]
df_abc = df_abc[['TotalMinutes', 'TravelMinutes']]


# Calculate and print the average, maximum, and difference for both TotalMinutes and TravelMinutes
def print_time_stats(df, source_name):
    total_minutes_avg = df['TotalMinutes'].mean()
    total_minutes_max = df['TotalMinutes'].max()
    travel_minutes_avg = df['TravelMinutes'].mean()
    travel_minutes_max = df['TravelMinutes'].max()

    total_minutes_diff = total_minutes_max - total_minutes_avg
    travel_minutes_diff = travel_minutes_max - travel_minutes_avg

    print(f"\n{source_name} Schedule:")
    print(f"Average TotalMinutes: {total_minutes_avg:.2f}")
    print(f"Max TotalMinutes: {total_minutes_max}")
    print(f"Difference in TotalMinutes: {total_minutes_diff:.2f}")

    print(f"Average TravelMinutes: {travel_minutes_avg:.2f}")
    print(f"Max TravelMinutes: {travel_minutes_max}")
    print(f"Difference in TravelMinutes: {travel_minutes_diff:.2f}")


# Print stats for both datasets
print_time_stats(df_dijkstra, "Dijkstra")
print_time_stats(df_abc, "ABC")

# Line plot for TravelMinutes comparison
plt.figure(figsize=(10, 6))

plt.plot(df_dijkstra['TravelMinutes'], label='Dijkstra TravelMinutes', color='blue', linestyle='-')
plt.plot(df_abc['TravelMinutes'], label='ABC TravelMinutes', color='green', linestyle='-')

plt.title('TravelMinutes Comparison: Dijkstra vs. ABC')
plt.xlabel('Index')
plt.ylabel('TravelMinutes')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig('delivery.png', dpi=300)
plt.show()