import pandas as pd

# Load the data from the CSV files
abc_data = pd.read_csv('abc_distances1000.csv')
bellman_data = pd.read_csv('bellman.csv')
dijkstra_data = pd.read_csv('dijkstra.csv')
a_star_data = pd.read_csv('a_star.csv')


# Create a new DataFrame with the ShortestDistance columns
combined_distances = pd.DataFrame({
    'abc_distances1000': abc_data['ShortestDistance'],
    'bellman': bellman_data['ShortestDistance'],
    'dijkstra': dijkstra_data['ShortestDistance'],
    'a_star': a_star_data['ShortestDistance']
})
def find_shortest(row):
    min_value = row.min()
    min_columns = row[row == min_value].index.tolist()
    if len(min_columns) > 1:
        return 'tie'
    return min_columns[0]  # Return the first (and only) element

combined_distances['shortest'] = combined_distances.apply(find_shortest, axis=1)
# Save the combined DataFrame to a new CSV file
combined_distances.to_csv('combined_distances.csv', index=False)

