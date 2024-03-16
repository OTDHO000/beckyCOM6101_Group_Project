import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import os

census_polygon = gpd.read_file('2021-census-info/LSUG_21C_lat_lng.json')

class map_census_polygon_restaurant:
    def __init__(self, census_polygon, restaurant_path, restaurant_name):
        self.census_polygon = census_polygon
        self.restaurant_path = restaurant_path
        self.restaurant_name = restaurant_name
    def map(self):
        restaurant = pd.read_csv(self.restaurant_path + self.restaurant_name)
        # if restaurant['lat'] and restaurant['lon'] are contained in census_polygon['geometry'], then the restaurant is in the census polygon
        try:
            restaurant['census_subnit'] = restaurant.apply(lambda row: self.census_polygon[self.census_polygon['geometry'].contains(Point(row['lng'], row['lat']))]['name'].values[0], axis=1)
        except:
            restaurant['census_subnit'] = restaurant.apply(lambda row: self.census_polygon[self.census_polygon['geometry'].contains(Point(row['lng'], row['lat']))]['name'].values, axis=1)
        # export the mapped restaurant to csv, named as the file name of the original restaurant csv file, to folder restaurant-info-hk/geo_mapped
        # check if 'restaurant-info-hk/geo_mapped/' exists, if not, create it
        if not os.path.exists('restaurant-info-hk/geo_mapped/'):
            os.makedirs('restaurant-info-hk/geo_mapped/')
        return restaurant.to_csv('restaurant-info-hk/geo_mapped/' + self.restaurant_name.replace('.csv.geo.csv', '') + '_geo_mapped.csv', index=False)
    
# loop all the restaurant csv files in folder restaurant-info-hk/geo, and map them to census polygon
restaurant_path = 'restaurant-info-hk/geo/'
for restaurant_name in os.listdir(restaurant_path):
    map_census_polygon_restaurant(census_polygon, restaurant_path, restaurant_name).map()