import os
import re
import copy
data_dir = "E:/CurAct/data/Notebooks/DATA/KB/HTMLS"
#data_dir = "E:/who/datathon/sunnystronghold/data/"
def ParseHtmlFiles():
    f = 1
    data_samples = []
    for filename in os.listdir(data_dir) :
        if filename.endswith(".html") : 
            #print(f,filename)
            html = open(data_dir + '\\' + filename,'r').read()
        
            html = re.sub(r'<.*?>', '\n', html)        
            html = re.sub(r'\n{1,}', '\n', html)

            # Cut out css and javascript
            Cuttof_Keyword = 'Toggle SideBar'
            ind = html.find(Cuttof_Keyword)
        
            html = html[(ind+len(Cuttof_Keyword)):len(html)]
            data_samples.append(html)
    ##        ind = html.find('Feedback')
    ##        html = html[0:ind]
        
#            print(html)
            
            f = f + 1
#            if f == 1000:
#                break
    print len(data_samples)
    return data_samples

#dt = ParseHtmlFiles()
#print dt
