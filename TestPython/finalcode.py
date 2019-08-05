from getColor import getColor2
from classifyMoth import classifyMoth
from classifyMoth import classifyMoth_distance
from roi_save_return import roi_save
from roi_save_return import roi_save_new
from roi_save_return import roi_save_new_general
from save_as_csv import saveDataAsCsv
from save_as_image import saveDataAsImage
import time
import os
import platform
# import dlib
import cv2
import numpy as np
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib import urlopen


def id_to_ip(id):
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=os.getcwd()[0:strlen-11]+'/Client_data/'
    txt_name='client_data.txt'
    
    try:
        dirName = filedir+txt_name
        

        if platform.system() == "Windows":
            dirName=  dirName.replace("\\","/")
        f = open(dirName, 'r')
        lines=f.readlines()
        old_id_list=[]
        old_ip_list=[]
        for i in lines:
            # print(i)
            before_list=i.split('\n')
            # print(before_list)
            before_list=before_list[0].split('\t')  
            # print(before_list)
            if (before_list[0]==id):
                f.close()
                return before_list[1]
        f.close()
        return None
    except:
        return None

def id_to_image(id):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
    # try: #python3
    #     resp = urlopen(url)
    # except: #python2
    #     resp = urlopen(url)    
    try:
        ip=id_to_ip(id)
        if ip is None:
            print("wrong ip address")
        # url = "http://"+ip+"/?action=snapshot"
        url = "http://"+ip+"camera/jpeg"
        print(url)
        resp=urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
        return image
    except:
        raise NameError('incorrect url. Double check it')


def combined_code (id,data,thresh_size_max,thresh_size_min,distance_threshold,autoSetting=False,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,imageShow=False,BugName=["1","2","3","4"],newFile=False,saveImage=False):

    each_labeled, imgs = roi_save_new_general(img_file=data, thresh_size_max= thresh_size_max ,thresh_size_min= thresh_size_min, distance_threshold=distance_threshold,newFile = newFile,imageShow=imageShow)
    # each_labeled, imgs = roi_save(data,sizethreshold,distance_threshold,newFile = newFile,imageShow=imageShow)

                                                                           
    datalist, deletenum = getColor2(each_labeled,distance_threshold,autoSetting=autoSetting,imageShow=imageShow,hlist=hlist,sup=sup,sdown=sdown,vup=vup,vdown=vdown)
    print(deletenum)

    message,clusterSum,clusterData,TrueorFalse = classifyMoth(datalist,Save,BugName)
    # message,clusterSum,clusterData,TrueorFalse = classifyMoth(datalist,Save,BugName)
    deletenum.reverse()
    for i in deletenum:
        del each_labeled[i]
    
    saveDataAsCsv(id, data=clusterSum, bugName=BugName, newFile=newFile)

    if saveImage == True:
        saveDataAsImage(id,imageData=each_labeled,clusterData=clusterData,bugName=BugName)

    return message,clusterSum,clusterData,TrueorFalse


def combined_code_id (id, sizethreshold,distance_threshold,autoSetting=False,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,imageShow=False,BugName=["1","2","3","4"],newFile=False,saveImage=False):

    data=id_to_image(id)
    now=time.localtime()

    outputFileName =str(now.tm_year)+"_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)+"."+ "jpg"
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=filedir[0:strlen-11]
    filedir=filedir+'/Client_data/'+id
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filedir=filedir+'/Picture/'
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filedir=filedir+'MJPG/'
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filedir=filedir +outputFileName



    if imageShow==True:
        cv2.imshow(filedir,data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    cv2.imwrite(filedir, data)
    a1, b1, c1, d1=combined_code(id,filedir,sizethreshold,distance_threshold,hlist=hlist,sup=sup,sdown=sdown,vup=vup,vdown=vdown
,Save=Save,imageShow=imageShow,BugName=BugName)
    return a1, b1, c1, d1
 