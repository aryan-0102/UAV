import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('dijkstra.csv', usecols=[4,5])
df2 = pd.read_csv('customer_data.csv', usecols=[3])

plt.scatter(df['ShortestDistance'],df2)

plt.xlabel('Shortest Distance')
plt.ylabel('Order Value')
plt.title('Simple Scatter Plot')

plt.show()

df2['NearestHub'] = df['NearestHub']

# Group order values by hubs
order_values_by_hub = df2.groupby('NearestHub')['OrderValue'].apply(list)


plt.figure(figsize=(8, 6))


colors = {'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'orange'}

for hub, values in order_values_by_hub.items():
    plt.scatter([hub] * len(values), values, color=colors[hub], label=f'Hub {hub}')


plt.xlabel('Nearest Hub')
plt.ylabel('Order Value')
plt.title('Order Value vs Nearest Hub')
plt.legend()
plt.show()

mean_values = df2.groupby('NearestHub')['OrderValue'].mean()  # Calculate mean
median_values = df2.groupby('NearestHub')['OrderValue'].median()  # Calculate median

# Combine mean and median into a summary statistics DataFrame
summary_stats = pd.DataFrame({
    'Mean': mean_values,
    'Median': median_values
})

print(summary_stats)
