#! python3
import requests
import json
from pathlib import Path
import os
import re
import psycopg2
import psycopg2.extras
##from config import config
from configparser import ConfigParser
import xml.etree.cElementTree as ET
from xml.dom import minidom

home_dir = Path(os.environ["HOME"])
xml_dir = Path(os.environ["XMLDIR"])

parser = ConfigParser()
filename=home_dir / '.database.ini'
parser.read(filename)
db = {}
params = parser.items('psqlaws')
for param in params:
    db[param[0]] = param[1]

## connect to postgres database
conn = psycopg2.connect(**db)
# create a cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
##cur = conn.cursor()

# execute a statement

qry = "SELECT code, shortname, name, map_code, map_version, map_source, contributors, m.update FROM functional_groups f LEFT JOIN map_metadata m USING (code) WHERE map_type='Web navigation' AND status = 'valid' ORDER BY code"
cur.execute(qry)
EFGs = cur.fetchall()

qry = "SELECT DISTINCT r.ref_code,author_list,date,title,container_title,post_title,doi FROM ref_list r LEFT JOIN map_references e USING (ref_code) LEFT JOIN map_metadata USING (map_code,map_version) WHERE map_type='Web navigation' AND status = 'valid' ORDER BY author_list ASC"
cur.execute(qry)
REFs = cur.fetchall()

#Start XML file here
root = ET.Element("root")
mapE = ET.SubElement(root, "Maps")
refE = ET.SubElement(root, "References")

# add list of maps
for i in EFGs:
    infoE = ET.SubElement(mapE, "Map", efg_code=i['code'], map_code=i['map_code'], map_version=i['map_version'], update=str(i['update'].date()))
    ET.SubElement(infoE, "Functional_group").text = i['name']
    ET.SubElement(infoE, "Description").text = i['map_source']
    authors = ET.SubElement(infoE, "Contributors")
    if i['contributors'] is not None:
        for j in i['contributors']:
            ET.SubElement(authors, "map-contributor").text = j
    ET.SubElement(infoE, "Filename").text = i['map_code']+'_'+i['map_version']+'.tif'

# add references
for k in REFs:
    ET.SubElement(refE, "Reference", name=k['ref_code']).text = "%s (%s) %s %s %s DOI:%s" % (k['author_list'],k['date'],k['title'],k['container_title'],k['post_title'],k['doi'])

# write xml file
file_name = xml_dir / "map-details"
xml_file = file_name.with_suffix(".xml")
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
with open(xml_file,"w") as f:
        f.write(xmlstr) #xmlstr.encode('utf-8')

cur.close()
conn.close()
