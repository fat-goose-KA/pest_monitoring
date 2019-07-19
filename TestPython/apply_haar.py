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

    each_labeled = roi_save(data,sizethreshold,distance_threshold,newFile = newFile,imageShow=imageShow)
    moth_cascade = cv2.CascadeClassifier('output.xml')
    print(len(each_labeled))
    for img in each_labeled:
        cv2.imshow("before",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        moth = moth_cascade.detectMultiScale(gray, 1.3, 2)
        for (x,y,w,h) in moth:
            print("how many?")
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex,ey,ew,eh) in eyes:
        #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        # cv2.imwrite("0718result.jpg",img)
        cv2.imshow("after",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()        

haar_combined_code(id="anwls328",data="/Users/moojin/Dropbox/Codes/python/code_combining_moojin/Picture/MJPG/3_2.png",sizethreshold=300,distance_threshold=10,imageShow=True,BugName=["a","b","c","d"])