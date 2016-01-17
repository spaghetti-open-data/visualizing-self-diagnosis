# source: http://wikipedia.readthedocs.org/en/latest/quickstart.html

import wikipedia

# print wikipedia.search("Barack")
# print wikipedia.suggest("Barak Obama")
# print wikipedia.search("Ford", results=3)
# print wikipedia.summary("GitHub")
# print wikipedia.summary("Apple III", sentences=1)

# wikipedia.summary("Mercury")
# try:
# 	mercury = wikipedia.summary("Mercury")
# except wikipedia.exceptions.DisambiguationError as e:
# 	print e.options
# wikipedia.summary("zvv")

page = wikipedia.page("New York")
print page.title		# u'New York'
print page.url		# u'http://en.wikipedia.org/wiki/NewYork'
# print page.content	# u'New York is a state in the Northeastern region of the United States. New York is the 27th-most exten'...
print page.images[0]	# u'http://upload.wikimedia.org/wikipedia/commons/9/91/New_York_quarter%2C_reverse_side%2C_2001.jpg'
print page.links[0]	# u'1790 United States Census'


wikipedia.set_lang("fr")
# print wikipedia.summary("Francois Hollande")

print 'en' in wikipedia.languages()		# True
# print wikipedia.languages()['es']		# espanol


# Finally, the last method you're going to want to know in the wikipedia module is wikipedia.donate
# wikipedia.donate()
# your favorite web browser will open to the donations page of the Wikimedia project
# because without them, none of this would be possible
