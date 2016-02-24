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

def encodeUtf8(string):
	return string.encode('utf-8')


dbCheck = True
start = 30524
batchsize = 2
# limit = 50
config = getConfig()['mongoDB']



medicinepages = getProjectPagesDictionary(0, 0)
npages = len(medicinepages)
print 'processing %d pages' % npages
mongo = getMongoClient(config)

# cursor = mongo.find(kargs={"language": "es"})
# for document in cursor:
# 	if document['parent'] > 0:
# 		print document['parent'], document['language']

dumpfile = open('dump.log', 'w')
for i in range(npages / batchsize + 1):
	if i < start / batchsize:
		continue
	langpages = {}
	nodes = []
	start = i * batchsize
	end = min(npages, (i + 1) * batchsize - 1)
	medicinepages = getProjectPagesDictionary(start, end)
	# print medicinepages #[start:end]
	# continue
	titleslist = [url.split('/wiki/')[-1].replace(' ', '%20') for url in medicinepages.values()]
	# titleslist = ['Rome', 'Paris', 'London']
	api = WikiAPI()
	pagedata = api.getPages(titleslist, True).get('pages')
	if not pagedata:
		print 'skipped', medicinepages
		continue
	for pageid, data in pagedata.items():

		data['title'] = encodeUtf8(data['title'])
		data['fullurl'] = encodeUtf8(data['fullurl'])

		# print data['title']
		# cursor = mongo.find(kargs={"title": data['title'].encode('utf-8')})
		if dbCheck and mongo.find(kargs={"title": data['title']}).count():
			continue
		elif dbCheck:
			dbCheck = False

		nodes.append(WikiNode(pageid, data))

		# prepare language dictionary
		# print pageid, print data
		if 'langlinks' in data.keys():
			nlang = len(data['langlinks'])
			for langdata in data['langlinks']:
				key = langdata['lang']
				langdata['url'] = encodeUtf8(langdata['url'])
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

			langdata['title'] = encodeUtf8(langdata['title'])
			langdata['fullurl'] = encodeUtf8(langdata['fullurl'])

			# cursor = mongo.find(kargs={"title": langdata['title']})
			# if cursor.count():
			# 	continue
			if dbCheck and mongo.find(kargs={"title": langdata['title']}).count():
				continue
			elif dbCheck:
				dbCheck = False

			# print langdata['fullurl'].split('/wiki/')[-1]
			# print langid, pformat(langpages[lang])
			langlinktitle = langdata['fullurl'].split('/wiki/')[-1]
			if not langlinktitle in langpages[lang].keys():
				warn = 'WARNING: %s skipped' % (langlinktitle, )
				dumpfile.writelines('%s\n' % (warn, ))
				print warn
				continue
			parentid = langpages[lang][langlinktitle]
			nodes.append(WikiNode(langid, langdata, parentid))


	print 'writing', len(nodes), 'nodes to db ( batch', start, '-', end, ')'
	# print pformat(pagedata)
	# print len(pagedata)
	for pagenode in nodes:
		# if pagenode.resolved:
		mongo.put(pagenode.asDict())
