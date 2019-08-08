from readcsv import readData
from readcsv import saveData
from getColor import getColor2
from classifyMoth import classifyMoth                                
from finalcode import combined_code
from finalcode import combined_code_id
from MakeDist import MakeDist
from MakeDist import MakeDist_id
from MakeDist import MakeDist_straight

from StabilizeDist import StabilizeDist
import csv
import itertools
import matplotlib.pyplot as plt     
import matplotlib as mpl   
import warnings                                                              
import numpy as np                                     
import os
import platform       
<<<<<<< HEAD
# "C:/Users/master/Desktop/20190629/Smarf/code_combining/Picture/Adoxophyes orana/01_13.jpg"            
# "C:/Users/master/Desktop/20190629/a.jpg"                        


warnings.filterwarnings(action="ignore", category=FutureWarning)  

                      
# a,b,c,d=combined_code(id="test",data="C:/Users/master/code_combining/Codes/5.jpg" ,thresh_size_max=50000,thresh_size_min=50,distance_threshold=15,imageShow=True,autoSetting=True,BugName=["a","b","c","d","new"],saveImage=True,newFile=True)
# print(a,b,c,d)
                                                                                                                                                                                                                                                             
                                                                                                                                         
                                  

MakeDist_id(id = "kim",clusterNum=12) 
# MakeDist_straight(clusterNum=13,data="C:/Users/master/Desktop/20190629/Blue/01.jpg")
# StabilizeDist(clusterNum =  8)
=======
                       
warnings.filterwarnings(action="ignore", category=FutureWarning)                             
                                                    
#data="C:/Users/master/Desktop/Blue/07.jpg"                                                                                                                 
# a,b,c,d=combined_code_id(id="mujin",sizethreshold=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
a,b,c,d=combined_code(id="anwls328",data="/Users/moojin/Dropbox/bugimages/5.jpg" ,thresh_size_max=5000,thresh_size_min=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
print(a,b,c,d)                                                
# MakeDist_id(id = "mujin",clusterNum=8)                                      
# MakeDist(clusterNum=8,data="C:/Users/master/Desktop/20190629/Blue/01.jpg")
>>>>>>> 4bec0db6727416b13c782b4e7bda0d01b02422d9


