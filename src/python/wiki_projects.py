import json


def getProjectPages(start=0, limit=100, cache=False):
	if not cache:
		print  'WARNING: API queries not supported yet'
		return []

	with open('config/medicine_dump.json') as jsonfile:    
		data = json.load(jsonfile)
		if limit < len(data):
			data = data[start:limit]
	return data
