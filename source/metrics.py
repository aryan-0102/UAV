import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def analyze_distance_matrix(file_path):

    df = pd.read_csv(file_path, index_col=0)


    values = df.values.flatten()
    values = values[values != 0]


    avg_distance = np.mean(values)
    std_dev = np.var(values)

    print(f"Average Distance: {avg_distance:.2f}")
    print(f"Variance: {std_dev:.2f}")


    plt.figure(figsize=(8, 5))
    sns.histplot(values, bins=20, kde=True)
    plt.xlabel("Distance Values")
    plt.ylabel("Frequency")
    plt.title("Distribution of Distance Values")
    plt.show()

    return avg_distance, std_dev



file_path = r"C:\Users\aryan\PycharmProjects\UAV\data\distance_matrix.csv"  # Update with your actual file path
analyze_distance_matrix(file_path)
