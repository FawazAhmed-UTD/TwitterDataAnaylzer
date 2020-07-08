from cliff.api import Cliff
import json
from pprint import pprint

my_cliff = Cliff("http://10.176.148.84:8080")


def extract_location(tweet):
	location = {}
	focus = my_cliff.parse_text(tweet)['results']['places']['focus']

	for key, value in focus.items():
		location[key] = [item['name'] for item in value]

	return location



def readFile(fileName):
	with open(fileName, 'r') as f:
		d = json.load(f)
	f.close()
	return d



def writeFile(fileName, data):
	with open(fileName, 'w') as f:
		json.dump(data, f)
	f.close()



if __name__ == '__main__':
	data = readFile('tweets_annotation.json')

	for tweet in data:
		if 'location_present' in tweet.keys():
			location = extract_location(tweet['text'])
			tweet['cliff_location'] = location

			if 'cities' not in location.keys():
				continue

			if location['cities'] == tweet['city']:
				tweet['location_identified_by'].append('cliff')
			else:
				tweet_location = extract_location(tweet['city'])

				if location['cities'] == tweet_location['cities']:
					tweet['location_identified_by'].append('cliff')
				else:
					sameLocation = input('Tweet Location:{}, Cliff Location:{}'.format(tweet['city'], location))

					if sameLocation == 'y':
						tweet['location_identified_by'].append('cliff')

	writeFile('cliff.json', data)

