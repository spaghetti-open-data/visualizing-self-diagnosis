import json
import os
from pprint import pformat

from wiki_languages import getLanglinks
from wiki_projects import getProjectPages
from wiki_node import WikiNode
from wiki_mongo import MongoDbClient, getMongoClient
from sketches.wiki_medicine_pages_get import getMedicinePageUrlsFromDump


def getConfig():
	basedir = os.path.dirname(__file__)
	with open(os.path.join(basedir, 'config/config.json')) as jsonfile:    
		data = json.load(jsonfile)
	# print pformat(data)
	return data

def getProjectPagesDictionary(start=0, limit=100):
	# get all english pages for medicine
	pages = getProjectPages(start=start, limit=limit, cache=True)
	urls = {}
	for page in pages:
		urls[page] = 'https://en.wikipedia.org/wiki/%s' % (page, )
	# print pformat(urls)
	return urls

def getLanguageDictionary(url):
	urlname = url.split('/wiki/')[-1]
	try:
		print urlname
	except:
		print 'WARNING: url skipped'
		return {}
	return getLanglinks(urlname)

def getPageLanguages(urls):
	for name, url in urls.items():
		langdict = getLanguageDictionary(url)
		if langdict:
			print pformat(langdict)


limit = 100
config = getConfig()['mongoDB']
medicinepages = getProjectPagesDictionary(0, limit)

medplist = medicinepages.keys()
# urls = {key: medicinepages[key] for key in medplist[:limit]}

# urls = getMedicinePageUrlsFromDump(limit)
# urls = {
# 	'1% rule (aviation medicine)': 'https://en.wikipedia.org/wiki/1%25_rule_(aviation_medicine)',
# 	# '1% rule (aviation medicine)': 'https://en.wikipedia.org/wiki/1%25 rule (aviation_medicine)',
# 	'1,1,1,2-Tetrafluoroethane': 'https://en.wikipedia.org/wiki/1,1,1,2-Tetrafluoroethane',
# 	'1,4-Dioxin': 'https://en.wikipedia.org/wiki/1,4-Dioxin'
# }

nodes = []
mongo = getMongoClient(config)
# for name, url in urls.items():
for name, url in medicinepages.items():
	pagenode = WikiNode(name)
	pagenode.setPageData(medplist)
	# for each page, print all translations
	# getPageLanguages(urls)
	print pagenode.name, pagenode.url
	# print pagenode.asDict(), type(pagenode.asDict())
	nodes.append(pagenode)
	if pagenode.resolved:
		pass
		# mongo.put(pagenode.asDict())
		# print pagenode.asDict()
		# break

# print pformat(nodes)
