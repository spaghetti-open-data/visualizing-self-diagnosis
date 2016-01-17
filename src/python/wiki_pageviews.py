""" Script for collecting views data from Wikipedia.

		Python requirements:
			- pip pip install mwviews
"""

from mwviews.api import PageviewsClient

from wiki_medicine_pages_get import getMedicinePageUrlsFromDump


from pprint import pformat


limit = 2
urls = getMedicinePageUrlsFromDump(limit)
# print pformat(urls)
pageurls = [url.split('wikipedia.org/wiki/')[1] for url in urls.values()]
# print pformat(pageurls)

viewsclient = PageviewsClient()
# articles = viewsclient.top_articles('en.wikipedia', limit=10)
# projectviews = viewsclient.project_views(['ro.wikipedia', 'de.wikipedia', 'commons.wikimedia'])
# print pformat(dict(projectviews))
articleviews = viewsclient.article_views('en.wikipedia', pageurls[:limit])
print pformat(dict(articleviews))





'''
# https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/1%25_rule_(aviation_medicine)/daily/2015121800/2016011700

project = 'project'
access = 'access'
agent = 'agent'
article = 'article'
granularity = 'granularity'
start = 'start'
end = 'end'

url = 'https://wikimedia.org/api/rest_v1'
url += '/metrics/pageviews/per-article'
url += '/' + project
url += '/' + access
url += '/' + agent
url += '/' + article
url += '/' + granularity
url += '/' + start
url += '/' + end

print url
'''
