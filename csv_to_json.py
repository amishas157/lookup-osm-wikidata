import csv
import json

csvfile = open('input.csv', 'r')
jsonfile = open('input.json', 'w')

fieldnames = ("City","Status","assignee","Type","name_en","name_zh","OSM Search","GM Search","osm_type","osm_id","GM locatio","OSM location","source","lon","lat","custom_name","comments")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
