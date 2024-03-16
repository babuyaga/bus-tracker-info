import requests
from geopy.distance import geodesic
import csv
import os
import time

# URL and parameters for the GET request
url = "https://bt.mytransitride.com/api/VehicleStatuses"
params = {"patternIds": "15750,15754,15787"}

# Path to the CSV file
csv_file_path = 'businfo.csv'

# Specific location (T)
specific_location = (43.12345, -80.23456)  # Example coordinates

def get_vehicle_statuses(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters

def process_vehicle_data(vehicle_data, specific_location):
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['VehicleID', 'Latitude', 'Longitude', 'TotalDistance'])
    
    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            existing_data = {int(row['VehicleID']): row for row in reader}
    except FileNotFoundError:
        existing_data = {}
    
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['VehicleID', 'Latitude', 'Longitude', 'TotalDistance'])
        writer.writeheader()
        
        for vehicle in vehicle_data:
            vehicle_id = vehicle['vehicleId']
            lat_x, lng_x = vehicle['lat'], vehicle['lng']
            distance_to_T = calculate_distance(lat_x, lng_x, *specific_location)
            
            if distance_to_T < 150:
                total_distance = 0
            elif vehicle_id in existing_data:
                lat_y, lng_y = float(existing_data[vehicle_id]['Latitude']), float(existing_data[vehicle_id]['Longitude'])
                distance_traveled = calculate_distance(lat_x, lng_x, lat_y, lng_y)
                total_distance = float(existing_data[vehicle_id]['TotalDistance']) + distance_traveled
            else:
                total_distance = 0
            
            writer.writerow({'VehicleID': vehicle_id, 'Latitude': lat_x, 'Longitude': lng_x, 'TotalDistance': total_distance})
            print(f"VehicleID: {vehicle_id}, Current Location: ({lat_x}, {lng_x}), Total Distance: {total_distance}")

while True:
    vehicle_statuses = get_vehicle_statuses(url, params)
    process_vehicle_data(vehicle_statuses, specific_location)
    time.sleep(10)
