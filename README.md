# CMGMercedesFall2024
This folder contains both the scripts for creating a Density Visualization Map as well as a the 2 datasets powering the tool.

Hello MBUSA Team! My name is Brian and I am on the CMG + MBUSA project and will give a quick runthrough
on what this folder encompasses.

----- Datasets -----

SF Vehicle Registrations ("registrations.csv")
  - downloaded from the California Energy Commission
  - includes 'Registration Year', 'Quarter', 'Fuel Type', 'Zip Code', and 'Number of Vehicles Sold'
  - Utilized to Map out EV stations year-to-year
  - originally was in the form of a .xlsx but just redownloaded as a csv file
SF EV Charging Stations ("sfstations.csv")
  - procured from the National Renewable Energy Labratory API
  - includes 'Station Name', 'Longitude', 'Latitude', 'City', 'Owner Type', 'Fuel Type'
  - Used to generate heat maps of where EV vehicles were being registered the most

----- stationsQuery.py -----

This file contains:
1. API Key
2. Base URL for API Query

What does it do? 
    This file makes a query into the National Renewable Energy Labratory that retrieves data in the
    form of a JSON object. We write the relevant data of the aforementioned variables to a CSV file,
    namely "sfstations.csv"

----- Visualizer.py -----

This file contains:
1. Function for generating map

What does it do? 
    This map protrays all the EV charging stations as well as the electric vehicle registrations 
    around the SF DMA as well as the neighboring surburbs. 

Steps:
1. Loads in the "sfstations.csv" into variable 'stations_df'
2. Loads in the "registrations.csv" into variable 'registrations_df'
3. Create a mapping of all the relevant zipcodes in the SF DMA + surrounding regions
4. Aggregate Registration Data and filter it based on zipcode
5. Normalize Data for color in heatmaps
6. Initialize the Folium Map that shows the layers of Stations and Registrations
7. Add each EV station to our Folium Map
8. Add each Registration (sales) layer to our Folium Map
9. Save the map as an .html file!

* How to Modify for Future *
  - In the case that there is new updates to either dataset, simply reupload the .csv files with the
    same name and rerun the visualizer.py file by calling 'python visualizer.py' in the folder
    where this file resides

----- Dependencies -----

pip install pandas, matplotlib, foliium
    
