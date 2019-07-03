import cv2 
import numpy as np
import itertools
from readcsv import saveData
from readcsv import readData
from getColor import getColor

#New Moth data




#Get Saved Moth data
#fileList "C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata01.csv"
#"C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata02.csv"
#,"C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata03.csv"
#,"C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata04.csv"

clusterNum=0



dist_data=readData(["C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata01.csv"])
dist_data=dist_data[0]
imglist=["C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_05.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_26.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_27.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_20.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_13.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_12.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_11.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_06.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_09.jpg",
"C:/Users/master/Desktop/20190629/Smarf/Picture/Adoxophyes orana/01_22.jpg"
]
for img in imglist:
    data=getColor(img,5)
    dist_avg_data_total=[]
    newdata=np.array(data)
    dist_avg_data=[]
    print(dist_data)
    dist_avg_data.append(np.average(dist_data,axis=0))
    print(dist_avg_data)
    # for i in dist_data:
    #     if i==[[],[],[],[],[]]:
    #         print("dfasd")
    #         break

    #     x = np.array(i)
    #     y = x.astype(np.float)
    #     print(y)
    #     avg=np.average(y,axis=0)
    #     dist_avg_data.append(avg)
    dist_avg_data_total.append(dist_avg_data)
    # 모평균과 모분산을 모르는 경우에 대한 T-distribution 계산식
    lowdist=1
    k=0
    origin=10000000
    clusterDistance=1000000000
    combn=itertools.permutations([1,2,3,4,5],5)
    for i in combn:
        distsum=0
        for j,k in enumerate(i):
            print(dist_avg_data_total)
            distsum=distsum+np.linalg.norm(dist_avg_data[k]-data[j])**2
        if distsum < origin:
            origin = distsum
            bestCombn = combn
    if origin < clusterDistance:
        clusterDistance=origin
        cluster=clusterNum
    saveData(data,cluster)
        

cv2.waitKey(0)
cv2.destroyAllWindows()