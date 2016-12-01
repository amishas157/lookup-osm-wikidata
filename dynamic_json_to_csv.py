import json, csv
fr = open('chinese.json', 'r')
fw = open('output.csv', 'w')

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('wikiyes.csv', 'r')
w = open('wikiyeschinese.csv','w')
keys = ["City","Status","assignee","Type","name_en","name_zh","OSM Search","GM Search","osm_type","osm_id","GM locatio","OSM location","source","lon","lat","custom_name","comments","wikidata","wikipedia"]

labels = set()

for line in fr:
	l = json.loads(line)
	labels.update(l['labels'].keys())

for label in list(labels):
	keys.append(str(label))

csvwriter = csv.writer(w)
csvwriter.writerow(keys)

fr = open('chinese.json','r')
for line in fr:
	line = json.loads(line)
	row = []
	for key in keys:
		if key in line:
			row.append(line[key])
		elif key in line['labels']:
			row.append(line['labels'][key]["value"])
		else:
			row.append("")
	csvwriter.writerow(row)

