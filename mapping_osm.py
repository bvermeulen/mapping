import geopandas as gpd
import matplotlib.pyplot as plt
# from PIL import Image
import contextily as ctx
from shapely.geometry import Point
import psycopg2


figsize = (12, 10)
osm_url = 'http://tile.stamen.com/terrain/{z}/{x}/{y}.png'
EPSG_OSM = 3857
EPSG_WGS84 = 4326

class MapTools:
    def __init__(self, pictures):
        self.pictures = pictures
        self.pictures.crs = EPSG_WGS84
        self.pictures = self.convert_to_osm(self.pictures)

        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
        self.callbacks_connect()

        # get initial extent of all pictures
        self.pictures.plot(ax=self.ax)
        self.plot_area = self.ax.axis()


    def convert_to_osm(self, df):
        return df.to_crs(epsg=EPSG_OSM)

    def callbacks_connect(self):
        self.zoomcallx = self.ax.callbacks.connect(
            'xlim_changed', self.on_limx_change)
        self.zoomcally = self.ax.callbacks.connect(
            'ylim_changed', self.on_limy_change)

        self.x_called = False
        self.y_called = False

    def callbacks_disconnect(self):
        self.ax.callbacks.disconnect(self.zoomcallx)
        self.ax.callbacks.disconnect(self.zoomcally)

    def on_limx_change(self, _):
        self.x_called = True
        if self.y_called:
            self.on_lim_change()

    def on_limy_change(self, _):
        self.y_called = True
        if self.x_called:
            self.on_lim_change()

    def on_lim_change(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.plot_area = (*xlim, *ylim)
        self.blit_map()

    def add_base_map_osm(self):
        # ctx.add_basemap(self.ax)
        zoom = 13
        try:
            basemap, extent = ctx.bounds2img(
                self.plot_area[0], self.plot_area[2],
                self.plot_area[1], self.plot_area[3],
                zoom='auto',
                url=osm_url,)
            self.ax.imshow(basemap, extent=extent, interpolation='bilinear')

        except Exception as e:
            print(f'unable to load map: {e}')

    def blit_map(self):
        self.ax.cla()
        self.callbacks_disconnect()
        pictures = self.pictures.cx[
            self.plot_area[0]:self.plot_area[1],
            self.plot_area[2]:self.plot_area[3]]
        pictures.plot(ax=self.ax)

        # DEBUG lines
        print('*'*80)
        print(self.plot_area)
        print(f'{len(pictures)} pictures in plot area')

        self.add_base_map_osm()
        self.callbacks_connect()

    @staticmethod
    def show():
        plt.show()


class PicBase:
    host = 'localhost'
    db_user = 'db_tester'
    db_user_pw = 'db_tester_pw'
    database = 'picture_base'

    table_pictures = 'pictures'

    @classmethod
    def get_meta_data(cls):
        ''' reads the picture database and return the locations in longitude, latitude
            Coordinates are expected to be in WGS84 (EPSG 4326)
            returns: list of Shapely Points (longitude, latitude)
        '''
        connect_string = (f'host=\'{cls.host}\' dbname=\'{cls.database}\''
                          f'user=\'{cls.db_user}\' password=\'{cls.db_user_pw}\'')

        with psycopg2.connect(connect_string) as connection:
            with connection.cursor() as cursor:
                sql = (f'select date_picture, gps_latitude, gps_longitude, '
                       f'gps_altitude, gps_img_dir, camera_make, camera_model '
                       f'from {cls.table_pictures} '
                       f'where gps_latitude ->> \'ref\' in (\'N\', \'S\') '
                       f'order by date_picture')

                cursor.execute(sql)

                picture_locations = []
                for record in cursor.fetchall():
                    latitude = cls.convert_gps_to_decimal_degrees(record[1])
                    longitude = cls.convert_gps_to_decimal_degrees(record[2])

                    picture_locations.append(Point(latitude, longitude))

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


def main():
    pic_locations = gpd.GeoDataFrame(geometry=PicBase().get_meta_data())
    map_tools = MapTools(pic_locations)
    # map_tools.blit_map()
    map_tools.show()

if __name__ == '__main__':
    main()
