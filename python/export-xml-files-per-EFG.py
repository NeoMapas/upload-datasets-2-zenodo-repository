#! python
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

qry = "SELECT distinct code FROM functional_groups "
cur.execute(qry)
EFGs = cur.fetchall()

for i in EFGs:
    EFG=i[0]
    # ALL SQL queries
    qry = "SELECT f.code,f.biome_code,b.name as biome,b.realms,f.name,f.shortname,f.shortdesc,f.update FROM functional_groups f LEFT JOIN biomes b USING (biome_code) WHERE code='%s'" % EFG
    cur.execute(qry)
    efg_info = cur.fetchone()
    qry = "SELECT e.description as traits,k.description as drivers,d.description as distribution,e.version,e.update as traits_date,d.update as drivers_date,e.update as distribution_date,e.contributors FROM efg_ecological_traits e LEFT JOIN efg_key_ecological_drivers k USING (code,version) LEFT JOIN efg_distribution d USING (code,version) WHERE e.code ='%s'  ORDER BY version DESC limit 1" % EFG
    cur.execute(qry)
    descs = cur.fetchone()
    ##    qry = "SELECT code,map_code,map_version,map_source,contributors FROM map_metadata WHERE map_type='Indicative Map' AND map_code like '%%orig' AND code='%s' ORDER BY map_version DESC LIMIT 1" % EFG # this was for version 1.1
    qry = "SELECT code,map_code,map_version,map_source,contributors FROM map_metadata WHERE map_type='Web navigation' AND status='valid' AND code='%s' ORDER BY map_version DESC LIMIT 1" % EFG # this was for version 1.1
    cur.execute(qry)
    map_info = cur.fetchone()
    qry = "WITH t AS (SELECT r.ref_code,author_list,date,title,container_title,post_title,doi FROM ref_list r LEFT JOIN efg_references e USING (ref_code) WHERE code ='%s' UNION  SELECT r.ref_code,author_list,date,title,container_title,post_title,doi FROM ref_list r LEFT JOIN map_references e USING (ref_code) WHERE map_code ='%s' AND map_version='%s' ) SELECT * FROM t ORDER BY author_list ASC" % (EFG,map_info['map_code'],map_info['map_version'])
    cur.execute(qry)
    refs = cur.fetchall()
    #Start XML file here
    root = ET.Element("EFGs")
    doc = ET.SubElement(root, "EFG",code=EFG,version=descs['version'],update=str(efg_info['update'].date()))
    realm = ET.SubElement(doc, "Realms")
    for i in efg_info['realms']:
        ET.SubElement(realm, "Realm").text = i
    ET.SubElement(doc, "Biome").text = efg_info['biome']
    ET.SubElement(doc, "Name").text = efg_info['name']
    ET.SubElement(doc, "Short-name").text = efg_info['shortname']
    authors = ET.SubElement(doc, "Contributors")
    for i in descs['contributors']:
        ET.SubElement(authors, "contributor").text = i
    if map_info['contributors'] is not None:
        for i in map_info['contributors']:
            ET.SubElement(authors, "map-contributor").text = i
    ET.SubElement(doc, "Short-description").text = efg_info['shortdesc']
    ET.SubElement(doc, "Ecological-traits",updated=str(descs['traits_date'])).text = descs['traits']
    ET.SubElement(doc, "Key-ecological-drivers",updated=str(descs['drivers_date'])).text = descs['drivers']
    ET.SubElement(doc, "Distribution",updated=str(descs['distribution_date'])).text = descs['distribution']
    ET.SubElement(doc, "Map",code=map_info['map_code'],version=map_info['map_version']).text = map_info['map_source']
    references = ET.SubElement(doc, "References")
    for ref in refs:
        ET.SubElement(references, "Reference", name=ref['ref_code']).text = "%s (%s) %s %s %s DOI:%s" % (ref['author_list'],ref['date'],ref['title'],ref['container_title'],ref['post_title'],ref['doi'])
    # write xml file
    file_name = xml_dir / efg_info['shortname'].replace(" ","_").replace(".","_").replace("/","_")
    xml_file = file_name.with_suffix(".xml")
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(xml_file,"w") as f:
        f.write(xmlstr) #xmlstr.encode('utf-8')



cur.close()
conn.close()

#    tree = ET.ElementTree(root)
#    tree.write(EFG + ".xml")
#json.dumps(refs,indent=1)
