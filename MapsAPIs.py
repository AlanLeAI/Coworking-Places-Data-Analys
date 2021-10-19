from pprint import pprint
import googlemaps
from datetime import datetime
import pandas as pd
import time
import numpy as np

from utils import initDict, exportToCsvfile

# Location of coworking space to investigate 
location_names = [
    '5255 Winthrop Ave #110, Indianapolis, IN 46220',
    '85 E Cedar St #1502, Zionsville, IN 46077',
    '12175 Visionary Way, Fishers, IN 46038',
    '350 Massachusetts Ave Suite 300, Indianapolis, IN 46204',
    '525 S Meridian St, Indianapolis, IN 46225'
]

# Put your API keys in APIkey.txt file
try:
    with open('APIkey.txt','r') as f:
        keys = f.read()
    gmaps = googlemaps.Client(key=keys)
except googlemaps.exceptions.ApiError:
    print("API can not be accessed")

# Get the latitude and longtitude of the location address
def get_place_info(location_name):
    try:
        response = gmaps.places(query=location_name)
        results = response.get("results")
        return results[0]
    except Exception as e:
        print(e)
        return None


# Get restaurants neabry the location address
# Input: a tuple contains (Latitude, Longtitude) of the location
# Output: a dataframe of the list of restaurants in 5 miles away
# Features : Status, Name, Type, Address, Price Level, Rating and Users rating

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
    # Capturing all the dataframe of restaurants nearby the location 
    listOfDF = []
    # Capturing the list of all the sheet name for each dataframe 
    nameOfExcels = []
    
    for location_name in location_names:
        nameOfExcel = location_name.split(' ')
        nameOfExcel = nameOfExcel[1:3]
        nameOfExcel = ''.join(nameOfExcel)
        nameOfExcels.append(nameOfExcel)
        results = get_place_info(location_name)
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
        df = getRestaurant((lat,lng), "restaurant", 5)
        listOfDF.append(df)


    with pd.ExcelWriter('submission.xlsx') as writer:
        for i in range(len(nameOfExcels)):
            listOfDF[i].to_excel(writer,sheet_name = nameOfExcels[i])
        
            

    
