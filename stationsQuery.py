import requests
import csv
import folium

# Replace with your actual API key
API_KEY = "PVQGdkNivlcvO9Aj2uyx6ts6XvYeXPRMuzREv9rJ"
BASE_URL = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json"

"""
Query into NREL API For SF EV Stations
"""
# Open a CSV file for appending
with open("sfstations.csv", "a", newline="") as csvfile:
    fieldnames = ["station_name", "longitude", "latitude", "city", "open_date", 'owner_type_code', 'fuel_type_code']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # If the file is empty, write the header row
    csvfile.seek(0, 2)  # Move to the end of the file to check if it's empty
    if csvfile.tell() == 0:
        writer.writeheader()

       # print(f"Fetching records {start} to {start + batchsize}...")
    params = {
        "limit": 'all',
        "fuel_type":"ELEC",
        "api_key": API_KEY
    }
    
    # API Call
    qresponse = requests.get(BASE_URL, params=params)

    # Process the response
    if qresponse.status_code == 200:
        data = qresponse.json()
        stations = data.get("fuel_stations", [])

        for i, station in enumerate(stations):
            if station.get("city") == "San Francisco":
                # Append the station's longitude, latitude, and other info to the CSV
                writer.writerow({
                    "station_name": station.get("station_name"),
                    "longitude": station.get("longitude"),
                    "latitude": station.get("latitude"),
                    "city": station.get("city"),
                    "open_date": station.get("open_date"),
                    "owner_type_code": station.get("owner_type_code"),
                    "fuel_type_code": station.get("fuel_type_code")
                })
    else:
        print(f"Error: {qresponse.status_code} - {qresponse.text}")

