import json
import requests
import shapely.geometry
from geopy.distance import vincenty
import csv
import ast
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

fr = open('output.csv', 'r')
fw = open('output.json', 'w')

line = fr.readline()
fieldnames = line.split(',')

count = 0
for field in fieldnames:
    fieldnames[count] = fieldnames[count].rstrip()
    count += 1

reader = csv.DictReader( fr, fieldnames)
for row in reader:
    json.dump(row, fw)
    fw.write('\n')

fr.close()
fw.close()

count = 0

labels = []

for arg in sys.argv:
    if count != 0:
        labels.append(sys.argv[count].strip())
    count += 1


def hasWikidata( wikidataId, l ):
    responsewiki = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + wikidataId + "&format=json")
    datawiki = responsewiki.json()

    l['wiki:logs'] = ''
    for label in labels:
        try:
            l['wiki:wikidata'] = wikidataId
            wikilabels = datawiki["entities"][wikidataId]["labels"][label]["value"]
            l['wiki:label:'+label] = wikilabels
            l['wiki:logs'] += label + " Present,"
        except:
            l['wiki:logs'] += "No " + label +  " label,"
    try:
        l['instance'] = datawiki["entities"][wikidataId]["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"]
    except:
        l['instance'] = ""
    try:
        l['wiki:label:en'] = datawiki["entities"][wikidataId]["labels"]["en"]["value"]
    except:
        l['wiki:label:en'] = ""
    try:
        l['wiki:wikipedia:en'] = datawiki["entities"][wikidataId]["sitelinks"]["enwiki"]["title"]
    except:
        l['wiki:wikipedia:en'] = ""
    try:
        l['latitude'] = datawiki["entities"][wikidataId]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"]
        l['longitude'] = datawiki["entities"][wikidataId]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"]

        geom_geojson = shapely.geometry.shape({"type": "Point", "coordinates": [longitude, latitude]})
        d = ast.literal_eval(l['osm:geometry'])
        geom_db = shapely.geometry.shape(d)

        centroid_geojson = geom_geojson.centroid
        centroid_db = geom_db.centroid

        distance = vincenty((centroid_geojson.x,centroid_geojson.y),(centroid_db.x, centroid_db.y)).km
        l['wiki:Distance'] = distance
    except Exception as e:
        l['wiki:Distance'] = ""
    return l


fr = open('output.json','r')
fw = open('finalOutput.json','w')
count = 0
fieldnames.extend(["wiki:logs", "wiki:wikidata", "wiki:label:en", "wiki:wikipedia:en", "wiki:wikipedia:vi", "longitude", "latitude", "wiki:Distance", "instance"])
for label in labels:
    fieldnames.extend(['wiki:label:'+label])

for line in fr:
    count = count + 1
    l = json.loads(line)
    if 'osm:wikidata' in l and l['osm:wikidata'] != "":
        try:
            l = hasWikidata(l['osm:wikidata'], l)
        except:
            l['wiki:logs'] = "Wiki API Error"

    elif 'osm:wikipedia' in l and l['osm:wikipedia'] != "":
        try:
            wiki = l['osm:wikipedia'].split(':')
            response = requests.get("https://" + wiki[0] + ".wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&titles=" + wiki[1])
            data = response.json()
            try:
                page = data['query']['pages'].keys()[0]
                wikidataId =  data['query']['pages'][page]['pageprops']['wikibase_item']
                l['wiki:wikidata'] = wikidataId
                l = hasWikidata(wikidataId, l)
            except:
                l['wiki:logs'] = "No wikidata"
        except:
            l['wiki:logs'] = "Wikipedia error"
    else:
        l['wiki:logs'] = "No wikidata / wikipedia"
    fw.write(json.dumps(l) + '\n')
    print count

fr.close()
fw.close()

fr = open('finalOutput.json','r')
fw = open('finalOutput.csv','w')

csvwriter = csv.writer(fw)

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
