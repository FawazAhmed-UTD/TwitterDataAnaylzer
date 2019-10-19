from twitter import *
import tweepy, schedule, time, json, pprint
from geopy.geocoders import Nominatim
numInc = 0

def geoLocator(latitude, longitude):
	geolocator = Nominatim(user_agent = "Twitter Searcher")
	coordinates = (str(latitude), str(longitude))
	location = geolocator.reverse(coordinates)
	print(location.address)
	locationPrecise = [x.strip() for x in location.address.split(',')]
	return locationPrecise[1];

def twitterSearcher(searchQuery):
	global numInc
	accessToken = "3939721633-EJIfdOWAcuWVjwFpsQp7Qs3P5NNyh3q7ihpC9ld"
	accessToken_Secret = "wyQ9uA8vZ02Ni2fimTJegOSdIJTO95ttIJWWkDZUxl5cZ"
	apiKey = "8VQzfyd9REr8gO2nesBRkJTru"
	apiKey_Secret = "2CS4iYIdBq6SNSmTJCWUFJuhOjAkN4b68bXkOIS7nYouuh7r8n"
	authenticator = tweepy.OAuthHandler(apiKey, apiKey_Secret)
	api = tweepy.API(authenticator)
	results = api.search(q=searchQuery, lang = "en")
	with open('output.json', 'w') as file:
		for tweet in results:
			json.dump((tweet.user.screen_name,tweet.text), file)
			file.write('\n')
	#print(tweet.user.screen_name,"Tweeted:",tweet.text)
	numInc+=1

def scheduleIteration(searchQuery, iterations):
	global numInc
	schedule.every(2).minutes.do(twitterSearcher, (searchQuery + " Accident"))
	while numInc < iterations:
		schedule.run_pending()
		time.sleep(1)

if __name__ == '__main__':
	lati = input("Enter latitude: ")
	long = input("Enter longitude: ")
	searchQuery = geoLocator(lati,long)
	iterations = int(input("Enter how many times before schedule stops "))
	scheduleIteration(searchQuery, iterations)
