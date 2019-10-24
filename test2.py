import pymongo, json
from pprint import pprint

client = pymongo.MongoClient('mongodb://localhost:27017/')
dataBase = client['TwitterSearcher']
collection = dataBase["Tweets"]
data = []

with open('output.json') as file:
	for line in file:
		data.append(json.loads(line))

x = collection.insert_many(data)

print(dataBase.list_collection_names())

for x in collection.find():
	pprint(x)
