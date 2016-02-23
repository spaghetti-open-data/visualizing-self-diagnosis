import json


def getProjectPages(start=0, end=100, cache=False):
	if not cache:
		print  'WARNING: API queries not supported yet'
		return []

	with open('config/medicine_dump.json') as jsonfile:    
		data = json.load(jsonfile)
		if end and end < len(data):
			data = data[start:end]
	return data
