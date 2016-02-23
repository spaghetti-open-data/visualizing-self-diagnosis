import wikipedia


from pprint import pformat


class WikiNode(object):

	pageid = -1
	name = ''
	title = ''
	url = ''
	views = 0
	links = None	# []
	exlinks = None		# []
	language = 'en'
	resolved = False

	# def __init__(self, pagename, parent=None):
	# 	self._parent = parent
	# 	self.name = pagename
	# 	self.url = 'https://en.wikipedia.org/wiki/%s' % (pagename, )
	# 	self._childrenLanguages = []
	# 	# self.pagedata = api.getpagedata()
	# 	# self.views = api.getviews()

	def __init__(self, idx, data, parent=-1):
		self.pageid = int(idx)
		self.language = data.get('pagelanguage')
		# self._parent = parent
		self.name = data.get('fullurl').split('/wiki/')[-1]
		# self.title = data.get('title').decode('utf-8')
		self.title = data.get('title')
		self.languages = None if 'langlinks' not in data.keys() else [datum['lang'] for datum in data['langlinks']]
		self.parent = int(parent)
		if 'links' in data.keys():
			# print pformat(data.get('links'))
			# print [datum['title'].encode('utf-8') for datum in data.get('links')]
			self.links = [self.encodeUtf8(datum['title']) for datum in data.get('links')]

		# print self.pageid, self.parent, self.language, self.name, self.title, self.languages
		#print data['fullurl']
		# print pformat(data)
		# self.url = 'https://en.wikipedia.org/wiki/%s' % (pagename, )
		# self._childrenLanguages = []

	def asDict(self):
		nodeDict = {
			'pid': self.pageid,
			# 'parent': self.parent,
			'name': self.name,
			'title': self.title,
			# 'url': self.url,
			# 'views': self.views,
			# 'allinks': self.links,
			# 'exlinks': self.exlinks,
			'lang': self.language
			# 'resolved': self.resolved
		}
		if self.parent > 0:
			nodeDict['parent'] = self.parent
		if self.links:
			nodeDict['allinks'] = self.links

		return nodeDict

	def encodeUtf8(self, string):
		return string.encode('utf-8')

	def setPageData(self, pages=None):
		try:
			page = wikipedia.page(self.name)
		except:
			print 'WARNING: page skipped: %s' % (self.name, )
			return
		self.resolved = True
		projectLinks = []
		externalLinks = []
		for link in page.links:
			if pages and link in pages:
				# projectLinks.append(link.encode('utf8'))
				projectLinks.append(unicode(link))
			else:
				externalLinks.append(unicode(link))
		# data = {
		# 	'title': page.title,
		# 	'url': page.url,
		# 	'id': page.pageid,
		# 	'links': projectLinks,
		# 	'exlinks': externalLinks
		# }
		# return data
		# self.title = page.title.encode('utf8')
		# self.url = page.url.encode('utf8')
		self.title = unicode(page.title)
		self.url = unicode(page.url)
		self.pageid = page.pageid
		self.links = projectLinks
		self.exlinks = externalLinks

	def langlinks(self):
		# https://www.mediawiki.org/wiki/API:Langlinks
		# https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=langlinks
		# https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&format=json&llprop=url&lllimit=max&indexpageids=&titles=Main%20Page
		self._childrenLanguages = [WikiPage(link) for link in db.get_langlinks(self.page)]

	def getViews(self):
		return 200

	def weightedViews(self):
		weight = 1 / len(self._children)
		childrenViews = [weight * n.views() for n in self._children]
		return self.views / n.views


class WikiChildNode(WikiNode):

	def __init__(self, pagename, parent=None):
		self._parent = parent
