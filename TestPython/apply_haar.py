from getColor import getColor2
from classifyMoth import classifyMoth
from roi_save_return import roi_save
from save_as_csv import saveDataAsCsv
from save_as_image import saveDataAsImage
import time
import os
# import dlib
import cv2
import numpy as np
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen


def haar_combined_code (id,data,sizethreshold,distance_threshold,autoSetting=False,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,imageShow=False,BugName=["1","2","3","4"],newFile=False,saveImage=False):

    each_labeled, each_data = roi_save(data,sizethreshold,distance_threshold,newFile = newFile,imageShow=imageShow)
    test_image=cv2.imread(data,cv2.IMREAD_COLOR)
    confirm_image=cv2.imread(data,cv2.IMREAD_COLOR)
    result_lst=[]
    for i in range(len(each_data)):
        test_image=confirm_image.copy()
        data=each_data[i]
        x_y=data.split(',')
        x1=int(x_y[0])
        y1=int(x_y[1])
        x_len=int(x_y[2])
        y_len=int(x_y[3])
        cv2.rectangle(test_image,(x1,y1),(x1+x_len,y1+y_len),(255,0,0),5)
        cv2.imshow("haar",test_image)
        cha=cv2.waitKey(0)      #press y: 121 if okay, n:110 if not, e:101 to edit. at the end of editing, press space: 32
        cv2.destroyAllWindows()
        if (cha==121):
            result_lst.append(data)                                 ######haar training file check and change this one as that form
            cv2.rectangle(confirm_image,(x1,y1),(x1+x_len,y1+y_len),(255,255,255),5)
        elif(cha==110):
            continue
        else:
            termination=0
            while (termination!=32):
                print("a")
            
    



haar_combined_code(id="anwls328",data="/Users/moojin/Dropbox/Codes/python/code_combining_moojin/Picture/MJPG/3_2.png",sizethreshold=300,distance_threshold=10,imageShow=False,BugName=["a","b","c","d"])