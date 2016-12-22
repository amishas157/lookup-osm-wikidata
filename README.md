# osm-wikidata
This tool helps in finding various language translations of a osm feature from its corresponding wikidata item, given its feature [ID](http://wiki.openstreetmap.org/wiki/ID) and feature [Type](https://wiki.openstreetmap.org/wiki/Elements). 

## How it works

### OSM

#### Input
 A csv with columns `osm_id, osm_type` present in it.

Script `osm.py` queries Mapbox api-dynamosm and fetches the following properties linked to osm feature.

- Wikidata
- name
- name:en
- Wikipedia - It is used to fetch wikidata ids of an item using wikipedia API.
- geometry - Coordinates from this is used to find distance between osm feature and corresponding wikidata item. Helps in validating wikidata tag of an osm feature.

- Optional - The script can also return additional properties from osm, required by user.

Run:

`python osm.py <space separated name of properties os osm feature (optional)>`

Example:

`python osm.py highway osm:version`

#### Output

Outputs a csv file called `output.csv` in which it appends the following columns to `input.csv`

`osm:wikidata osm:wikipedia osm:name osm:name:en osm:geometry osm:logs osm:additional properties`

osm:logs contains one of the following:

- `Success` : Either of wikidata or wikipedia tag present for osm feature
- `No wikidata/wikipedia`: None of wikidata/ wikipedia present
- `Dynamosm request failure`: API to query osm failed
- `No OSM Id/ Type`: Either of osm_id or osm_type not present in input

wiki.py - A python script to query wikidata API for chinese labels

### Run
- python osm.py
- python wiki.py

### Output

finalOutput.csv - Input CSV with added columns: osm:wikidata, osm:wikipedia, wiki:wikidata, wiki:label:zh
