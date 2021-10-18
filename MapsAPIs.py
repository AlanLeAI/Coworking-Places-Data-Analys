from pprint import pprint
import googlemaps
from datetime import datetime
import pandas as pd
import time
import numpy as np

from utils import initDict

# Location of coworking space to investigate 
location_name = '525 S Meridian St, Indianapolis, IN 46225'

# Put your API keys in APIkey.txt
try:
    with open('APIkey.txt','r') as f:
        keys = f.read()
    gmaps = googlemaps.Client(key=keys)
except googlemaps.exceptions.ApiError:
    print("API can not be accessed")


def get_place_info(location_name):
    try:
        response = gmaps.places(query=location_name)
        results = response.get("results")
        return results[0]
    except Exception as e:
        print(e)
        return None

def exportToCsvfile(info, nameCsv= None):
    result = {}
    result['address'] = info['formatted_address']
    result['latitude'] = info['geometry']['location']['lat']
    result['longtitude'] = info['geometry']['location']['lng']
    result['place_id'] = info['place_id']

    return result

def getRestaurant(location, search_string, distance):
    distance = distance*1_609.344
    response = gmaps.places_nearby(
        location = location,
        keyword =  search_string,
        radius = distance
    )
    response = response.get("results")
    dictDF = initDict()
    for restaurant in response:
        dictDF["business_status"].append(restaurant['business_status'])
        latitude = restaurant['geometry']['location']['lat']
        longtitude =restaurant['geometry']['location']['lng']
        dictDF['address'].append(gmaps.reverse_geocode((latitude,longtitude))[0]['formatted_address'])
        dictDF["name"].append(restaurant['name'])
        try:
            dictDF['price_level'].append(restaurant['price_level'])
        except:
            dictDF['price_level'].append(np.nan)
        dictDF['rating'].append(restaurant['rating'])
        dictDF['Users_Rating'].append(restaurant['user_ratings_total'])
        dictDF['type'].append(','.join(restaurant["types"]))
    dictDF = pd.DataFrame(dictDF)
    return dictDF





if __name__ == '__main__':
    results = get_place_info(location_name)
    lat = results['geometry']['location']['lat']
    lng = results['geometry']['location']['lng']
    df = getRestaurant((lat,lng), "restaurant", 5)
    df.to_excel("SMeridian.xlsx")
   
