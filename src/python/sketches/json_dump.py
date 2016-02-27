import json


txtdump = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\python\\sketches\\output\\medicine_dump.txt'
jsondump = 'C:\\Users\\Stefan\\Documents\\GitHub\\futuroanteriore\\visualizing-self-diagnosis\\src\\python\\config\\medicine_dump.json'


with open(txtdump, 'r') as infile:
	lines = [line.replace('\n', '') for line in infile.readlines()]

with open(jsondump, 'w') as outfile:
	json.dump(lines, outfile, indent=4)
