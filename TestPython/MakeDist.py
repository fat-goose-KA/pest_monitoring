import cv2 
import numpy as np
import itertools
from getColor import getColor2
from classifyMoth import classifyMoth
from classifyMoth import classifyMoth_distance
from roi_save_return import roi_save
from roi_save_return import roi_save_new
from save_as_csv import saveDataAsCsv
from save_as_image import saveDataAsImage
from readcsv import saveData
from readcsv import readData
import time
import os
import platform
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen

def distanceHSV(a,b):
    h = abs(a[0]-b[0])
    s = abs(a[1]-b[1])
    v = abs(a[2]-b[2])
    result = ((2*s*h/5)**2+(6*v)**2+(20*s/3.141592)**2)**(1/2)
    return result
# 분석한 이미지 곤충 종류의 Number
# ex) 복숭아 순나방의 경우 0번.
# ex) clusterNum=2

# 저장하고 싶은 이미지들의 리스트
# ex) imglist=["C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_11.bmp",
# ex) "C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_12.bmp"]

 
# 스마프 파일이 저장된 위치
# ex) direc ="C:/Users/master/Desktop/20190629/Smarf"

def id_to_ip(id):
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=os.getcwd()[0:strlen-11]+'/Client_data/'
    txt_name='client_data.txt'
    
    try:
        dirName = filedir+txt_name
        

        if platform.system() == "Windows":
            dirName=  dirName.replace("\\","/")
        f = open(dirName, 'r')
        lines=f.readlines()
        old_id_list=[]
        old_ip_list=[]
        for i in lines:
            # print(i)
            before_list=i.split('\n')
            # print(before_list)
            before_list=before_list[0].split('\t')  
            # print(before_list)
            if (before_list[0]==id):
                f.close()
                return before_list[1]
        f.close()
        return None
    except:
        return None

def id_to_image(id):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
    # try: #python3
    #     resp = urlopen(url)
    # except: #python2
    #     resp = urlopen(url)    
    try:
        ip=id_to_ip(id)
        if ip is None:
            print("wrong ip address")
        # url = "http://"+ip+"/?action=snapshot"
        url = "http://"+ip+"camera/jpeg"
        resp=urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
        return image
    except:
        raise NameError('incorrect url. Double check it')


def MakeDist(clusterNum,data,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1):

    dirName=os.getcwd()
    strlen=len(dirName)
    dirName = dirName[0:strlen-11]
    if platform.system() == "Windows":
        dirName=  dirName.replace("\\","/")
    # Change the direcoty to real directory of data
    if clusterNum<10:
        directory = dirName + "/MothData/MothData" + "0" + str(clusterNum) + ".csv"
    else :
        directory = dirName + "/MothData/MothData" + str(clusterNum) + ".csv"
    
    # Set the initial variable
    dist_avg_data=[]

    each_labeled, imgs = roi_save_new(data,300,10,imageShow = False,newFile = True)


    datalist = getColor2(each_labeled,sizethreshold=300,distance_threshold=10,imageShow = False, autoSetting=True,sup=sup,sdown=sdown,vup=vup,vdown=vdown)




    # Loop for each image.
    for data in datalist:
        # If the file is empty, Write the data in the first row.
        if not (os.path.exists(directory)):
            saveData(data[0],clusterNum)
        else:
            # Read the existing bug data from directory.
            dist_data=readData([directory])

            
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

            # Calculte all combination between 5-point of exsisting average data and 5-point of new data
            # Find the order of 5-point data that has the smallest distance value.
            for i in itertools.permutations([1,2,3,4,0],5):
                distsum=0
                for j,k in enumerate(i):
                    # Sum of square of distances between two points.
                    distsum=distsum+distanceHSV(avglist[j],data[0][k])
                if distsum < clusterDistance:
                    clusterDistance = distsum
                    bestCombn = i
            newdata=[]
            for j in bestCombn:
                newdata.append(data[0][j])

            # Save the data with the right order in the csv file.
            saveData(newdata,clusterNum)
        
def MakeDist_id(clusterNum,id,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1):
    data=id_to_image(id)
    now=time.localtime()

    outputFileName =str(now.tm_year)+"_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)+"."+ "jpg"
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=filedir[0:strlen-11]
    filedir=filedir+'/Client_data/'+id
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filedir=filedir+'/Picture/'
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filedir=filedir+'MJPG/'
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filedir=filedir +outputFileName

    cv2.imwrite(filedir, data)
    print("befores")
    MakeDist(clusterNum,filedir,hlist,sup,sdown,vup,vdown)