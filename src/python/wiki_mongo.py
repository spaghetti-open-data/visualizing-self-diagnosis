'''
	- pip install pymongo
'''

from pymongo import MongoClient

from bson.objectid import ObjectId


class MongoDbClient(object):

	def __init__(self, host, port, user, dbpwd, dbname, collection):
		super(MongoDbClient, self).__init__()
		self.host = host
		self.port = port
		self.dbuser = user
		self.dbpwd = dbpwd
		self.dbname = dbname
		self.collection = collection
		self.connect()
		print 'MongoDbClient initialized'

	def get(self, uid):
		return self.db.find_one({'_id': ObjectId(uid)})

	def put(self, data):
		self.db.insert(data)

	def connect(self):
		self.connection = MongoClient(self.host, self.port)
		# print self.connection
		db = self.connection[self.dbname]
		db.authenticate(self.dbuser, self.dbpwd)
		# print self.dbuser, self.dbpwd, db
		# the following should be managed via an additional switch, if necessary
		# self.connection = MongoClient(self.dburi)
		# self.db = ?
		self.db = db[self.collection]

	def find(self, kargs=None, limit=0):
		if limit == 0:
			if kargs:
				return self.db.find(kargs)
			return self.db.find()
		else:
			'''
			for post in posts.find({'Longevity' : {"$gte" : 20, "$lte" : 100}}):
				print search
			'''
			if kargs:
				return self.db.find(kargs)[:limit]
			return self.db.find()[:limit]

	def search(self, query):
		return list(self.db.find(query))

	def update(self, searchKwargs, newKwargs, multi=False):
		self.db.update(searchKwargs, newKwargs, multi=multi)

def getMongoClient(config):
	return MongoDbClient(
		config.get('server'),
		config.get('port'),
		config.get('username'),
		config.get('password'),
		config.get('db_name'),
		config.get('collection')
	)
