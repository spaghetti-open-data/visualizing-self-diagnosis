""" Dumps
"""
import json
import os

import wiki_mongo
import utils

basedir = os.path.dirname(__file__)
DUMP_FOLDER = os.path.join(basedir, "dump")

def get_languages():
	data = {}
	languages_file = os.path.join(basedir, "config", "languages.json")
	if os.path.exists(languages_file):
		with open(languages_file, "r") as my_file:
			data = json.load(my_file)
	return data

def dump_language_links(mongo, limit=None):
	""" Creates 1 dump file per language, with all links of that language.
		The content is: page ID: page name (as in DB)
	"""
	language_path = os.path.join(DUMP_FOLDER, "medicine_%s.json")
	languages = get_languages()
	for lang in languages:
		links = mongo.find(kargs={"lang": lang}, limit=limit)
		links_dump = {link["name"]: link["pid"] for link in links}
		with open(language_path % lang, "w") as my_file:
			json.dump(links_dump, my_file)


def test():
	basedir = os.path.dirname(__file__)
	with open(os.path.join(basedir, 'config/config.json')) as jsonfile:    
		data = json.load(jsonfile)
	config = data['mongoDB']
	mongo = wiki_mongo.getMongoClient(config)
	with utils.timeIt("query totalona"):
		dump_language_links(mongo)

test()