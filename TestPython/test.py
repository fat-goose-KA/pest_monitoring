from readcsv import readData
from readcsv import saveData
from getColor import getColor
import csv
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np

# data=getColor("C:/Users/master/Desktop/20190629/Smarf/Picture/Test/03.png",5)
# print(data)
# readData(["C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata01.csv"])
# print(data)
for i in itertools.permutations([1,2,3,4,0],5):
    for j,k in enumerate(i):
        print (j,k)