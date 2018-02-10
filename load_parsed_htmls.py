import os
import json

def load_parsed_htmls(dir_path):
    res = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        holder = json.load(open(file_path))
        res.append(holder)
    return res