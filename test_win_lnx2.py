import geopandas as gpd
from shapely.geometry import Point

EPSG_OSM = 3857
EPSG_WGS84 = 4326

longitude = 45
latitude = 0
my_location = gpd.GeoDataFrame(geometry=[Point(longitude, latitude)])

geom = my_location.loc[0].geometry
print(f'long: {geom.x:15.4f}, lat: {geom.y:15.4f}')

my_location.crs = EPSG_WGS84
my_location = my_location.to_crs(epsg=EPSG_OSM)

geom = my_location.loc[0].geometry
print(f'x   : {geom.x:15.4f}, y  : {geom.y:15.4f}')

'''
Linux
long:          0.0000, lat:        -45.0000
x   :          0.0000, y  :   -5621521.4862

long:         45.0000, lat:          0.0000
x   :    5009377.0857, y  :          0.0000

'''
