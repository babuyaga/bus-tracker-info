import csv
from bus_1 import Data

# Define CSV file path
csv_file = "bus_1_data.csv"

# Define CSV field names
field_names = ["patternID", "pointSeqNo", "stopID", "stopNumber", "latitude", "longitude", "isPublic"]

# Write data to CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    
    # Write header
    writer.writeheader()
    
    # Write data rows
    writer.writerows(Data)

print("CSV file created successfully.")
