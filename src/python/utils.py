from contextlib import contextmanager
from datetime import datetime

@contextmanager
def timeIt(label=""):
	start = datetime.now()
	yield
	end = datetime.now()
	print "Time took %s: %s" % (label, end - start)
