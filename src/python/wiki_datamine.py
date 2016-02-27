import math

from wiki_api import WikiAPI
from wiki_languages import getLanglinks
from wiki_projects import getProjectPages
from wiki_node import WikiNode
from wiki_mongo import MongoDbClient, getMongoClient
from wiki_dump import get_languages
import utils
from sketches.wiki_medicine_pages_get import getMedicinePageUrlsFromDump
import json


from pprint import pformat


def getConfig():
	with open('config/config.json') as jsonfile:    
		data = json.load(jsonfile)
	return data

def getLangJson(lang=None):
	lang = lang or 'en'
	with open('dump/medicine_%s.json' % (lang, )) as jsonfile:    
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

def encodeUtf8(string):
	return string.encode('utf-8')

def parseMediginePagesBatch(config, start=0, batchsize=50, dbCheck=True):	# limit = 50
	medicinepages = getProjectPagesDictionary(0, 0)
	npages = len(medicinepages)
	print 'processing %d pages' % npages
	mongo = getMongoClient(config)

	api = WikiAPI()
	for i in range(npages / batchsize + 1):
		if i < start / batchsize:
			continue
		langpages = {}
		nodes = []
		start = i * batchsize
		end = min(npages, (i + 1) * batchsize - 1)
		medicinepages = getProjectPagesDictionary(start, end)
		# print medicinepages #[start:end]
		titleslist = [url.split('/wiki/')[-1].replace(' ', '%20') for url in medicinepages.values()]
		pagedata = api.getPages(titleslist, True).get('pages')
		if not pagedata:
			print 'skipped', medicinepages
			continue
		for pageid, data in pagedata.items():

			data['title'] = encodeUtf8(data['title'])
			data['fullurl'] = encodeUtf8(data['fullurl'])

			if dbCheck and mongo.find(kargs={"title": data['title']}).count():
				continue
			elif dbCheck:
				dbCheck = False

			nodes.append(WikiNode(pageid, data))

			# prepare language dictionary
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
			titleslist = items.keys()
			pagedata = api.getPages(titleslist, lang=lang).get('pages')
			if not pagedata:
				continue

			for langid, langdata in pagedata.items():
				langdata['title'] = encodeUtf8(langdata['title'])
				langdata['fullurl'] = encodeUtf8(langdata['fullurl'])

				if dbCheck and mongo.find(kargs={"title": langdata['title']}).count():
					continue
				elif dbCheck:
					dbCheck = False

				langlinktitle = langdata['fullurl'].split('/wiki/')[-1]
				if not langlinktitle in langpages[lang].keys():
					warn = 'WARNING: %s skipped' % (langlinktitle, )
					print warn
					continue
				parentid = langpages[lang][langlinktitle]
				nodes.append(WikiNode(langid, langdata, parentid))

		print 'writing', len(nodes), 'nodes to db ( batch', start, '-', end, ')'
		for pagenode in nodes:
			# if pagenode.resolved:
			mongo.put(pagenode.asDict())

# start = 30524
# batchsize = 2
failed = []
notFound = []
batchsize = 200
config = getConfig()
dbconfig = config.get('mongoDB')
api = WikiAPI()
mongo = getMongoClient(dbconfig)

for lang in get_languages():
	with utils.timeIt("query for %s" % lang):
		try:
			# parseMediginePagesBatch(dbconfig, start=start, batchsize=batchsize)
			langjson = getLangJson(lang)
			langpages = [name for name, idx in langjson.items()]
			npages = len(langpages)
			#print "npages:", npages
			# for i in range(int(math.ceil(float(npages) / batchsize) + 1)):
			for i in range(npages / batchsize + 1):
				start = i * batchsize
				end = min(npages, (i + 1) * batchsize - 1)
				if i < start / batchsize:
					continue
				querypages = langpages[start:end + 1]
				print 'batch:', start, '-', end
				#print querypages
				# print querypages
				pageviews = api.getPageviews(querypages, lang=lang)
				# print pformat(pageviews)
				#print len(pageviews)
				#break

				# print pageviews
				# print pageviews.keys()
				# mongopages = mongo.find(kargs={'name': pageviews.keys()}) # 'lang': lang,
				pagescursor = mongo.find(kargs={"lang": lang, "name": {'$in': pageviews.keys()}}) #kargs={'name': pageviews.keys()} 'lang': lang,
				mongopages = {page.get('name'): page for page in pagescursor}
				#print mongopages, pagescursor.count()

				for name, data in pageviews.items():

					page = mongopages.get(name)
					if not page:
						notFound.append(name)
						#print 'EXCEPTION:', name
						continue

					links = []
					for link in page.get('allinks', []):
						if link in langjson:
							links.append(langjson[link])
					#print "links", links
					if links:
						page.pop('allinks')
						page['links'] = links
					
					if 'stats' in data:
						page['stats'] = data['stats']
					if 'views' in data:
						page['views'] = data['views']
					mongo.update({"pid": page["pid"]}, page)
					#print "updated", page["pid"]
					# page[]
					#print pformat(page)
					# print name

		except:
			failed.append(lang)

if notFound:
	print "%d pages not found in pageviews:" % len(notFound)
	print notFound
if failed:
	print "%d languages failed" % len(failed)
	print failed
