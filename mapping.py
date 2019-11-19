'''  geopandas mapping
'''
import os
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
os.environ['GDAL_DATA'] = os.environ['CONDA_PREFIX'] + r'\Library\share\gdal'
os.environ['PROJ_LIB'] = os.environ['CONDA_PREFIX'] + r'\Library\share'
import geopandas as gpd

class WorldMap:

    def __init__(self):
        world_key = 'naturalearth_lowres'
        cities_key = 'naturalearth_cities'
        self.world = gpd.read_file(gpd.datasets.get_path(world_key))

        # remove Antarctica
        self.world = self.world[(self.world.name != 'Antarctica')]
        self.cities = gpd.read_file(gpd.datasets.get_path(cities_key))

    def plot(self):
        self.world.plot

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        ax.set_aspect('equal')

        self.world.plot(ax=ax, color='white', edgecolor='black')
        self.cities.plot(ax=ax, marker='o', color='blue', markersize=5)

        plt.show()


if __name__ == '__main__':
    world = WorldMap()
    print(world.world.head(100))
    world.plot()
    pass