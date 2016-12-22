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

#### Run

`python osm.py <space separated name of properties os osm feature (optional)>`

Example:

`python osm.py highway osm:version`

#### Output

Outputs a csv file called `output.csv` in which it appends the following columns to `input.csv`

`osm:wikidata osm:wikipedia osm:name osm:name:en osm:geometry osm:logs osm:additional properties`

#### osm:logs

- `Success` : Either of wikidata or wikipedia tag present for osm feature
- `No wikidata/wikipedia`: None of wikidata/ wikipedia present
- `Dynamosm request failure`: API to query osm failed
- `No OSM Id/ Type`: Either of osm_id or osm_type not present in input


### Wikidata

#### Input
A csv with columns `osm:wikidata, osm:wikipdia, osm:geometry` present in it. (output from osm.py i.e. output.csv)

Script `wiki.py` queries wikipedia API to fetch wikidata for thise items which don't have `osm:wikidata`. Then it queries wikidata API to fetch required language translations.

#### Run
`python wiki.py <space separated language codes of the languages in which translation is required>`

Example:

`python wiki.py zh zh-hans`

#### Output

Outputs a csv file called `finalOutput.csv` in which it appends the following columns to `output.csv`

`wiki:wikidata wiki:Distance wiki:label:languageCodes wiki:logs`

#### wiki:Distance

This represents distance(in km.) between osm feature and corresponding wikidata item which can be used to validate the wikidata item linked to osm feature. Higher the distance indicates higher is the suspicion of mislinking of wikidata tag.

#### wiki:label:languageCode

Each of these contain the translations for corresponding language code

#### wiki:logs

- languageCode Present: Translation for this language code present in wikidata
- No languageCode label: Translation for this language code not present in wikidata
- Wiki API Error: API to query wikidata failed
- No wikidata: None of `osm:wikidata` or `wiki:wikidata` present
- Wikipedia error: API to query wikipedia failed
- No wikidata / wikipedia: None of osm:wikidata or osm:wikipedia present
