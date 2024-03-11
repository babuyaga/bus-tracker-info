import csv
import os
import requests
from geopy.distance import geodesic
import time

# URL for the GET request
url = "https://bt.mytransitride.com/api/VehicleStatuses?patternIds=15750"

# Function to get current location from API
def get_current_location():
    response = requests.get(url)
    data = response.json()

    # Assuming you're interested in the first vehicle in the response
    vehicle = data[0] if data else None
    if vehicle:
        return (vehicle['lat'], vehicle['lng'])
    else:
        return None

# Function to read the last known location from the CSV file
def read_last_location(csv_file_path):
    if not os.path.exists(csv_file_path):
        return None, 0  # No last location, 0 distance

    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Ensure row is not empty
                return (float(row[0]), float(row[1])), float(row[2])
    return None, 0

# Function to calculate distance and update the CSV file
def update_location_and_distance(csv_file_path, current_location):
    last_location, total_distance = read_last_location(csv_file_path)

    if current_location:
        if last_location:
            distance = geodesic(last_location, current_location).kilometers
            total_distance += distance
        else:
            total_distance = 0  # If there's no last location, start with 0 distance

        # Update CSV with the new location and total distance
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_location[0], current_location[1], total_distance])

        print(f"Updated total distance: {total_distance} kilometers")
    else:
        print("No current location available.")

# Main function to tie it all together
def main():
    csv_file_path = "businfo.csv"
    while True:  # This creates an infinite loop
        current_location = get_current_location()
        update_location_and_distance(csv_file_path, current_location)
        time.sleep(30)  # Wait for 30 seconds before the next update

if __name__ == "__main__":
    main()
