import pandas as pd
from geopy.distance import geodesic

# Read the CSV file
df = pd.read_csv("bus_1_data.csv")

# Initialize an empty list to store distances
distances = []

# Iterate through each row in the DataFrame
for i in range(len(df)):
    if i == 0:
        # For the first row, set distance as 0
        distances.append(0)
    else:
        # Calculate distance between current and previous locations
        prev_location = (df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude'])
        curr_location = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])
        distance = geodesic(prev_location, curr_location).kilometers
        distances.append(distance)

# Add distances as a new column in the DataFrame
df['distance_to_previous'] = distances

# Write the updated DataFrame back to CSV
df.to_csv("bus_1_output_file.csv", index=False)

print("Distance calculations completed and saved to 'output_file.csv'.")
