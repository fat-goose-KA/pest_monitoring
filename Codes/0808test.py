import numpy as np
import cv2
import time
import socket
import cv2
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen
moth_cascade = cv2.CascadeClassifier('output.xml')
#ip=socket.gethostbyname(socket.gethostname())
ip=socket.gethostbyname(socket.getfqdn())
print(ip)


for i in range(10):
    try:
        url = "http://"+ip+":8000/camera/jpeg"
        print(url)
        resp=urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        cv2.imwrite(str(i)+'.jpg',image)
        time.sleep(10)
    except:
        raise NameError('incorrect url. Double check it')


   # # img = cv2.imread('/Users/moojin/Dropbox/Codes/python/code_combining/Picture/MJPG/2_1.jpeg')
  #  #img=cv2.imread(image)
 #   img=image.copy()
    ## img=img[1000:1500,1000:2000]
    #cv2.imshow("before",img)
   # cv2.waitKey(0)
  #  cv2.destroyAllWindows()
 #   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    moth = moth_cascade.detectMultiScale(gray, 1.01, 3)
    #count=0
    #for (x,y,w,h) in moth:
        ##  print("how many?")
        #if (w*h>1000):
           # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
          #  roi_gray = gray[y:y+h, x:x+w]
         #   roi_color = img[y:y+h, x:x+w]
        #    count=count+1
       # # eyes = eye_cascade.detectMultiScale(roi_gray)
      #  # for (ex,ey,ew,eh) in eyes:
     #   #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    #print(count)
    #cv2.imshow("after",img)
   # time.sleep(60)
  #  print(str(i)+" turn")
 #   # cv2.waitKey(0)
#    cv2.destroyAllWindows()

