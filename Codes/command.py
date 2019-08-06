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
#/Users/moojin/Dropbox/Codes/python/code_combining/TestPython
def read(length):
    dirName=os.getcwd()
    strlen=len(dirName)
    dirName = dirName[0:strlen-6]+'/Client_data/'+sys.argv[2]+'/TimeData/'
    dirlist=os.listdir(dirName)
    last_file=dirlist[0]
    f=open(dirName+last_file,"r")
    x = csv.reader(f)
    xlist=[]
    for j in x:
        if j!=[]:
            xlist.append(j)
    f.close()
    print(dirlist)
    print(last_file)
    print(xlist)


warnings.filterwarnings(action="ignore", category=FutureWarning)    
##sys input:: python ~.py new id
print(sys.argv)
if (len(sys.argv)<3):
    print("please write option and your id")
else:
    if (sys.argv[1]=="new"):
        read(1)
    elif (sys.argv[1]=="total"):
        read(5)