import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point


latitude = 45
longitude = -45
my_location = gpd.GeoDataFrame(geometry=[Point(latitude, longitude)])

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

_, ax = plt.subplots(figsize=(8, 6))

ax.set_title('Windows: latitude = 45, longitude = -45\n'
             'Point(latitude, longitude)')
world.plot(ax=ax, color='white', edgecolor='black')
my_location.plot(ax=ax, color='red', markersize=20)

plt.show()
