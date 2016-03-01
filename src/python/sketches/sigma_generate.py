import codecs
import os
import json
import math
import random
import HTMLParser

basedir = os.path.dirname(__file__)
dest = os.path.join(basedir, '..', '..', 'javascript','sketches', 'data')
outjson = 'wiki_sample_network.json'

rawpath = os.path.join(basedir, '..', 'dump', 'medicine_en.json')


with codecs.open(rawpath, encoding='utf-8') as rawjson:
	data = json.load(rawjson)


sigmajson = {
	'nodes': [],
	'edges': []
}
# with open(os.path.join(dest, outjson), 'w') as outjsonfile:
radius = 1
limit = 220
k = sorted(data)[:limit]
parser = HTMLParser.HTMLParser()
parsed_ids = []
for i, page in enumerate(k):
	radius += float(1)/len(k)
	idx = data[page]
	if idx in parsed_ids:
		print "Skipped duplicate:", idx
		continue
	parsed_ids.append(idx)
	keys = random.sample(k, min(limit, max(0, random.randint(-3, 3))))
	# [52, 3, 10, 92, 86, 42, 99, 73, 56, 23]
	values = [data[key] for key in keys]
	# print values
	for j, trgtidx in enumerate(values):
		edge = {
			'id': '%de%d' % (j, idx),
			'source': '%d' % idx,
			'target': '%d' % trgtidx
		}
		sigmajson['edges'].append(edge)
	node = {
		'id': '%d' % idx,
		'label': parser.unescape(page),
		'x': radius * math.sin(math.pi * 2 * i / limit + 1),
		'y': radius * math.cos(math.pi * 2 * i / limit + 1),
		'size': random.randint(1, 3) + len(values)
	}
	sigmajson['nodes'].append(node)
	# outjsonfile.writelines('%s: %d\n' % (page, idx))

# print sigmajson
with open(os.path.join(dest, outjson), 'w') as outjsonfile:
	json.dump(sigmajson, outjsonfile, indent=1)
