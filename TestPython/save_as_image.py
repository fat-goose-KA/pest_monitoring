import datetime 
import csv
import os
import platform
import numpy as np
import cv2

def saveDataAsImage(id,imageData, clusterData, bugName):
     # Find or create a csv file
    bugName.sort()
    now = datetime.datetime.now()


    fileDir=os.getcwd()
    strlen=len(fileDir)
    print(os.getcwd()[0:strlen])
    nowTime = now.strftime('%m-%d %H-%M-%S')    
    fileDir=os.getcwd()[0:strlen-11]+'/Client_data/'+id+'/ImageData'
    if platform.system() == "Windows":
        fileDir=  fileDir.replace("\\","/")

    
    if not os.path.exists(fileDir):
        print(fileDir)
        os.mkdir(fileDir)
    
    fileDir = fileDir + '/' +nowTime
    os.mkdir(fileDir)
    
    bugName.remove('Time')
    dirList = []
    for i in bugName:
        dirName = fileDir +"/" + i 
        dirList.append(dirName)
    dirName=fileDir+"/NonPest"
    dirList.insert(0,dirName)
    for i in dirList:
        os.mkdir(i)
    
    clusterData=list(map(int, clusterData))
    print("------------")
    print(dirList)
    print("------------")
    for i,j in enumerate(imageData):
        clusterNum = clusterData[i]
        if clusterNum == -1:
            clusterNum = 0 
        fullPath =dirList[clusterNum]+"/"+str(i)+".jpg"
        print(clusterNum,fullPath)

        cv2.imwrite(fullPath,j)
