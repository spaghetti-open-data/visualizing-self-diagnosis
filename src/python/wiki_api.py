""" Script for collecting views data from Wikipedia.

		Python requirements:
			- pip pip install mwviews

		References:
			- https://github.com/mediawiki-utilities/python-mwviews
"""

import urllib2
import json
import datetime

from mwviews.api import PageviewsClient

import utils

from pprint import pformat

# query pageviews (last month, all), sum. max query? mongo: write views (short + long)


class WikiAPI(object):

	root = 'https://en.wikipedia.org/w/api.php?'
	mwbegin = datetime.date(2015, 8, 1) # '2015080100'

	
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

	def getPageviews(self, pages, lang='en', limit=None):
		if limit and limit > len(pages):
			pages = pages[:limit]
		print len(pages)
		titles = sorted(pages)
		with utils.timeIt('pageviews'):
			viewsclient = PageviewsClient()
			articleviews = viewsclient.article_views('%s.wikipedia' % (lang, ), titles, start=self.mwbegin)
			print len(titles), 'titles,', len(articleviews), 'articleviews'
			pagecounts = {}
			# print pformat(dict(articleviews))
			for time in sorted(articleviews):
				stats = articleviews[time]
				# print time, len(stats)
				# print pformat(stats)
				for title in titles:
					if title not in pagecounts:
						pagecounts[title] = []
					pagecounts[title].append(int(stats.get(title) or 0))

			for title, pageviews in pagecounts.items():
				nviews = sum(pageviews)
				pagecounts[title] = {'views': nviews}
				if nviews:
					pagecounts[title]['stats'] = pageviews
		return pagecounts		
