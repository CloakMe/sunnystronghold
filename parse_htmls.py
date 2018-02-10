#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 13:52:17 2018

@author: evgeniy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup

#import pandas as pd
#from collections import Counter
#import re
#from urllib.request import urlopen
import os
import sys


dir_source_htmls = sys.argv[1]
dir_target_htmls = sys.argv[2]

path = dir_source_htmls
#path = '/home/evgeniy/Documents/Datathon2018/HTMLS/' 

file_names = os.listdir(path)

#file_name = '2055935.html'

file_names = [os.path.join(path, file_name) for file_name in file_names]

def extract_content(file_path, language='English'):
    # file_path = os.path.join(path, file_name)
    file_object  = open(file_path)
    
    # from collections import OrderedDict
    
    file_text = file_object.read()

    soup = BeautifulSoup(file_text, 'html.parser')    
    lang = soup.findAll("span", {"class": "uiOutputText"})[-1].text
    # print(lang)
    if lang != language:
        return None               
                        
    divs = soup.findAll("div", {"class": "slds-p-vertical_small cKM_OutputField"})
    # document_name, document_id = divs[0].text.split()
    def find_document_div(divs):
        for div in divs:
            tuples = div.text.split()
            if tuples[0] == 'Document':
                return div
        return None
    
    div_doc = find_document_div(divs)        
    if div_doc is None:
        return None
        
    doc_id = div_doc.text.split()
    if len(doc_id) != 2:
        print(doc_id)
    else:
        document_name, document_id = doc_id
    assert document_name == 'Document'
    
    holder = {document_name: document_id}

    for div in divs:
        paragraphName = div.findAll("b")[0].text        
        holder[paragraphName] = div.text
    return holder


#holders_english = [ extract_content(file_path, 'English') for file_path in file_names ]    


#paths_parsed = '/home/evgeniy/Documents/Datathon2018/HTML_parsed01'
paths_parsed = dir_source_htmls

for file_path in file_names:
    holder = extract_content(file_path, 'English')
    if holder is None:
        continue
    doc_id = holder['Document']
    
    json_name = os.path.join(paths_parsed, doc_id + '.json')
    
    with open(json_name, 'w') as fp:
        json.dump(holder, fp, indent=4)
    
    
#for holder in holders_english:
#    holder

#for holder in holders_english:
#    doc_id = holder['Document']
#    json.dump(holder, open(os.path.join(paths_parsed, doc_id), 'wb'))

    
#holder = extract_content(file_text, language='English') 




   
    