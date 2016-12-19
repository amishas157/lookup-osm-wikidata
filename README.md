# osm-wikidata
A tool to match osm feature to wikidata tags and querying the corresponding wikidata for chinese label.

### Input 
input.csv - A CSV of osm features having osm_id and osm_type

### How it works

osm.py - A python script to look into input file and query api-dynamosm for each osm features and getting it's wikidata/wikipedia tag if present.

wiki.py - A python script to query wikidata API for chinese labels

### Run
- python osm.py
- python wiki.py

### Output

finalOutput.csv - Input CSV with added columns: osm:wikidata, osm:wikipedia, wiki:wikidata, wiki:label:zh
