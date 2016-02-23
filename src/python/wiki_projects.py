import json
import os

def getProjectPages(start=0, end=100, cache=False):
	if not cache:
		print  'WARNING: API queries not supported yet'
		return []
	basedir = os.path.dirname(__file__)
	with open(os.path.join(basedir, 'config/medicine_dump.json')) as jsonfile:    
		data = json.load(jsonfile)
		if end and end < len(data):
			data = data[start:end]
	return data
