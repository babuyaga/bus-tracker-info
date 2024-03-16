import gspread
import requests
import time
import math



def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def update_vehicle_data():
    # Authenticate with the Google Sheets API
    sa = gspread.service_account(filename="bttrack-ca98b5f7a1a1.json")
    sh = sa.open("VehicleData")
    wks = sh.worksheet("Sheet1")

    # Make the GET request to the API
    response = requests.get("https://bt.mytransitride.com/api/VehicleStatuses?patternIds=15778,15787,")
    vehicles = response.json()
    print(vehicles)
    # Retrieve all existing vehicle names in the sheet to determine if update or append is needed
    existing_names = wks.col_values(1)[1:]  # Skip the header row, assuming names are in the first column
    if existing_names:
        existing_names_dict = {name: i + 2 for i, name in enumerate(existing_names)}  # Row indices start at 2 considering the header
    else:
        existing_names_dict = {}
    
    for vehicle in vehicles:
        name = vehicle["name"]
        
        row = [
            name,  # Use name instead of vehicleID
            vehicle["lat"],
            vehicle["lng"],
            vehicle["velocity"],
            0  # Total distance initialized to 0 (modify as needed)
        ]

        if name in existing_names_dict:
            # Update the existing row
            row_range = f"B{existing_names_dict[name]}:E{existing_names_dict[name]}"
            data = (wks.get( f"B{existing_names_dict[name]}:E{existing_names_dict[name]}"))
            lat = float(data[0][0])
            lng = float(data[0][1])
            distance = haversine(lat,lng,vehicle["lat"],vehicle["lng"])
            row[4] = distance + float(data[0][3])
            wks.update(row_range, [row[1:]])
            # Skip name for update
        else:
            # Append a new row at the end
            wks.append_row(row)

def main():
    while True:
        update_vehicle_data()
        print("")
        time.sleep(10)  # Wait for 10 seconds before the next update

if __name__ == "__main__":
    main()
