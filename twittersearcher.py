from twitter import *
import json
from pprint import pprint
actor = "Obama"
twitter = Twitter(auth = OAuth("3939721633-EJIfdOWAcuWVjwFpsQp7Qs3P5NNyh3q7ihpC9ld",
                  "wyQ9uA8vZ02Ni2fimTJegOSdIJTO95ttIJWWkDZUxl5cZ",
                  "8VQzfyd9REr8gO2nesBRkJTru",
                  "2CS4iYIdBq6SNSmTJCWUFJuhOjAkN4b68bXkOIS7nYouuh7r8n"))
query = twitter.search.tweets(q = actor)
print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))
with open('out.txt', 'w') as outfile:
	print("\nData collected on", "\"", actor, "\"\n", file=outfile)
	for result in query["statuses"]:
		print((result["created_at"], result["user"]["screen_name"], result["text"]), '\n', file= outfile)
with open('output.json','w') as file:
	for result in query["statuses"]:
		json.dump((result["created_at"], result["user"]["screen_name"], result["text"]), file)
		file.write('\n')
#print((result["created_at"], result["user"]["screen_name"], result["text"]))#!/usr/bin/env python
