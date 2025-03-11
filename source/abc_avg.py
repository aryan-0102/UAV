import pandas as pd
import matplotlib.pyplot as plt

# List of iteration numbers
names = [100, 200, 300, 400, 500, 1000]

# Initialize an empty list to store DataFrames
dataframes = []

# Read CSV files into DataFrames
for i in names:
    filename = f'abc_distances{i}.csv'
    dataframes.append(pd.read_csv(filename))


df100, df200, df300, df400, df500, df1000 = dataframes


df_names = [df100, df200, df300, df400, df500, df1000]


for i, df in zip(names, df_names):
    label = f'{i} Iterations'
    if 'Distance(meters)' in df.columns:  # Ensure the column exists
        plt.plot(df['Distance(meters)'], linestyle='-', label=label)
    else:
        print(f"Column 'Distance(meters)' not found in DataFrame {i}")


plt.legend()
plt.grid(True)
plt.xlabel('Index')
plt.ylabel('Distance (meters)')
plt.title('Distance vs Iterations')
plt.show()

mean_distances = {}
for name, df in zip(names, df_names):
    if 'Distance(meters)' in df.columns:  # Ensure the column exists
        mean_distances[f'df_{name}'] = df['Distance(meters)'].mean()
        print(f"Mean distance for df_{name}: {mean_distances[f'df_{name}']}")
    else:
        print(f"Column 'Distance(meters)' not found in DataFrame {name}")


keys = list(mean_distances.keys())
values = list(mean_distances.values())


plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.plot(keys, values,marker='o', color='red',ls ='-')
plt.xlabel('No of Iterations', fontsize=12)
plt.ylabel('Mean Distance (meters)', fontsize=12)
plt.title('Mean Distances V/S No. of Iterations', fontsize=14)
for x, y in zip(keys, values):
    plt.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()