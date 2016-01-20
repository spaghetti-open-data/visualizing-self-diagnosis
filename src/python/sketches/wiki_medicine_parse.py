""" Script for collecting data from Wikipedia.

		Python requirements:
			- pip install beautifulsoup4
"""

import os
import urllib, urllib2
import HTMLParser

from bs4 import BeautifulSoup

from pprint import pformat


# ul = soup.find('ul')
# for li in ul:
# 	print li.find('a')
# print ul
# print ul.fetch('a')

def getSoupFromUrl(url):
	response = urllib2.urlopen(url)
	html = response.read()
	return BeautifulSoup(html, "html.parser")

def dumpWikiSoup(soup, dump, prjstring):
	with open(dump, 'w') as dump:
		for a in soup.find_all('a', href=True):
			# print '%s%s' % (medprojurl, a['href'])
			link = a['href']
			if '/wiki/' not in link[:6] or prjstring in link:
				continue
			title = a['title']
			# htmlparser = HTMLParser.HTMLParser()
			# title = htmlparser.unescape(title)
			title = title.encode('utf8')
			dump.writelines('%s\n' % (title, ))
			# hack to break parsing when pagelist is finished
			if '/wiki/Special:MyTalk' in link:
				break

medprojurl = 'https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Medicine/Lists_of_pages/Articles'
prjstring = '/'.join(medprojurl.split('/')[3:5])
destination = 'output/medicine_dump.txt'
if not os.path.isdir('output'):
	os.mkdir('output')
print medprojurl, prjstring, destination

soup = getSoupFromUrl(medprojurl)
dumpWikiSoup(soup, destination, prjstring)
