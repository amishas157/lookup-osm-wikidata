# osm-wikidata
A tool to match osm feature to wikidata tags and then fetch all languages translation present in it's wikidata

### Input 
input.csv - A CSV of osm features having osm_id and osm_type

### Output
wikino.csv - A CSV of osm features not having wikidata/wikipedia tags 
wikiyes.csv - A CSV of osm features having wikidata/wikipedia tags
wikiyeschinese.csv - A CSV of osm features with their all the language traslationn present in wikidata

### How it works

script.py - A python script to look into input file and query api-dynamosm for each osm features and getting it's wikidata/wikipedia tag if present. It creates two buckets: wikiyes.csv and wikino.csv

loopUpChinese.py - A python script to query wikidata API for language translations for osm features present in wikiyes.csv. It creates bucket wikiyeschinese.csv
