import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# ============================ comparing shortest distances ==============================================
# Load the data from the CSV files
abc_data = pd.read_csv('abc_distances1000.csv')
bellman_data = pd.read_csv('bellman.csv')
dijkstra_data = pd.read_csv('dijkstra.csv')
a_star_data = pd.read_csv('a_star.csv')

# Set the style for all plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Comparison 1: ABC vs Bellman-Ford
plt.figure()
sns.lineplot(x=abc_data.index, y=abc_data['ShortestDistance'], label='ABC')
sns.lineplot(x=bellman_data.index, y=bellman_data['ShortestDistance'], label='Bellman-Ford')
plt.title('ABC vs Bellman-Ford', fontsize=16)
plt.xlabel('Data Point Index', fontsize=14)
plt.ylabel('Shortest Distance', fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('abc_vs_bellman.png', dpi=300)
plt.close()

# Comparison 2: ABC vs Dijkstra
plt.figure()
sns.lineplot(x=abc_data.index, y=abc_data['ShortestDistance'], label='ABC')
sns.lineplot(x=dijkstra_data.index, y=dijkstra_data['ShortestDistance'], label='Dijkstra')
plt.title('ABC vs Dijkstra', fontsize=16)
plt.xlabel('Data Point Index', fontsize=14)
plt.ylabel('Shortest Distance', fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('abc_vs_dijkstra.png', dpi=300)
plt.close()

# Comparison 3: ABC vs A*
plt.figure()
sns.lineplot(x=abc_data.index, y=abc_data['ShortestDistance'], label='ABC')
sns.lineplot(x=a_star_data.index, y=a_star_data['ShortestDistance'], label='A*')
plt.title('ABC vs A*', fontsize=16)
plt.xlabel('Data Point Index', fontsize=14)
plt.ylabel('Shortest Distance', fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('abc_vs_astar.png', dpi=300)
plt.close()

# Comparison 4: All algorithms together
plt.figure()
sns.lineplot(x=abc_data.index, y=abc_data['ShortestDistance'], label='ABC')
sns.lineplot(x=bellman_data.index, y=bellman_data['ShortestDistance'], label='Bellman-Ford')
sns.lineplot(x=dijkstra_data.index, y=dijkstra_data['ShortestDistance'], label='Dijkstra')
sns.lineplot(x=a_star_data.index, y=a_star_data['ShortestDistance'], label='A*')
plt.title('Comparison of All Algorithms', fontsize=16)
plt.xlabel('Data Point Index', fontsize=14)
plt.ylabel('Shortest Distance', fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('all_algorithms_comparison.png', dpi=300)
plt.close()

print("All plots have been saved with 300 DPI.")


# ===============================================================================================


