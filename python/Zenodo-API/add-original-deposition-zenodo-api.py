## follow instructions in https://developers.zenodo.org/#introduction

## make sure anaconda is activated
##conda install requests
conda activate

python
import requests
import json
import xml.dom.minidom
from pathlib import Path
import os

## create token in https://zenodo.org/account/settings/applications/tokens/new/
## copy/paste in new file, read from file:

## use sandbox.zenodo.org/api for testing,
## zenodo Sandbox jferrer-test
fo = open("/home/jferrer/.ZenodoSandboxToken","r")
SANDBOX_TOKEN = fo.readline(60)
SANDBOX_URL = "sandbox.zenodo.org"
fo.close()

## For the final version we use the real Zenodo site zenodo.org/api
## jferrer-unsw
fo = open("/home/jferrer/.ZenodoToken","r")
ZENODO_TOKEN = fo.readline(60)
ZENODO_URL = "zenodo.org"
fo.close()

## list of published items in my profile
headers = {"Content-Type": "application/json"}
r = requests.get('https://%s/api/deposit/depositions'  % ZENODO_URL,
                   params={'access_token': ZENODO_TOKEN},
                   headers=headers)
r.status_code
r.json()

## now use post to add a new deposition
headers = {"Content-Type": "application/json"}
r = requests.post('https://%s/api/deposit/depositions'  % ZENODO_URL,
                   params={'access_token': ZENODO_TOKEN}, json={},
                   headers=headers)
r.status_code
r.json()
## we will need this ID to add the metadata
r.json()['id']
deposition_id = r.json()['id']


## Set up all the metadata
data=

## this fill add the metadata to the deposition_id
r = requests.put('https://%s/api/deposit/depositions/%s' % (ZENODO_URL,deposition_id),
                  params={'access_token': ZENODO_TOKEN}, data=json.dumps(data),
                  headers=headers)
r.status_code

## now we get the list of data to add to the deposition
## in this case we are adding one zip file with the geotiff map, a png image of the map and the xml of the profile for each ecosystem functional group.
zip_dir = Path(os.environ["ZIPDIR"])
# prj_dir = Path(os.environ["SCRIPTDIR"])
# xml_dir = prj_dir /  "web" / "xml" / "EFG"
xml_dir = Path(os.environ["XMLDIR"])
for archivo in sorted(list(xml_dir.glob("*.xml"))):
    EFG = archivo.stem
    xml_doc =open(archivo,"r")
    doc = xml.dom.minidom.parse(xml_doc)
    NameTag = doc.getElementsByTagName("Short-name")
    if NameTag.length>0:
        sname=NameTag[0].childNodes[0].nodeValue;
        fname=sname.replace(" ","_").replace(".","_")+".tar.bz2"
    else:
        NameTag = doc.getElementsByTagName("Name")
        sname=NameTag[0].childNodes[0].nodeValue;
        fname=sname.replace(" ","_").replace(".","_")+".tar.bz2"
    file_name = zip_dir /  EFG
    zip_file = open(file_name.with_suffix(".tar.bz2"), 'rb')
    ##print(file_name) ## <-- just to check that we are including the right files
    ## This will upload the file to zenodo:
    data = {'name': fname}
    files = {'file': zip_file}
    r = requests.post('https://%s/api/deposit/depositions/%s/files' % (ZENODO_URL,deposition_id),
                       params={'access_token': ZENODO_TOKEN}, data=data,
                       files=files)
    print([r.status_code,fname])
    ##r.json() ## <-- this will print out the details
    xml_doc.close()
    zip_file.close()


## To do for next version: ADD one tar.bz2 file with all EFGs bundled together.

## When we are ready to publish we can do this, but it is better to do this directly on the site
#r = requests.post('https://sandbox.zenodo.org/api/deposit/depositions/%s/actions/publish' % deposition_id,
#                  params={'access_token': ACCESS_TOKEN} )
# r.status_code

## should be downloadable at:
#https://sandbox.zenodo.org/record/413773/files/{FILENAME}?download=1
