#wiki_dbqueries

from wiki_mongo import MongoDbClient, getMongoClient
from sketches.wiki_medicine_pages_get import getMedicinePageUrlsFromDump
import json

from pprint import pformat

def getConfig():
	with open('config/config.json') as jsonfile:    
		data = json.load(jsonfile)
	return data

config = getConfig()['mongoDB']
mongo = getMongoClient(config)
# get list of all languages stored in db
# languages = mongo.db.distinct('lang')

# cursor = mongo.find(kargs={"lang": "es"})
# for document in cursor:
# 	if document['parent'] > 0:
# 		print document['parent'], document['language']
