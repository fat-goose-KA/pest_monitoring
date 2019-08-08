import cv2 
import numpy as np
import itertools
from getColor import getColor2
from classifyMoth import classifyMoth
from classifyMoth import classifyMoth_distance
from roi_save_return import roi_save
from roi_save_return import roi_save_new
from roi_save_return import roi_save_new_general
from save_as_csv import saveDataAsCsv
from save_as_image import saveDataAsImage
from readcsv import saveData
from readcsv import readData
from sklearn.cluster import KMeans
import time
import os
import platform
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen

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

def id_to_ip(id):
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=os.getcwd()[0:strlen-6]+'/Client_data/'
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


def MakeDist(clusterNum,data,hlist=[[0,180]],thresh_size_max=5000,thresh_size_min=100,sup=254,sdown=1,vup=254,vdown=1):

    dirName=os.getcwd()
    strlen=len(dirName)
    dirName = dirName[0:strlen-6]
    if platform.system() == "Windows":
        dirName=  dirName.replace("\\","/")
    # Change the direcoty to real directory of data
    if clusterNum<10:
        directory = dirName + "/MothData/MothData" + "0" + str(clusterNum) + ".csv"
    else :
        directory = dirName + "/MothData/MothData" + str(clusterNum) + ".csv"
    
    # Set the initial variable
    dist_avg_data=[]

    each_labeled, imgs = roi_save_new_general(data,thresh_size_max= thresh_size_max ,thresh_size_min= thresh_size_min, distance_threshold=10,imageShow = False,newFile = True)


    datalist, deletenum= getColor2(each_labeled,distance_threshold=10,imageShow = False, autoSetting=True,sup=sup,sdown=sdown,vup=vup,vdown=vdown)




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
    filedir=filedir[0:strlen-6]
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

    
def MakeDist_straight(clusterNum,data,hlist=[[0,180]],thresh_size_max=5000,thresh_size_min=100,sup=254,sdown=1,vup=254,vdown=1):

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
    img_file = data
    im_in = cv2.imread(img_file, cv2.IMREAD_COLOR)
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')

    img_YUV = cv2.cvtColor(im_in, cv2.COLOR_BGR2YUV)
    y = img_YUV[:,:,0]    
    
    rows = y.shape[0]    
    cols = y.shape[1]
    
    ### illumination elements reflectance elements
    imgLog = np.log1p(np.array(y, dtype='float') / 255) # 
    
    M = 2*rows + 1
    N = 2*cols + 1
    sigma = 10
    (X, Y) = np.meshgrid(np.linspace(0, N-1, N), np.linspace(0, M-1, M)) 
    Xc = np.ceil(N/2) 
    Yc = np.ceil(M/2)
    gaussianNumerator = (X - Xc)**2 + (Y - Yc)**2 
    
    LPF = np.exp(-gaussianNumerator / (2*sigma*sigma))
    HPF = 1 - LPF
    
    LPF_shift = np.fft.ifftshift(LPF.copy())
    HPF_shift = np.fft.ifftshift(HPF.copy())
    img_FFT = np.fft.fft2(imgLog.copy(), (M, N))
    img_LF = np.real(np.fft.ifft2(img_FFT.copy() * LPF_shift, (M, N)))
    img_HF = np.real(np.fft.ifft2(img_FFT.copy() * HPF_shift, (M, N)))
    
    gamma1 = 0.3
    gamma2 = 1.5
    img_adjusting = gamma1*img_LF[0:rows, 0:cols] + gamma2*img_HF[0:rows, 0:cols]
    
    img_exp = np.expm1(img_adjusting) # exp(x) + 1
    img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp))
    img_out = np.array(255*img_exp, dtype = 'uint8') 
    
    img_YUV[:,:,0] = img_out
    result = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    height, width, channels =result.shape
    average=[]
    total=height*2+width*2-4
    color =[]
    for i in range(0,height):
        color.append( result[i][0])
        color.append( result[i][width-1])
    for i in range(0,width):
        color.append( result[0][i])
        color.append( result[height-1][i])
    color = np.array(color)
    maxrgb=np.median(color,axis=0)
    r= maxrgb[2]
    g= maxrgb[1]
    b= maxrgb[0]
    Cmax = max(r,g,b)
    Cmin = min(r,g,b)
    delta = Cmax-Cmin
    if delta ==0:
        mh=0
    elif Cmax==r:
        mh=30*(((g-b)/delta)%6)
    elif Cmax==g:
        mh=30*((b-r)/delta+2)
    elif Cmax==b:
        mh=30*((r-g)/delta+4)
    
    if Cmax==0:
        ms=0
    else:
        ms=delta/Cmax*255

    mv=Cmax

    print(mh,ms,mv)
    # print("++++++++++++++++changed h,s,v+++++++++++++++")

    sdown = ms - 20
    vdown = mv - 20
    sup = ms + 20
    vup = mv + 20
    # hsv eliminate blue one
    mask = cv2.inRange(v,vup,255) + cv2.inRange(v,0,vdown)
    mask2 = cv2.inRange(s,sup,255) + cv2.inRange(s,0,sdown)
    mask3 = cv2.inRange(h,mh+8,180)+ cv2.inRange(h,0,mh-8)
    res = cv2.bitwise_and(gray, gray, mask=mask)
    res = cv2.bitwise_and(res, res, mask=mask2)
    bgr = cv2.bitwise_and(res, res, mask=mask3)
    
    # cv2.imshow("realrealreal", bgr)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # fill the blank and delete noise
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(bgr, cv2.MORPH_CLOSE, kernel)    
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    th, im_otsu = cv2.threshold(opening, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    rgb = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

    # Reshape for applying Kmean function to the image.
    im_otsu = im_otsu.reshape(im_otsu.shape[0] * im_otsu.shape[1], 1)
    rgb = rgb.reshape(rgb.shape[0] * rgb.shape[1], 3)
    # The masked area has v==0 for HSV value
    k=0
    bdelete = []
    for i in im_otsu:
        if i[0]==0:

            # Find the Black point and append in bdelete list
            bdelete.append(k)
        k=k+1

    #Delete the Masked area from the image.
    rgb2=np.delete(rgb, bdelete,0)

    # Calculate the Color Clusters of Image by the KMeans Class.
    clt = KMeans(n_clusters = 5)
    clt.fit(rgb2)



    # If the file is empty, Write the data in the first row.
    if not (os.path.exists(directory)):
        saveData(clt.cluster_centers_,clusterNum)
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
                distsum=distsum+distanceHSV(avglist[j],clt.cluster_centers_[k])
            if distsum < clusterDistance:
                clusterDistance = distsum
                bestCombn = i
        newdata=[]
        for j in bestCombn:
            newdata.append(clt.cluster_centers_[j])

        # Save the data with the right order in the csv file.
        saveData(newdata,clusterNum)