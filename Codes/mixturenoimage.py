import os
import time
import platform
import cv2
import numpy as np
import socket
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen
moth_cascade = cv2.CascadeClassifier('output.xml')
ip=socket.gethostbyname(socket.getfqdn())

##################################################################################
#roi saving version
####################################################################################

def roi_save_new_general(img_file, thresh_size_max,thresh_size_min,distance_threshold,newFile,imageShow=False):  #img_file: file name
    adc=0
    im_in = cv2.imread(img_file, cv2.IMREAD_COLOR)
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
    img_YUV = cv2.cvtColor(im_in, cv2.COLOR_BGR2YUV)
    y = img_YUV[:,:,0]    
    rows = y.shape[0]    
    cols = y.shape[1]
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
    light_removed=result.copy()
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

    #print(mh,ms,mv)

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
    kernel = np.ones((6,6),np.uint8)
    closing = cv2.morphologyEx(bgr, cv2.MORPH_CLOSE, kernel)    
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    th, im_otsu = cv2.threshold(opening, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    output= cv2.connectedComponentsWithStats(im_otsu) 
    new_data=[]
    im_origin = cv2.imread(img_file, cv2.IMREAD_COLOR)
    im_origin2 = result
    old_list=[]  
    new_data=[]
    new_list=[]
    for i in range(1,output[0]):
        if (output[2][i,cv2.CC_STAT_AREA]<thresh_size_min):
            continue
        if (output[2][i,cv2.CC_STAT_AREA]>thresh_size_max):
            continue
        x0=output[2][i,cv2.CC_STAT_LEFT]
        y0=output[2][i,cv2.CC_STAT_TOP]
        x=output[2][i,cv2.CC_STAT_WIDTH]
        y=output[2][i,cv2.CC_STAT_HEIGHT]
        cv2.rectangle(im_origin,(x0,y0),(x0+x,y0+y),(255,0,0),3)
        adc=adc+1
        flag=True
        flagg=True
        for j in range(len(old_list)):
            x_y=old_list[j].split(',')
            x1=int(x_y[0])
            y1=int(x_y[1])
            x_len=int(x_y[2])
            y_len=int(x_y[3])
            if (((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))<distance_threshold):
                if (((x-x_len)*(x-x_len)+(y-y_len)*(y-y_len))<distance_threshold):
                    flag=False
            if (x0<x1) and (x1<x0+x) and (y0<y1) and (y1<y0+y):
                flagg=False
                newx=x1
                newy=y1
        subimg=im_origin2[y0:y+y0,x0:x+x0]
        if flag==True:
            if flagg==False:
                subimg=im_origin2[y0:newy,x0:newx]
            new_data.append(subimg)
            new_list.append(str(x0)+','+str(y0)+','+str(x)+','+str(y))
#    cv2.imshow("otsu",im_origin)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    return light_removed, im_origin, adc

for i in range(800):
    try:
        url = "http://"+ip+":8000/camera/jpeg"
        # print(url)
        # print("image has saved")
        resp=urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        filename='0808show/'+str(i)+'.jpg'
        cv2.imwrite(filename,image)
        # time.sleep(10)
    except:
        raise NameError('incorrect url. Double check it')    

    nolight, imoriginal,c=roi_save_new_general(filename,5000,400,10,True)

    # img = cv2.imread('/Users/moojin/Dropbox/Codes/python/code_combining/Picture/MJPG/2_1.jpeg')
    #img=cv2.imread(image)
    img=nolight.copy()
    # img=img[1000:1500,1000:2000]

    now=time.localtime()
    current_time=str(now.tm_year)+"_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)
    print("current time is :"+current_time)
    #cv2.imshow(current_time+"before",img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    moth = moth_cascade.detectMultiScale(gray, 1.005, 3)
    count=c
    for (x,y,w,h) in moth:
        #  print("how many?")
        if (w*h>500):
            cv2.rectangle(imoriginal,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            count=count+1
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex,ey,ew,eh) in eyes:
        #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    #cv2.imshow(current_time+"after",imoriginal)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() 
    print("bugs : "+str(count))
    cv2.imwrite('0808show/'+str(i)+'_after.jpg',imoriginal)   
    # print(str(i)+" turn")
    time.sleep(60)
    # cv2.waitKey(0)
