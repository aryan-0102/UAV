import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Create a DataFrame with the statistics
algorithms = ['Dijkstra', 'Astar',  'ABC']
avg_values = [36.43, 37.82, 140.41]
max_values = [38.48, 38.12, 145.80]
min_values = [36.04, 37.62, 138.23]

# Reshape data for seaborn
data = pd.DataFrame({
    'Algorithm': np.repeat(algorithms, 3),
    'Statistic': np.tile(['Average', 'Maximum', 'Minimum'], 3),
    'Value': np.concatenate([
        np.array([avg_values[0], max_values[0], min_values[0]]),
        np.array([avg_values[1], max_values[1], min_values[1]]),
        np.array([avg_values[2], max_values[2], min_values[2]])
    ])
})

# Set the style and figure size
sns.set_style("whitegrid")
plt.figure(figsize=(12, 8))

# Create the grouped bar plot with seaborn
ax = sns.barplot(
    x='Algorithm',
    y='Value',
    hue='Statistic',
    data=data,
    palette='viridis'
)

# Add annotations to each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', fontsize=10)

# Customize the plot
plt.title('Performance Comparison of Path-Finding Algorithms', fontsize=18, pad=20)
plt.xlabel('Algorithms', fontsize=14, labelpad=10)
plt.ylabel('Time (sec)', fontsize=14, labelpad=10)
plt.legend(title='Statistics', title_fontsize=12, fontsize=10)

# Adjust y-axis to start from 0
plt.ylim(0, max(max_values) * 1.15)

# Add a subtle border
for spine in ax.spines.values():
    spine.set_edgecolor('#CCCCCC')
    spine.set_linewidth(1)

# Customize tick parameters
plt.tick_params(axis='both', which='major', labelsize=12)

# Show the plot
plt.tight_layout()
# After creating your plot, before plt.show()
plt.savefig('all_time_300dpi.png', dpi=300, bbox_inches='tight')
plt.show()

