dest = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\javascript\\sketches\\data'
outjson = 'wiki_sample_network.json'

rawpath = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\python\\dump\\medicine_it.json'

import os
import json

with open(rawpath, 'r') as rawjson:
	data = json.load(rawjson)

with open(os.path.join(dest, outjson), 'w') as outjsonfile:
	for i, (page, idx) in enumerate(data.items()):
		if i > 10:
			break
		outjsonfile.writelines(page)
