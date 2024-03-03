'''
Logic: User sends request from frontend, for example, the rent range, the type of store, the industry, and the location
Backend receives these data and will find the vacant stores that meet the requirements in the database
Then the model will score these stores
Finally, the result will be sent back to the frontend
'''
from flask import Flask
import pandas as pd
import geopandas as gpd
from sklearn.preprocessing import StandardScaler
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
# create a Flask app
# app = Flask(__name__)

# # a class object to process the request from frontend, searching suitable vacant stores in the database, calculating the score and sending the result back to frontend

database_path = 'data_source/demo_vacant_store_mapped.geojson'

class Backend:
    def __init__(self, industry, type, district, sub_district, rent_min = 0, rent_max = 100000):
        self.industry = industry
        self.type = type
        self.district = district
        self.sub_district = sub_district
        self.rent_min = rent_min
        self.rent_max = rent_max
        self.database = gpd.read_file(database_path)
    def search(self):
        # from the database, find the vacant stores that meet the requirements
        # return a list of vacant stores
        # convert the district and sub_district to lsbg first
        lsbg_dict = {'Kwai Tsing District' : {'Kwai Chung' : ['320', '326', '327', '328', '329'], 'Tsing Yi' : ['350', '351']}, 
                    'Tsuen Wan District':{'Tsuen Wan' : ['310', '321', '322', '323', '324'], 'Lei Muk Shue' : ['325'], 'Ting Kau' : ['731'],
                    'Sham Tseng' : ['335', '336'], 'Ma Wan' : ['975']}}
        lsbg = lsbg_dict[self.district][self.sub_district]
        # find which rows in the database meet the requirements
        database_meet = self.database[(self.database['lsbg'].isin(lsbg)) & (self.database['rent'] >= self.rent_min) & (self.database['rent'] <= self.rent_max)]
        return database_meet
    def calculate_score(self):
        vacant_store_list = self.search()
        param_path = 'data_source/'
        # by the self.industry and self.type, find the relevant parameters for calculating the score
        # if self.industry == 'restaurant' and self.type == 'RR', use param_RR.csv to calculate the weight score
        # if self.industry == 'restaurant' and self.type == 'RL', use param_RL.csv to calculate the weight score
        param_dict = {}
        if self.industry == 'restaurant' and self.type == 'RR':
            param_file = pd.read_csv(param_path + 'param_RR.csv')
        elif self.industry == 'restaurant' and self.type == 'RL':
            param_file = pd.read_csv(param_path + 'param_RL.csv')
        for i in range(len(param_file)):
            param_dict[param_file['feature'][i]] = param_file['weight'][i]
        # calculate the score for each vacant store, based on the parameters. but we need to scale the features columns with StandardScaler first
        # find out the features columns first, then scale them
        features = list(param_dict.keys())
        scaler = StandardScaler()
        vacant_store_list.loc[:, features] = scaler.fit_transform(vacant_store_list[features])
        # to dtype = float
        vacant_store_list.loc[:, features] = vacant_store_list[features].astype(float)
        # calculate score for each component, for example, vacant_store_list['number_of_nearby_restaurants_score'] = vacant_store_list['number_of_nearby_restaurants'] * param_dict['number_of_nearby_restaurants'] * 10.5
        for i in features:
            vacant_store_list[i] = np.abs(vacant_store_list[i] * param_dict[i]) * 92
        # group scores to different categories: param_dict[0].keys() is the categories "competition"
        # param_dict[1:2].keys() is the categories "accessibility"
        # param_dict[3:8].keys() is the categories "facilities"
        # param_dict[9:].keys() is the categories "demographic"
        vacant_store_list['competition'] = vacant_store_list[list(param_dict.keys())[0:1]].sum(axis = 1)
        vacant_store_list['accessibility'] = vacant_store_list[list(param_dict.keys())[1:2]].sum(axis = 1)
        vacant_store_list['facilities'] = vacant_store_list[list(param_dict.keys())[3:8]].sum(axis = 1)
        vacant_store_list['demographic'] = vacant_store_list[list(param_dict.keys())[9:]].sum(axis = 1)
        # balancing the score weight for different categories, reduce the weight of "competition" by * 0.75
        # increase other categories by * 1.25
        vacant_store_list['competition'] = vacant_store_list['competition'] * 0.75
        vacant_store_list['accessibility'] = vacant_store_list['accessibility'] * 1.25
        vacant_store_list['facilities'] = vacant_store_list['facilities'] * 1.25
        vacant_store_list['demographic'] = vacant_store_list['demographic'] * 1.25
        # calculate the total score by summing up the scores in different categories
        vacant_store_list['score'] = vacant_store_list[['competition', 'accessibility', 'facilities', 'demographic']].sum(axis = 1).astype(int)
        # sort the vacant_store_list by score
        vacant_store_list = vacant_store_list.sort_values(by = 'score', ascending = False)
        # change all categories scores to int
        vacant_store_list[['competition', 'accessibility', 'facilities', 'demographic']] = vacant_store_list[['competition', 'accessibility', 'facilities', 'demographic']].astype(int)
        # return top 10 vacant stores only
        vacant_store_list = vacant_store_list.head(10)
        return vacant_store_list

# try to use the backend class, by district = 'Kwai Tsing District', sub_district = 'Kwai Chung', industry = 'restaurant', type = 'RR', rent_min = 10000, rent_max = 20000
backend = Backend(industry = 'restaurant', type = 'RR', district = 'Kwai Tsing District', sub_district = 'Kwai Chung', rent_min = 0, rent_max = 50000).calculate_score()

# total score is store in 'score' column
# the frontend should show the 'score' column to the user first
# then show the marks allocation of 'competition', 'accessibility', 'facilities', 'demographic' columns to the user

print(backend)

