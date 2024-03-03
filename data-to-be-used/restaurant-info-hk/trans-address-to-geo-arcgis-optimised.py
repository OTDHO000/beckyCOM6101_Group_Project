# transform address to geo location, with arcgis geocoding, then save to csv file
import os
import pandas as pd
import geocoder

API_KEY = "AAPK3ac33a03387e472db4ac246ec302438c69Oee1EeJzIYy8Qlsbogx5ZziXUuE247Xeb2ASN4douVyGLHZ9MwCGHEtPdJPJz8"

folder_path = 'restaurant-info-hk/csv'
output_folder = 'restaurant-info-hk/geo'

# create output folder if not exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Iterate through all CSV files in the folder_path
# columns: TYPE, DIST, LICNO, SS, ADR, INFO, EXPDATE
# column ADR is the address

# use old csv file to reference if address already exist
old_file = 'restaurant-info-hk/geo/old_file.csv'

for filename in os.listdir(folder_path):
    # only retrive csv file and file not end with .finished.csv
    if filename.endswith(".csv") and not filename.endswith(".finished.csv"):
        print(f'start converting {filename} to geo location')
        csv_file = os.path.join(folder_path, filename)
        geo_file = os.path.join(output_folder, filename + ".geo.csv")
        # find rows if ADR contains ['KWAI CHUNG"] or ['TSUEN WAN']
        # transform ADR to upper case first
        df = pd.read_csv(csv_file, encoding='utf-8')
        df['ADR'] = df['ADR'].str.upper()
        df = df.loc[lambda df: df['ADR'].str.contains('KWAI CHUNG') | df['ADR'].str.contains('TSUEN WAN')]
        # add new columns for geo location
        lat = []
        lng = []
        df.reset_index(inplace=True, drop=True)
        # check if df['ADR'] == old_df['ADR']
        old_df = pd.read_csv(old_file, encoding='utf-8')
        for i in range(len(df)):
            if df['ADR'][i] in old_df['ADR'].values:
                # if address already exist in old_df, then use the geo location in old_df
                lat.append(old_df.loc[old_df['ADR'] == df['ADR'][i], 'lat'].iloc[0])
                lng.append(old_df.loc[old_df['ADR'] == df['ADR'][i], 'lng'].iloc[0])
                print(f"Converted {df['ADR'][i]} to {old_df.loc[old_df['ADR'] == df['ADR'][i], 'lat'].iloc[0]}, {old_df.loc[old_df['ADR'] == df['ADR'][i], 'lng'].iloc[0]}, by referencing old csv file")
                continue
            g = geocoder.arcgis(df['ADR'][i], key = API_KEY)
            lat.append(g.lat)
            lng.append(g.lng)
            print(f"Converted {df['ADR'][i]} to {g.lat}, {g.lng}")
        df['lat'] = lat
        df['lng'] = lng
        df.to_csv(geo_file, index=False)
        # rename the original csv file to finished
        os.rename(csv_file, os.path.join(folder_path, filename + ".finished.csv"))
        print(f"Converted {filename} to {filename}")
print("All csv files converted to geo location")