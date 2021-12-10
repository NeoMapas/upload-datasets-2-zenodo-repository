#!python
import requests
import json
#import xml.dom.minidom
#import re
from pathlib import Path
import os
import sys
import xml.etree.cElementTree as ET

if len(sys.argv) != 2:
    raise ValueError('Please provide code of EFG.')

EFG = sys.argv[1]

## load Zenodo token:
home_dir = Path(os.environ["HOME"])
filename=home_dir / '.ZenodoToken'

fo = open(filename,"r")
ZENODO_TOKEN = fo.readline(60)
ZENODO_URL = "zenodo.org"
fo.close()

## set up work dir
zip_dir = Path(os.environ["ZIPDIR"])
work_dir = zip_dir / EFG

for fl in work_dir.glob("*.xml"):
    print(fl.name)

autaff = { ## currently only four direct contributors to the maps
        "DA Keith" : {'affiliation': 'University of New South Wales', 'name': 'Keith, David A.'},
        "JR Ferrer-Paris" : {'affiliation': 'University of New South Wales', 'name': 'Ferrer-Paris, Jose R.', 'orcid': '0000-0002-9554-3395'},
        "P Pliscoff" : {'affiliation': 'Pontifica Universidad Católica de Chile', 'name': 'Pliscoff, Patricio','orcid': '0000-0002-5971-8880', 'type': 'Researcher'},
        "NJ Murray" : {'affiliation': 'James Cook University', 'name': 'Murray, Nicholas J.', 'orcid': '0000-0002-4008-3053', 'type': 'Researcher'}
    }
xf = open(fl,"r")
tree = ET.parse(xf)
root = tree.getroot()
# [elem.tag for elem in root.iter()]
authorlist = []
for aut in root.iter('map-contributor'):
    authorlist.append(autaff[aut.text])

for mapinfo in root.iter('Map'):
    mapver = mapinfo.attrib
    mapcode="%s %s" % (mapver['code'],mapver['version'])

for name in root.iter('Name'):
    efgname = name.text

xf.close()

title = 'Indicative distribution map for Ecosystem Functional Group ' + efgname

description = '<p>This archive contains indicative distribution maps and profiles for <strong>{name}</strong>, a ecosystem functional group (EFG, level 3) of the <a href=https://global-ecosystems.org/>IUCN Global Ecosystem Typology</a> (v2.0). Please refer to Keith <em>et al.</em> (2020) for details.</p>\n\n<p>The descriptive profiles provide brief summaries of key ecological traits and processes, maps are indicative of global distribution patterns, and are not intended to represent fine-scale patterns. The maps show areas of the world containing major (value of 1, coloured red) or minor occurrences (value of 2, coloured yellow) of each ecosystem functional group. Minor occurrences are areas where an ecosystem functional group is scattered in patches within matrices of other ecosystem functional groups or where they occur in substantial areas, but only within a segment of a larger region. Given bounds of resolution and accuracy of source data, the maps should be used to query which EFG are likely to occur within areas, rather than which occur at particular point locations. Detailed methods and references for the maps are included in the profile (xml format).</p>'.format(name=efgname)

related_ids = [{'identifier': '10.2305/IUCN.CH.2020.13.en', 'relation': 'isSupplementTo', 'resource_type': 'publication-book', 'scheme': 'doi'},
{'identifier': '10.5281/zenodo.5090419', 'relation': 'isSourceOf', 'resource_type': 'dataset', 'scheme': 'doi'}]

kwds = ['Ecosystem science', 'Ecosystem classification', 'Functional biomes', 'Earth sciences', 'Human impact', 'Life sciences', 'Biodiversity conservation', 'Ecosystem services', 'Ecosystem management', 'Ecosystem assembly', 'Aichi targets', 'Ecosystem Functional Groups', 'Ecosystem traits', 'Ecosystem types']

notes = "This dataset is part of the publication:\n Keith DA, Ferrer-Paris JR, Nicholson E, Kingsford RT (Eds.) (2020) 'The IUCN Global Ecosystem Typology v2.0: Descriptive profiles for Biomes and Ecosystem Functional Groups'. The International Union for the Conservation of Nature (IUCN), Gland. DOI:10.2305/IUCN.CH.2020.13.en.\n\n DAK, &amp; JRFP were supported by ARC Linkage Grants LP170101143 and LP180100159 and the MAVA Foundation."

## create new deposition
headers = {"Content-Type": "application/json"}
params = {'access_token': ZENODO_TOKEN}
r = requests.post('https://%s/api/deposit/depositions' % ZENODO_URL,
                   params=params,
                   json={},
                   headers=headers)
r.status_code
r.json()

bucket_url = r.json()["links"]["bucket"]
deposition_id = r.json()['id']

for archivo in sorted(list(work_dir.glob("*"))):
    fname = archivo.name
    print(fname)
    with open(archivo, "rb") as fp:
        r = requests.put(
            "%s/%s" % (bucket_url, fname),
            data=fp,
            params=params,
        )
    print([r.status_code,fname]) # 200 success


data={
 'metadata': {
 'communities': [{'identifier': 'iucn-rle'}],
 'description': description,
 'keywords': kwds,
 'language': 'eng',
 'license': 'CC-BY-4.0',
 'notes': notes,
 'publication_date': '2021-07-10',
 'title': title,
 'upload_type': 'dataset',
 'version': mapcode,
 'access_right':'open',
 'creators': authorlist,
 'related_identifiers': related_ids
 }
 }



r = requests.put('https://zenodo.org/api/deposit/depositions/%s' % deposition_id, params=params, data=json.dumps(data), headers=headers)

print(r.status_code)
