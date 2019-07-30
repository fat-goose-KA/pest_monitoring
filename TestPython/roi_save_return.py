import os
import time
import platform
import cv2
import numpy as np
##################################################################################
#roi saving version
####################################################################################


def roi_save(img_file, thresh_size, distance_threshold,newFile,imageShow):  #img_file: file name

    im_in = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
    for i in range(len(im_in)):
        for j in range(len(im_in[0])):
            if (im_in[i][j]<140):
                im_in[i][j]=255
    ######################################################
    # cv2.imshow("change?",im_in)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    th, im_th = cv2.threshold(im_in, 150, 255, cv2.THRESH_BINARY_INV)
    im_floodfill = im_in.copy()
    h, w = im_floodfill.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_in, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv
    ######################################################
    # cv2.imshow("Foreground", im_out)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()     #for check whether filtering has proccessed well
    th, im_twocol = cv2.threshold(im_out, 150, 255, cv2.THRESH_BINARY)   ## use  filter again

    ######################################################
    # cv2.imshow("adfadad", im_twocol)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()     #for check whether filtering has proccessed well

    kernel = np.ones((8,8),np.uint8)
    closing = cv2.morphologyEx(im_twocol, cv2.MORPH_CLOSE, kernel)    
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    th, im_otsu = cv2.threshold(closing, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    cv2.imshow("otsu",im_otsu)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    output= cv2.connectedComponentsWithStats(im_otsu) # 4 or 8
    # def drawbox(im, stats):
    #     for i in range(1,stats[0]):
    #         print("huh")
    #         x0=stats[2][i,cv2.CC_STAT_LEFT]
    #         y0=stats[2][i,cv2.CC_STAT_TOP]
    #         x=stats[2][i,cv2.CC_STAT_WIDTH]
    #         y=stats[2][i,cv2.CC_STAT_HEIGHT]
    #         cv2.rectangle(im,(x0,y0),(x0+x,y0+y),(255,255,255),10)
    # drawbox(im_otsu, output)



    ######################################################
    new_data=[]
    im_origin = cv2.imread(img_file, cv2.IMREAD_COLOR)
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=os.getcwd()[0:strlen-11]+'/roi_log/'
    if platform.system() == "Windows":
        filedir=  filedir.replace("\\","/")
    txt_name="1.txt"
    # print(filedir+txt_name)
    if newFile == False:
        try:
            f=open(filedir+txt_name,'r')
            lines=f.readlines()
            lastline=lines[-1] # parsing into elements separate by tab character @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # print(lastline)
            before_list=lastline.split('\n')
            before_list=before_list[0].split('\t')
            if (len(before_list)==1):
                old_list=[]
            else:
                old_list=before_list[1:] # save them in point_list ##if it has no point??
            # for i in old_list:
            #     print(i)
            # print("end?")
            f.close()
        except:
            old_list=[]    
    else:
        old_list=[]  
    new_data=[]
    new_list=[]
    for i in range(1,output[0]):
        # print("huh")
        if (output[2][i,cv2.CC_STAT_AREA]<thresh_size):
            continue
        x0=output[2][i,cv2.CC_STAT_LEFT]
        y0=output[2][i,cv2.CC_STAT_TOP]
        x=output[2][i,cv2.CC_STAT_WIDTH]
        y=output[2][i,cv2.CC_STAT_HEIGHT]
        cv2.rectangle(im_otsu,(x0,y0),(x0+x,y0+y),(255,255,255),10)
        flag=True
        flagg=True
        for j in range(len(old_list)):
            x_y=old_list[j].split(',')
            x1=int(x_y[0])
            y1=int(x_y[1])
            x_len=int(x_y[2])
            y_len=int(x_y[3])
            # print(str((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1)))
            # print(((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))<distance_threshold)
            if (((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))<distance_threshold):
                if (((x-x_len)*(x-x_len)+(y-y_len)*(y-y_len))<distance_threshold):
                    flag=False
            if (x0<x1) and (x1<x0+x) and (y0<y1) and (y1<y0+y):
                flagg=False
                newx=x1
                newy=y1
        if imageShow == True:
            cv2.imshow("otsu",im_otsu)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # subimg=im_origin[x:x+x0, y:y+y0]
        subimg=im_origin[y0:y+y0,x0:x+x0]
        if flag==True:
            if flagg==False:
                subimg=im_origin[y0:newy,x0:newx]
            new_data.append(subimg)
            new_list.append(str(x0)+','+str(y0)+','+str(x)+','+str(y))
        if imageShow == True:
            cv2.imshow("sub",subimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # print(flag)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
    # print(result)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
    try:
        f = open(filedir+txt_name, 'a')
    except:
        f = open(filedir+txt_name,'w')
    now=time.localtime()    
    current_time=str(now.tm_year)+"_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)
    f.write(current_time)
    ########################################
    # print(old_list)
    # print("######################################################")
    # print(new_list)
    # print("######################################################")
    for i in range(len(old_list)):
        f.write('\t'+old_list[i])
    for i in range(len(new_list)):
        f.write('\t'+new_list[i])
    f.write('\n')
    f.close()
    print(len(new_list))
    if imageShow == True:
        for i in new_data:
            cv2.imshow("return",i)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return new_data, new_list
########################################################################


def roi_save_new(img_file, thresh_size, distance_threshold,newFile,imageShow):  #img_file: file name

    im_in = cv2.imread(img_file, cv2.IMREAD_COLOR)
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
    # for i in range(len(im_in)):
    #     for j in range(len(im_in[0])):
    #         if (im_in[i][j]<140):
    #             im_in[i][j]=255
    ######################################################
    # cv2.imshow("change?",im_in)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # th, im_th = cv2.threshold(im_in, 150, 255, cv2.THRESH_BINARY_INV)
    # im_floodfill = im_in.copy()
    # h, w = im_floodfill.shape[:2]
    # mask = np.zeros((h+2, w+2), np.uint8)
    # cv2.floodFill(im_in, mask, (0,0), 255)
    # im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # im_out = im_th | im_floodfill_inv
    ######################################################
    # cv2.imshow("Foreground", im_out)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()     #for check whether filtering has proccessed well
    # th, im_twocol = cv2.threshold(im_out, 150, 255, cv2.THRESH_BINARY)   ## use  filter again

    ######################################################
    # cv2.imshow("adfadad", im_twocol)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()     #for check whether filtering has proccessed well


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
    gamma2 = 1.5
    img_adjusting = gamma1*img_LF[0:rows, 0:cols] + gamma2*img_HF[0:rows, 0:cols]
    
    img_exp = np.expm1(img_adjusting) # exp(x) + 1
    img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp))
    img_out = np.array(255*img_exp, dtype = 'uint8') 
    
    img_YUV[:,:,0] = img_out
    result = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)


    cv2.imshow("otsu",result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # hsv eliminate blue one
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    mask = cv2.inRange(v,1,254)
    mask2 = cv2.inRange(s,1,254)
    mask3_up = cv2.inRange(h,108,180)
    mask3_down = cv2.inRange(h,0,92)
    mask3=(mask3_up+mask3_down)
    res = cv2.bitwise_and(gray, gray, mask=(mask))
    res = cv2.bitwise_and(res, res, mask=(mask2))
    res = cv2.bitwise_and(res, res, mask=mask3)

    cv2.imshow("otsu",res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # fill the blank and delete noise
    kernel = np.ones((8,8),np.uint8)
    closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)    
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    th, im_otsu = cv2.threshold(opening, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    output= cv2.connectedComponentsWithStats(im_otsu) # 4 or 8

    new_data=[]
    # im_origin = cv2.imread(img_file, cv2.IMREAD_COLOR)
    im_origin = result
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=os.getcwd()[0:strlen-11]+'/roi_log/'
    if platform.system() == "Windows":
        filedir=  filedir.replace("\\","/")
    txt_name="1.txt"
    if newFile == False:
        try:
            f=open(filedir+txt_name,'r')
            lines=f.readlines()
            lastline=lines[-1] 
            before_list=lastline.split('\n')
            before_list=before_list[0].split('\t')
            if (len(before_list)==1):
                old_list=[]
            else:
                old_list=before_list[1:] 
            f.close()
        except:
            old_list=[]    
    else:
        old_list=[]  
    new_data=[]
    new_list=[]
    for i in range(1,output[0]):
        if (output[2][i,cv2.CC_STAT_AREA]<thresh_size):
            continue
        x0=output[2][i,cv2.CC_STAT_LEFT]
        y0=output[2][i,cv2.CC_STAT_TOP]
        x=output[2][i,cv2.CC_STAT_WIDTH]
        y=output[2][i,cv2.CC_STAT_HEIGHT]
        cv2.rectangle(im_otsu,(x0,y0),(x0+x,y0+y),(255,255,255),10)
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
        if imageShow == True:
            cv2.imshow("otsu",im_otsu)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        subimg=im_origin[y0:y+y0,x0:x+x0]
        if flag==True:
            if flagg==False:
                subimg=im_origin[y0:newy,x0:newx]
            new_data.append(subimg)
            new_list.append(str(x0)+','+str(y0)+','+str(x)+','+str(y))
        if imageShow == True:
            cv2.imshow("sub",subimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    try:
        f = open(filedir+txt_name, 'a')
    except:
        f = open(filedir+txt_name,'w')
    now=time.localtime()    
    current_time=str(now.tm_year)+"_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)
    f.write(current_time)
    for i in range(len(old_list)):
        f.write('\t'+old_list[i])
    for i in range(len(new_list)):
        f.write('\t'+new_list[i])
    f.write('\n')
    f.close()
    print(len(new_list))
    if imageShow == True:
        for i in new_data:
            cv2.imshow("return",i)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return new_data, new_list
########################################################################