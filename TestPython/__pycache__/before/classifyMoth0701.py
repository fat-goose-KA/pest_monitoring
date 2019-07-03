import cv2 
import numpy as np
import itertools
from readcsv import saveData
from readcsv import readData
from getColor import getColor

#New Moth data




#Get Saved Moth data
fileList = ["C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata01.csv","C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata02.csv","C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata03.csv","C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata04.csv"]
dist_data_total=readData(fileList)
dist_avg_data_total=[]
data=getColor("C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_05.jpg",5)
newdata=np.array(data)
for dist_data in dist_data_total:
#dist_data = [[[1,2,3],[2,3,4],[5,3,2],[5,3,1]],[[1,2,3],[2,3,4],[5,3,2]],[[1,2,3],[2,3,4],[5,3,2]],[[1,2,3],[2,3,4],[5,3,2]],[[1,2,3],[2,3,4],[5,3,2]]]
    dist_avg_data=[]
    dist_var_data=[]
    for i in dist_data:
        if i==[[],[],[],[],[]]:
            print("dfasd")
            break
        print("=================")
        print(i)
        print("=================")

        x = np.array(i)
        y = x.astype(np.float)
        avg=np.average(y,axis=0)
        dist_avg_data.append(avg)
        # varsum=0
        # for j in i:
        #     varsum=varsum+ (j[0]-avg[0])**2+(j[1]-avg[1])**2+(j[2]-avg[2])**2 
        # var=varsum/(np.size(i,axis=0)-1)
        # dist_var_data.append(var)
    dist_avg_data_total.append(dist_avg_data)
    print(dist_avg_data)
# 모평균과 모분산을 모르는 경우에 대한 T-distribution 계산식
lowdist=1
k=0
origin=10000000
clusterDistance=1000000000
combn=itertools.permutations([1,2,3,4,5],5)
for l,r in enumerate(dist_avg_data_total):
    for i in combn:
        distsum=0
        for j,k in enumerate(i):
            distsum=distsum+np.linalg.norm(r[k]-data[j])**2
        if distsum < origin:
            origin = distsum
            bestCombn = combn
    if origin < clusterDistance:
        clusterDistance=origin
        cluster=l
saveData(data,cluster)

if(cluster==0):
    print("This moth is ~~~1")
elif(cluster==1):
    print("This moth is ~~~2")
elif(cluster==2):
    print("This moth is ~~~3")
elif(cluster==3):
    print("This moth is ~~~4")
    

cv2.waitKey(0)
cv2.destroyAllWindows()
