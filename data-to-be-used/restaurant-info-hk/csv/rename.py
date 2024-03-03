import pandas as pd
import os

path = 'restaurant-info-hk\csv'

# rename all files to first 6 digits of filename only

for filename in os.listdir(path):
    if filename.endswith('.csv'):
        df = pd.read_csv(path + '\\' + filename)
        df.to_csv(path + '\\' + filename[:6] + '.csv', index=False)
        os.remove(path + '\\' + filename)
        print(filename + ' renamed to ' + filename[:6] + '.csv')
        