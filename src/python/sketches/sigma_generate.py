import os
import json
import math
import random
import HTMLParser


dest = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\javascript\\sketches\\data'
outjson = 'wiki_sample_network.json'

rawpath = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\python\\dump\\medicine_en.json'


with open(rawpath, 'r') as rawjson:
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
for i, page in enumerate(k):
	radius += float(1)/len(k)
	idx = data[page]
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
