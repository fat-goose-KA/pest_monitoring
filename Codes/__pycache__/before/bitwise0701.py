import cv2
import numpy as np

src = cv2.imread("C:/Users/master/Desktop/20190629/Smarf/Picture/Carposina sasakii Matsumura/03_09.png", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
#mask = cv2.inRange(hsv, lower_blue, upper_blue)
mask = cv2.inRange(v,3,195)
mask2 = cv2.inRange(s,10,250)
res = cv2.bitwise_and(src, src, mask=mask)
cv2.imshow('image',src)
cv2.imshow('res',res)
cv2.imshow('mask',mask)

cv2.waitKey(0)
cv2.destroyAllWindows()