# source: 

import requests

def query(request):
	request['action'] = 'query'
	request['format'] = 'json'
	lastContinue = {'continue': ''}
	while True:
		# Clone original request
		req = request.copy()
		# Modify it with the values returned in the 'continue' section of the last result.
		req.update(lastContinue)
		# Call API
		result = requests.get('http://en.wikipedia.org/w/api.php', params=req).json()
		if 'error' in result: raise Error(result['error'])
		if 'warnings' in result: print(result['warnings'])
		if 'query' in result: yield result['query']
		if 'continue' not in result: break
		lastContinue = result['continue']

for result in query( {'generator':'allpages', 'prop':'links'} ):
	# print result
	pass # your code processing here
