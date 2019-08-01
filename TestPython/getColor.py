import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plts
from callee import roi
import time

from roi_save_return import roi_save

def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist

def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar 

def getColor2(data,sizethreshold,distance_threshold,imageShow,autoSetting=False,clusterNum=5,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1):
    result=[]
    
    for src in data:
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

            # print(mh,ms,mv)
            # print("++++++++++++++++changed h,s,v+++++++++++++++")

            hlist = [[mh+3,mh-3]]

            sdown = ms - 5
            vdown = mv - 5
            sup = ms + 5
            vup = mv + 5
        # print("")
        # print(hlist, sdown,sup,vdown,vup)
        # print("")
        # mask = cv2.inRange(v,1,254)
        # mask2 = cv2.inRange(s,1,254)
        mask3_up = cv2.inRange(h,125,180)
        mask3_down = cv2.inRange(h,0,80)
        mask3 = (mask3_up+mask3_down)
        mask = cv2.inRange(v,vup,255) + cv2.inRange(v,0,vdown)
        mask2 = cv2.inRange(s,sup,255) + cv2.inRange(s,0,sdown)
        for i in hlist:
            mask3 = mask3 + cv2.inRange(h,i[0],i[1])

        res = cv2.bitwise_and(src, src, mask=mask)
        res = cv2.bitwise_and(res, res, mask=mask2)
        bgr = cv2.bitwise_and(res, res, mask=mask3)

        if imageShow == True:
            cv2.imshow('bgr',bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # openCV get a image as a BGR format
        # Convert the image to RGB format
        #for check whether filtering has proccessed well

        # kernel = np.ones((2,2),np.uint8)
        # closing = cv2.morphologyEx(bgr, cv2.MORPH_CLOSE, kernel)    
        # opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        # if imageShow == True:
        #     cv2.imshow('bgr',opening)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
        # bgr = opening

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        # Reshape for applying Kmean function to the image.
        rgb = rgb.reshape(rgb.shape[0] * rgb.shape[1], 3)
        # The masked area has v==0 for HSV value
        k=0
        bdelete = []
        for i in rgb:
            if i[2]==0:

                # Find the Black point and append in bdelete list
                bdelete.append(k)
            k=k+1

        #Delete the Masked area from the image.
        rgb2=np.delete(rgb, bdelete,0)
        if len(rgb2)<5:
            rgb2=np.array([[0,0,0],[1,1,1],[1,0,0],[0,1,0],[0,0,1]])
        # The number of cluster is 5
        clusterNum = 5 

        # Calculate the Color Clusters of Image by the KMeans Class.
        clt = KMeans(n_clusters = clusterNum)
        clt.fit(rgb2)

        #Represent the time to finish the clustering
        # print("time - clustering is finished :", time.time() - start)
        centers = []


        # # show our color bart
        hist = centroid_histogram(clt)
        # bar = plot_colors(hist, clt.cluster_centers_)
        
        # if imageShow==True:
        #     plts.figure()
        #     plts.axis("off")
        #     plts.imshow(bar)
        #     plts.show()

        clusterData=[]
        
        for i in range(0,clusterNum):
            clusterData.append(rgb2[clt.labels_==i])

        cluster_num=[]
        cluster_var=[]
        for i,j in enumerate(clusterData):
            csize = j.size/3
            cluster_num.append(csize)
            csum=0
            ccenter=clt.cluster_centers_[i]
            for k in j:
                csum = csum + np.linalg.norm(ccenter-k)**2
            cvar = (csum/(csize-1))**0.5
            cluster_var.append(cvar)
        
        resultData = [clt.cluster_centers_,cluster_var,cluster_num]
        
        result.append(resultData)


    return result    