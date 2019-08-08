from data_making import training_data_making
import time
import os
# import dlib
import cv2
import numpy as np
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen
ix,iy=-1,-1
down=False
up=False
result_lst=[]
def haar_training(data,sizethreshold,distance_threshold,autoSetting=False,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,imageShow=False,BugName=["1","2","3","4"],newFile=False,saveImage=False):
    imgname=data
    global ix
    global iy
    global up
    global down
    global result_lst
    each_data=training_data_making(data,sizethreshold,distance_threshold,newFile)
    print(each_data)
    test_image=cv2.imread(data,cv2.IMREAD_COLOR)
    confirm_image=cv2.imread(data,cv2.IMREAD_COLOR)
    original_image=cv2.imread(data,cv2.IMREAD_COLOR)
    def draw_box(event, x, y, flags, param, img=test_image):
        global ix, iy
        global down, up
        global result_lst
        # while(event != cv2.EVENT_LBUTTONDOWN):
        if event== cv2.EVENT_LBUTTONDOWN:
            ix,iy=x,y
            up=True
                # break
            print("dddddddddddddddddddd")
        if event == cv2.EVENT_LBUTTONUP:
            ex,ey=x,y
            cv2.rectangle(confirm_image, (ix, iy), (ex, ey), (255,255,255), 5)
            component=str(ix)+","+str(iy)+","+str(ex-ix)+","+str(ey-iy)
            result_lst.append(component)
            down=True
            # test_image=confirm_image.copy()
            print("uuuuuuuuuu")
        # print("#########################################################end")
    # result_lst=[]
    for i in range(len(each_data)):
        test_image=confirm_image.copy()
        data=each_data[i]
        x_y=data.split(',')
        x1=int(x_y[0])
        y1=int(x_y[1])
        x_len=int(x_y[2])
        y_len=int(x_y[3])
        cv2.rectangle(test_image,(x1,y1),(x1+x_len,y1+y_len),(255,0,0),5)
        cv2.imshow("press y if u want pass, n if not, e if u want edit, r to remove last box",test_image)
        cha=cv2.waitKey(0)      #press y: 121 if okay, n:110 if not, e:101 to edit. space for every turn:32 at the end of editing, press e again, r:114 to remove
        cv2.destroyAllWindows()
        if (cha==114):
            # while (cha==114):
            result_lst.pop()
            # cha=cv2.waitKey(0)
            confirm_image=original_image.copy()
            for j in result_lst:
                # print("ho!")
                x_y1=j.split(',')
                x11=int(x_y1[0])
                y11=int(x_y1[1])
                x_len1=int(x_y1[2])
                y_len1=int(x_y1[3])
                cv2.rectangle(confirm_image,(x11,y11),(x11+x_len1,y11+y_len1),(255,255,255),5)
            test_image=confirm_image.copy()
            cv2.imshow("press y if u want pass, n if not, e if u want edit, r to remove last box",test_image)
            cha=cv2.waitKey(0)      #press y: 121 if okay, n:110 if not, e:101 to edit. space for every turn:32 at the end of editing, press e again
            cv2.destroyAllWindows()                
        if (cha==121):
            result_lst.append(data)                                 ######haar training file check and change this one as that form
            cv2.rectangle(confirm_image,(x1,y1),(x1+x_len,y1+y_len),(255,255,255),5)
        elif(cha==110): 
            continue
        elif(cha==101):
            termination=0
            ix,iy=-1,-1
            up=False
            down=False
            while (termination!=101):
                cv2.namedWindow("draw with mouse")
                cv2.setMouseCallback("draw with mouse", draw_box)
                cv2.imshow("draw with mouse",test_image)
                termination=cv2.waitKey(1)
    cv2.destroyAllWindows()
    cv2.imshow("from now, add untracked objects by drawing",confirm_image) #d: 100 space: 32
    cha=cv2.waitKey(0)      
    cv2.destroyAllWindows()
    while (cha!=100):
        termination=0
        # ix,iy=-1,-1
        up=False
        down=False
        # while (termination!=100):
        cv2.namedWindow("If there's no more objects, press d. To add more objects, press space for every turn")
        cv2.setMouseCallback("If there's no more objects, press d. To add more objects, press space for every turn", draw_box)
        cv2.imshow("If there's no more objects, press d. To add more objects, press space for every turn",confirm_image)
        cha=cv2.waitKey(1)
        # cv2.destroyAllWindows()
        # cv2.imshow("If there's no more objects, press d. To add more objects, press space for every turn",confirm_image) #d: 100 space: 32
        # cha=cv2.waitKey(1)      #press y: 121 if okay, n:110 if not, e:101 to edit. space for every turn:32 at the end of editing, press e again             
    cv2.destroyAllWindows()
    filedir=os.getcwd()

    getname=imgname.split('/')
    name=getname[-1]
    realname=name.split('.')
    realname=realname[0]

    txt_name="/"+realname+".txt"
    f = open(filedir+txt_name,'w')
    f.write("rawdata/"+name)
    for i in range(len(result_lst)):
        element=result_lst[i].split(',')
        f.write(" "+element[0]+" "+element[1]+" "+element[2]+" "+element[3])    
    return result_lst


res=haar_training(data="/Users/moojin/Dropbox/Codes/python/pest_monitoring/Picture/MJPG/3_2.png",sizethreshold=500,distance_threshold=10,imageShow=False,BugName=["a","b","c","d"])
print(res)