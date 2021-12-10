#!python
import requests
import json
import xml.dom.minidom
from pathlib import Path
import os
import re

## create token in https://zenodo.org/account/settings/applications/tokens/new/
## copy/paste in new file, read from file:
## jferrer-unsw
## home_dir = Path(os.environ["HOME"])
## filename=home_dir / '.ZenodoToken'

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
## check title and select the appropriate one
r.json()[1]['title']
## we will need to extract the id
deposition_id = r.json()[1]['id']

## now use post to open for editing an existing deposition
r = requests.post('https://%s/api/deposit/depositions/%s/actions/edit' % (ZENODO_URL,deposition_id),
                  params={'access_token': ZENODO_TOKEN}, data={},
                  headers=headers)
r.status_code # Code: 201 Created or 403 if already open

#r = requests.post('https://%s/api/deposit/depositions/%s/actions/discard' % (ZENODO_URL,deposition_id),
#                  params={'access_token': ZENODO_TOKEN}, data={},
#                  headers=headers)
#r.status_code # Code: 201 Created or 403 if already open

## Update metadata
data={
'metadata': {
'communities': [{'identifier': 'iucn-rle'}],
'description': '<p>This dataset includes the original version of the indicative distribution maps and profiles for <strong>Ecological Functional Groups</strong> - Level 3 of IUCN Global Ecosystem Typology (v2.0). Please refer to Keith <em>et al.</em> (2020).</p>\n\n<p>The descriptive profiles provide brief summaries of key ecological traits and processes for each functional group of ecosystems to enable any ecosystem type to be assigned to a group.</p>\n\n<p>Maps are indicative of global distribution patterns are not intended to represent fine-scale patterns. The maps show areas of the world containing major (value of 1, coloured red) or minor occurrences (value of 2, coloured yellow) of each ecosystem functional group. Minor occurrences are areas where an ecosystem functional group is scattered in patches within matrices of other ecosystem functional groups or where they occur in substantial areas, but only within a segment of a larger region. Most maps were prepared using a coarse-scale template (e.g. ecoregions), but some were compiled from higher resolution spatial data where available (see details in profiles). Higher resolution mapping is planned in future publications.</p>\n\n<p>We emphasise that spatial representation of Ecosystem Functional Groups does not follow higher-order groupings described in respective ecoregion classifications. Consequently, when Ecosystem Functional Groups are aggregated into<strong> functional biomes</strong> (Level 2 of the Global Ecosystem Typology), spatial patterns may differ from those of biogeographic biomes. Differences reflect the distinctions between functional and biogeographic interpretations of the term, &ldquo;biome&rdquo;.</p>',
'keywords': ['Ecosystem science', 'Ecosystem classification', 'Functional biomes', 'Earth sciences', 'Human impact', 'Life sciences', 'Biodiversity conservation', 'Ecosystem services', 'Ecosystem management', 'Ecosystem assembly', 'Aichi targets', 'Ecosystem Functional Groups', 'Ecosystem traits', 'Ecosystem types'],
'language': 'eng',
'license': 'CC-BY-4.0',
'notes': "This dataset is part of the publication:\nDavid A. Keith, Jose R. Ferrer-Paris, Emily Nicholson, Melanie J. Bishop, Beth A. Polidoro, Eva Ramirez-Llodra, Mark G. Tozer, Jeanne L. Nel, Ralph Mac Nally, Edward J. Gregr, Kate E. Watermeyer, Franz Essl, Don Faber-Langendoen, Paul S. Giller, Belinda Robson, Janet Franklin, Caroline E. R. Lehmann, Andres Etter, Dirk J. Roux, Jonathan S. Stark, Jessica A. Rowland, Neil A. Brummitt, Ulla C. Fernandez-Arcaya, Iain M. Suthers, Thomas M. Iliffe, Vasilis Gerovasileiou, Troy S. Sakihara, Susan K. Wiser, Ian Donohue, Leland J. Jackson, R. Toby Pennington, Christy Linardich, Nathalie Pettorelli, Angela Andrade, Tytti Kontula, Arild Lindgaard, Teemu Tahvanainan, Aleks Terauds, Oscar Venter, James E. M. Watson, Michael A Chadwick, Nicholas J. Murray, Justin Moat, Patricio Pliscoff, Richard T. Corlett, Kenneth R. Young, Matthew S. McGlone, Richard T. Williams, Javier Loidi, Jeremy Russell-Smith, David Gibson, David J. Eldridge, Alexandre M. B. Anesio, Christian H. Körner, Richard Harper, Patrick W. Bogaart, P. Bhanumati, Monica Sharma, Grant C. Hose, Brett C. Gonzalez, David Brankovits, Alejandro Martínez García, Megan Lamson, Barbara Seidel, Dena M. Sedar, Scott Santos, Justin Havird, Jane A. Catford, Mark C. Rains, Kenneth Irvine, Angela H. Arthington, Mary Kelly-Quinn, Stefan Bertilsson, J. Tim Hollibaugh, Alan Channing, Martin J Siegert, Catherine Reidy Liermann, Malcom Beveridge, Thomas S. Bianchi, Ryan J. Woodland, Katherine A. Dafforn, Sarah L. McSweeney, Nick A. Cutler, Robert J. Orth, Andrew H. Altieri, Sergio Rossi, Charles R. C. Sheppard, Stephen E. Swearer, Ryan R. Rykaczewski , Lynne J. Shannon, Imants G. Priede, Tracey T. Sutton, Jeremy T. Claisse, Alicia T.R. Acosta, Paul E. Carnell,  Tasman P. Crowe, Louise B. Firth, Neil D. Burgess, Sylvia E. Hay, Lila García, Irene Zager, Lucie M. Bland, Richard T. Kingsford (2020) 'The IUCN Global Ecosystem Typology v2.0: Descriptive profiles for Biomes and Ecosystem Functional Groups'\n\n The PLuS Alliance supported a workshop in London to initiate development. DAK, EN, RTK, JRFP, JAR &amp; NJM were supported by ARC Linkage Grants LP170101143 and LP180100159 and the MAVA Foundation. The IUCN Commission on Ecosystem Management supported travel for DAK to present aspects of the research to peers and stakeholders at International Congresses on Conservation Biology in 2017 and 2019, and at meetings in Africa, the middle east and Europe.",
'publication_date': '2020-07-24',
'title': 'Indicative distribution maps for Ecological Functional Groups - Level 3 of IUCN Global Ecosystem Typology',
'upload_type': 'dataset',
'version': '2.0.0',
'access_right':'open',
## updated author info in creators node // contributor list is optional, requires a role for each contributor (might be minor contribution)
'creators': [
{'affiliation': 'University of New South Wales', 'name': 'Keith, David A.'},
{'affiliation': 'University of New South Wales', 'name': 'Ferrer-Paris, Jose R.', 'orcid': '0000-0002-9554-3395'},
{'affiliation': 'Deakin University', 'name': 'Nicholson, Emily', 'orcid': '0000-0003-2199-3446'},
{'affiliation': 'Macquarie University', 'name': 'Bishop, Melanie J.', 'orcid': '0000-0001-8210-6500'},
{'affiliation': 'Arizona State University', 'name': 'Polidoro, Beth A.','orcid': '0000-0002-4361-0189'},
{'affiliation': 'Norwegian Institute for Water Research', 'name': 'Ramirez-Llodra, Eva','orcid':'0000-0003-0137-1906'},
{'affiliation': 'NSW Department of Planning, Industry and Environment', 'name': 'Tozer, Mark G.'},
{'affiliation': 'Nelson Mandela University', 'name': 'Nel, Jeanne L.'},
{'affiliation': 'University of Canberra', 'name': 'Mac Nally, Ralph', 'orcid': '0000-0002-4473-1636'},
{'affiliation': 'University of British Columbia', 'name': 'Gregr, Edward J.'},
{'affiliation': 'Deakin University', 'name': 'Watermeyer, Kate E.'},
{'affiliation': 'University of Vienna', 'name': 'Essl, Franz','orcid':'0000-0001-8253-2112'},
{'affiliation': 'NatureServe', 'name': 'Faber-Langendoen, Don'},
#######
{'affiliation': 'University College Cork', 'name': 'Giller, Paul S.'},
{'affiliation': 'Murdoch University', 'name': 'Robson, Belinda J.'},
#########
{'affiliation': 'University of California', 'name': 'Franklin, Janet', 'orcid': '0000-0003-0314-4598'},
{'affiliation': 'University of Edinburgh', 'name': 'Lehmann, Caroline E. R.','orcid':'0000-0002-6825-124X'},
{'affiliation': 'Pontificia Universidad Javeriana', 'name': 'Etter, Andres','orcid':'0000-0003-0665-9300'},
{'affiliation': 'South African National Parks', 'name': 'Roux, Dirk J.','orcid': '0000-0001-7809-0446'},
{'affiliation': 'Australian Antarctic Division', 'name': 'Stark, Jonathan S.','orcid':'0000-0002-4268-8072'},
{'affiliation': 'Deakin University', 'name': 'Rowland, Jessica A.'},
{'affiliation': 'Natural History Museum, London', 'name': 'Brummitt, Neil A.'},
{'affiliation': 'Instituto Español de Oceanografía', 'name': 'Fernandez-Arcaya, Ulla C.','orcid':'0000-0002-5588-3520'},
{'affiliation': 'University of New South Wales', 'name': 'Suthers, Iain M.','orcid':'0000-0002-9340-7461'},
#
{'affiliation': 'Texas A&M University', 'name': 'Iliffe,Thomas M.'},
{'affiliation': 'Hellenic Centre for Marine Research', 'name': 'Gerovasileiou,Vasilis'},
{'affiliation': 'Department of Land and Natural Resources, Hawaii', 'name': 'Sakihara,Troy S.'},
##
{'affiliation': 'Manaaki Whenua - Landcare Research', 'name': 'Wiser, Susan K.','orcid':'0000-0002-8938-8181'},
{'affiliation': 'Trinity College Dublin', 'name': 'Donohue, Ian','orcid':'0000-0002-4698-6448'},
{'affiliation': 'University of Calgary', 'name': 'Jackson, Leland J.'},
{'affiliation': 'University of Exeter', 'name': 'Pennington, R. Toby','orcid': '0000-0002-8196-288X'},
{'affiliation': 'Arizona State University', 'name': 'Linardich, Christy'},
{'affiliation': 'Zoological Society of London', 'name': 'Pettorelli, Nathalie','orcid':'0000-0002-1594-6208'},
{'affiliation': 'Conservation International Colombia', 'name': 'Andrade, Angela'},
##
{'affiliation': 'Finnish Environment Institute', 'name': 'Kontula, Tytti'},
##
{'affiliation': 'Norwegian Biodiversity Information Centre', 'name': 'Lindgaard, Arild'},
{'affiliation': 'University of Eastern Finland', 'name': 'Tahvanainen, Teemu'},
{'affiliation': 'Australian Antarctic Division', 'name': 'Terauds, Aleks','orcid':'0000-0001-7804-6648'},
{'affiliation': 'University of Northern British Columbia', 'name': 'Venter, Oscar'},
{'affiliation': 'Wildlife Conservation Society', 'name': 'Watson, James E. M.','orcid':'0000-0003-4942-1984'},
{'affiliation': "King's College London", 'name': 'Chadwick, Michael A.','orcid':'0000-0003-4891-4357'},
{'affiliation': 'James Cook University', 'name': 'Murray, Nicholas J.', 'orcid': '0000-0002-4008-3053'},
{'affiliation': 'Royal Botanic Gardens Kew', 'name': 'Moat, Justin', 'orcid': '0000-0002-5513-3615'},
{'affiliation': 'Pontifica Universidad Católica de Chile', 'name': 'Pliscoff, Patricio','orcid': '0000-0002-5971-8880'},
##
{'affiliation': 'Xishuangbanna Tropical Botanical Garden', 'name': 'Corlett,Richard T.'},
{'affiliation': 'University of Texas', 'name': 'Young, Kenneth R.'},
{'affiliation': 'Manaaki Whenua - Landcare Research', 'name': 'McGlone, Matthew S.'},
{'affiliation': 'CSIRO', 'name': 'Williams, Richard T.'},
{'affiliation': 'University of the Basque Country', 'name': 'Loidi, Javier'},
{'affiliation': 'Charles Darwin University', 'name': 'Russell-Smith, Jeremy'},
{'affiliation': 'University of New South Wales', 'name': 'Eldridge, David J.'},
{'affiliation': 'Southern Illinois University', 'name': 'Gibson, David'},
{'affiliation': 'Aarhus University', 'name': 'Anesio, Alexandre M. B.'},
{'affiliation': 'University of Basel', 'name': 'Körner, Christian H.'},
{'affiliation': 'Murdoch University', 'name': 'Harper, Richard'},
{'affiliation': 'United Nations Statistics Division', 'name': 'Bogaart, Patrick W.'},
{'affiliation': 'Ministry of Statistics and Programme Implementation', 'name': 'Bhanumati, P.'},
{'affiliation': 'Consultant to the United Nations', 'name': 'Sharma, Monica'},
{'affiliation': 'Macquarie University', 'name': 'Hose, Grant C.'},
{'affiliation': 'Smithsonian National Museum of Natural History', 'name': 'Gonzalez, Brett C.'},
{'affiliation': 'Texas A&M University', 'name': 'Brankovits, David'},
{'affiliation': 'Italian National Research Council', 'name': 'Martínez García, Alejandro'},
{'affiliation': 'University of Hawaii', 'name': 'Lamson, Megan'},
{'affiliation': 'The Nature Conservancy', 'name': 'Seidel, Barbara'},
{'affiliation': 'Hawaii State Parks', 'name': 'Sedar, Dena M.'},
{'affiliation': 'Auburn University', 'name': 'Santos, Scott'},
{'affiliation': 'Colorado  State  University', 'name': 'Havird, Justin'},
{'affiliation': 'Kings College London', 'name': 'Catford, J.A.'},
{'affiliation': 'University of South Florida', 'name': 'Rains, M.C.'},
#B Robson,
{'affiliation': 'IHE Delft Institute for Water Education', 'name': 'Irvine, Kenneth'},
{'affiliation': 'Griffith University', 'name': 'Arthington, Angela H.'},
{'affiliation': 'University College Dublin', 'name': 'Kelly-Quinn, Mary'},
{'affiliation': 'Swedish University of Agricultural Sciences', 'name': 'Bertilsson, Stefan'},
{'affiliation': 'University of Georgia', 'name': 'Hollibaugh, J. Tim'},
{'affiliation': 'Cardiff University', 'name': 'Channing, A.'},
{'affiliation': 'Imperial College London', 'name': 'Siegert, Martin J.'},
{'affiliation': 'Western Washington University', 'name': 'Liermann, Catherine Reidy'},
{'affiliation': 'University of Stirling', 'name': 'Beveridge, Malcom'},
{'affiliation': 'University of Florida', 'name': 'Bianchi, Thomas S.'},
{'affiliation': 'University of Maryland', 'name': 'Woodland, Ryan J.'},
{'affiliation': 'Macquarie University', 'name': 'Dafforn, Katherine A.'},
{'affiliation': 'The University of Melbourne', 'name': 'McSweeney, Sarah L.'},
{'affiliation': 'Newcastle University', 'name': 'Cutler, Nick A.'},
{'affiliation': 'South African Association for Marine Biological Research', 'name': 'Porter, Sean N.'},
{'affiliation': 'Virginia Institute of Marine Science', 'name': 'Orth, Robert J.'},
{'affiliation': 'University of Florida', 'name': 'Altieri, Andrew H.'},
{'affiliation': 'Università del Salento', 'name': 'Rossi, Serio'},
{'affiliation': 'University of Warwick', 'name': 'Sheppard, Charles R. C.'},
{'affiliation': 'The University of Melbourne', 'name': 'Swearer, Stephen E. '},
{'affiliation': 'NOAA Pacific Islands Fisheries Science Center', 'name': 'Rykaczewski, Ryan R.'},
{'affiliation': 'University of Cape Town', 'name': 'Shannon, Lynne J. '},
{'affiliation': 'University of Aberdeen', 'name': 'Priede, Imants G. '},
{'affiliation': 'Nova Southeastern University', 'name': 'Sutton, Tracey T.'},
{'affiliation': 'California State Polytechnic University', 'name': 'Claisse, Jeremy T.'},
{'affiliation': 'Università Roma', 'name': 'Acosta, Alicia T. R.'},
{'affiliation': 'Deakin University', 'name': 'Carnell, Paul E.'},
{'affiliation': 'University College Dublin', 'name': 'Crowe, Tasman P.'},
{'affiliation': 'University of Plymouth', 'name': 'Firth, Louise B.'},
{'affiliation': 'United Nations Environment Programme', 'name': 'Burgess, Neil D.'},
{'affiliation': 'University of New South Wales', 'name': 'Hay, Sylvia E.'},
{'affiliation': 'Provita', 'name': 'García Riveiro, Lila'},
{'affiliation': 'Provita', 'name': 'Zager, Irene'},
{'name': 'Bland, Lucie'},
{'affiliation': 'University of New South Wales', 'name': 'Kingsford,  Richard T.','orcid':'0000-0001-6565-4134'}
]}}

#
#

## this fill update the metadata to the new version of the deposition_id
r = requests.put('https://%s/api/deposit/depositions/%s' % (ZENODO_URL,deposition_id),
                  params={'access_token': ZENODO_TOKEN}, data=json.dumps(data),
                  headers=headers)
r.status_code #Code: 201 Created

## check if correct and publish
r = requests.post('https://%s/api/deposit/depositions/%s/actions/publish' % (ZENODO_URL,deposition_id),
                  params={'access_token': ZENODO_TOKEN}, data=json.dumps(data),
                  headers=headers)
r.status_code #Code: 202 Accepted


exit()
