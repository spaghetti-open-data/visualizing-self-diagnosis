""" Script for collecting views data from Wikipedia.

		Python requirements:
			- pip pip install mwviews

		References:
			- https://github.com/mediawiki-utilities/python-mwviews
"""

import urllib2
import json

from mwviews.api import PageviewsClient

from pprint import pformat

# query pageviews (last month, all), sum. max query? mongo: write views (short + long)


class WikiAPI(object):

	root = 'https://en.wikipedia.org/w/api.php?'
	
	def __init__(self):
		pass

	def getResponse(self, action, lang='en'):
		root = self.root.replace('en', lang)
		url = '%s%s' % (root, action)
		# print url
		response = None
		try:
			response = urllib2.urlopen(url)
			data = json.load(response)
			return data['query']
		except:
			print 'response could not be json-decoded', url, response
			return {}

	def filterTitleExceptions(self, titles):
		result = []
		for title in titles:
			result.append(title.encode("utf-8"))
		return result

	def getPages(self, titleslist, languages=False, lang='en'):
		titlesQuery = '|'.join(self.filterTitleExceptions(titleslist))
		langoption = '|langlinks&llprop=url&lllimit=max' if languages else ''
		action = 'action=query&titles=%s&prop=info|links%s&format=json&inprop=url' % (titlesQuery, langoption)
		# prop=links 		list=backlinks			list=alllinks
		# prop=templates 	list=embeddedin			list=alltransclusions
		# prop=categories 	list=categorymembers 	list=allcategories
		# prop=images 		list=imageusage 		list=allimages
		# prop=langlinks 	list=langbacklinks 	
		# prop=iwlinks		list=iwbacklinks 	
		# prop=extlinks
		return self.getResponse(action, lang)

	def getPagesLanguages(self, titleslist):
		titlesQuery = '|'.join(titleslist)
		action = 'action=query&titles=%s&prop=langlinks&format=json&llprop=url&lllimit=max' % (titlesQuery, )
		return self.getResponse(action)

	def getPagesById(self, idslist, languages=False):
		titlesQuery = '|'.join('%d' % idslist)
		langoption = '|langlinks' if languages else ''
		action = 'action=query&pageids=%s&prop=info|links%s&format=json&llprop=url&lllimit=max' % (titlesQuery, langoption)
		return self.getResponse(action)

	def getPageviews(self, titles):
		
