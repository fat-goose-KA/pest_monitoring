import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plts
import time

from roi_save_return import roi_save


def distanceHSV(a,b):
    h = abs(a[0]-b[0])
    h = min(h,180-h)
    s = abs(a[1]-b[1])
    v = abs(a[2]-b[2])
    result = ((4*s*h/5)**2+(6*v)**2+(20*s/3.141592)**2)**(1/2)
    return result

def getColor2(data,distance_threshold,imageShow,autoSetting=False,clusterNum=5,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1):
    result=[]
    deletenum=[]
    for num,src in enumerate(data):
        # src = np.float32(src)
        # Check the initial time
        start = time.time() 
        # Read the data from the directory named data.
        # Convert the image to hsv format.
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)

        # Mask the image by hsv input condition
        # v and s has one interval 
        # h has sevral interval and it returns the union of the interval. 
        if autoSetting == True:
            height, width, channels =src.shape
            average=[]
            total=height*2+width*2-4
            color =[]
            for i in range(0,height):
                color.append( src[i][0])
                color.append( src[i][width-1])
            for i in range(0,width):
                color.append( src[0][i])
                color.append( src[height-1][i])
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


            sdown = ms - 10
            vdown = mv - 10
            sup = ms + 10
            vup = mv + 10
            hlist = [[mh-8,mh+8]]
        mask = cv2.inRange(v,vup,255) + cv2.inRange(v,0,vdown)
        mask2 = cv2.inRange(s,sup,255) + cv2.inRange(s,0,sdown)
        mask3 = cv2.inRange(h,0,92)+ cv2.inRange(h,108,180)
        for i in hlist:
            mask3 = mask3 + cv2.inRange(h,0,i[0])+ cv2.inRange(h,i[1],180)
        
        res = cv2.bitwise_and(src, src, mask=mask)
        res = cv2.bitwise_and(res, res, mask=mask2)
        bgr = cv2.bitwise_and(res, res, mask=mask3)
        gray = cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)

        if imageShow == True:
            cv2.imshow('bgr',bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # openCV get a image as a BGR format
        # Convert the image to RGB format
        # for check whether filtering has proccessed well

        kernel = np.ones((2,2),np.uint8)
        closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)    
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        # Reshape for applying Kmean function to the image.
        rgb = rgb.reshape(rgb.shape[0] * rgb.shape[1], 3)
        gray = gray.reshape(gray.shape[0] * gray.shape[1],1)
        # The masked area has v==0 for HSV value
        k=0
        bdelete = []
        for i in gray:
            if i[0]==0:

                # Find the Black point and append in bdelete list
                bdelete.append(k)
            k=k+1

        #Delete the Masked area from the image.
        rgb2=np.delete(rgb, bdelete,0)
        if len(rgb2)<5:
            deletenum.append(num)
            continue
        # The number of cluster is 5
        clusterNum = 5 

        # Calculate the Color Clusters of Image by the KMeans Class.
        clt = KMeans(n_clusters = clusterNum)
        clt.fit(rgb2)
        centers = []

        clusterData=[]
        cltnum=0
        breaking = False
        for i in range(0,clusterNum):
            clusterData.append(rgb2[clt.labels_==i])
            if len(rgb2[clt.labels_==i])==0:
                breaking = True
        if breaking ==True:
            deletenum.append(num)
            continue
        cluster_num=[]
        cluster_var=[]
        for i,j in enumerate(clusterData):
            csize = j.size/3
            cluster_num.append(csize)
            csum=0
            ccenter=clt.cluster_centers_[i]
            for k in j:
                csum = csum + distanceHSV(ccenter,k)**2
            cvar = (csum/(csize-1))**0.5
            cluster_var.append(cvar)
        
        resultData = [clt.cluster_centers_,cluster_var,cluster_num]
        
        result.append(resultData)


    return result,deletenum