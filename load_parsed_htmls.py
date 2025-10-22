import os
import json

def load_parsed_htmls(dir_path, 
                      number_to_load=None):    
    res = []
    listed_files = os.listdir(dir_path)
    for nmb, file_name in enumerate(listed_files):
        if number_to_load is not None and nmb >= number_to_load:
            break            
        file_path = os.path.join(dir_path, file_name)
        with open(file_path) as f:
            holder = json.load(f)
            res.append(holder)
    return res