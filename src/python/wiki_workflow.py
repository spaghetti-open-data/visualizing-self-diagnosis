
class WikiEnPage(object):

	id = -1
	name = ''
	url = ''
	views = 0
	projlinks = None # []
	extlinks = None # []
	language = 'en'
	languages = { 'en': self }


	def __init__(pagename):
		api.getpagedata()
		api.getviews()

	def langlinks():
		# https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=langlinks
		self._childrenOtherLanguages = [WikiPage(link) for link in db.get_langlinks(self.page)]

	def views():
		return 200

	def weightedViews():
		weight = 1 / len(self._children)
		childrenViews = [weight * n.views() for n in self._children]
		return self.views / n.views]


class WikiLanguagePage(WikiEnPage):
	def __init__(pagename, parent=None):
		self._parent = parent



pagenodes = []

# get all english pages for medicine
for pages in medicine:

	# for each page, get all translations
	for page in pages:
		links = page.langlinks()
		pagenodes.append(WikiEnPage(page, links))
		# for current page and all translations, get page data and pageviews
		for pagelang in links:
			pagenodes.append(WikiLanguagePage(pagelang, page)) 


# visualization
# layer graphs of each language, representing pages as knots and links as connections

