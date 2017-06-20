# lookup-osm-wikidata
This tool helps in finding various language translations of a osm feature from its corresponding wikidata item, given its feature [ID](http://wiki.openstreetmap.org/wiki/ID) and feature [Type](https://wiki.openstreetmap.org/wiki/Elements).


This repository has two scripts that help matching OSM features to Wikidata, and get metadata like translations from Wikidata API.

## osm.py

osm.py queries Mapbox's Dynamosm API to fetch the following properties for an OSM feature:

- wikidata - Wikidata ID of the feature.
- name
- name:en
- wikipedia - Wikipedia reference of the feature.
- geometry
- optional properties - script can return additional properties from osm, required by user.

**Usage**
`python osm.py input.csv highway`

#### Input

A csv with columns `osm_id, osm_type`.

#### Output

Output is a csv file called `output.csv` which is similar to input.csv, with additional properties.
The CSV has the following log information that might be useful to debug:

**osm:logs**:
- `Success` : Either of wikidata or wikipedia tag present for osm feature
- `No wikidata/wikipedia`: None of wikidata/wikipedia present
- `Dynamosm request failure`: API to query osm failed
- `No OSM Id/ Type`: Either of osm_id or osm_type not present in input

## wiki.py

`wiki.py` queries wikipedia API to fetch wikidata ID for those items which don't have `osm:wikidata`. Then it queries wikidata API to fetch required language translations.

#### Input

A csv with columns `osm:wikidata, osm:wikipdia, osm:geometry`.

#### Output

Output is a csv file called `finalOutput.csv` in which it appends the following columns to the input file: `wiki:wikidata wiki:Distance wiki:label:languageCodes wiki:logs`

**`wiki:Distance`**

This represents distance in kilo meterts between osm feature and corresponding wikidata item which can be used to validate the match. Higher distance indicates a potential descripency.

**`wiki:label:languageCode`**

Each of these contain the translations for corresponding language code

**`wiki:logs`**

- `languageCode Present`: Translation for this language code present in wikidata
- `No languageCode label`: Translation for this language code not present in wikidata
- `Wiki API Error`: API to query wikidata failed
- `No wikidata`: None of `osm:wikidata` or `wiki:wikidata` present
- `Wikipedia error`: API to query wikipedia failed
- `No wikidata / wikipedia`: None of osm:wikidata or osm:wikipedia present

#### Example
`python wiki.py zh zh-hans`
