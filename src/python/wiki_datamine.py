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
	pages = getProjectPages(start=start, end=limit, cache=True)
	urls = {}
	for page in pages:
		urls[page] = 'https://en.wikipedia.org/wiki/%s' % (page, )
	return urls

def getLanguageDictionary(url):
	urlname = url.split('/wiki/')[-1].encode("utf-8")
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

# start = 0
# limit = 50
config = getConfig()['mongoDB']
medicinepages = getProjectPagesDictionary(0, 0)

npages = len(medicinepages)
mongo = getMongoClient(config)
for i in range(npages / 50 + 1):
	langpages = {}
	nodes = []
	start = i * 50
	end = min(npages, (i + 1) * 50 - 1)
	medicinepages = getProjectPagesDictionary(start, end)
	# print medicinepages #[start:end]
	# continue
	titleslist = [url.split('/wiki/')[-1].replace(' ', '%20') for url in medicinepages.values()]
	# titleslist = ['Rome', 'Paris', 'London']
	api = WikiAPI()
	pagedata = api.getPages(titleslist, True)['pages']
	for pageid, data in pagedata.items():
		nodes.append(WikiNode(pageid, data))
		# print pageid, print data
		if 'langlinks' in data.keys():
			nlang = len(data['langlinks'])
			for langdata in data['langlinks']:
				key = langdata['lang']
				if key not in langpages.keys():
					langpages[key] = {}
				langpages[key][langdata['url'].split('/wiki/')[-1]] = pageid
				# print langdata

	for lang, items in langpages.items():
		# print lang
		titleslist = items.keys()
		# print len(titleslist)
		pagedata = api.getPages(titleslist, lang=lang).get('pages')
		if not pagedata:
			continue
		# print titleslist
		# print pformat(pagedata)
		for langid, langdata in pagedata.items():
			# print langid, langpages[lang][langdata['fullurl'].split('/wiki/')[-1]]
			parentid = langpages[lang][langdata['fullurl'].split('/wiki/')[-1]]
			nodes.append(WikiNode(langid, langdata, parentid))

		break

	print 'writing', len(nodes), 'nodes to db ( batch', start, '-', end, ')'
	# print pformat(pagedata)
	# print len(pagedata)

	break

	for pagenode in nodes:
		# if pagenode.resolved:
		mongo.put(pagenode.asDict())

'''
medplist = medicinepages.keys()
nodes = []
# for name, url in urls.items():
for name, url in medicinepages.items():
	pagenode = WikiNode(name)
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
