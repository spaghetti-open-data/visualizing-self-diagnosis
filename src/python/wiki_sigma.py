import os
import json
import math
import random
import HTMLParser

from wiki_mongo import MongoDbClient, getMongoClient

from pprint import pformat


def getConfig():
	with open('config/config.json') as jsonfile:    
		data = json.load(jsonfile)
	return data


def lerp(val, minv, maxv):
	return (val - minv) / (maxv - minv)


lang='en'
config = getConfig()
dbconfig = config.get('mongoDB')
mongo = getMongoClient(dbconfig)

basedir = os.path.dirname(__file__)
dest = os.path.join(basedir, '..', 'javascript','sketches', 'data')
outjson = 'wiki_sample_network.json'
rawpath = os.path.join(basedir, 'dump', 'medicine_en.json')

radius = 1

vmin = mongo.db.find_one({"views": {"$gt": 0}}, sort=[("views", 1)])["views"]
vmax = mongo.db.find_one({"views": {"$gt": 0}}, sort=[("views", -1)])["views"]
# avg = mongo.db.find_one({"views": {"$avg": True}})
avgCursor = mongo.db.aggregate([{'$group':{'_id':None, 'average':{'$avg':"$views"}}}])
for node in avgCursor:
	avg = node['average']
	break

# gap = (vmax - vmin) / 5
# print vmin, vmax, gap

pages = mongo.find(
	kargs={
		"lang": "en",
		"pid": {
			"$gt": 0
		},
		"views": {
			"$gt": 0
		}
	} #, limit=100
)
limit = pages.count()
sigmajson = {
	'nodes': [],
	'edges': []
}
# parser = HTMLParser.HTMLParser()
parsed_ids = []
sigma_links = {}
for i, page in enumerate(pages):
	if page['pid'] in parsed_ids:
		print "Skipped duplicate:", page['pid']
		continue
	parsed_ids.append(page['pid'])
	views = page['views']
	radius = 1
	if views < avg:
		radius += int(lerp(views, vmin, avg) * 4)
	else:
		radius += int(lerp(views, avg, vmax) * 4)
	# print page['views'], radius
	if 'links' in page.keys():
		sigma_links[page['pid']] = page['links']
	node = {
		'id': '%d' % page['pid'],
		'label': page['title'], # parser.unescape(page),
		'x': math.sin(math.pi * 2 * i / limit + 1),
		'y': math.cos(math.pi * 2 * i / limit + 1),
		'size': radius
	}
	sigmajson['nodes'].append(node)

for pid, links in sigma_links.iteritems():
	for j, link in enumerate(links):
		if link in parsed_ids:
			edge = {
				'id': '%de%d' % (j, pid),
				'source': '%d' % pid,
				'target': '%d' % link
			}
			sigmajson['edges'].append(edge)

with open(os.path.join(dest, outjson), 'w') as outjsonfile:
	json.dump(sigmajson, outjsonfile, indent=1)
