import csv
from datetime import datetime, timedelta
import random

# Function to generate a random time between 00:00 and 23:59
def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return datetime(2025, 3, 20, hour, minute).strftime('%H:%M')

# Open the CSV file for reading
with open('abc_distances1000.csv', 'r') as infile:
    reader = csv.reader(infile)
    data = list(reader)

# Add 'Time' to the header
data[0].append('Time')

# Add random times to each row except the header
for row in data[1:]:
    row.append(random_time())

# Write the updated data back to a new CSV file
with open('abc_distances1000_with_time.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)

print("CSV file has been updated with random times.")
