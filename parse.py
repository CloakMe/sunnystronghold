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
            string_buffer = ''
            #data_samples.append(html)

            # Get everything up until the Language
            data_arr = html.split('\n')
            di = 1
            Stop_Writing = 0
        
            for d in data_arr :

                if 'Request a Product Feature' in d :
                    Stop_Writing = 1

                if Stop_Writing == 0 :
                    #file.write(d + '\n')
                    string_buffer = string_buffer + d + '\n'            
                if 'Language :' in d :
                    Lang = data_arr[di]
                    break
                di = di + 1        

            # Keep only English files 
            if Lang == 'English' :
                data_samples.append(string_buffer) 
                       
            f = f + 1
            if (not max_num_files == 0) and f > max_num_files:
                break
    print('Processed',len(data_samples),'items.')
    return data_samples

#dt = ParseHtmlFiles()
#print dt[0]