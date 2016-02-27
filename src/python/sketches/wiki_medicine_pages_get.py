""" Script for collecting data from Wikipedia.
	This test reads a dump of pages for a certain project and fetches pages data.
	For each page's link, it checks whether they send to other pages
	within the same project, or to external ones.

		Python requirements:
			- pip install wikipedia

		References:
			- http://wikipedia.readthedocs.org/en/latest/quickstart.html
			- http://wikipedia.readthedocs.org/en/latest/code.html#api
			- http://www.compjour.org/tutorials/exploring-wikipedia-api-via-python

"""

import os

# import HTMLParser
import wikipedia


from pprint import pformat


def getPageData(pagetitle, pages):
	# &prop=langlinks
	page = wikipedia.page(pagetitle)
	projectLinks = []
	# externalLinks = []
	for link in page.links:
		if link in pages:
			projectLinks.append(link)
		# else:
		# 	externalLinks.append(link)
	data = {
		'title': page.title,
		'url': page.url,
		'id': page.pageid,
		'links': projectLinks

	}
	return data

def printPageData(pagetitle, pages):
	page = wikipedia.page(pagetitle)
	print page.title, ':', page.url, ':', page.pageid
	projectLinks = []
	externalLinks = []
	for link in page.links:
		if link in pages:
			projectLinks.append(link)
		else:
			externalLinks.append(link)
	# print page.links
	print projectLinks
	print externalLinks
	# print page.images

def printPagesData(pages, limit=5):
	for i, page in enumerate(pages):
		printPageData(page, pages)
		if i > limit:
			break

def getMedicinePagesFromDump(limit=10):
	pages = []
	exceptions = []

	path = os.path.dirname(os.path.abspath(__file__))

	with open(os.path.join(path, 'output/medicine_dump.txt'), 'r') as dump:
		for i, line in enumerate(dump.readlines()):
			if i > limit:
				break
			# h = HTMLParser.HTMLParser()
			# line = h.unescape(line).replace('/wiki/','').replace('%', '\%')
			try:
				line = line.encode('utf8').replace('\n', '')
				pages.append(line)
			except:
				exceptions.append(line)
				continue
	return pages, exceptions

def getMedicinePageUrlsFromDump(limit=10):
	pages, exceptions = getMedicinePagesFromDump(limit)
	urls = {}
	for i, page in enumerate(pages):
		if i > limit:
			break
		data = getPageData(page, pages)
		urls[data['title']] = data['url']
	return urls

def printPagesDataFromDump(limit=5):
	pages, exceptions = getMedicinePagesFromDump()
	if exceptions:
		print 'WARNING: %d exceptions found' % (len(exceptions))
	print '%d pages found' % (len(pages))
	printPagesData(pages)

# printPagesDataFromDump()
