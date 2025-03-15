import pandas as pd

files = [100,200,300,400,500,1000]
distance = []
for file in files:
    data = (f'abc_distances{file}.csv')
    df = pd.read_csv(data)
    distance.append(df['Distance(meters)'].sum()/1000)
print(distance)



# List of distances to process
distances = [100, 200, 300, 400, 500, 1000]

# Dictionary to store the data from each file
data_dict = {}

# Process each file
for distance in distances:
    # Construct the filename
    filename = f"abc_distances{distance}.csv"

    try:
        # Read the CSV file
        df = pd.read_csv(filename)

        # Extract the Distance(meters) column
        if 'Distance(meters)' in df.columns:
            # Use the filename (without extension) as the column name
            column_name = f"distances{distance}"

            # Add the distance values to the dictionary
            data_dict[column_name] = df['Distance(meters)'].values
        else:
            print(f"Warning: 'Distance(meters)' column not found in {filename}")

    except FileNotFoundError:
        print(f"Warning: File {filename} not found")

# Create a DataFrame from the dictionary
# Note: If files have different numbers of rows, shorter columns will be filled with NaN
combined_data = pd.DataFrame(data_dict)

# Save the combined data to a new CSV file
combined_data.to_csv("combined_distances_abc.csv", index=False)

print("Combined data saved to combined_distances.csv")
