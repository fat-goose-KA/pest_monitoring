import os
import time
import sys
import platform
import cv2
import numpy as np
##################################################################################
#roi saving version
####################################################################################


def training_data_making(img_file, thresh_size, distance_threshold, newFile):  #img_file: file name
    im_original = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    # im_in=im_original.copy()
    if im_original is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
    cv2.imshow("original img",im_original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    black_line_flag=True
    black_line_threshold=0
    black_line_previous=im_original.copy()
    black_line_choice=0
    im_in=im_original.copy()
    while black_line_flag==True:
        if(black_line_choice=="5"):
            black_line_flag=False
            break
        im_in=im_original.copy()
        print("from now, we are going to remove balck grid into white")
        print("1: threshold +1 ")
        print("2: threshold +10 ")
        print("3: threshold +50 ")
        print("4: prior state")
        print("5: done")
        black_line_choice=raw_input()
        print("you chose"+black_line_choice)
        if (black_line_choice=="4"):
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
        black_line_previous=im_in.copy()
        th, im_in = cv2.threshold(im_in, black_line_threshold, 255, cv2.THRESH_TOZERO)
        th, im_in = cv2.threshold(im_in, 1, 255, cv2.THRESH_BINARY_INV)
        im_in= im_in | im_original
        # # for i in range(len(im_in)):
        # #     for j in range(len(im_in[0])):
        # #         if (im_in[i][j]<black_line_threshold):
        # #             im_in[i][j]=255
        cv2.imshow("removed?",im_in)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # th, im_inv = cv2.threshold(im_in, 254, 0, cv2.THRESH_BINARY_INV)
        # cv2.imshow("inversed", im_inv)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # im_add=cv2.add(im_inv,im_original)
        # cv2.imshow("add", im_add)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    threshold_flag=True
    threshold_choice="0"
    threshold_threshold=130
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
        th, im_th = cv2.threshold(im_in, threshold_threshold, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow("background black?", im_th)
        cv2.waitKey(0)
        cv2.destroyAllWindows()     #for check whether filtering has proccessed well

        kernel = np.ones((8,8),np.uint8)
        kernel_1 = np.ones((2,2),np.uint8)
        closing = cv2.erode(im_th,kernel_1,iterations = 1)
        cv2.imshow("line removed?", closing)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        for i in range(40):
            closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)    
            closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

        
        #####################################################
        cv2.imshow("nicely done? -background : black, else: white", closing)
        cv2.waitKey(0)
        cv2.destroyAllWindows()     #for check whether filtering has proccessed        
    th, im_otsu = cv2.threshold(closing, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    output= cv2.connectedComponentsWithStats(im_otsu) # 4 or 8

    for i in range(1,output[0]):
        print(str(i))
        # if (output[2][i,cv2.CC_STAT_AREA]<thresh_size):
        #     continue
        # x0=output[2][i,cv2.CC_STAT_LEFT]
        # y0=output[2][i,cv2.CC_STAT_TOP]
        # x=output[2][i,cv2.CC_STAT_WIDTH]
        # y=output[2][i,cv2.CC_STAT_HEIGHT]
        # cv2.rectangle(im_otsu,(x0,y0),(x0+x,y0+y),(255,255,255),10)
        # cv2.imshow("otsu",im_otsu)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # subimg=im_original[y0:y+y0,x0:x+x0]
        # cv2.imshow("sub",subimg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()




training_data_making("/Users/moojin/Dropbox/Codes/python/figure2.jpg", thresh_size=500, distance_threshold=10,newFile=True)