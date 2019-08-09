import cv2 
import numpy as np
import csv
import os
import platform
import math
from scipy.stats import t

def distanceHSV(a,b):
    h = abs(a[0]-b[0])
    h = min(h,180-h)
    s = abs(a[1]-b[1])
    v = abs(a[2]-b[2])
    result = ((2*s*h/5)**2+(6*v)**2+(20*s/3.141592)**2)**(1/2)
    return result
# ex) clusterNum=2

# Location of Image
# ex) imglist=["C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_11.bmp",
# ex) "C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_12.bmp"]

 
# Location of Smarf Folder
# ex) direc ="C:/Users/master/Desktop/20190629/Smarf"


def StabilizeDist(clusterNum):
    strlen=len(os.getcwd())
    if clusterNum <10:
        filedir=os.getcwd()[0:strlen-6]+'/MothDataHsv/'+'Mothdata' +"0"+ str(clusterNum) + ".csv"
    else :
        filedir=os.getcwd()[0:strlen-6]+'/MothDataHsv/'+'Mothdata' + str(clusterNum) + ".csv"
    f=open(filedir,'r')
    x = csv.reader(f)
    xlist=[]
    for j in x:
        if j!=[]:
            xlist.append(j)
    f.close()

    # change the list of list to nparray
    y = np.array([xi+[None]*(15-len(xi)) for xi in xlist])
    
    dist_data = y.astype(np.float)

    dist_avg_data=[]
    if dist_data[0]==[]:
        print("Empty Distribution")
        return 
    dist_avg_data=np.average(dist_data,axis=0)
    avglist =[]
    # Change the scala row data to point row data
    for j in range(0,5):
        avglist.append(dist_avg_data[j*3:j*3+3])

    varlist=[]
    numlist=[]
    for k in range(0,5):
        csum = 0
        for j in dist_data:
            csum = csum + distanceHSV(j[k*3:k*3+3], avglist[k])**2
        csize = dist_data.size/15
        cvar = (csum/(csize-1))**0.5
        varlist.append(cvar)
        numlist.append(csize)
    delete=[]
    for i,j in enumerate(dist_data):
        pLogSum=0
        for k in range(0,5):
            x1 = avglist[k]
            x2 = j[k*3:(k+1)*3]
            s1 = varlist[k]
            n1 = numlist[k]
            Tvalue = distanceHSV(x1,x2)/(s1*s1/n1)**0.5
            dF = n1-1
            
            pvalue = t.sf(Tvalue, dF)
            if pvalue != 0:
                plog = -math.log(pvalue)
            else :
                plog = 308
            # Sum of square of distances between two points.\
            if plog >20:
                pLogSum=200
            pLogSum = pLogSum + plog
            print(plog)
        if pLogSum>200:
            delete.append(i)
    delete.reverse()
    for i in delete:
        dist_data = np.delete(dist_data,i,axis=0)

    filedir=os.getcwd()[0:strlen-6]+'/MothDataHsv/'+'Mothdata' +"0"+ str(clusterNum) + ".csv"
    if platform.system() == "Windows":
        f=open(filedir, 'w',newline='')
    else:
        f=open(filedir, 'w')
    wr = csv.writer(f)
    # Conver the data to one row data.
    output=[]
    for i in dist_data:
        wr.writerow(i)
    

    f.close()   