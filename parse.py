import os
import re
import copy
def ParseHtmlFiles(data_dir='HTMLS/',max_num_files=0):
    f = 1
    data_samples = []
    for filename in os.listdir(data_dir) :
        if filename.endswith(".html") : 
            #print(f,filename)
            html = open(data_dir + '/' + filename,'r').read()
        
            html = re.sub(r'<.*?>', '\n', html)        
            html = re.sub(r'\n{1,}', '\n', html)

            # Cut out css and javascript
            Cuttof_Keyword = 'Toggle SideBar'
            ind = html.find(Cuttof_Keyword)
        
            html = html[(ind+len(Cuttof_Keyword)):len(html)]
            data_samples.append(html)
            
            f = f + 1
            if (not max_num_files == 0) and f > max_num_files:
                break
    print('Processed',len(data_samples),'items.')
    return data_samples