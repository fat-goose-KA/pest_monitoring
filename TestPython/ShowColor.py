import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plts
import time

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

color =[ 137.3568699	,120.9149628	,103.9781501	,52.13147499	,44.03250923,	44.83307596	,207.2485702,	199.1832096	,181.004289,	97.14292966,	85.26343431,	79.64532057	,176.7021457	,164.9729707	,148.9695598]
avglist=[]
for j in range(0,5):
    avglist.append(color[j*3:j*3+3])
print(avglist)
avglist = [[151.62380952, 139.00912698, 127.42857143],[114.5768595 , 104.36473829,  95.81763085],[66.41509434, 59.03633823, 53.17819706],[230.97932935, 227.53284336, 223.23977951],[181.56376887, 169.33263925, 157.68610099]]
avglist = np.array(avglist)
hist= [0.2,0.2,0.2,0.2,0.2]
bar = plot_colors(hist, avglist)


plts.figure()
plts.axis("off")
plts.imshow(bar)
plts.show()