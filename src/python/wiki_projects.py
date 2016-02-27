import codecs
import json
import os

def getProjectPages(start=0, end=100, cache=False):
	if not cache:
		print  'WARNING: API queries not supported yet'
		return []
	basedir = os.path.dirname(__file__)
	with codecs.open(os.path.join(basedir, 'config/medicine_dump.json'), encoding='utf-8') as jsonfile:    
		data = json.load(jsonfile)
		if end and end < len(data):
			data = data[start:end]
	return data
