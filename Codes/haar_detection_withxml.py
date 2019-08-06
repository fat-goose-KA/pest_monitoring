import numpy as np
import cv2
moth_cascade = cv2.CascadeClassifier('output.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# img = cv2.imread('/Users/moojin/Dropbox/Codes/python/code_combining/Picture/MJPG/3_2.png')
img = cv2.imread('/Users/moojin/Dropbox/Codes/python/code_combining/Picture/MJPG/2_1.jpeg')
# for i in range(len(img)):
#    for j in range(len(im_in[0])):
#       if (im_in[i][j]<140):
#             im_in[i][j]=255
print(len(img))
print(len(img[0]))
# img=img[1000:1500,1000:2000]
cv2.imshow("before",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
moth = moth_cascade.detectMultiScale(gray, 1.001, 5)
count=0
for (x,y,w,h) in moth:
   #  print("how many?")
   if (w*h>1000):
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
      roi_gray = gray[y:y+h, x:x+w]
      roi_color = img[y:y+h, x:x+w]
      count=count+1
   # eyes = eye_cascade.detectMultiScale(roi_gray)
   # for (ex,ey,ew,eh) in eyes:
   #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
print(count)
# cv2.imwrite("0718result.jpg",img)
cv2.imshow("after",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

