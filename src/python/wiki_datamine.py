from wiki_api import WikiAPI
from wiki_languages import getLanglinks
from wiki_projects import getProjectPages
from wiki_node import WikiNode
from wiki_mongo import MongoDbClient, getMongoClient
from sketches.wiki_medicine_pages_get import getMedicinePageUrlsFromDump
import json

from pprint import pformat

def getConfig():
	with open('config/config.json') as jsonfile:    
		data = json.load(jsonfile)
	return data

def getProjectPagesDictionary(start=0, limit=100):
	# get all english pages for medicine
	pages = getProjectPages(start=start, limit=limit, cache=True)
	urls = {}
	for page in pages:
		urls[page] = 'https://en.wikipedia.org/wiki/%s' % (page, )
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


start = 0
limit = 50
config = getConfig()['mongoDB']
medicinepages = getProjectPagesDictionary(start, limit)
medplist = medicinepages.keys()


# print [url.split('/')[-1] for url in medicinepages.values()]
titleslist = [url.split('/wiki/')[-1].replace(' ', '%20') for url in medicinepages.values()]
# titleslist = ['Rome', 'Paris', 'London']
api = WikiAPI()
pagedata = api.getPages(titleslist, True)['pages']

langpages = {}
nodes = []
for pageid, data in pagedata.items():
	# WikiNode(pageid, data)
	
	# print pageid
	# print data
	if 'langlinks' in data.keys():
		nlang = len(data['langlinks'])
		for langdata in data['langlinks']:
			key = langdata['lang']
			if key not in langpages.keys():
				langpages[key] = []
			langpages[key].append((langdata['url'].split('/wiki/')[-1], pageid))
			# print langdata
	#	languages = [datum['url'].split('/wiki/')[-1] for datum in data['langlinks']]
	# 	for i in range(nlang / 50 + 1):
	# 		start = i * 50
	# 		end = min(nlang, (i + 1) * 50 - 1)
	# 		# print 'batch', nlang, ':', start, '-', end
	# 		# print languages[start:end]
	# 		languagepages = api.getPages(languages[start:end]).get('pages')
	# 		print pformat(languagepages)
	# 		break
	# 		# print languages[start:end]
	# 		if not languagepages:
	# 			continue
	# 		for langpageid, languagepage in languagepages.items():
	# 			WikiNode(langpageid, languagepages, pageid)
	# 		# api.getPagesById()

	# break

print pformat(langpages)

# print pformat(pagedata)
# print len(pagedata)

'''
nodes = []
mongo = getMongoClient(config)
# for name, url in urls.items():
for name, url in medicinepages.items():
	pagenode = WikiNode(name)
	pagenode.setPageData(medplist)
	# for each page, print all translations
	# getPageLanguages(urls)
	try:
		print pagenode.name, pagenode.url
		# print pagenode.url
		# print pagenode.pageid
		# print pagenode.links
		# print pagenode.exlinks
	except:
		# this should catch our current error:
		# 'ascii' codec can't encode character u'\u2013' ordinal not in range(128)
		continue
	# print pagenode.asDict(), type(pagenode.asDict())
	nodes.append(pagenode)
	if pagenode.resolved:
		# mongo.put(pagenode.asDict())
		pass
# print pformat(nodes)
'''
