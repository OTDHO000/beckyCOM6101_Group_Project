# visualise LSUG_21C.json to a map
import geopandas as gpd
import folium

gpdf = gpd.read_file('LSUG_21C.json')

# create a map object, centered on Hong Kong
m = folium.Map(location=[22.3, 114.1], zoom_start=10)
folium.GeoJson(data=gpdf["geometry"]).add_to(m)

# add other layers to the map fr

# export map to html
m.save('LSUG_21C.html')