#!python
import requests
import json
import xml.dom.minidom
from pathlib import Path
import os
import re

## create token in https://zenodo.org/account/settings/applications/tokens/new/
## copy/paste in new file, read from file:

home_dir = Path(os.environ["HOME"])
filename=home_dir / '.ZenodoToken'

fo = open(filename,"r")
ZENODO_TOKEN = fo.readline(60)
ZENODO_URL = "zenodo.org"
fo.close()

## list of published items in my profile
headers = {"Content-Type": "application/json"}
r_list = requests.get('https://%s/api/deposit/depositions'  % ZENODO_URL,
                   params={'access_token': ZENODO_TOKEN},
                   headers=headers)
r_list.status_code
r_list.json()
## check title and select the appropriate one
r_list.json()[1]['title']
## we will need to extract the id
deposition_id = r_list.json()[0]['id']

## now use post to add a new version to an existing deposition
r_add = requests.post('https://%s/api/deposit/depositions/%s/actions/newversion' % (ZENODO_URL,deposition_id),
                  params={'access_token': ZENODO_TOKEN}, data={},
                  headers=headers)
r_add.status_code # Code: 201 Created or 403 if already open

##r_add = None

## double check:

r_new = requests.get('https://%s/api/deposit/depositions/%s'  % (ZENODO_URL,deposition_id),
                   params={'access_token': ZENODO_TOKEN},
                   headers=headers)
r_new.status_code
r_new.json()
r_new.json()['links']['latest_draft']

##find new deposition id
#re.findall('[0-9]+',r.json()['links']['latest_draft'])
new_deposition_id=re.findall('[0-9]+',r_new.json()['links']['latest_draft'])[0]


## read metadata
#data=r.json()

authorlist = [
{'affiliation': 'University of New South Wales', 'name': 'Keith, David A.'},
{'affiliation': 'University of New South Wales', 'name': 'Ferrer-Paris, Jose R.', 'orcid': '0000-0002-9554-3395'},
{'affiliation': 'Deakin University', 'name': 'Nicholson, Emily', 'orcid': '0000-0003-2199-3446'},
{'affiliation': 'University of New South Wales', 'name': 'Kingsford,  Richard T.','orcid':'0000-0001-6565-4134'}
]

contributorlist = [
{'affiliation': 'Macquarie University', 'name': 'Bishop, Melanie J.', 'orcid': '0000-0001-8210-6500', 'type': 'Researcher'},
{'affiliation': 'Arizona State University', 'name': 'Polidoro, Beth A.','orcid': '0000-0002-4361-0189', 'type': 'Researcher'},
{'affiliation': 'Norwegian Institute for Water Research', 'name': 'Ramirez-Llodra, Eva','orcid':'0000-0003-0137-1906', 'type': 'Researcher'},
{'affiliation': 'NSW Department of Planning, Industry and Environment', 'name': 'Tozer, Mark G.', 'type': 'Researcher'},
{'affiliation': 'Nelson Mandela University', 'name': 'Nel, Jeanne L.', 'type': 'Researcher'},
{'affiliation': 'University of Canberra', 'name': 'Mac Nally, Ralph', 'orcid': '0000-0002-4473-1636', 'type': 'Researcher'},
{'affiliation': 'University of British Columbia', 'name': 'Gregr, Edward J.', 'type': 'Researcher'},
{'affiliation': 'Deakin University', 'name': 'Watermeyer, Kate E.', 'type': 'Researcher'},
{'affiliation': 'University of Vienna', 'name': 'Essl, Franz','orcid':'0000-0001-8253-2112', 'type': 'Researcher'},
{'affiliation': 'NatureServe', 'name': 'Faber-Langendoen, Don', 'type': 'Researcher'},
#######
{'affiliation': 'University College Cork', 'name': 'Giller, Paul S.', 'type': 'Researcher'},
{'affiliation': 'Murdoch University', 'name': 'Robson, Belinda J.', 'type': 'Researcher'},
#########
{'affiliation': 'University of California', 'name': 'Franklin, Janet', 'orcid': '0000-0003-0314-4598', 'type': 'Researcher'},
{'affiliation': 'University of Edinburgh', 'name': 'Lehmann, Caroline E. R.','orcid':'0000-0002-6825-124X', 'type': 'Researcher'},
{'affiliation': 'Pontificia Universidad Javeriana', 'name': 'Etter, Andres','orcid':'0000-0003-0665-9300', 'type': 'Researcher'},
{'affiliation': 'South African National Parks', 'name': 'Roux, Dirk J.','orcid': '0000-0001-7809-0446', 'type': 'Researcher'},
{'affiliation': 'Australian Antarctic Division', 'name': 'Stark, Jonathan S.','orcid':'0000-0002-4268-8072', 'type': 'Researcher'},
{'affiliation': 'Deakin University', 'name': 'Rowland, Jessica A.', 'type': 'Researcher'},
{'affiliation': 'Natural History Museum, London', 'name': 'Brummitt, Neil A.', 'type': 'Researcher'},
{'affiliation': 'Instituto Español de Oceanografía', 'name': 'Fernandez-Arcaya, Ulla C.','orcid':'0000-0002-5588-3520', 'type': 'Researcher'},
{'affiliation': 'University of New South Wales', 'name': 'Suthers, Iain M.','orcid':'0000-0002-9340-7461', 'type': 'Researcher'},
#
{'affiliation': 'Texas A&M University', 'name': 'Iliffe,Thomas M.', 'type': 'Researcher'},
{'affiliation': 'Hellenic Centre for Marine Research', 'name': 'Gerovasileiou,Vasilis', 'type': 'Researcher'},
{'affiliation': 'Department of Land and Natural Resources, Hawaii', 'name': 'Sakihara,Troy S.', 'type': 'Researcher'},
##
{'affiliation': 'Manaaki Whenua - Landcare Research', 'name': 'Wiser, Susan K.','orcid':'0000-0002-8938-8181', 'type': 'Researcher'},
{'affiliation': 'Trinity College Dublin', 'name': 'Donohue, Ian','orcid':'0000-0002-4698-6448', 'type': 'Researcher'},
{'affiliation': 'University of Calgary', 'name': 'Jackson, Leland J.', 'type': 'Researcher'},
{'affiliation': 'University of Exeter', 'name': 'Pennington, R. Toby','orcid': '0000-0002-8196-288X', 'type': 'Researcher'},
{'affiliation': 'Arizona State University', 'name': 'Linardich, Christy', 'type': 'Researcher'},
{'affiliation': 'Zoological Society of London', 'name': 'Pettorelli, Nathalie','orcid':'0000-0002-1594-6208', 'type': 'Researcher'},
{'affiliation': 'Conservation International Colombia', 'name': 'Andrade, Angela', 'type': 'Researcher'},
##
{'affiliation': 'Finnish Environment Institute', 'name': 'Kontula, Tytti', 'type': 'Researcher'},
##
{'affiliation': 'Norwegian Biodiversity Information Centre', 'name': 'Lindgaard, Arild', 'type': 'Researcher'},
{'affiliation': 'University of Eastern Finland', 'name': 'Tahvanainen, Teemu', 'type': 'Researcher'},
{'affiliation': 'Australian Antarctic Division', 'name': 'Terauds, Aleks','orcid':'0000-0001-7804-6648', 'type': 'Researcher'},
{'affiliation': 'University of Northern British Columbia', 'name': 'Venter, Oscar', 'type': 'Researcher'},
{'affiliation': 'Wildlife Conservation Society', 'name': 'Watson, James E. M.','orcid':'0000-0003-4942-1984', 'type': 'Researcher'},
{'affiliation': "King's College London", 'name': 'Chadwick, Michael A.','orcid':'0000-0003-4891-4357', 'type': 'Researcher'},
{'affiliation': 'James Cook University', 'name': 'Murray, Nicholas J.', 'orcid': '0000-0002-4008-3053', 'type': 'Researcher'},
{'affiliation': 'Royal Botanic Gardens Kew', 'name': 'Moat, Justin', 'orcid': '0000-0002-5513-3615', 'type': 'Researcher'},
{'affiliation': 'Pontifica Universidad Católica de Chile', 'name': 'Pliscoff, Patricio','orcid': '0000-0002-5971-8880', 'type': 'Researcher'},
{'affiliation': 'Xishuangbanna Tropical Botanical Garden', 'name': 'Corlett,Richard T.', 'type': 'Researcher'},
{'affiliation': 'University of Texas', 'name': 'Young, Kenneth R.', 'type': 'Researcher'},
{'affiliation': 'Manaaki Whenua - Landcare Research', 'name': 'McGlone, Matthew S.', 'type': 'Researcher'},
{'affiliation': 'CSIRO', 'name': 'Williams, Richard T.', 'type': 'Researcher'},
{'affiliation': 'University of the Basque Country', 'name': 'Loidi, Javier', 'type': 'Researcher'},
{'affiliation': 'Charles Darwin University', 'name': 'Russell-Smith, Jeremy', 'type': 'Researcher'},
{'affiliation': 'Southern Illinois University', 'name': 'Gibson, David', 'type': 'Researcher'},
{'affiliation': 'University of New South Wales', 'name': 'Eldridge, David J.', 'type': 'Researcher'},
{'affiliation': 'Aarhus University', 'name': 'Anesio, Alexandre M. B.', 'type': 'Researcher'},
{'affiliation': 'University of Basel', 'name': 'Körner, Christian H.', 'type': 'Researcher'},
{'affiliation': 'Murdoch University', 'name': 'Harper, Richard', 'type': 'Researcher'},
{'affiliation': 'United Nations Statistics Division', 'name': 'Bogaart, Patrick W.', 'type': 'Researcher'},
{'affiliation': 'Ministry of Statistics and Programme Implementation', 'name': 'Bhanumati, P.', 'type': 'Researcher'},
{'affiliation': 'Consultant to the United Nations', 'name': 'Sharma, Monica', 'type': 'Researcher'},
{'affiliation': 'Macquarie University', 'name': 'Hose, Grant C.', 'type': 'Researcher'},
{'affiliation': 'Smithsonian National Museum of Natural History', 'name': 'Gonzalez, Brett C.', 'type': 'Researcher'},
{'affiliation': 'Texas A&M University', 'name': 'Brankovits, David', 'type': 'Researcher'},
{'affiliation': 'Italian National Research Council', 'name': 'Martínez García, Alejandro', 'type': 'Researcher'},
{'affiliation': 'University of Hawaii', 'name': 'Lamson, Megan', 'type': 'Researcher'},
{'affiliation': 'The Nature Conservancy', 'name': 'Seidel, Barbara', 'type': 'Researcher'},
{'affiliation': 'Hawaii State Parks', 'name': 'Sedar, Dena M.', 'type': 'Researcher'},
{'affiliation': 'Auburn University', 'name': 'Santos, Scott', 'type': 'Researcher'},
{'affiliation': 'Colorado  State  University', 'name': 'Havird, Justin', 'type': 'Researcher'},
{'affiliation': 'Kings College London', 'name': 'Catford, J.A.', 'type': 'Researcher'},
{'affiliation': 'University of South Florida', 'name': 'Rains, M.C.', 'type': 'Researcher'},
#B Robson,
{'affiliation': 'IHE Delft Institute for Water Education', 'name': 'Irvine, Kenneth', 'type': 'Researcher'},
{'affiliation': 'Griffith University', 'name': 'Arthington, Angela H.', 'type': 'Researcher'},
{'affiliation': 'University College Dublin', 'name': 'Kelly-Quinn, Mary', 'type': 'Researcher'},
{'affiliation': 'Swedish University of Agricultural Sciences', 'name': 'Bertilsson, Stefan', 'type': 'Researcher'},
{'affiliation': 'University of Georgia', 'name': 'Hollibaugh, J. Tim', 'type': 'Researcher'},
{'affiliation': 'Cardiff University', 'name': 'Channing, A.', 'type': 'Researcher'},
{'affiliation': 'Imperial College London', 'name': 'Siegert, Martin J.', 'type': 'Researcher'},
{'affiliation': 'Western Washington University', 'name': 'Liermann, Catherine Reidy', 'type': 'Researcher'},
{'affiliation': 'University of Stirling', 'name': 'Beveridge, Malcom', 'type': 'Researcher'},
{'affiliation': 'University of Florida', 'name': 'Bianchi, Thomas S.', 'type': 'Researcher'},
{'affiliation': 'University of Maryland', 'name': 'Woodland, Ryan J.', 'type': 'Researcher'},
{'affiliation': 'Macquarie University', 'name': 'Dafforn, Katherine A.', 'type': 'Researcher'},
{'affiliation': 'The University of Melbourne', 'name': 'McSweeney, Sarah L.', 'type': 'Researcher'},
{'affiliation': 'Newcastle University', 'name': 'Cutler, Nick A.', 'type': 'Researcher'},
#{'affiliation': 'South African Association for Marine Biological Research', 'name': 'Porter, Sean N.'},
{'affiliation': 'Virginia Institute of Marine Science', 'name': 'Orth, Robert J.', 'type': 'Researcher'},
{'affiliation': 'University of Florida', 'name': 'Altieri, Andrew H.', 'type': 'Researcher'},
{'affiliation': 'Università del Salento', 'name': 'Rossi, Serio', 'type': 'Researcher'},
{'affiliation': 'University of Warwick', 'name': 'Sheppard, Charles R. C.', 'type': 'Researcher'},
{'affiliation': 'The University of Melbourne', 'name': 'Swearer, Stephen E.', 'type': 'Researcher'},
{'affiliation': 'NOAA Pacific Islands Fisheries Science Center', 'name': 'Rykaczewski, Ryan R.', 'type': 'Researcher'},
{'affiliation': 'University of Cape Town', 'name': 'Shannon, Lynne J.', 'type': 'Researcher'},
{'affiliation': 'University of Aberdeen', 'name': 'Priede, Imants G.', 'type': 'Researcher'},
{'affiliation': 'Nova Southeastern University', 'name': 'Sutton, Tracey T.', 'type': 'Researcher'},
{'affiliation': 'California State Polytechnic University', 'name': 'Claisse, Jeremy T.', 'type': 'Researcher'},
{'affiliation': 'Università Roma', 'name': 'Acosta, Alicia T. R.', 'type': 'Researcher'},
{'affiliation': 'Deakin University', 'name': 'Carnell, Paul E.', 'type': 'Researcher'},
{'affiliation': 'University College Dublin', 'name': 'Crowe, Tasman P.', 'type': 'Researcher'},
{'affiliation': 'University of Plymouth', 'name': 'Firth, Louise B.', 'type': 'Researcher'},
#{'affiliation': 'United Nations Environment Programme', 'name': 'Burgess, Neil D.'},
{'affiliation': 'University of New South Wales', 'name': 'Hay, Sylvia E.','type': 'Other'},
{'affiliation': 'Provita', 'name': 'García Riveiro, Lila','type': 'Other'},
{'affiliation': 'Provita', 'name': 'Zager, Irene','type': 'Other'},
{'name': 'Bland, Lucie','type': 'Other'}
] # possible roles DataCurator, DataManager

## Update metadata
data={
'metadata': {
'communities': [{'identifier': 'iucn-rle'}],
'description': '<p>This dataset includes the original version of the indicative distribution maps and profiles for <strong>Ecosystem Functional Groups</strong> - Level 3 of IUCN Global Ecosystem Typology (v2.0). Please refer to Keith <em>et al.</em> (2020).</p>\n\n<p>The descriptive profiles provide brief summaries of key ecological traits and processes for each functional group of ecosystems to enable any ecosystem type to be assigned to a group.</p>\n\n<p>Maps are indicative of global distribution patterns are not intended to represent fine-scale patterns. The maps show areas of the world containing major (value of 1, coloured red) or minor occurrences (value of 2, coloured yellow) of each ecosystem functional group. Minor occurrences are areas where an ecosystem functional group is scattered in patches within matrices of other ecosystem functional groups or where they occur in substantial areas, but only within a segment of a larger region. Most maps were prepared using a coarse-scale template (e.g. ecoregions), but some were compiled from higher resolution spatial data where available (see details in profiles). Higher resolution mapping is planned in future publications.</p>\n\n<p>We emphasise that spatial representation of Ecosystem Functional Groups does not follow higher-order groupings described in respective ecoregion classifications. Consequently, when Ecosystem Functional Groups are aggregated into<strong> functional biomes</strong> (Level 2 of the Global Ecosystem Typology), spatial patterns may differ from those of biogeographic biomes. Differences reflect the distinctions between functional and biogeographic interpretations of the term, &ldquo;biome&rdquo;.</p>',
'keywords': ['Ecosystem science', 'Ecosystem classification', 'Functional biomes', 'Earth sciences', 'Human impact', 'Life sciences', 'Biodiversity conservation', 'Ecosystem services', 'Ecosystem management', 'Ecosystem assembly', 'Aichi targets', 'Ecosystem Functional Groups', 'Ecosystem traits', 'Ecosystem types'],
'language': 'eng',
'license': 'CC-BY-4.0',
'notes': "This dataset is part of the publication:\n Keith DA, Ferrer-Paris JR, Nicholson E, Kingsford RT (Eds.) (2020) 'The IUCN Global Ecosystem Typology v2.0: Descriptive profiles for Biomes and Ecosystem Functional Groups'. The International Union for the Conservation of Nature (IUCN), Gland. DOI:10.2305/IUCN.CH.2020.13.en.\n\n The PLuS Alliance supported a workshop in London to initiate development. DAK, EN, RTK, JRFP, JAR &amp; NJM were supported by ARC Linkage Grants LP170101143 and LP180100159 and the MAVA Foundation. The IUCN Commission on Ecosystem Management supported travel for DAK to present aspects of the research to peers and stakeholders at International Congresses on Conservation Biology in 2017 and 2019, and at meetings in Africa, the middle east and Europe.",
'publication_date': '2021-07-05',
'title': 'Indicative distribution maps for Ecosystem Functional Groups - Level 3 of IUCN Global Ecosystem Typology',
'upload_type': 'dataset',
'version': '2.1.1',
'access_right':'open',
## updated author info in creators node // contributor list is optional, requires a role for each contributor (might be minor contribution)
'creators': authorlist,
'contributors': contributorlist,
## Related/alternate identifiers
'related_identifiers':[{'identifier': '10.2305/IUCN.CH.2020.13.en', 'relation': 'isSupplementTo', 'resource_type': 'publication-book', 'scheme': 'doi'}]
}
}

#

## this fill update the metadata to the new version of the deposition_id
r_mod = requests.put('https://%s/api/deposit/depositions/%s' % (ZENODO_URL,new_deposition_id),
                  params={'access_token': ZENODO_TOKEN}, data=json.dumps(data),
                  headers=headers)
r_mod.status_code ## 200 success, 4XX some error

## now we need to replace files with newer versions


## list files
fls = requests.get('https://%s/api/deposit/depositions/%s/files' % (ZENODO_URL,new_deposition_id),
                  params={'access_token': ZENODO_TOKEN},
                  headers=headers)
fls.status_code

archivos = fls.json()
len(archivos)

## delete one file
##archivos[101]['filename']
##dfls = requests.delete('https://%s/api/deposit/depositions/%s/files/%s' % (ZENODO_URL,new_deposition_id,archivos[100]['id']),
##                  params={'access_token': ZENODO_TOKEN},
##                  headers=headers)

## delete ten files
#for i in xrange(1,10):
## delete all files
for i in range(0,len(archivos)):
    dfls = requests.delete('https://%s/api/deposit/depositions/%s/files/%s' % (ZENODO_URL,new_deposition_id,archivos[i]['id']),
                  params={'access_token': ZENODO_TOKEN},
                  headers=headers)



## now we get the list of data to add to the deposition
## first two large zip files with all the raster and all the vector maps, each with a README and xml documentation of map methods and references

# Now, let’s upload a new file. We have recently released a new API, which is significantly more perfomant and supports much larger file sizes. While the older API supports 100MB per file, the new one has no size limitation.
#To use the new files API we will do a PUT request to the bucket link. The bucket is a folder-like object storing the files of our record. Our bucket URL will look like this: https://zenodo.org/api/files/568377dd-daf8-4235-85e1-a56011ad454b and can be found under the links key in our records metadata.
bucket_url = r_mod.json()["links"]["bucket"]

zip_dir = Path(os.environ["ZIPDIR"])
for archivo in sorted(list(zip_dir.glob("all*.tar.bz2"))):
    fname = archivo.stem + ".bz2"
    zip_file = open(archivo, 'rb')
    r = requests.put('%s/%s' % (bucket_url,fname),
                    data=zip_file,
                       params={'access_token': ZENODO_TOKEN})
    print([r.status_code,fname]) # 200 success
    zip_file.close()

# r.json() ## <-- this will print out the details of the last call

## Now we are are adding one zip file with the geotiff map, a png image of the map and the xml of the profile for each ecosystem functional group. Here we can use the old API approach...

#for archivo in sorted(list(zip_dir.glob("[MFTS]*.tar.bz2"))):
#    fname = archivo.stem + ".bz2"
#    zip_file = open(archivo, 'rb')
#    data = {'name': fname} # a '/' in filename is changed to '_'
#    files = {'file': zip_file}
#    r = requests.post('https://%s/api/deposit/depositions/%s/files' % (ZENODO_URL,new_deposition_id),
#                       params={'access_token': ZENODO_TOKEN}, data=data,
#                       files=files)
#    print([r.status_code,fname]) # 201 instead of 200 ?
    ##r.json() ## <-- this will print out the details
#    zip_file.close()




## When we are ready to publish we can do this, but it is better to do this directly on the site
#r = requests.post('https://sandbox.zenodo.org/api/deposit/depositions/%s/actions/publish' % deposition_id,
#                  params={'access_token': ACCESS_TOKEN} )
# r.status_code

exit()
