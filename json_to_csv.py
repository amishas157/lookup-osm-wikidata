import csv
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fr = open('wikiyes.json','r')
fw = open('wikiyes.csv','w')

csvwriter = csv.writer(fw)
csvwriter.writerow(["City","Status","assignee","Type","name_en","name_zh","OSM Search","GM Search","osm_type","osm_id","GM locatio","OSM location","source","lon","lat","custom_name","comments","wikidata","wikipedia"])
for line in fr:
	line = json.loads(line)
	if 'wikidata' in line and 'wikipedia' in line:
		csvwriter.writerow([line["City"],
	                line["Status"],
	                line["assignee"],
	                line["Type"],
	                line["name_en"],
			line["name_zh"],
			line["OSM Search"],
			line["GM Search"],
			line["osm_type"],
			line["osm_id"],
			line["GM locatio"],
			line["OSM location"],
			line["source"],
			line["lon"],
			line["lat"],
			line["custom_name"],
			line["comments"],
			line["wikidata"],
			line["wikipedia"]
			])
	elif 'wikidata' in line:
		csvwriter.writerow([line["City"],
	                line["Status"],
	                line["assignee"],
	                line["Type"],
	                line["name_en"],
			line["name_zh"],
			line["OSM Search"],
			line["GM Search"],
			line["osm_type"],
			line["osm_id"],
			line["GM locatio"],
			line["OSM location"],
			line["source"],
			line["lon"],
			line["lat"],
			line["custom_name"],
			line["comments"],
			line["wikidata"],
			""
			])
	elif 'wikipedia' in line:
		csvwriter.writerow([line["City"],
	                line["Status"],
	                line["assignee"],
	                line["Type"],
	                line["name_en"],
			line["name_zh"],
			line["OSM Search"],
			line["GM Search"],
			line["osm_type"],
			line["osm_id"],
			line["GM locatio"],
			line["OSM location"],
			line["source"],
			line["lon"],
			line["lat"],
			line["custom_name"],
			line["comments"],
			"",
			line["wikipedia"]
			])