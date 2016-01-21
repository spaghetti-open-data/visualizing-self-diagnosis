
class WikiNode(object):

	pageid = -1
	name = ''
	url = ''
	views = 0
	projlinks = None	# []
	extlinks = None		# []
	language = 'en'
	_childrenLanguages = None


	def __init__(pagename):
		self.pagedata = api.getpagedata()
		self.views = api.getviews()

	def langlinks():
		# https://www.mediawiki.org/wiki/API:Langlinks
		# https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=langlinks
		# https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&format=json&llprop=url&lllimit=max&indexpageids=&titles=Main%20Page
		self._childrenLanguages = [WikiPage(link) for link in db.get_langlinks(self.page)]

	def views():
		return 200

	def weightedViews():
		weight = 1 / len(self._children)
		childrenViews = [weight * n.views() for n in self._children]
		return self.views / n.views]


class WikiChildNode(WikiEnPage):

	def __init__(pagename, parent=None):
		self._parent = parent
