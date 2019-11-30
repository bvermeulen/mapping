import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

EPSG_OSM = 3857
EPSG_WGS84 = 4326

latitude = 45
longitude = -45
my_location = gpd.GeoDataFrame(geometry=[Point(latitude, longitude)])
my_location.crs = EPSG_WGS84
my_location = my_location.to_crs(epsg=EPSG_OSM)

for _, loc in my_location.iterrows():
    x = loc.geometry.x
    y = loc.geometry.y
    print(f'x: {x}, y: {y}')

''' answer on windows:
x: -5009377.085697311, y: 5621521.486192066
'''