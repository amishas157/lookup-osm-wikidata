import csv
import json
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fr = open('input.csv', 'r')
fw = open('input.json', 'w')

line = fr.readline()
fieldnames = line.split(',')
fieldnames.pop() #remove the end \n element

reader = csv.DictReader( fr, fieldnames)
for row in reader:
    json.dump(row, fw)
    fw.write('\n')

fr.close()
fw.close()

count = 0

tags = []

for arg in sys.argv:
    if count != 0:
        tags.append(sys.argv[count].strip())
    count += 1

fr = open('input.json','r')
fw = open('output.json','w')

fieldnames.extend(["osm:logs", "osm:wikidata", "osm:wikipedia", "osm:name", "osm:name:en", "osm:geometry"])

for tag in tags:
    fieldnames.extend(['osm:'+tag])

count = 0;

for line in fr:
    count = count + 1
    l = json.loads(line)
    if l["osm_id"] and l["osm_type"]:
        r = requests.get('https://jzvqzn73ca.execute-api.us-east-1.amazonaws.com/api/feature/'+l["osm_type"]+'/'+l["osm_id"])
        response = r.json()
        if 'properties' in response:
            if 'wikidata' in response["properties"] or 'wikipedia' in response["properties"]:
                if 'wikidata' in response["properties"]:
                    l["osm:wikidata"] = response["properties"]["wikidata"]
                if 'wikipedia' in response["properties"]:
                    l["osm:wikipedia"] = response["properties"]["wikipedia"]
                l["osm:logs"] = "Success"
            else:
                l["osm:logs"] = "No wikidata/wikipedia"

            if 'name' in response["properties"]:
                l["osm:name"] = response["properties"]["name"]
            if 'name:en' in response["properties"]:
                l["osm:name:en"] = response["properties"]["name:en"]
            if 'geometry' in response and 'coordinates' in response["geometry"]:
                l["osm:geometry"] = response["geometry"]

            for tag in tags:
                if tag in response["properties"]:
                    l["osm:"+tag] = response["properties"][tag]
        else:
            l["osm:logs"] = "Dynamosm request failure"
    else:
        l["osm:logs"] = "No OSM Id/ Type"
    print count
    fw.write(json.dumps(l) + '\n')

fr.close()
fw.close()

fr = open('output.json','r')
fw = open('output.csv','w')

csvwriter = csv.writer(fw)
fieldnames.append('')
csvwriter.writerow(fieldnames)
for line in fr:
    line = json.loads(line)
    obj = []
    for key in fieldnames:
        try:
            obj.append(line[key])
        except:
            obj.append("")
    csvwriter.writerow(obj)

fr.close()
fw.close()