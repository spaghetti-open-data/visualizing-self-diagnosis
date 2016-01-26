import wikipedia

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

	def __init__(self, pagename, parent=None):
		super(WikiNode, self).__init__()
		self._parent = parent
		self.name = pagename
		self.url = 'https://en.wikipedia.org/wiki/%s' % (pagename, )
		self._childrenLanguages = []
		self._views_client = _viewsApi.PageviewsClient()
		# self.pagedata = api.getpagedata()

	def asDict(self):
		return {
			'pageid': self.pageid,
			'name': self.name,
			'title': self.title,
			'url': self.url,
			'views': self.views,
			'links': self.links,
			'exlinks': self.exlinks,
			'language': self.language
			# 'resolved': self.resolved
		}

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

	def weightedViews(self):
		weight = 1 / len(self._children)
		childrenViews = [weight * n.views() for n in self._children]
		return self.views / n.views


class WikiChildNode(WikiNode):

	def __init__(self, pagename, parent=None):
		super(WikiChildNode, self).__init__()
		self._parent = parent
