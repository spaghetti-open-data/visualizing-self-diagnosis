import wikipedia

def getPageData(pagetitle, pages=None):
	page = wikipedia.page(pagetitle)
	projectLinks = []
	externalLinks = []
	for link in page.links:
		if pages and link in pages:
			projectLinks.append(link)
		else:
			externalLinks.append(link)
	data = {
		'title': page.title,
		'url': page.url,
		'id': page.pageid,
		'links': projectLinks,
		'exlinks': externalLinks
	}
	return data
