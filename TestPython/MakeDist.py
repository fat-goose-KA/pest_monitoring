import cv2 
import numpy as np
import itertools
from readcsv import saveData
from readcsv import readData
from getColor import getColor


# 분석한 이미지 곤충 종류의 Number
# ex) 복숭아 순나방의 경우 0번.
# ex) clusterNum=2

# 저장하고 싶은 이미지들의 리스트
# ex) imglist=["C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_11.bmp",
# ex) "C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_12.bmp"]

 
# 스마프 파일이 저장된 위치
# ex) direc ="C:/Users/master/Desktop/20190629/Smarf"


def MakeDist(clusterNum,imglist,direc,hlist=[[0,180]],sup=255,sdown=0,vup=255,vdown=0):
    # Change the direcoty to real directory of data
    if clusterNum<10:
        directory=direc+"/MothData/BugData"+"0"+str(clusterNum+1)+ ".csv"
    else :
        directory=direc+"/MothData/BugData"+str(clusterNum+1)+ ".csv"
    
    print(directory)
    # Set the test variable
    directory="C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata03.csv"
    clusterNum=2
    imglist=["C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_11.bmp"]
        
    # Set the initial variable
    dist_avg_data=[]

    # Loop for each image.
    for img in imglist:

        # Read the existing bug data from directory.
        dist_data=readData([directory])

        # If the file is empty, Write the data in the first row.
        if dist_data == []:
            saveData(getColor(img,5),clusterNum)
            break

        # Calculate the average of existing data.
        dist_data=dist_data[0]
        y = dist_data.astype(np.float)
        dist_avg_data = (np.average(y,axis=0))
        avglist=[]
        
        # Change the scala row data to point row data
        for j in range(0,5):
            avglist.append(dist_avg_data[j*3:j*3+3])
        
        # Set initial value
        lowdist=1
        k=0
        combn=itertools.permutations([1,2,3,4,0],5)
        sumlist=[]

        # Set a very very high value
        origin=1000000000
        clusterDistance=1000000000

        # Get the RGB value data from the image by getColor function
        data=getColor(img,5,hlist,sup,sdown,vup,vdown)

        # Calculte all combination between 5-point of exsisting average data and 5-point of new data
        # Find the order of 5-point data that has the smallest distance value.
        for i in combn:
            distsum=0
            for j,k in enumerate(i):
                # Sum of square of distances between two points.
                distsum=distsum+np.linalg.norm(avglist[j]-data[k])**2
            if distsum < origin:
                origin = distsum
                bestCombn = i
            sumlist.append(distsum)
        newdata=[]
        for j in bestCombn:
            newdata.append(data[j])

        # Save the data with the right order in the csv file.
        saveData(newdata,clusterNum)
        