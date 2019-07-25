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
    for i in range(len(im_in)):
        for j in range(len(im_in[0])):
            if (im_in[i][j]<140):
                im_in[i][j]=255
    ######################################################
    # cv2.imshow("change?",im_in)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
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
    # cv2.imshow("otsu",im_otsu)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
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

roi_save("/Users/moojin/Dropbox/Codes/python/code_combining/Picture/MJPG/3_2.png", 500, 10,newFile=True,imageShow=True)