import GetOldTweets3 as got
import tweepy
import json
import pymongo

'''
Twitter Authentication
'''
access_token = "XXXX"
access_token_Secret = "XXXX"
consumer_api_key = "XXXX"
consumer_api_key_secret = "XXXX"
PRODUCT = 'XXXX'
LABEL = 'XXXX'
'''
MongoDB
'''
client = pymongo.MongoClient('mongodb://localhost:XXXX/')
data_base = client['XXXX']
collection = data_base["XXXX"]


def store_results_in_file(results):  # Stores into a json and csv
    new_data = []
    with open('XXXX.json') as File:
        for tweet in File:
            new_data.append(json.loads(tweet))
    new_data.append(results)
    with open('XXXX.json', 'w') as File:
        for x in new_data:
            json.dump(x, File)
            File.write('\n')


def get_tweet_data(tweet):  # returns dict of the tweet's data
    tweet_data = {
        'id_str': str(tweet.id),
        'link': str(tweet.permalink),
        'username': str(tweet.username),
        'to': str(tweet.to),
        'text': str(tweet.text),
        'created_at': str(tweet.date),
        'retweets': str(tweet.retweets),
        'favorites': str(tweet.favorites),
        'mentions': str(tweet.mentions),
        'hashtags': str(tweet.hashtags),
        'geo': str(tweet.geo),
        'url': "https://twitter.com/" + str(tweet.username) + "/status/" + str(tweet.id)
    }
    return tweet_data


def API():  # authenticates with tweepy
    authenticator = tweepy.OAuthHandler(consumer_api_key, consumer_api_key_secret)
    api = tweepy.API(authenticator)
    return api


def store_in_mongoDB(single_dict):  # takes in one dict
    collection.insert_one(single_dict)


def get_file_data(file_name):
    with open(file_name, "r") as read:
        fileData = json.load(read)
    return fileData


if __name__ == '__main__':
    tweets_got = []
    tweets_api = []
    tweets_api_ids = []

    query = "Accident"
    place = "Dallas, TX"
    lang = "en"
    misc = "-is:retweet"

    search_query = {'Search Query': query + " place:\"" + place + "\" lang:" + lang + " " + misc}
    requestDates = get_file_data("XXXX.json")

    for date in requestDates:
        tweets_to_store = []
        api_sinceDate = date['Since'].replace('-', '') + "0000"
        api_untilDate = date['Until'].replace('-', '') + "0000"

        tweetCriteria = got.manager.TweetCriteria() \
            .setQuerySearch(query) \
            .setNear(place) \
            .setMaxTweets(0) \
            .setSince(date['Since']) \
            .setUntil(date['Until']) \
            .setLang(lang)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        for tweet in tweets:
            tweet_raw = get_tweet_data(tweet)
            tweet_raw.update(search_query)
            tweets_got.append(tweet_raw)

        for tweet in tweepy.Cursor(API().search_full_archive,
                                   query=search_query['Search Query'],
                                   environment_name=LABEL,
                                   maxResults=500,
                                   fromDate=api_sinceDate,
                                   toDate=api_untilDate).items():
            tweet_raw = tweet._json
            tweet_raw.update(search_query)
            tweets_api.append(tweet_raw)
            tweets_api_ids.append(tweet_raw["id_str"])

        for tweet in tweets_got:
            if tweet["id_str"] not in tweets_api_ids:
                tweets_to_store.append(tweet)

        for tweet in tweets_to_store:
            store_in_mongoDB(tweet)
