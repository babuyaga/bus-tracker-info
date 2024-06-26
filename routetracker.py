import requests
from geopy.distance import geodesic
import csv
import os

# URL and parameters for the GET request
url = "https://bt.mytransitride.com/api/VehicleStatuses"
params = {"patternIds": "15750,15754,15787"}

# Path to the CSV file
csv_file_path = 'businfo.csv'

def get_vehicle_statuses(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters

def update_csv_with_vehicle_data(vehicle_data):
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
            
            if vehicle_id in existing_data:
                lat_y, lng_y = float(existing_data[vehicle_id]['Latitude']), float(existing_data[vehicle_id]['Longitude'])
                total_distance = float(existing_data[vehicle_id]['TotalDistance']) + calculate_distance(lat_x, lng_x, lat_y, lng_y)
            else:
                total_distance = 0  # Assuming new vehicles start with 0 total distance
            
            # Update the data
            writer.writerow({'VehicleID': vehicle_id, 'Latitude': lat_x, 'Longitude': lng_x, 'TotalDistance': total_distance})
            
            print(f"VehicleID: {vehicle_id}, Current Location: ({lat_x}, {lng_x}), Total Distance: {total_distance}")

vehicle_statuses = get_vehicle_statuses(url, params)
update_csv_with_vehicle_data(vehicle_statuses)
