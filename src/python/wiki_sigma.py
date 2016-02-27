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
dest = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\javascript\\sketches\\data'
outjson = 'wiki_sample_network.json'
rawpath = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\python\\dump\\medicine_en.json'

radius = 1
limit = 220
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

sigmajson = {
	'nodes': [],
	'edges': []
}
# parser = HTMLParser.HTMLParser()
for i, page in enumerate(pages):
	views = page['views']
	radius = 1
	if views < avg:
		radius += int(lerp(views, vmin, avg) * 4)
	else:
		radius += int(lerp(views, avg, vmax) * 4)
	# print page['views'], radius
	if 'links' in page.keys():
		for j, link in enumerate(page['links']):
			edge = {
				'id': '%de%d' % (j, page['pid']),
				'source': '%d' % page['pid'],
				'target': '%d' % link
			}
			sigmajson['edges'].append(edge)
	node = {
		'id': '%d' % page['pid'],
		'label': page['title'], # parser.unescape(page),
		'x': math.sin(math.pi * 2 * i / limit + 1),
		'y': math.cos(math.pi * 2 * i / limit + 1),
		'size': radius
	}
	sigmajson['nodes'].append(node)

with open(os.path.join(dest, outjson), 'w') as outjsonfile:
	json.dump(sigmajson, outjsonfile, indent=1)
