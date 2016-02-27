from wiki_medicine_pages_get import getMedicinePageUrlsFromDump

import urllib2
import json

from pprint import pformat


def langlinks(page):
	root = 'https://en.wikipedia.org/w/api.php?'
	action = 'action=query&prop=langlinks&format=json&llprop=url&lllimit=max&indexpageids=&titles=%s' % (page, )
	url = '%s%s' % (root, action)
	# print url
	response = urllib2.urlopen(url)
	data = json.load(response)   

	jsondict = data['query']
	pageid = jsondict['pages'].keys()[0]
	print pformat(jsondict['pages'][pageid])
	if not 'langlinks' in jsondict['pages'][pageid]:
		return
	links = jsondict['pages'][pageid]['langlinks']
	for link in links:
		lang = link['lang']
		url = link['url']
		print lang, url
	# print pformat(jsondict)
	# print pageid, links
	# https://www.mediawiki.org/wiki/API:Langlinks
	# https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=langlinks
	# self._childrenOtherLanguages = [WikiPage(link) for link in db.get_langlinks(self.page)]


page = 'Main_Page'
# langlinks(page)


# get all english pages for medicine
limit = 2
# urls = getMedicinePageUrlsFromDump(limit)
# test
urls = {
	# u'1% rule (aviation medicine)': u'https://en.wikipedia.org/wiki/1%25_rule_(aviation_medicine)',
	u'1% rule (aviation medicine)': u'https://en.wikipedia.org/wiki/1%25 rule (aviation_medicine)',
	u'1,1,1,2-Tetrafluoroethane': u'https://en.wikipedia.org/wiki/1,1,1,2-Tetrafluoroethane',
	u'1,4-Dioxin': u'https://en.wikipedia.org/wiki/1,4-Dioxin'
}

# for each page, get all translations
for name, url in urls.items():
	urlname = url.split('/wiki/')[-1]
	print urlname
	langlinks(urlname)

pagenodes = []

for page in []: # medicine.pages():
	links = page.langlinks()
	pagenodes.append(WikiEnPage(page, links))
	# for current page and all translations, get page data and pageviews
	for pagelang in links:
		pagenodes.append(WikiLanguagePage(pagelang, page)) 


# visualization
# layer graphs of each language, representing pages as knots and links as connections

