from readcsv import readData
from readcsv import saveData
from getColor import getColor2
from combined_code import classifyMoth
from finalcode import combined_code
import csv
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl 

import numpy as np


a,b,c=combined_code(data="C:/Users/master/Desktop/Test2.jpg",sizethreshold=300,imageShow=True)


print("==========")
print(a)
print("==========")
print(b)
print("==========")
print(c)
print("==========")

 