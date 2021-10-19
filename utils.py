from pprint import pprint

def initDict():
    dictDF = {'business_status':[],'name':[],'type':[],'address':[],'price_level':[],'rating':[],'Users_Rating':[]}
    return dictDF

def exportToCsvfile(info, nameCsv= None):
    result = {}
    result['address'] = info['formatted_address']
    result['latitude'] = info['geometry']['location']['lat']
    result['longtitude'] = info['geometry']['location']['lng']
    result['place_id'] = info['place_id']

    return result