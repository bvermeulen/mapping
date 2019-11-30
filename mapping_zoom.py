import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx


figsize = (12, 10)
osm_url = 'http://tile.stamen.com/terrain/{z}/{x}/{y}.png'
EPSG_OSM = 3857
EPSG_WGS84 = 4326

class MapTools:
    def __init__(self):
        self.cities = gpd.read_file(
            gpd.datasets.get_path('naturalearth_cities'))
        self.cities.crs = EPSG_WGS84
        self.cities = self.convert_to_osm(self.cities)

        self.fig, self.ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
        self.callbacks_connect()

        # get extent of the map for all cities
        self.cities.plot(ax=self.ax)
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
        if abs(self.plot_area[1] - self.plot_area[0]) < 100:
            zoom = 13

        else:
            zoom = 'auto'

        try:
            basemap, extent = ctx.bounds2img(
                self.plot_area[0], self.plot_area[2],
                self.plot_area[1], self.plot_area[3],
                zoom=zoom,
                url=osm_url,)
            self.ax.imshow(basemap, extent=extent, interpolation='bilinear')

        except Exception as e:
            print(f'unable to load map: {e}')

    def blit_map(self):
        self.ax.cla()
        self.callbacks_disconnect()
        cities = self.cities.cx[
            self.plot_area[0]:self.plot_area[1],
            self.plot_area[2]:self.plot_area[3]]
        cities.plot(ax=self.ax, color='red', markersize=3)

        print('*'*80)
        print(self.plot_area)
        print(f'{len(cities)} cities in plot area')

        self.add_base_map_osm()
        self.callbacks_connect()

    @staticmethod
    def show():
        plt.show()


def main():
    map_tools = MapTools()
    map_tools.show()

if __name__ == '__main__':
    main()
