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
import time

#a,b,c=combined_code(data="/Users/moojin/Dropbox/Codes/python/code_combining_mo$
for i in range(10):
        sleep(600)
        a,b,c=combined_code_url(id="anwls328",sizethreshold=300,imageShow=True)