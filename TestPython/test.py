from readcsv import readData
from readcsv import saveData
from getColor import getColor2
from combined_code import classifyMoth
from finalcode import combined_code
from finalcode import combined_code_url
import csv
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl 

import numpy as np
<<<<<<< Updated upstream


a,b,c=combined_code(data="/Users/moojin/Dropbox/Codes/python/code_combining/Picture/MJPG/2019_7_4_17_0_25.jpg",sizethreshold=300,imageShow=True)
# a,b,c=combined_code_url(data_url="http://211.179.225.31:25000/?action=snapshot",sizethreshold=300,imageShow=True)

=======
  
a,b,c=combined_code(data="C:/Users/master/Desktop/Test4.jpg",autoSetting=True,sizethreshold=150,imageShow=False,sdown=40)
# def combined_code (data,sizethreshold,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
# ,Save=False,imageShow=False,NumberofType=4,BugName=["1","2","3","4"]): 
     
>>>>>>> Stashed changes
print("==========")
print(a) 
print("==========")
print(b)
print("==========")
print(c)
print("==========")

 