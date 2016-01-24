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

	def __init__(self, pagename, parent=None):
		self._parent = parent
		self.name = pagename
		self.url = 'https://en.wikipedia.org/wiki/%s' % (pagename, )
		self._childrenLanguages = []
		# self.pagedata = api.getpagedata()
		# self.views = api.getviews()

	def asDict():
		return {
			'pageid': self.pageid,
			'name': self.name,
			'title': self.title,
			'url': self.url,
			'views': self.views,
			'links': self.links,
			'exlinks': self.exlinks,
			'language': self.language
		}

	def setPageData(self, pages=None):
		page = wikipedia.page(self.name)
		projectLinks = []
		externalLinks = []
		for link in page.links:
			if pages and link in pages:
				projectLinks.append(link)
			else:
				externalLinks.append(link)
		# data = {
		# 	'title': page.title,
		# 	'url': page.url,
		# 	'id': page.pageid,
		# 	'links': projectLinks,
		# 	'exlinks': externalLinks
		# }
		# return data
		self.title = page.title
		self.url = page.url
		self.pageid = page.pageid
		self.links = projectLinks
		self.exlinks = externalLinks

	def langlinks(self):
		# https://www.mediawiki.org/wiki/API:Langlinks
		# https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=langlinks
		# https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&format=json&llprop=url&lllimit=max&indexpageids=&titles=Main%20Page
		self._childrenLanguages = [WikiPage(link) for link in db.get_langlinks(self.page)]

	def views(self):
		return 200

	def weightedViews(self):
		weight = 1 / len(self._children)
		childrenViews = [weight * n.views() for n in self._children]
		return self.views / n.views


class WikiChildNode(WikiNode):

	def __init__(self, pagename, parent=None):
		self._parent = parent
