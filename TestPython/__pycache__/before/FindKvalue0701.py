import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import time
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

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

start = time.time() 
src = cv2.imread("C:/Users/master/Desktop/Picture/Adoxophyes orana/01_20.jpg", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
mask = cv2.inRange(v,0,250)
bgr = cv2.bitwise_and(src, src, mask=mask)
cv2.imshow('bg',bgr)
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
height ,width ,channel = hsv.shape
print(height, width , channel)
hsv = hsv.reshape((hsv.shape[0] * hsv.shape[1], 3))

print("time1 :", time.time() - start)
Sum_of_squared_distances = []
K = range(2,8)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(hsv)    
    if k is not 2:
        diff = before -km.inertia_
        Sum_of_squared_distances.append(diff)
    before=km.inertia_
    print("time",k, ":",time.time() - start)
plt.plot(range(3,8), Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()