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
# "C:/Users/master/Desktop/20190629/Smarf/code_combining/Picture/Adoxophyes orana/01_13.jpg"            
# "C:/Users/master/Desktop/20190629/a.jpg"                        


warnings.filterwarnings(action="ignore", category=FutureWarning)  

                      
# a,b,c,d=combined_code(id="test",data="C:/Users/master/code_combining/Codes/5.jpg" ,thresh_size_max=50000,thresh_size_min=50,distance_threshold=15,imageShow=True,autoSetting=True,BugName=["a","b","c","d","new"],saveImage=True,newFile=True)
# print(a,b,c,d)
                                                                                                                                                                                                                                                             
                                                                                                                                         
                                  

MakeDist_id(id = "kim",clusterNum=12) 
# MakeDist_straight(clusterNum=13,data="C:/Users/master/Desktop/20190629/Blue/01.jpg")
# StabilizeDist(clusterNum =  8)


