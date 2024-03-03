'''
A module for mapping the database data to relevant features
The mapped file will be used for calculating the score for vacant stores
'''
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import random

# select 100 random sample data from data_source/sample_data/demo_vacant_RL.csv lng lat, then generate random rent from 5000 to 50000
random.seed(123)
sample_data_1 = pd.read_csv('data_source/sample_data/demo_vacant_RL.csv')
sample_data_2 = pd.read_csv('data_source/sample_data/demo_vacant_RR.csv')

# randomly select 100 rows from sample_data_1 and sample_data_2
sample_data_1 = sample_data_1.sample(n = 100)
sample_data_2 = sample_data_2.sample(n = 100)

# extract the columns we need: lng, lat, and generate store_id and rent
sample_data_1 = sample_data_1[['lng', 'lat']]
sample_data_1['store_id'] = ['RL' + str(i) for i in range(1, 101)]
sample_data_1['rent'] = [random.randint(5000, 50000) for i in range(100)]
sample_data_2 = sample_data_2[['lng', 'lat']]
sample_data_2['store_id'] = ['RR' + str(i) for i in range(1, 101)]
sample_data_2['rent'] = [random.randint(5000, 50000) for i in range(100)]

# combine sample_data_1 and sample_data_2
sample_data = pd.concat([sample_data_1, sample_data_2], ignore_index = True)

# read the data from the database
sample_data = gpd.GeoDataFrame(sample_data, geometry = gpd.points_from_xy(sample_data.lng, sample_data.lat))
# for sample data, there are 4 columns: 'store_id', 'rent', 'lat', 'lng'
# competitor data is in data_source/restaurant_competitor.geojson
competitor_data = gpd.read_file('data_source/restaurant_competitors.geojson')

# geospatial data is in data_source/geospatial_202312.geojson
geospatial_data = gpd.read_file('data_source/geospatial_202312.geojson')

# census data is in data_source/LSUG_21C_cleaned.json
census_data = gpd.read_file('data_source/LSUG_21C_cleaned.json')

# function to find nearby restaurants for each vacant store
def number_of_nearby_restaurants(row, competitor_data):
    circle = row.geometry.buffer(0.0005)
    # find the number of nearby restaurants, ignore count if their lng and lat are the same
    nearby_restaurant = competitor_data[(competitor_data.geometry.within(circle)) & (competitor_data['lng'] != row['lng']) & (competitor_data['lat'] != row['lat'])]
    number_of_nearby_restaurants = len(nearby_restaurant)
    return number_of_nearby_restaurants

# function to find nearby facilities for each vacant store
def find_nearby_facilities(row, facilities):
    circle = row.geometry.buffer(0.001)
    number_of_bus_stops = len(facilities[(facilities.geometry.within(circle)) & (facilities['CLASS'] == 'BUS')])
    number_of_MTR_stations = len(facilities[(facilities.geometry.within(circle)) & (facilities['CLASS'] == 'TRS') & ((facilities['TYPE'] == 'RSN') | (facilities['TYPE'] == 'MTA') | (facilities['TYPE'] == 'LRA'))])
    number_of_commercial_facilities = len(facilities[(facilities.geometry.within(circle)) & ((facilities['CLASS'] == 'COM') | (facilities['CLASS'] == 'MUF') | (facilities['CLASS'] == 'RSF'))])
    number_of_government_facilities = len(facilities[(facilities.geometry.within(circle)) & (facilities['CLASS'] == 'GOV')])
    number_of_religious_facilities = len(facilities[(facilities.geometry.within(circle)) & (facilities['CLASS'] == 'REL')])
    number_of_medical_facilities = len(facilities[(facilities.geometry.within(circle)) & (facilities['CLASS'] == 'HNC')])
    number_of_hotel_facilities = len(facilities[(facilities.geometry.within(circle)) & (facilities['CLASS'] == 'AMD')])
    number_of_schools = len(facilities[(facilities.geometry.within(circle)) & (facilities['CLASS'] == 'SCH')])
    return number_of_bus_stops, number_of_MTR_stations, number_of_schools, number_of_commercial_facilities, number_of_government_facilities, number_of_religious_facilities, number_of_medical_facilities, number_of_hotel_facilities

# try to map sample_data to relevant features
# first, map sample_data to number of nearby restaurants
sample_data['number_of_nearby_restaurants'] = sample_data.apply(number_of_nearby_restaurants, competitor_data = competitor_data, axis = 1)

# second, map sample_data to number of nearby facilities
sample_data['number_of_bus_stops'], sample_data['number_of_MTR_stations'], sample_data['number_of_schools'], sample_data['number_of_commercial_facilities'], sample_data['number_of_government_facilities'], sample_data['number_of_religious_facilities'], sample_data['number_of_medical_facilities'], sample_data['number_of_hotel_facilities'] = zip(*sample_data.apply(find_nearby_facilities, facilities = geospatial_data, axis = 1))

# third, find census_subnit for each vacant store first
sample_data['census_subnit'] = sample_data.apply(lambda row: census_data[census_data['geometry'].contains(Point(row['lng'], row['lat']))]['name'].values[0], axis=1)
# join census data to sample data by census_subnit == name
sample_data = sample_data.merge(census_data, left_on = 'census_subnit', right_on = 'name', how = 'left')
# drop the duplicated column 'name' and geometry column
sample_data = sample_data.drop(['name', 'geometry_x', 'geometry_y'], axis = 1)

# finally, save the mapped data to geojson file, but convert sample_data to geodataframe first
sample_data = gpd.GeoDataFrame(sample_data, geometry = gpd.points_from_xy(sample_data.lng, sample_data.lat))
sample_data.to_file('data_source/demo_vacant_store_mapped.geojson', driver = 'GeoJSON')
