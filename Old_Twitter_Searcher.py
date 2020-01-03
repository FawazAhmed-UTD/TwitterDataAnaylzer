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
    with open('tweets.json') as File:
        for tweet in File:
            new_data.append(json.loads(tweet))
    new_data.append(results)
    with open('tweets.json', 'w') as File:
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
        'geo': str(tweet.geo)
    }
    return tweet_data


def API():  # authenticates with tweepy
    authenticator = tweepy.OAuthHandler(consumer_api_key, consumer_api_key_secret)
    api = tweepy.API(authenticator)
    return api


def store_in_mongoDB(single_dict, error_count):  # takes in one dict
    global collection
    try:
        collection.insert_one(single_dict)
    except:
        try:
            collection.insert_many(single_dict)
        except:
            error_count += 1
            if error_count < 500:
                try:
                    store_results_in_file(single_dict)
                except:
                    error = {'error': str(single_dict)}
                    store_results_in_file(error)
    return error_count


def get_file_data(file_name):
    with open(file_name, "r") as read:
        fileData = json.load(read)
    return fileData


def searchTwitter(sinceDate, untilDate, query, place, lang, misc):
    tweets_got = []
    tweets_api_ids = []
    tweets_to_store = []

    search_query = set_searchQuery(query, place, lang, misc)
    api_sinceDate = sinceDate.replace('-', '') + "0000"
    api_untilDate = untilDate.replace('-', '') + "0000"

    tweetCriteria = got.manager.TweetCriteria() \
        .setQuerySearch(query) \
        .setNear(place) \
        .setMaxTweets(0) \
        .setSince(sinceDate) \
        .setUntil(untilDate) \
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
        tweets_to_store.append(tweet_raw)
        tweets_api_ids.append(tweet_raw["id_str"])

    for tweet in tweets_got:
        if tweet["id_str"] not in tweets_api_ids:
            tweets_to_store.append(tweet)
    print("Storing ", len(tweets_to_store), " Tweets")
    return tweets_to_store


def set_searchQuery(query, place, lang, misc):
    searchQuery = {'Search Query': ""}

    if query != "":
        searchQuery = {'Search Query': searchQuery['Search Query'] + query}
    if place != "":
        searchQuery = {'Search Query': searchQuery['Search Query'] + " place: " + place}
    if lang != "":
        searchQuery = {'Search Query': searchQuery['Search Query'] + " lang:" + lang}
    if misc != "":
        searchQuery = {'Search Query': searchQuery['Search Query'] + misc}
    return searchQuery


if __name__ == '__main__':
    error_count = 0
    tweet_count = 0
    setQuery = "Accident"
    setPlace = "Dallas, TX"
    setLang = "en"
    setMisc = "-is:retweet"
    requestDates = get_file_data("requestDates.json")

    for date in requestDates:
        print("Since: " + date['Since'])
        print("Until: " + date['Until'])

        results = searchTwitter(date['Since'], date['Until'], setQuery, setPlace, setLang, setMisc)
        tweet_count += len(results)
        for tweet in results:
            error_count += store_in_mongoDB(tweet, error_count)

    print(error_count, " Tweets out of ", tweet_count, " Failed")
