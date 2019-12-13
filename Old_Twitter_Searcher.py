import GetOldTweets3 as got
from datetime import datetime, timedelta
import json


def get_tweets(longitude, latitude, date_time):
    untilDate = datetime.strptime(str(date_time)[0:10], '%Y-%m-%d') + timedelta(days=1)
    sinceDate = datetime.strptime(str(date_time)[0:10], '%Y-%m-%d') - timedelta(days=1)
    accidentTime = str(date_time)[11:19]
    tweets_data = []

    if accidentTime < "00:05:00":  # edge case where tweet accidentTime is near midnight
        tweetCriteria = got.manager.TweetCriteria().setSince(str(sinceDate)[0:10]).setUntil(str(untilDate)[0:10]) \
            .setQuerySearch("Accident").setNear(str(longitude) + ", " + str(latitude)).setMaxTweets(100)  # searches
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)  # stores results
        for new_tweet in tweets:
            tweets_data.append(get_tweet_data(new_tweet))  # stores in a list of dicts
            # if is_time_between(accidentTime, str(tweet.time)[11:19], midnight=True):
            #     tweets_data.append(get_tweet_data(tweet))  # stores in a list of dicts
    else:
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch("Accident") \
            .setNear(str(longitude) + ", " + str(latitude)).setMaxTweets(100).setSince(str(sinceDate)[0:10]) \
            .setUntil(str(untilDate)[0:10])  # searches
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)  # stores results
        for new_tweet in tweets:
            tweets_data.append(get_tweet_data(new_tweet))  # stores in a list of dicts
            # if is_time_between(accidentTime, str(tweet.date)[11:19], midnight=False):
            #     tweets_data.append(get_tweet_data(tweet))
    return tweets_data


def is_time_between(check_time, tweet_time, midnight):  # compares tweet time if it is in range
    if midnight:  # edge case
        begin_time = "23:55:00"
        end_time = str(datetime.strptime(check_time, '%H:%M:%S') + timedelta(minutes=30))
        return tweet_time >= begin_time or tweet_time <= end_time
    else:
        begin_time = str(datetime.strptime(check_time, '%H:%M:%S') - timedelta(minutes=5))[11:19]
        end_time = str(datetime.strptime(check_time, '%H:%M:%S') + timedelta(minutes=20))[11:19]
        return begin_time <= tweet_time <= end_time


def get_tweet_data(tweet):  # returns dict of the tweet's data
    tweet_data = {
        'id': str(tweet.id),
        'link': str(tweet.permalink),
        'username': str(tweet.username),
        'to': str(tweet.to),
        'text': str(tweet.text),
        'date': str(tweet.date),
        'retweets': str(tweet.retweets),
        'favorites': str(tweet.favorites),
        'mentions': str(tweet.mentions),
        'hashtags': str(tweet.hashtags),
        'geo': str(tweet.geo)
    }
    return tweet_data


def get_useable_datetime(accidentDate, accidentTime):
    accidentDate = datetime.strptime(accidentDate, '%m/%d/%y').strftime('%Y-%m-%d')
    accidentTime = datetime.strptime(accidentTime, '%I:%M %p').strftime('%H:%M')
    return datetime.strptime(accidentDate + " " + accidentTime + ":00", '%Y-%m-%d %H:%M:%S')


def get_incident_info(incidentData, x):
    incidentData_dict = {'location': incidentData[x]['maps_output'][0]['geometry']['location'],
                         'time': incidentData[x]['time'],
                         'incident_id': incidentData[x]['id'],
                         'date': incidentData[x]['date']}
    return incidentData_dict


def store_results_in_file(result, incident_id):  # Stores into a json and csv
    new_data = []
    with open('tweets_v2.json') as File:
        for tweet in File:
            new_data.append(json.loads(tweet))

    result = {"Incident_id": incident_id, 'Tweet Number': len(result), 'Twitter Data': result}
    new_data.append(result)

    with open('tweets_v2.json', 'w') as File:
        for y in new_data:
            json.dump(y, File)
            File.write('\n')


if __name__ == '__main__':
    with open("reported_incidents_v2.json", "r") as read:
        data = json.load(read)

    for x in range(len(data)):
        try:
            incidentData = get_incident_info(data, x)
            results = get_tweets(incidentData['location']['lat'], incidentData['location']['lng'],
                                 get_useable_datetime(incidentData['date'], incidentData['time']))
            store_results_in_file(results, incidentData['incident_id'])
        except:
            print("Error in location, time, date, or incident_id for iteration: ", x)
