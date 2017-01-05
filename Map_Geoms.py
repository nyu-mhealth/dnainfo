import matplotlib.pyplot as plt
import geopandas as gpd
import shapely
from functools import partial
import numpy as np


fs = r'C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\data_raw.geojson'
ny_nhoods = gpd.read_file(fs)

ny_nhoods.crs = {'init': 'epsg:4326'}
ny_nhoods = ny_nhoods.to_crs({'init':'epsg:32118'})
"""
ny_area = shapely.geometry.box(278336,36613,325339,83164)
ax = ny_nhoods[ny_nhoods.geometry.within(ny_area)].plot(figsize=(8,10))
ax.set_aspect(2)
ax.set_xlim([278336,325339])
ax.set_ylim([36613,83164])

plt.show()
"""
# Now make something that makes an image for each neighbourhood

# First restrict the data to the wider NYC area by way of a bounding box.

ny_area = shapely.geometry.box(278336,36613,325339,83164)
ny_nhoods = ny_nhoods[ny_nhoods.geometry.within(ny_area)]
# Add area field
ny_nhoods['areakm2'] = ny_nhoods['geometry'].area/10**6

# Some records are incomplete polygons (effectively lines) and have area = 0.0km2. Remove these (there are 62).
ny_nhoods = ny_nhoods[ny_nhoods['areakm2'] > 0.0]

"""
ax = ny_Allerton.plot(figsize=(8,10))
ax.set_aspect(2)
ax.set_xlim([bounds[0],bounds[2]])
ax.set_ylim([bounds[1],bounds[3]])
"""
# Get all the bounding boxes (envelopes)

bound = {}
ny_groups = ny_nhoods.groupby('neighborhoodLive')

for nh, grp in ny_groups:
    bound[str(nh)] = shapely.geometry.MultiPolygon(grp['geometry'].tolist()).envelope

# We can plot all the envelopes, just to see what is going on. Put them into a geodataframe
df = []
geom = []
for i, j in bound.iteritems():
    df.append(i)
    geom.append(j)

bound_df = gpd.GeoDataFrame(df,columns = ['neighborhoodLive'],geometry=geom)

#bound_df.plot()
#plt.show()

# Iterate through neighbourhoods and plot individual maps
"""
for nh, grp in ny_groups:
    
    bounds = bound_df[bound_df['neighborhoodLive'] == nh].geometry.bounds
    ax = grp.plot()
    ax.set_aspect(2)
    ax.set_xlim([float(bounds.minx),float(bounds.maxx)])
    ax.set_ylim([float(bounds.miny),float(bounds.maxy)])
    ax.set_title(nh)
    fn = r"C:\Users\ppehdlew\OneDrive\Draw-Your-Neighborhood-master\Images\nhood_" + nh + ".png"
    fn = fn.replace("/","-")
    plt.savefig(fn,dpi=300)
    plt.close()
"""

# Define the summary statistics required (need to use partial to get percentiles)
aggs = {'n':'count','mean':'mean','Std. Dev.': 'std','min':'min','max':'max','median':'median','P25th': partial(np.percentile,q=25),'P75th': partial(np.percentile,q=75)}
# output descriptives and export to spreadsheet
descriptives = ny_groups.agg({'areakm2':aggs})
descriptives.to_csv('desc.csv')

# Let's have a look at a histogram of 
