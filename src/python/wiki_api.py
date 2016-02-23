import urllib2
import json

from pprint import pformat


class WikiAPI(object):

	root = 'https://en.wikipedia.org/w/api.php?'
	
	def __init__(self):
		pass

	def getResponse(self, action, lang='en'):
		root = self.root.replace('en', lang)
		url = '%s%s' % (root, action)
		# print url
		response = urllib2.urlopen(url)
		try:
			data = json.load(response)
			return data['query']
		except:
			print 'response could not be json-decoded', response
			return {}

	def getPagesLanguages(self, titleslist):
		titlesQuery = '|'.join(titleslist)
		action = 'action=query&titles=%s&prop=langlinks&format=json&llprop=url&lllimit=max' % (titlesQuery, )
		# action = 'action=query&prop=langlinks&format=json&llprop=url&lllimit=max&titles=%s' % (titlesQuery, )
		# action = 'action=query&prop=langlinks&format=json&llprop=url&lllimit=max&indexpageids=&titles=%s' % (page, )
		return self.getResponse(action)

	def filterTitleExceptions(self, titles):
		result = []
		for title in titles:
			result.append(title.encode("utf-8"))
			# try:
			# 	print title.encode("utf-8")
			# 	result.append(title.encode("utf-8"))
			# except:
			# 	print 'WARNING: url skipped'
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
		# action = 'action=query&prop=revisions&rvprop=content&format=json&titles=Rome|London'
		return self.getResponse(action, lang)

	def getPagesById(self, idslist, languages=False):
		titlesQuery = '|'.join('%d' % idslist)
		langoption = '|langlinks' if languages else ''
		action = 'action=query&pageids=%s&prop=info|links%s&format=json&llprop=url&lllimit=max' % (titlesQuery, langoption)
		return self.getResponse(action)

'''
pageid = jsondict['pages'].keys()[0]
if 'langlinks' in jsondict['pages'][pageid]:
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
	print langdict
'''
