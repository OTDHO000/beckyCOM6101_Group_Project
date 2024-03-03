from flask import request, jsonify
import pandas as pd
from flask import Blueprint
from backend import Backend

queryinfo = Blueprint('QueryInfoController',__name__)

    
def responseMsg( data):
    respSuccess = {'status':'success'}
    respErr = {'status':'error'}
    
    if not data:
        return respErr
        
    else:
        respSuccess['places'] = data
        return respSuccess
    
@queryinfo.route('/querytest/<id>', methods=['POST','GET'])
def get_string(id):
    print(id)
    return responseMsg("")

@queryinfo.route('/queryinfo',methods=['POST','GET'])
def QueryInfo():
    # industry = 'restaurant', type = 'RR', district = 'Kwai Tsing District', sub_district = 'Kwai Chung', rent_min
    json = request.json
    industry_req =  json.get('industry')
    type_req =   json.get('type')
    district_req = json.get('district')
    sub_district_req = json.get('sub_district')
    rent_min_req = json.get('rent_min')
    rent_max_req = json.get('rent_max')

    print("request parameter-----")
    print(industry_req,type_req,district_req,sub_district_req,rent_min_req,rent_max_req)

    geodataframe = Backend(industry=industry_req, type=type_req, district=district_req,sub_district=sub_district_req, 
            rent_min=rent_min_req, rent_max=rent_max_req).calculate_score()
    # Backend(industry = 'restaurant', type = 'RR', district = 'Kwai Tsing District', sub_district = 'Kwai Chung', rent_min = 0, rent_max = 50000).calculate_score()

    # Backend(industry=industry_req, type=type_req, district=district_req,sub_district=sub_district_req, 
    #         rent_min=rent_min_req, rent_max=50000).calculate_score()
    
    res = pd.DataFrame(geodataframe)
    places = res[["lng","lat", "store_id", "rent", "competition", "accessibility", "facilities", "demographic","score"]].head(5).to_dict(orient= "records")

    return responseMsg(places)

