import geopandas as gpd
import mapping_osm_win as mp

pic_locations = gpd.GeoDataFrame(geometry=mp.PicBase().get_meta_data())

for i, pic in pic_locations.iterrows():
    x = pic.geometry.x
    y = pic.geometry.y
    print(f'{i:5}, {x:10.5f}, {y:10.5f}')
