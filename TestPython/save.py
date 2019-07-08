import datetime 
import csv
import os
import platform
import numpy as np
import cv2

def saveDataAsImage(imageData, clusterData, bugName):
     # Find or create a csv file
    bugName.sort()
    now = datetime.datetime.now()


    fileDir=os.getcwd()
    strlen=len(fileDir)
    print(fileDir)
    print(os.getcwd()[0:strlen])
    nowTime = now.strftime('%m-%d %H-%M-%S')    
    fileDir=os.getcwd()[0:strlen-11]+'/ImageData/' +nowTime
    if platform.system() == "Windows":
        fileDir=  fileDir.replace("\\","/")

    
    if not os.path.exists(fileDir):
        os.mkdir(fileDir)

    dirList = []
    for i in bugName:
        dirName = fileDir +"/" + i 
        dirList.append(dirName)
    dirName=fileDir+"/NonPest"
    dirList.insert(0,dirName)

    for i in dirList:
        os.mkdir(i)
    
    clusterData=list(map(int, clusterData))
    for i,j in enumerate(imageData):
        clusterNum = clusterData[i]
        if clusterNum == -1:
            clusterNum = 0 
        fullPath =dirList[clusterNum]+"/"+str(i)+".jpg"
        print(fullPath)
        cv2.imwrite(fullPath,j)

# im1 = cv2.imread("/Users/master/Desktop/test.jpg")
# im2 = cv2.imread("/Users/master/Desktop/test2.jpg")
# im3 = cv2.imread("/Users/master/Desktop/test3.jpg")
# im4 = cv2.imread("/Users/master/Desktop/test4.jpg")
# imglist = [im1,im2,im3,im4]
# clusterData = [3,2,1,-1]
# saveDataAsImage(imglist, clusterData, ["a","b","c","d","e","f"])