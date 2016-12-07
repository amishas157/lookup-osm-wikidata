import json
import requests
fr = open('input.json','r')
wikiyes = open('wikiyes.json','w')
wikino = open('wikino.json','w')
requestfail = open('requestfail.json','w')
noidtype = open('noidtype.json','w')

for line in fr:
	l = json.loads(line)
	if l["osm_id"] and l["osm_type"]:
		r = requests.get('https://jzvqzn73ca.execute-api.us-east-1.amazonaws.com/api/feature/'+l["osm_type"]+'/'+l["osm_id"])
		response = r.json()
		if 'properties' in response:
			if 'wikidata' in response["properties"] or 'wikipedia' in response["properties"]:
				print response
				if 'wikidata' in response["properties"]:
					l["wikidata"] = response["properties"]["wikidata"]
				if 'wikipedia' in response["properties"]:
					l["wikipedia"] = response["properties"]["wikipedia"]
				wikiyes.write(json.dumps(l) + '\n')
			else:
				wikino.write(json.dumps(l) + '\n')
		else:
			requestfail.write(json.dumps(l) + '\n')
	else:
		noidtype.write(json.dumps(l) + '\n')
		
