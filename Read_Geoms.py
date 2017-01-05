import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import shapely
import json
import os

# Get the names of all the New York folders.
ny_nhoods = os.listdir(r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\Draw-Your-Neighborhood-master\New_York')

# Get all files within
drawings = os.listdir(r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\Draw-Your-Neighborhood-master\New_York\\' + ny_nhoods[0])

# Ideally I want everything in a single geopandas geodataframe to start with

# This is the template to join everything to. Remember to delete this row later!
fs = r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\Draw-Your-Neighborhood-master\New_York\alphabet-city\alphabet-city_0.geojson'
data = gpd.read_file(fs)

for hood in ny_nhoods:
    drawings = os.listdir(r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\Draw-Your-Neighborhood-master\New_York\\' + hood)
    for drawing in drawings:
        fs_temp = r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\Draw-Your-Neighborhood-master\New_York\\' + hood + '\\' + drawing
        temp = gpd.read_file(fs_temp)
        # This is a clunky evivalent of a += operation. Seems to work.
        data = gpd.GeoDataFrame(pd.concat([data,temp],ignore_index=True))
    print hood

data = data.drop(0)

# Set the projection to WGS-84
data.crs = {'init': 'epsg:4326'}

#fs = r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\data_raw_WGS84.geojson'
#with open(fs,'w') as f:
    #f.write(data.to_json())


# Let's see about exporting that whole file as a geojson.
#data.to_file(r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\raw_wgs84.geojson',driver='GeoJSON')

# Now project to a projected coordinate system

# EPSG:32118 - New York Long Island, NAD83-based projection in metres.

#data = data.to_crs({'init':'epsg:32118'})
#data.to_file(r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\raw_NYproj.geojson')

# EPSG: 32618 - UTM Zone 18N, metres.
#data = data.to_crs({'init':'epsg:32618'})
#data.to_file(r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\raw_UTM18N.geojson')


"""
ny_area = shapely.geometry.box(-74.3,40.47,-73.6,40.95)
ax = data[data.geometry.intersects(ny_area)].plot()
ax.set_aspect(2)
fig = plt.gcf()

plt.show()
"""
