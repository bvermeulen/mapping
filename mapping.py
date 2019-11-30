'''  geopandas mapping
'''
# import os
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
# os.environ['GDAL_DATA'] = os.environ['CONDA_PREFIX'] + r'\Library\share\gdal'
# os.environ['PROJ_LIB'] = os.environ['CONDA_PREFIX'] + r'\Library\share'
import geopandas as gpd
import psycopg2


class PicBase:
    host = 'localhost'
    db_user = 'db_tester'
    db_user_pw = 'db_tester_pw'
    database = 'picture_base'

    table_pictures = 'pictures'

    @classmethod
    def get_meta_data(cls):
        connect_string = (f'host=\'{cls.host}\' dbname=\'{cls.database}\''
                          f'user=\'{cls.db_user}\' password=\'{cls.db_user_pw}\'')

        with psycopg2.connect(connect_string) as connection:
            with connection.cursor() as cursor:
                sql = (f'select date_picture, gps_latitude, gps_longitude, '
                       f'gps_altitude, gps_img_dir, camera_make, camera_model '
                       f'from {cls.table_pictures} '
                       f'where gps_latitude ->> \'ref\' in (\'N\', \'S\') and '
                       f'id in(23100, 23200,23160,23255)'
                       f'order by date_picture')

                cursor.execute(sql)

                picture_locations = []
                for record in cursor.fetchall():
                    latitude = cls.convert_gps_to_decimal_degrees(record[1])
                    longitude = cls.convert_gps_to_decimal_degrees(record[2])

                    picture_locations.append(Point(longitude, latitude))


        return picture_locations

    @staticmethod
    def convert_gps_to_decimal_degrees(lat_long_value):
        ref = lat_long_value.get('ref', '')
        fractions = lat_long_value.get('pos', ([0, 1], [0, 1], [0, 1]))
        degrees = fractions[0][0] / fractions[0][1]
        minutes = fractions[1][0] / fractions[1][1]
        seconds = fractions[2][0] / fractions[2][1]

        if fractions[1][0] == 0 and fractions[2][0] == 0:
            if ref in ['S', 'W']:
                degrees = -degrees

        elif fractions[2][0] == 0:
            degrees += minutes / 60
            if ref in ['S', 'W']:
                degrees = -degrees

        else:
            degrees += minutes / 60 + seconds / 3600

            if ref in ['S', 'W']:
                degrees = -degrees

        return degrees

class WorldMap:

    def __init__(self):
        world_key = 'naturalearth_lowres'
        cities_key = 'naturalearth_cities'
        self.world = gpd.read_file(gpd.datasets.get_path(world_key))

        # remove Antarctica
        self.world = self.world[(self.world.name != 'Antarctica')]
        self.cities = gpd.read_file(gpd.datasets.get_path(cities_key))

        pic_locations = PicBase().get_meta_data()
        self.pictures = gpd.GeoDataFrame(geometry=pic_locations)

    def plot(self):
        fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 6))
        ax0.set_aspect('equal')
        ax1.set_aspect('equal')

        self.world.plot(ax=ax0, color='white', edgecolor='black')
        self.pictures.plot(ax=ax0, marker='o', color='blue', markersize=5)

        nld = self.world[(self.world.name == 'Thailand')]
        ams = self.cities[(self.cities.name == 'Bangkok')]

        xmin, ymin, xmax, ymax = nld.total_bounds
        pictures_nld = self.pictures.cx[xmin:xmax, ymin:ymax]

        nld.plot(ax=ax1, color='white', edgecolor='black')
        pictures_nld.plot(ax=ax1, marker='o', color='blue', markersize=5)

        plt.show()


if __name__ == '__main__':
    world = WorldMap()
    print(world.world.head(100))
    world.plot()
