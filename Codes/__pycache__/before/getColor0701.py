import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plts
import time

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


def getColor(data,clusterNum,hup=180,hdown=0,sup=255,sdown=0,vup=255,vdown=0):
    start = time.time() 
    src = cv2.imread(data, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    mask = cv2.inRange(v,0,250)
    bgr = cv2.bitwise_and(src, src, mask=mask)

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    rgb = rgb.reshape(rgb.shape[0] * rgb.shape[1], 3)
    k=0
    bdelete = []
    list1= np.array([0,0,0])
    print("time :", time.time() - start)
    for i in rgb:
        if np.array_equal(i,list1):
            bdelete.append(k)
        k=k+1
    rgb2=np.delete(rgb, bdelete,0)
    print(rgb2.size)
    print("time1 :", time.time() - start)
    clusterNum = 5 # 예제는 5개로 나누겠습니다
    clt = KMeans(n_clusters = clusterNum)
    clt.fit(rgb2)
    print("time2 :", time.time() - start)
    centers = []
    for center in clt.cluster_centers_:
        print(center)
    print("time3 :", time.time() - start)
    hist = centroid_histogram(clt)
    print(hist)    
    bar = plot_colors(hist, clt.cluster_centers_)
    print("time4 :", time.time() - start)

     #show our color bart

    plts.figure()
    plts.axis("off")
    plts.imshow(bar)
    plts.show()

    return(clt.cluster_centers_)






