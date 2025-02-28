#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(point1, point2):
    R = 6371  # Earth's radius in kilometers
    lon1, lat1 = point1
    lon2, lat2 = point2
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def create_distance_matrix(input_file, output_file):
    # Read CSV file
    df = pd.read_csv(input_file)
    
    # Extract coordinates and names
    coords = df[['longitude', 'latitude']].values
    names = df['Name'].values
    
    # Calculate distance matrix
    distances = pdist(coords, metric=haversine_distance)
    distance_matrix = squareform(distances)
    
    # Create DataFrame with distance matrix
    result_df = pd.DataFrame(distance_matrix, index=names, columns=names)
    
    # Round to 2 decimal places
    result_df = result_df.round(2)
    
    # Save to CSV
    result_df.to_csv(output_file)
    print(f"Distance matrix has been created and saved to {output_file}")

# Usage
input_file = 'UAV/data/Map_chandigarh.csv'
output_file = 'UAV/data/distance_matrix.csv'
create_distance_matrix(input_file, output_file)
