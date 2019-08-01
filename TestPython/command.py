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
import sys
import platform 
import csv
import platform
import numpy as np
                       
warnings.filterwarnings(action="ignore", category=FutureWarning)    
##sys input:: python ~.py new id
if (len(sys.argv)<4):
    print("please write option and your id")
else:
    if (sys.argv[2]=="new"):
        a,b,c,d=combined_code_id(id=sys.argv[3],sizethreshold=500,distance_threshold=30,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=False)
    elif (sys.argv[2]=="total"):
        a,b,c,d=combined_code_id(id=sys.argv[3],sizethreshold=500,distance_threshold=30,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
    elif(sys.argv[2]=="log"):
        filedir='d'
        f=open(filedir,"r")
        x = csv.reader(f)
        xlist=[]
        for j in x:
            if j!=[]:
                xlist.append(j)        