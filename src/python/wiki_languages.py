import urllib2
import json

from pprint import pformat


def getLanglinks(page):
	root = 'https://en.wikipedia.org/w/api.php?'
	# https://www.mediawiki.org/wiki/API:Langlinks
	action = 'action=query&prop=langlinks&format=json&llprop=url&lllimit=max&indexpageids=&titles=%s' % (page, )
	url = '%s%s' % (root, action)
	# print url
	response = urllib2.urlopen(url)
	data = json.load(response)   

	jsondict = data['query']
	pageid = jsondict['pages'].keys()[0]
	# print pformat(jsondict['pages'][pageid])
	if not 'langlinks' in jsondict['pages'][pageid]:
		return {}
	links = jsondict['pages'][pageid]['langlinks']
	langdict = {}
	for link in links:
		# lang = link['lang']
		# url = link['url']
		# print lang, url
		langdict[link['lang']] = link['url']
	# print pformat(jsondict)
	# print pageid, links
	# self._childrenOtherLanguages = [WikiPage(link) for link in db.get_langlinks(self.page)]
	return langdict
