import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

gpdf = '2021-census-info/LSUG_21C.json'

class transform_LSUG:
    def __init__(self, gpdf, epsg=2326):
        self.gpdf = gpd.read_file(gpdf)
        self.epsg = epsg
    def transform(self):
        self.gpdf = self.gpdf.set_crs(epsg=self.epsg, allow_override=True)
        self.gpdf = self.gpdf.to_crs(epsg=4326)
        self.gpdf['name'] = self.gpdf.index
        self.gpdf = self.gpdf.explode()
        self.gpdf['geometry'] = self.gpdf['geometry'].apply(lambda x: Polygon(x.exterior.coords))
        return self.gpdf
    def export(self):
        self.transform()
        return self.gpdf.to_file('2021-census-info/LSUG_21C_lat_lng.json', driver='GeoJSON')

transform_LSUG(gpdf).export()