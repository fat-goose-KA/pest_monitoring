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


a,b,c=combined_code(data="/Users/moojin/Dropbox/Codes/python/code_combining/Picture/MJPG/2019_7_4_17_0_25.jpg",sizethreshold=300,imageShow=True)
# a,b,c=combined_code_url(data_url="http://211.179.225.31:25000/?action=snapshot",sizethreshold=300,imageShow=True)

print("==========")
print(a)
print("==========")
print(b)
print("==========")
print(c)
print("==========")

 