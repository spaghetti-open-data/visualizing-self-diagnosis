path = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\python\\dump'

import os

files = os.listdir(path)
for f in files:
	if not '~origin_dev-moe' in f:
		continue
	print f[:-15], f[:-15] in files
	os.rename(os.path.join(path, f), os.path.join(path, f[:-15]))
