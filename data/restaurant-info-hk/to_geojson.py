import pandas as pd
import geopandas as gpd

df = pd.read_csv('restaurant-info-hk/geo_full/211201.csv.geo.csv')

# transform to geodataframe, lat and lng are the column names of the coordinates
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lng, df.lat))

count = 0

while count < 4:
    # randomly delete some rows, let's say delete 500 rows
    # this is for demonstrating how we do machine learning on the data
    gdf = gdf.sample(frac=1).reset_index(drop=True)
    gdf = gdf.iloc[500:]

    # save as geojson, name the file as 210531_geo_mapped + 'random_1' + '.geojson'
    gdf.to_file('restaurant-info-hk/geo_mapped/211201_geo_mapped_random_' + str(count) + '.geojson', driver='GeoJSON')
    count += 1
