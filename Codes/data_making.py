import os
import time
import sys
import platform
import cv2
import numpy as np


def training_data_making(img_file, thresh_size, distance_threshold, newFile):  #img_file: file name

####################################################################################################
    im_in = cv2.imread(img_file, cv2.IMREAD_COLOR)
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
    img_YUV = cv2.cvtColor(im_in, cv2.COLOR_BGR2YUV)
    y = img_YUV[:,:,0]    
    
    rows = y.shape[0]    
    cols = y.shape[1]
    
    ### illumination elements reflectance elements
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
    gamma2 = 1.0
    img_adjusting = gamma1*img_LF[0:rows, 0:cols] + gamma2*img_HF[0:rows, 0:cols]
    
    img_exp = np.expm1(img_adjusting) # exp(x) + 1
    img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp))
    img_out = np.array(255*img_exp, dtype = 'uint8') 
    
    img_YUV[:,:,0] = img_out
    result = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)


####################################################################################################

    im_color=result.copy()
    im_in = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    im_in = clahe.apply(im_in)
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
    cv2.imshow("original img",im_in)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    black_line_flag=True
    black_line_threshold=0
    black_line_previous=im_in.copy()
    black_line_choice=0
    while black_line_flag==True:
        print("from now, we are going to remove balck grid into white")
        print("1: threshold +1 ")
        print("2: threshold +10 ")
        print("3: threshold +50 ")
        print("4: threshold -1 ")
        print("5: threshold -10 ")
        print("6: threshold -50 ")
        print("7: prior state")
        print("8: done")
        black_line_choice=raw_input()
        print("you chose"+black_line_choice)
        if(black_line_choice=="8"):
            black_line_flag=False
            break
        elif (black_line_choice=="7"):
            im_in=black_line_previous.copy()
            cv2.imshow("previous img",im_in)
            cv2.imshow("previous img?",black_line_previous)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            continue
        elif (black_line_choice=="1"):
            black_line_threshold+=1
        elif (black_line_choice=="2"):
            black_line_threshold+=10
        elif (black_line_choice=="3"):
            black_line_threshold+=50
        elif (black_line_choice=="4"):
            black_line_threshold-=1
        elif (black_line_choice=="5"):
            black_line_threshold-=10
        elif (black_line_choice=="6"):
            black_line_threshold-=50            
        black_line_previous=im_in.copy()
        
        hsv = cv2.cvtColor(im_color, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        mask = cv2.inRange(v,black_line_threshold,255)
        mask_inv=cv2.bitwise_not(mask)
        result= mask_inv | im_in.copy()
        cv2.imshow("removed?",result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    threshold_flag=True
    threshold_choice="0"
    threshold_threshold=51
    while threshold_flag==True:
        print("from now, we are going to make background black and target white")
        print("1: threshold +1 ")
        print("2: threshold +10 ")
        print("3: threshold +50 ")
        print("4: threshold -1 ")
        print("5: threshold -10 ")
        print("6: threshold -50 ")
        print("7: done")
        threshold_choice=raw_input()
        print("you chose"+threshold_choice)
        if(threshold_choice=="7"):
            threshold_flag=False
            break
        elif (threshold_choice=="1"):
            threshold_threshold+=1
        elif (threshold_choice=="2"):
            threshold_threshold+=10
        elif (threshold_choice=="3"):
            threshold_threshold+=50
        elif (threshold_choice=="4"):
            threshold_threshold-=1
        elif (threshold_choice=="5"):
            threshold_threshold-=10
        elif (threshold_choice=="6"):
            threshold_threshold-=50
        print("current threshold is :"+str(threshold_threshold))

        th, im_th = cv2.threshold(result, 253, 255, cv2.THRESH_BINARY)
        cv2.imshow("line white?", im_th)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        hsv1 = cv2.cvtColor(im_color, cv2.COLOR_BGR2HSV)
        h1,s1,v1 = cv2.split(hsv1)
        mask1 = cv2.inRange(v1,threshold_threshold,255)
        cv2.imshow("background white and bug black?", mask1)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        for_now=mask1 | im_th    # -> line and background: 255, left : black

        # cv2.imshow("background including grid white?", for_now)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()     #for check whether filtering has proccessed well
        
        im_floodfill = for_now.copy()
        h, w = im_floodfill.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(for_now, mask, (0,0), 255)
        # cv2.imshow("floodfill?", for_now)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # im_out = for_now | im_floodfill_inv
        im_out=for_now.copy()
        # cv2.imshow("or merge", im_out)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        th, im_twocol = cv2.threshold(im_out, threshold_threshold, 255, cv2.THRESH_BINARY)   ## use  filter again
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(im_twocol, cv2.MORPH_CLOSE, kernel)    
        closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        for i in range(1):
            closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)    
            closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)            

        th, im_otsu = cv2.threshold(closing, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imshow("done? -background : white, else: balck", im_otsu)
        cv2.waitKey(0)
        cv2.destroyAllWindows()     #for check whether filtering has proccessed well
        final=cv2.bitwise_not(im_otsu)
        output= cv2.connectedComponentsWithStats(final) # 4 or 8
    print(output[0])

    data_list=[]
    data_img=[]
    for i in range(1,output[0]):
        if (output[2][i,cv2.CC_STAT_AREA]<thresh_size):
            continue
        x0=output[2][i,cv2.CC_STAT_LEFT]
        y0=output[2][i,cv2.CC_STAT_TOP]
        x=output[2][i,cv2.CC_STAT_WIDTH]
        y=output[2][i,cv2.CC_STAT_HEIGHT]
        cv2.rectangle(im_otsu,(x0,y0),(x0+x,y0+y),(0,0,0),10)
        flag=True
        flagg=True
        for j in range(len(data_list)):
            x_y=data_list[j].split(',')
            x1=int(x_y[0])
            y1=int(x_y[1])
            x_len=int(x_y[2])
            y_len=int(x_y[3])
            if (((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))<distance_threshold):
                if (((x-x_len)*(x-x_len)+(y-y_len)*(y-y_len))<distance_threshold):
                    flag=False
            # if (x0<x1) and (x1<x0+x) and (y0<y1) and (y1<y0+y):
            #     flagg=False
            #     newx=x1
            #     newy=y1
        # cv2.imshow("otsu",im_otsu)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        subimg=im_color[y0:y+y0,x0:x+x0]
        if flag==True:
            # if flagg==False:
            #     subimg=im_color[y0:newy,x0:newx]
            data_img.append(subimg)
            data_list.append(str(x0)+','+str(y0)+','+str(x)+','+str(y))
        # # if imageShow == True:
        # cv2.imshow("sub",subimg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    print(len(data_list))

    # new_data=[]
    return data_list
# training_data_making("/Users/moojin/Dropbox/Codes/python/pest_monitoring/Picture/MJPG/3_2.png", thresh_size=500, distance_threshold=10,newFile=True)
# training_data_making("/Users/moojin/Dropbox/Codes/python/figure2.jpg", thresh_size=500, distance_threshold=10,newFile=True)