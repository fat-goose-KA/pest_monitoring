from readcsv import readData
from readcsv import saveData
from getColor import getColor2
from classifyMoth import classifyMoth                                
from finalcode import combined_code
from finalcode import combined_code_id
from MakeDist import MakeDist
from MakeDist import MakeDist_id
import csv
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl 
import warnings
import numpy as np  
import os
import platform 
                       
warnings.filterwarnings(action="ignore", category=FutureWarning)                             

#data="C:/Users/master/Desktop/Blue/07.jpg"      
# a,b,c,d=combined_code_id(id="mujin",sizethreshold=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
# a,b,c,d=combined_code(id="mujin",data="C:/Users/master/Desktop/Blue/03.jpg" ,sizethreshold=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
                                                          
# MakeDist_id(id = "mujin",clusterNum=8) 
# MakeDist(clusterNum=5,data="C:/Users/master/Desktop/Blue/07.jpg")






















_file=["C:/Users/master/Desktop/20190629/Smarf/code_combining/Picture/Adoxophyes orana/", 
"C:/Users/master/Desktop/20190629/Smarf/code_combining/Picture/Archips breviplicanus/",
"C:/Users/master/Desktop/20190629/Smarf/code_combining/Picture/Carposina sasakii Matsumura/",
"C:/Users/master/Desktop/20190629/Smarf/code_combining/Picture/Grapholita molesta/"]
nlist =[]
# for _filedir in _file:
#     _dirlist=os.listdir(_filedir)
#     nsum=np.array([0,0,0,0])
#     for i in _dirlist:                                                     
#         data =_filedir+i
#         a,b,c,d=combined_code(id="anwl38",data=data,sizethreshold=500,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=False,newFile=True)
#         nsum = nsum + np.array(b)
#     nlist.append(nsum)
#     print(nlist)
# a,b,c,d=combined_code_id(id="anwls3281",sizethreshold=300,distance_threshold=10,imageShow=False)
# a,b,c=combined_code_id(data_url="http://211.179.225.31:25000/?action=snapshot",sizethreshold=300,imageShow=True)

                                                       