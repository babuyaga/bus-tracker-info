from google.oauth2 import service_account
from googleapiclient.discovery import build
from geopy.distance import geodesic
import requests
import time

# Configuration
SPREADSHEET_ID = "your_spreadsheet_id_here"
SERVICE_ACCOUNT_FILE = "bustracker-417102-40ca8e0c21c2.json"
SHEET_NAME = "Sheet1"  # Adjust based on your actual sheet name within the spreadsheet
URL = "https://bt.mytransitride.com/api/VehicleStatuses"
PARAMS = {"patternIds": "15750,15754,15787"}
SPECIFIC_LOCATION = (43.12345, -80.23456)  # Example coordinates

# Authenticate and construct service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, 
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()

def get_vehicle_statuses(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters

def get_existing_data():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
    values = result.get('values', [])
    headers = values[0]  # Assumes the first row contains headers
    return [dict(zip(headers, row)) for row in values[1:]] if values else []

def update_google_sheet(data):
    for row in data:
        range_update = f"{SHEET_NAME}!A{row['row']}:D{row['row']}"
        values = [[row['VehicleID'], row['Latitude'], row['Longitude'], row['TotalDistance']]]
        body = {'values': values}
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_update, valueInputOption="USER_ENTERED", body=body).execute()

def process_vehicle_data(vehicle_data, specific_location):
    existing_data = get_existing_data()
    updates = []
    
    for vehicle in vehicle_data:
        vehicle_id = vehicle['vehicleId']
        lat_x, lng_x = vehicle['lat'], vehicle['lng']
        distance_to_T = calculate_distance(lat_x, lng_x, *specific_location)
        
        total_distance = 0 if distance_to_T < 150 else None
        
        for idx, record in enumerate(existing_data, start=2):
            if int(record['VehicleID']) == vehicle_id:
                lat_y, lng_y = float(record['Latitude']), float(record['Longitude'])
                if total_distance is None:  # Calculate new total distance only if not resetting
                    distance_traveled = calculate_distance(lat_x, lng_x, lat_y, lng_y)
                    total_distance = float(record['TotalDistance']) + distance_traveled
                updates.append({'row': idx, 'VehicleID': vehicle_id, 'Latitude': lat_x, 'Longitude': lng_x, 'TotalDistance': total_distance})
                break
        
        if total_distance is None:  # If vehicle not found in existing data
            total_distance = 0
        
        print(f"VehicleID: {vehicle_id}, Current Location: ({lat_x}, {lng_x}), Total Distance: {total_distance}")
    
    if updates:
        update_google_sheet(updates)

while True:
    vehicle_statuses = get_vehicle_statuses(URL, PARAMS)
    process_vehicle_data(vehicle_statuses, SPECIFIC_LOCATION)
    time.sleep(10)
