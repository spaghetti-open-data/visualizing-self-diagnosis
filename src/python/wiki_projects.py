import json
import os

def getProjectPages(limit=100, cache=False):
	if not cache:
		print  'WARNING: API queries not supported yet'
		return []
	basedir = os.path.dirname(__file__)
	with open(os.path.join(basedir, 'config/medicine_dump.json')) as jsonfile:    
		data = json.load(jsonfile)
		if limit < len(data):
			data = data[:limit]
	return data
