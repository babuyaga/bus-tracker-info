import gspread
from math import radians, cos, sin, sqrt, atan2


sa = gspread.service_account(filename="bttrack-ca98b5f7a1a1.json")
sh = sa.open("VehicleData")

wks = sh.worksheet("master_sheet")
print(wks.row_values(1))
values = wks.row_values(6)
print(values[6])


sh = sa.open("Routes")

wks_route = sh.worksheet(f"{values[6]}")

# wks_route = sh.worksheet("1")
lat_string = wks_route.col_values(5)[1:]
lng_string = wks_route.col_values(6)[1:]

lat = [float(value) for value in lat_string]
lng = [float(value) for value in lng_string]

coordinates = list(zip(lat,lng))
# print(coordinates)





def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles
    return c * r

def find_closest_coordinate_index(target_lat, target_lon, coordinates):
    """
    Find the index of the closest coordinate to a given location.
    
    :param target_lat: Latitude of the target location
    :param target_lon: Longitude of the target location
    :param coordinates: A list of tuples, where each tuple contains (latitude, longitude)
    :return: The index of the closest (latitude, longitude) in the list
    """
    closest_index = None
    min_distance = float('inf')
    
    for index, coord in enumerate(coordinates):
        lat, lon = coord
        distance = haversine(target_lat, target_lon, lat, lon)
        
        if distance < min_distance:
            closest_index = index
            min_distance = distance
            
    return closest_index

# Example usage
coordinates_list = coordinates
target_location = (39.952583, -75.165222)  # Philadelphia

closest_location_index = find_closest_coordinate_index(target_location[0], target_location[1], coordinates_list)
print(f"Index of the closest location: {closest_location_index}")


print(f"other nearest locations are:{coordinates[closest_location_index-1]} and {coordinates[closest_location_index+1]}")





# print('Rows:',wks.row_count)
# print('Columns:',wks.col_count)

# print(wks.acell('a9').value)
# print(wks.cell(3,4).value)

# print(wks.get('A7:E9'))

# print(wks.get_all_records())

# print(wks.get_all_values())

# wks.update('A3',"Anthony")


# wks.update('D2:E3',[['business','engineering'],['tennis','pottery']])

# wks.update('F2','=UPPER(E2)',raw=False)

# wks.delete_rows(25)