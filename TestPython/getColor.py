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

            if ms<40:
                sdown = min(ms+10,40)
            elif ms>220:
                sup = max(ms-10,220)
            if mv<40:
                vdown = min(mv+10,40)
            elif mv>220:
                vup = max(mv-10,220)
        # print("")
        # print(hlist, sdown,sup,vdown,vup)
        # print("")

        mask = cv2.inRange(v,vdown,vup)
        mask2 = cv2.inRange(s,sdown,sup)
        mask3 = cv2.inRange(h,0,180)
        for i in hlist:
            mask3 = mask3 + cv2.inRange(h,i[0],i[1])

        res = cv2.bitwise_and(src, src, mask=mask)
        res = cv2.bitwise_and(res, res, mask=mask2)
        bgr = cv2.bitwise_and(res, res, mask=mask3)

        # openCV get a image as a BGR format
        # Convert the image to RGB format
        if imageShow==True:
            cv2.imshow("letmesee",bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()     #for check whether filtering has proccessed well

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        # Reshape for applying Kmean function to the image.
        rgb = rgb.reshape(rgb.shape[0] * rgb.shape[1], 3)

        # The masked area has (0,0,0) RGB value
        blackPoint= np.array([0,0,0])
        k=0
        bdelete = []
        for i in rgb:
            if np.array_equal(i,blackPoint):

                # Find the Black point and append in bdelete list
                bdelete.append(k)
            k=k+1

        #Delete the Masked area from the image.
        rgb2=np.delete(rgb, bdelete,0)

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
        bar = plot_colors(hist, clt.cluster_centers_)
        
        if imageShow==True:
            plts.figure()
            plts.axis("off")
            plts.imshow(bar)
            plts.show()

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
            cvar = csum/(csize-1)
            cluster_var.append(cvar)
        
        resultData = [clt.cluster_centers_,cluster_var,cluster_num]
        
        result.append(resultData)


    return result    