import tweepy, schedule, time, json, pymongo
from pprint import pprint
from geopy.geocoders import Nominatim
numInc = 0
radius = 10
accessToken = "3939721633-EJIfdOWAcuWVjwFpsQp7Qs3P5NNyh3q7ihpC9ld"
accessToken_Secret = "wyQ9uA8vZ02Ni2fimTJegOSdIJTO95ttIJWWkDZUxl5cZ"
apiKey = "8VQzfyd9REr8gO2nesBRkJTru"
apiKey_Secret = "2CS4iYIdBq6SNSmTJCWUFJuhOjAkN4b68bXkOIS7nYouuh7r8n"

def authenticate(): #authenticates with tweepy
	global accessToken, accesssToken_Secret, apiKey, apiKey_Secert
	authenticator = tweepy.OAuthHandler(apiKey, apiKey_Secret)
	API = tweepy.API(authenticator)
	return API

#This func compares tweets that were searched with only the search query with tweets that were searched with both the search query and coordinates
#it then updates the first set of tweets on whether it was tweeted in the location or not
#this is because searching with location and a query in tweepy does not give tweets from users who may have tweeted about the accident but are not in the general radius.
def compareResults(results_without_location, results_with_location):
	global radius, last_tweetID
	i = 0
	tweets_set1 = []
	tweets_set2 = []
	tweetedIn = {'Tweeted within' : str(radius) + ' miles'}				#either one of these two dicts will be updated to the first set of tweets
	tweetedOut = {'Not tweeted within' : str(radius) + ' miles'}
	for tweet in results_without_location: 						#stores tweets with out location in a dict
		tweets = {'Username' : tweet.user.screen_name, 'Tweet' : tweet.text}
		last_tweetID = tweet.id
		tweets_set1.append(tweets)
		i+=1
	i = 0
	for tweet in results_with_location:						#same thing here but with tweets with a location
		tweets = {'Username' : tweet.user.screen_name, 'Tweet' : tweet.text}
		tweets_set2.append(tweets)
		i+=1
	len1 = len(tweets_set1)
	len2 = len(tweets_set2)
	for x in range(len1):
		for y in range(len2):
			if tweets_set1[x] == tweets_set2[y]:
				tweets_set1[x].update(tweetedIn)
				break
			else:
				tweets_set1[x].update(tweetedOut)

#	storeResults(tweets_set1)
	mongoDB(tweets_set1)

def mongoDB(results):	#Stores in mongodb
	client = pymongo.MongoClient('mongodb://localhost:27017/')
	dataBase = client['TwitterSearcher']
	collection = dataBase["Tweets Data"]
	oldData = []
	tweets = []
	for x in collection.find():
		oldData.append(x)
	for i in oldData:
		if "_id" in i:
			del i["_id"]
	for i in oldData:
		if i not in tweets:
			tweets.append(i)
	for i in results:
		if i not in tweets:
			tweets.append(i)
#	pprint(tweets)
	delete = collection.delete_many({})
	print(str(len(tweets)))
	for i in tweets:
		tweet = collection.insert_one(i)
#	print(dataBase.list_collection_names())

def storeResults(results): #Stores into a json
	oldData = []
	tweets = []
	with open('output.json') as file:
		for tweet in file:
			oldData.append(json.loads(tweet))
	for i in oldData:
		if i not in tweets:
			tweets.append(i)
	for i in results:
		if i not in tweets:
			tweets.append(i)
	with open('output.json', 'w') as file:
		for x in range(len(tweets)):
			json.dump(tweets[x], file)
			file.write('\n')
def search_without_location(searchQuery): #searches with out a location
	results = authenticate().search(q=searchQuery, lang = "en", count = 100)
	return results

def search_with_location(latitude, longitude, searchQuery): #searches with coordinates and has a radius that is changeable
	global radius
	location = str(latitude) + "," + str(longitude) + "," + str(radius) + "mi"
	locationResults = authenticate().search(q = searchQuery, geocode = location, land = "en", count = 100)
	return locationResults

def geoLocator(latitude, longitude): #reverse geolocator for the coords
	geolocator = Nominatim(user_agent = "Twitter Searcher")
	coordinates = (str(latitude), str(longitude))
	location = geolocator.reverse(coordinates)
	locationPrecise = [x.strip() for x in location.address.split(',')]
	print(locationPrecise)
	print("    0		1		2	3	 4 	     5")
	precision = int(input("how precise "))
	return locationPrecise[precision];

#everytime this function is called by the schedule fuction it adds 1 so we can keep track of how many times it program should run in the schedule before it stops
def twitterSearcher(latitude, longitude, searchQuery):
	global numInc
	compareResults(search_without_location(searchQuery), search_with_location(latitude, longitude, searchQuery))
	numInc+=1
	print("Status: " + str(numInc))
def scheduleIteration(latitude, longitude, searchQuery, iterations):	#schedule which calls the twitter searcher function as well
	global numInc
	schedule.every(2).minutes.do(twitterSearcher, latitude, longitude, searchQuery)
	if iterations == -1:
		schedule.run_pending()
		time.sleep(1)
	else:
		while numInc < iterations:
			schedule.run_pending()
			time.sleep(1)

if __name__ == '__main__':
#	lati = input("Enter latitude: ")
#	long = input("Enter longitude: ")
	lati = 6.5244
	long = 3.3792 #lagos coordinates
#	print(geoLocator(lati,long))
	searchQuery = geoLocator(lati,long) + " Accident -filter:retweets" 	#-filter:retweets removes retweets
	print(searchQuery)
#	searchQuery = "Accident -filter:retweets"
#	twitterSearcher(lati, long, searchQuery) 				#remove or comment this line and just used the schedule function to start the program
	iterations = int(input("Enter how many times before schedule stops "))
	scheduleIteration(lati, long, searchQuery, iterations)

