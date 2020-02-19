'''
Simple Old twitter api searcher
Tokens and keys are blank and need to be filled
'''

import pymongo
import tweepy

client = pymongo.MongoClient('mongodb://localhost:27017/')
data_base = client['']
collection = data_base['']

access_token = ""
access_token_Secret = ""
consumer_api_key = ""
consumer_api_key_secret = ""
LABEL = ''

searchQuery = {'Search Query': 'Accident place:Lagos,Nigeria lang:en'}
'''
reference: https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators
'''
tweets_to_store = []


def API():  # authenticates with tweepy
    authenticator = tweepy.OAuthHandler(consumer_api_key, consumer_api_key_secret)
    api = tweepy.API(authenticator)
    return api


for tweet in tweepy.Cursor(API().search_full_archive,
                           query=searchQuery['Search Query'],
                           environment_name=LABEL,
                           maxResults=100,
                           fromDate='201712010000',
                           toDate='201806020000').items():
    tweet_raw = tweet._json
    tweet_raw.update(searchQuery)
    tweets_to_store.append(tweet_raw)
for tweet in tweets_to_store:
    collection.insert_one(tweet)
