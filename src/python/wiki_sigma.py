import os
import json
import math
import random
import HTMLParser

from wiki_mongo import MongoDbClient, getMongoClient


def getConfig():
	with open('config/config.json') as jsonfile:    
		data = json.load(jsonfile)
	return data


lang='en'
config = getConfig()
dbconfig = config.get('mongoDB')
mongo = getMongoClient(dbconfig)

pages = mongo.find(
	kargs={
		"lang": "en",
		"views": {
			"$gt": 0
		}
	}, limit=100
)

for page in pages:
	print page
	break
