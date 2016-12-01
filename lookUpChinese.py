import json
import requests

fr = open('wikiyes.json','r')
fw = open('chinese.json','w')

for line in fr:
	l = json.loads(line)
	if 'wikidata' in l:
		response = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + l['wikidata'] + "&format=json")
		data = response.json()
		if 'entities' in data:
			labels = data["entities"][l['wikidata']]["labels"]
			l['labels'] = labels
			fw.write(json.dumps(l) + '\n')
	elif 'wikipedia' in l:
		wiki = l['wikipedia'].split(':')
		response = requests.get("https://" + wiki[0] + ".wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&titles=" + wiki[1])
		data = response.json()
		try:
			page = data['query']['pages'].keys()[0]
			wikidataId =  data['query']['pages'][page]['pageprops']['wikibase_item']
                	responsewiki = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + wikidataId + "&format=json")
                	datawiki = responsewiki.json()
                	if 'entities' in datawiki:
                        	labels = datawiki["entities"][wikidataId]["labels"]
				l['labels'] = labels
				fw.write(json.dumps(l) + '\n')
		except KeyError, e:
			print l['osm_id']
