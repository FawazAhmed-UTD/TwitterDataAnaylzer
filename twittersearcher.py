from twitter import *
import json
import pprint
from geopy.geocoders import Nominatim

def geoLocator(latitude, longitude):
	geolocator = Nominatim(user_agent = "Twitter Searcher")
	coordinates = (str(latitude), str(longitude))
	location = geolocator.reverse(coordinates)
	print(location.address)
	#print(location.raw)
	locationPrecise = [x.strip() for x in location.address.split(',')]
	print(locationPrecise[0])
	return;

def twitterSearcher(searchQuery):
	accessToken = "3939721633-EJIfdOWAcuWVjwFpsQp7Qs3P5NNyh3q7ihpC9ld"
	accessToken_Secret = "wyQ9uA8vZ02Ni2fimTJegOSdIJTO95ttIJWWkDZUxl5cZ"
	apiKey = "8VQzfyd9REr8gO2nesBRkJTru"
	apiKey_Secret = "2CS4iYIdBq6SNSmTJCWUFJuhOjAkN4b68bXkOIS7nYouuh7r8n"
	twitter = Twitter(auth = OAuth(accessToken, accessToken_Secret, apiKey, apiKey_Secret))
	query = twitter.search.tweets(q = searchQuery)
	#print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))
	#with open('out.txt', 'w') as outfile:
	#	print("\nData collected on", "\"", searchQuery, "\"\n", file=outfile)
	#	for result in query["statuses"]:
	#		print((result["created_at"], result["user"]["screen_name"], result["text"]), '\n', file= outfile)
	with open('output.json','w') as file:
		for result in query["statuses"]:
			json.dump((result["created_at"], result["user"]["screen_name"], result["text"]), file)
			file.write('\n')
	#print((result["created_at"], result["user"]["screen_name"], result["text"]))#!/usr/bin/env python

if __name__ == '__main__':
	lati = input("Enter latitude: ")
	long = input("Enter longitude: ")
	actor = "Obama"
	geoLocator(lati,long)
	twitterSearcher(actor)
