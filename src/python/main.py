from wiki_languages import getLanglinks
from wiki_mongo import MongoDbClient
from sketches.wiki_medicine_pages_get import getMedicinePageUrlsFromDump
import json

from pprint import pformat

def getConfig():
	with open('config/config.json') as jsonfile:    
		data = json.load(jsonfile)
	return data

config = getConfig()['mongoDB']
# print pformat(config)
mongo = MongoDbClient(
	config.get('server'),
	config.get('port'),
	config.get('username'),
	config.get('password'),
	config.get('db_name'),
	config.get('collection')
)

# get all english pages for medicine
limit = 20
urls = getMedicinePageUrlsFromDump(limit)
# test
# urls = {
# 	'1% rule (aviation medicine)': 'https://en.wikipedia.org/wiki/1%25_rule_(aviation_medicine)',
# 	# '1% rule (aviation medicine)': 'https://en.wikipedia.org/wiki/1%25 rule (aviation_medicine)',
# 	'1,1,1,2-Tetrafluoroethane': 'https://en.wikipedia.org/wiki/1,1,1,2-Tetrafluoroethane',
# 	'1,4-Dioxin': 'https://en.wikipedia.org/wiki/1,4-Dioxin'
# }

# for each page, get all translations
for name, url in urls.items():
	urlname = url.split('/wiki/')[-1]
	print urlname
	langdict = getLanglinks(urlname)
	if langdict:
		mongo.put(langdict)
		print pformat(langdict)
