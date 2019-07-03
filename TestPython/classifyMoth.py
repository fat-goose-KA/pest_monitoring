import cv2 
import numpy as np
import itertools
from readcsv import saveData
from readcsv import readData
from getColor import getColor





# Get Saved Moth data
fileList = ["C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata01.csv","C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata02.csv","C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata03.csv","C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata04.csv"]
dist_data_total=readData(fileList)

# Get Color from moth data
dist_avg_data_total=[]
data=getColor("C:/Users/master/Desktop/20190629/Smarf/Picture/Test/03.png",5)
newdata=np.array(data)

# Calculate the avearage of the existing data.
for dist_data in dist_data_total:
    dist_avg_data=[]
    dist_var_data=[]
    if dist_data[0]==[]:
        print("dfasd")
        break
    y = dist_data.astype(np.float)
    dist_avg_data=np.average(y,axis=0)
    avglist =[]
    # Change the scala row data to point row data
    for j in range(0,5):
        avglist.append(dist_avg_data[j*3:j*3+3])
    dist_avg_data_total.append(avglist)


# Set initial value
lowdist=1
k=0

# Set a very very high value
origin=10000000
clusterDistance=1000000000

# Calculte all combination between 5-point of exsisting average data and 5-point of new data
# Find the order of 5-point data that has the smallest distance value.
for l,r in enumerate(dist_avg_data_total):
    for i in itertools.permutations([1,2,3,4,0],5):
        distsum=0
        for j,k in enumerate(i):
            # Sum of square of distances between two points.
            distsum=distsum+np.linalg.norm(r[j]-data[k])**2
        if distsum < origin:
            origin = distsum
            bestCombn = i
    if origin < clusterDistance:
        clusterDistance=origin
        cluster=l

newdata=[]
for j in bestCombn:
    newdata.append(data[j])
saveData(newdata,cluster)

# return the meassage informing type of bug
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
