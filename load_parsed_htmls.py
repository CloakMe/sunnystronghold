import os
import json

def load_parsed_htmls(dir_path):
    res = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        with open(file_path) as f:
            holder = json.load(f)
            res.append(holder)
    return res