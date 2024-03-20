import gspread
import requests
import time
import math

def updateVehicles():
# Assuming the response is directly fetched from the URL
    response = requests.get("https://bt.mytransitride.com/api/Route")
    data = response.json()

# Initialize an empty list to hold our extracted data
    extracted_data = []

# Iterate over each item in the data
    for item in data:
    # Extract the routeName and patternID
        route_name = item["routeName"]
        pattern_id = item["patternID"]
     # Append them as a list to our extracted_data list
        extracted_data.append([ pattern_id,route_name])

    sa = gspread.service_account(filename="bttrack-ca98b5f7a1a1.json")
    sh = sa.open("VehicleData")
    wks2 = sh.worksheet("Sheet2")
    wks2.update(extracted_data)
# # Print the result
# for item in extracted_data:
#     wks.append_row(item)

