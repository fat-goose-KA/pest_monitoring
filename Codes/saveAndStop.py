from finalcode import combined_code
from finalcode import combined_code_id
from MakeDist import MakeDist
from MakeDist import MakeDist_id
import os
import time
import numpy as np
import cv2
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen

url="http://192.168.0.145:8000/camera/jpeg"
end = 'taskkill /f /im cam2web.exe' 
num = 0


while True:

    # a,b,c,d=combined_code_id(id="mujin",sizethreshold=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True)
    # a,b,c,d=combined_code(id="mujin",data="C:/Users/master/Desktop/Blue/03.jpg" ,sizethreshold=100,distance_threshold=10,imageShow=False,autoSetting=True,BugName=["a","b","c","d"],saveImage=True,newFile=True) 
    MakeDist_id(id = "mujin",clusterNum=8) 

    os.system(end)
    num = num+1
    time.sleep(15)
    