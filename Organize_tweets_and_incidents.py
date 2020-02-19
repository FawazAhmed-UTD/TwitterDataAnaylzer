'''
Orders the tweets from MongoDB and the incidents from the incident file by date
Saves in tweets.csv
'''
import csv
import pymongo
from datetime import timedelta, date, datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
data_base = client['TwitterSearcher']
collection = data_base["Old Tweets Data"]

fieldnames = ["Date", "Incident/s", "Incident Count", "Tweet/s", "Tweet Count"]
start_date = date(2017, 12, 1)
end_date = date(2018, 6, 1)
delta = timedelta(days=1)
incident_dates = []

with open('reported_incidents_v2.json', 'r') as file:
    for x in file:
        incident_dates.append(json.loads(x))

with open('tweets.csv', mode='w', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator = '\n')
    writer.writeheader()

    while start_date <= end_date:
        row = {'Date': str(start_date)}
        tweets = []
        incidents = []

        for tweet in collection.find({'Search Query': 'Accident place:Lagos,Nigeria lang:en'}):
            formatted_date = datetime.strptime(tweet['created_at'][0:10] + ' ' + tweet['created_at'][-4:],
                                               '%a %b %d %Y').strftime('%Y-%m-%d')
            if str(start_date) == str(formatted_date):
                tweets.append(tweet['id'])
        row.update({'Tweet/s': tweets, 'Tweet Count': len(tweets)})

        for incident in incident_dates[0]:
            formatted_date = datetime.strptime(incident['date'][:-2] + '20' + incident['date'][-2:], '%m/%d/%Y')\
                .strftime('%Y-%m-%d')
            if str(start_date) == str(formatted_date):
                incidents.append(incident['id'])

        row.update({'Incident/s': incidents, 'Incident Count': len(incidents)})
        try:
            writer.writerow(row)
        except:
            writer.writerow(row)

        start_date += delta
