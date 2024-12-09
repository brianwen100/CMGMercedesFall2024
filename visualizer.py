import pandas as pd
import folium
from folium.plugins import HeatMap
from matplotlib.colors import Normalize, to_hex
import matplotlib

# Load the EV stations dataset
stations_df = pd.read_csv('sfstations.csv', parse_dates=['open_date'])

# Extract the year from 'open_date'
stations_df['year'] = stations_df['open_date'].dt.year
stations_df['date_numeric'] = (stations_df['open_date'] - stations_df['open_date'].min()).dt.total_seconds()

# Load the EV registrations dataset
registrations_df = pd.read_csv('registrations.csv')

# Filter EV registrations for San Francisco ZIP codes and Electric vehicles
sf_zip_codes = [
    # San Francisco ZIP Codes
    "94102", "94103", "94104", "94105", "94107", "94108", "94109", "94110",
    "94111", "94112", "94114", "94115", "94116", "94117", "94118", "94121",
    "94122", "94123", "94124", "94127", "94129", "94130", "94131", "94132",
    "94133", "94134", "94158",
    # Daly City ZIP Codes
    "94014", "94015",
    # Colma ZIP Code
    "94014",
    # South San Francisco ZIP Codes
    "94080",
    # Brisbane ZIP Code
    "94005",
    # Millbrae ZIP Codes
    "94030",
    # Burlingame ZIP Codes
    "94010",
    # San Bruno ZIP Codes
    "94066",
    # Pacifica
    "94044", 
    # San Mateo ZIP Codes
    "94401", "94402", "94403", "94404"
]
sf_registrations = registrations_df[ 
    (registrations_df['ZIP'].astype(str).isin(sf_zip_codes)) & 
    (registrations_df['FUEL_TYPE'] == 'Electric')
]

# Group by year and ZIP code to aggregate sales
aggregated_sales = sf_registrations.groupby(['Data_Year', 'ZIP'])['Number of Vehicles'].sum().reset_index()

# Map ZIP codes to coordinates (latitude, longitude)
zip_to_coords = {
    # San Francisco
    "94102": [37.7798, -122.4194], "94103": [37.7725, -122.4103],
    "94104": [37.7912, -122.4039], "94105": [37.7898, -122.3966],
    "94107": [37.7693, -122.4027], "94108": [37.7918, -122.4101],
    "94109": [37.7993, -122.4227], "94110": [37.7487, -122.4158],
    "94111": [37.7986, -122.3986], "94112": [37.7213, -122.4446],
    "94114": [37.7583, -122.4358], "94115": [37.7860, -122.4380],
    "94116": [37.7446, -122.4842], "94117": [37.7701, -122.4446],
    "94118": [37.7819, -122.4619], "94121": [37.7798, -122.4855],
    "94122": [37.7589, -122.4841], "94123": [37.7989, -122.4381],
    "94124": [37.7285, -122.3908], "94127": [37.7349, -122.4630],
    "94129": [37.7989, -122.4662], "94130": [37.8168, -122.3709],
    "94131": [37.7412, -122.4376], "94132": [37.7215, -122.4782],
    "94133": [37.8053, -122.4098], "94134": [37.7194, -122.4108],
    "94158": [37.7705, -122.3911],
    # Daly City
    "94014": [37.6869, -122.4702], "94015": [37.6919, -122.4719],
    # Colma
    "94014": [37.6764, -122.4500],
    # South San Francisco
    "94080": [37.6547, -122.4077], 
    # Brisbane
    "94005": [37.6808, -122.3999],
    # Millbrae
    "94030": [37.5986, -122.3872],
    # Burlingame
    "94010": [37.5778, -122.3480],
    # San Bruno
    "94066": [37.6305, -122.4111],
    # Pacifica ZIP Codes
    "94044": [37.6138, -122.4869],
    # San Mateo
    "94401": [37.5747, -122.3228], "94402": [37.5493, -122.3300],
    "94403": [37.5391, -122.3042], "94404": [37.5554, -122.2688]
}

# Map the Longitude and Latitudes to every zip code
aggregated_sales['Latitude'] = aggregated_sales['ZIP'].map(lambda z: zip_to_coords.get(str(z), [None, None])[0])
aggregated_sales['Longitude'] = aggregated_sales['ZIP'].map(lambda z: zip_to_coords.get(str(z), [None, None])[1])
aggregated_sales = aggregated_sales.dropna(subset=['Latitude', 'Longitude'])

# Normalize date_numeric for color mapping
norm = Normalize(vmin=stations_df['date_numeric'].min(), vmax=stations_df['date_numeric'].max())
cmap = matplotlib.colormaps.get_cmap('viridis')

# Initialize the folium map
map_center = [stations_df['latitude'].mean(), stations_df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Add EV stations for each year
def add_station_layer(year):
    """Add a layer for EV stations opened in the given year."""
    year_data = stations_df[stations_df['year'] == year]

    # Create a FeatureGroup for the year
    fg = folium.FeatureGroup(name=f"Stations {year}", show=False)

    # Add stations to the layer
    for _, row in year_data.iterrows():
        normalized_date = norm(row['date_numeric'])
        color = to_hex(cmap(normalized_date))
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['station_name']} (Opened: {row['year']})"
        ).add_to(fg)

    # Add the layer to the map
    fg.add_to(m)


# Add vehicle sales for a specific year with improved gradient
def add_sales_layer(year):
    """Add vehicle sales for the given year to the map."""
    year_data = aggregated_sales[aggregated_sales['Data_Year'] == year]

    # Create a FeatureGroup for the year
    fg = folium.FeatureGroup(name=f"Vehicle Sales {year}")

    # Add heatmap for sales
    if not year_data.empty:
        max_sales = year_data['Number of Vehicles'].max()  # Get max sales for normalization
        heat_data = [
            [row['Latitude'], row['Longitude'], row['Number of Vehicles']]
            for _, row in year_data.iterrows()
        ]
        HeatMap(heat_data, radius=15, max_val=max_sales).add_to(fg)  # Normalize to actual max

    # Add markers for sales
    for _, row in year_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"ZIP: {row['ZIP']}<br>Year: {row['Data_Year']}<br>Sales: {row['Number of Vehicles']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(fg)

    fg.add_to(m)

# Add vehicle sales layers for each year
for year in sorted(aggregated_sales['Data_Year'].unique()):
    add_sales_layer(year)
    
# Add layers for each unique year
for year in sorted(stations_df['year'].unique()):
    add_station_layer(year)

# Add layer control to toggle years
folium.LayerControl(collapsed=False).add_to(m)


# Save the map
m.save('bay_final_electric.html')
