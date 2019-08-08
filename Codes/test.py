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
                       
warnings.filterwarnings(action="ignore", category=FutureWarning)                             
                                                    
#data="C:/Users/master/Desktop/Blue/07.jpg"                                                                                                                 
# a,b,c,d=combined_code_id(id="mujin",sizethreshold=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
a,b,c,d=combined_code(id="anwls328",data="C:/Users/master/Desktop/20190629/Blue/01.jpg" ,thresh_size_max=5000,thresh_size_min=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
print(a,b,c,d)                                                
# MakeDist_id(id = "mujin",clusterNum=8)                                      
# MakeDist(clusterNum=8,data="C:/Users/master/Desktop/20190629/Blue/01.jpg")


