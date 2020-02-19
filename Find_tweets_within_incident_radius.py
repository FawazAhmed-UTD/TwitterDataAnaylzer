'''
Given a radius this program will find tweets within the radius of the incident of that day.
Uses mongoDB and tweets.csv
Takes 1-2 min to finish
'''

import re
import csv
import pymongo
import json
from math import radians, cos, sin, asin, sqrt

client = pymongo.MongoClient('mongodb://localhost:27017/')
data_base = client['TwitterSearcher']
collection = data_base["Old Tweets Data"]

incidents = []
tweets = []
date_dict = {}
dates = []
collected_data = []

'''
Change the radius
'''
radius = 15.00


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


with open('reported_incidents_v2.json', 'r') as file:
    for x in file:
        incidents.append(json.loads(x))
    incidents = incidents[0]

with open('tweets.csv', mode='r', encoding='utf-8') as file:
    readCSV = csv.reader(file, delimiter=',')
    for row in readCSV:
        save_in_dict = []
        dates_incidents = re.sub('[,\[\]]', '', row[1])
        dates_incidents = dates_incidents.split()
        save_in_dict.append({'Incidents': dates_incidents})

        tweet_incidents = re.sub('[,\[\]]', '', row[3])
        tweet_incidents = tweet_incidents.split()
        save_in_dict.append({'Tweets': tweet_incidents})

        date_dict = {str(row[0]): save_in_dict}

        dates.append(date_dict)

dates.pop(0)

for date in dates:
    incident_point = []
    tweet_point = []
    for key in date:
        for incident in incidents:
            for incident_id in date[key][0]['Incidents']:  # We start looping through the incidents per date
                if str(incident['id']) == incident_id:  # If we found it
                    try:  # some incidents dont have lat/lng
                        incident_point = [{'lat': incident['maps_output'][0]['geometry']['location']['lat'],
                                           'lng': incident['maps_output'][0]['geometry']['location']['lng']}]
                    except:
                        incident_point = []
                    for tweet_id in date[key][1]['Tweets']: # Looping through the tweet ids
                        for x in collection.find({'id_str': tweet_id,
                                                  'Search Query': 'Accident place:Lagos,Nigeria lang:en'}):
                            if x['geo'] is not None:
                                tweet_point = [{'lat': x['geo']['coordinates'][0], 'lng': x['geo']['coordinates'][1]}]
                            else:
                                tweet_point = []
                        if len(tweet_point) == 0 or len(incident_point) == 0:
                            break
                        lat1 = incident_point[0]['lat']
                        lon1 = incident_point[0]['lng']
                        lat2 = tweet_point[0]['lat']
                        lon2 = tweet_point[0]['lng']
                        a = haversine(lon1, lat1, lon2, lat2)
                        if a < radius:
                            found_in_radius = {'Radius': radius,
                                               'Incident_id': incident_id,
                                               'Incident_point': incident_point,
                                               'Tweet_id': tweet_id,
                                               'Tweet_point': tweet_point,
                                               'Date': key}
                            collected_data.append(found_in_radius)
                    break

'''
collected_data is a list of dics
'''
print(len(collected_data))
# pprint(collected_data)
