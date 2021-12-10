#!python
import requests
import json
import xml.dom.minidom
from pathlib import Path
import os
import re
import pandas as pd
import tarfile

## create token in https://zenodo.org/account/settings/applications/tokens/new/
## copy/paste in new file, read from file:

zip_dir = Path(os.environ["ZIPDIR"])
# print(*zip_dir.iterdir(),sep="\n")
print(*zip_dir.glob("all*bz2"),sep="\n")
fp = tarfile.open(zip_dir / "all-maps-raster-geotiff.tar.bz2","r:bz2")
##fp.list()
readme=fp.extractfile('README')
data=list(readme)
readme.close()
fp.close()

mcodes=list()
for line in data:
    sline = str(line)
    if ".tif" in sline:
        mcodes.append(re.sub('.*\\(([A-Z_a-z0-9.]+)_([a-z0-9.]+)\\).*','\\1 \\2',sline))

home_dir = Path(os.environ["HOME"])
filename=home_dir / '.ZenodoToken'

fo = open(filename,"r")
ZENODO_TOKEN = fo.readline(60)
ZENODO_URL = "zenodo.org"
fo.close()

headers = {"Content-Type": "application/json"}

## Query main depositions with summary of maps
qry="title:IUCN Global Ecosystem Typology"
search_deposition = requests.get('https://%s/api/deposit/depositions?q=%s'  % (ZENODO_URL,qry),
                   params={'access_token': ZENODO_TOKEN},
                   headers=headers)
search_deposition.status_code
len(search_deposition.json())

#Check:
maintitle='Indicative distribution maps for Ecosystem Functional Groups - Level 3 of IUCN Global Ecosystem Typology'
for i in search_deposition.json():
    if i['title']==maintitle:
        main_deposition = i
        deposition_id = i['id']

main_deposition.keys()


## Query uploaded depositions for each indicative map
qsize=200
qry="title:Indicative distribution map for"
r_list = requests.get('https://%s/api/deposit/depositions?size=%s&q=%s'  % (ZENODO_URL,qsize,qry),
                   params={'access_token': ZENODO_TOKEN},
                   headers=headers)


r_list.status_code
#r_list.json()
len(r_list.json())
type(r_list.json())

my_dict = [{'id':i['id'], 'doi':i['doi'], 'state':i['state'], 'version':i['metadata']['version'], 'title':i['title']} for i in r_list.json()]

df = pd.DataFrame(my_dict)
##df.to_csv('mycsvfile.csv', index=False)
df.value_counts('state')


int(df.loc[df['title']==maintitle].id)


metadata = main_deposition['metadata']


rids = [{'identifier': '10.2305/IUCN.CH.2020.13.en', 'relation': 'isSupplementTo', 'resource_type': 'publication-book', 'scheme': 'doi'}]


target=df.loc[(df.state =='done') & df.title.str.contains('Indicative distribution map for') & df['version'].isin(mcodes)]

for i in target.id:
    rids.append({'identifier': '10.5281/zenodo.%s' % int(i), 'relation': 'isDerivedFrom', 'resource_type': 'dataset', 'scheme': 'doi'})

len(rids)

metadata['related_identifiers'] = rids

data={'metadata':metadata}

r_edit = requests.post(main_deposition['links']['edit'],
                  params={'access_token': ZENODO_TOKEN}, data={},
                  headers=headers)
r_edit.status_code # Code: 201 Created or 403 if already open

r_mod = requests.put(main_deposition['links']['self'],
                  params={'access_token': ZENODO_TOKEN}, data=json.dumps(data),
                  headers=headers)
r_mod.status_code ## 200 success, 4XX some error

r_pub = requests.post(main_deposition['links']['publish'],
                  params={'access_token': ZENODO_TOKEN},
                  headers=headers)
r_pub.status_code ## 200 success, 4XX some error

mlist =pd.DataFrame(mcodes)
mlist['idx'] = mlist[0].isin(df.version)
mlist[mlist["idx"]==False]

exit()
