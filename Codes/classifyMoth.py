import os
import cv2 
import numpy as np
import itertools
import platform
import math
from readcsv import saveData
from readcsv import readData
from getColor import getColor2
from callee import roi
from scipy.stats import t



# return value (a,b,c)
# a: Message
# b: The number of Specific bug in the Picture -[1,0,0,5]
# c: if the function is failed to run completely - return False.
#    if the function is succeed to run           - return True
def distanceHSV(a,b):
    h = abs(a[0]-b[0])
    s = abs(a[1]-b[1])
    v = abs(a[2]-b[2])
    result = ((4*s*h/5)**2+(6*v)**2+(20*s/3.141592)**2)**(1/2)
    return result

def distanceEuc(a,b):

    return np.linalg.norm(a,b)


# print(os.getcwd())
def classifyMoth(datalist,Save=False,BugName=["1","2","3","4"]):
    # try:
    NumberofType=len(BugName)

    # get dir list by os dir function
    
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=os.getcwd()[0:strlen-6]+'/MothDataHsv/'
    dirlist=os.listdir(filedir)
    fileList=[]
    for i in dirlist:
        if i.find('csv') is not -1:
            if i.find('Mothdata') is not -1:
                fileList.append(filedir+i)
        # print(filedir+i)
    # roi("./test.png",5000)
    # print (fileList) #:: current directory
    # Get Saved Moth data
    dist_data_total=readData(fileList)

    # Get Color from moth data
    dist_avg_data_total=[]
    #nonfileList=["/Users/moojin/Dropbox/Codes/python/code_combining/NonBugData/NonBugData01.csv"]  ##change later
    _filedir=os.getcwd()[0:strlen-6]+'/NonBugData/'
    if platform.system() == "Windows":
        _filedir=  _filedir.replace("\\","/")


    _dirlist=os.listdir(_filedir)
    nonfileList=[]
    for i in _dirlist:
        if i.find('csv') is not -1:
            if i.find('NonBug') is not -1:
                nonfileList.append(_filedir+i)
    #if nonfileList is empty -> error message
    dist_non_data_total=readData(nonfileList)
    # dist_non_data_total=[[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]]
    ##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##
    ##########################################################
    ##change below part using url to get image from python,
    ## or get dir?##
    ## getColor2(filename, clusternum, sizethreshold) \
    dist_avg_data_total=[]
    dist_avg_non_data_total=[]
    dist_var_data_total = []
    dist_var_non_data_total = []
    dist_num_data_total=[]
    dist_num_non_data_total=[]
    numberofBug=[]
    for i in range(0,NumberofType):
        numberofBug.append(0)
    # Calculate the avearage of the existing data.
    # Calculate the avearage of the existing data.
    for dist_data in dist_data_total:
        
        dist_data = dist_data.astype(np.float)

        dist_avg_data=[]
        if dist_data[0]==[]:
            print("Empty Distribution")
            break
        dist_avg_data=np.average(dist_data,axis=0)
        avglist =[]
        # Change the scala row data to point row data
        for j in range(0,5):
            avglist.append(dist_avg_data[j*3:j*3+3])
        dist_avg_data_total.append(avglist)

        varlist=[]
        numlist=[]
        for k in range(0,5):
            csum = 0
            for j in dist_data:
                csum = csum + distanceHSV(j[k*3:k*3+3], avglist[k])**2
            csize = dist_data.size/15
            cvar = (csum/(csize-1))**0.5
            varlist.append(cvar)
            numlist.append(csize)
        dist_num_data_total.append(numlist)
        dist_var_data_total.append(varlist)

    for dist_non_data in dist_non_data_total:

        dist_non_data = dist_non_data.astype(np.float)

        dist_avg_non_data=[]
        if dist_non_data[0]==[]:
            print("")
            break
        # print(dist_non_data)
        y = dist_non_data.astype(np.float)
        dist_avg_non_data=np.average(y,axis=0)
        avglist =[]
        # Change the scala row data to point row data
        for j in range(0,5):
            avglist.append(dist_avg_non_data[j*3:j*3+3])
        dist_avg_non_data_total.append(avglist)

        varlist=[]
        numlist=[]
        for k in range(0,5):
            csum = 0
            for j in dist_non_data:
                csum = csum + distanceHSV(j[k*3:k*3+3], avglist[k])**2
            csize = dist_non_data.size/15
            cvar = (csum/(csize-1))*0.5
            varlist.append(cvar)
            numlist.append(csize)
        dist_num_non_data_total.append(numlist)
        dist_var_non_data_total.append(varlist)
 


    clusterData=[]
    length = len(datalist)
    progress = 0
    for data in datalist:
        
       
        # Set initial value
        lowdist=1
        k=0

        # Set a very very high value
        origin = 1540
        clusterDistance = 1540
        cluster = -1
        # Calculte all combination between 5-point of exsisting average data and 5-point of new data
        # Find the order of 5-point data that has the smallest distance value.
        for l,r in enumerate(dist_avg_data_total):
            for i in itertools.permutations([1,2,3,4,0],5):
                pMultiple=1
                pLogSum=0
                for j,k in enumerate(i):
                    x1 = r[j]
                    x2 = data[0][k]
                    s1 = dist_var_data_total[l][j]
                    s2 = data[1][k]
                    n1 = dist_num_data_total[l][j]
                    n2 = data[2][k]
                    Tvalue = distanceHSV(x1,x2)/(s1*s1/n1+s2*s2/n2)**0.5
                    dF = round(s1*s1/n1+s2*s2/n2)**2/((s1*s1/n1)/(n1-1)+(s2*s2/n2)**2/(n2-1))
                    
                    pvalue = t.sf(Tvalue, dF)
                    if pvalue != 0:
                        plog = -math.log(pvalue)
                    else :
                        plog = 308
                    # Sum of square of distances between two points.\
                    pLogSum = pLogSum + plog
                if pLogSum < origin:
                    origin = pLogSum
                    bestCombn = i
            if origin < clusterDistance:
                #     pMultiple = pMultiple * pvalue
                # if pMultiple > origin:
                    # origin = pMultiple
            #         bestCombn = i
            # if origin > clusterDistance:
                clusterDistance=origin
                cluster=l+1
        for l,r in enumerate(dist_avg_non_data_total):
            for i in itertools.permutations([1,2,3,4,0],5):
                pMultiple = 1
                pLogSum = 0
                for j,k in enumerate(i):
                    # Sum of square of distances between two points.
                    x1 = r[j]
                    x2 = data[0][k]
                    s1 = dist_var_non_data_total[l][j]
                    s2 = data[1][k]
                    n1 = dist_num_non_data_total[l][j]
                    n2 = data[2][k]
                    Tvalue = distanceHSV(x1,x2)/(s1*s1/n1+s2*s2/n2)**0.5
                    dF = round(s1*s1/n1+s2*s2/n2)**2/((s1*s1/n1)/(n1-1)+(s2*s2/n2)**2/(n2-1))
                    pvalue = t.sf(Tvalue, dF)
                    if pvalue != 0:
                        plog = -math.log(pvalue)
                    else :
                        plog = 308
                    # Sum of square of distances between two points.
                    
                    pLogSum = pLogSum + plog
                if pLogSum < clusterDistance:
                    # pMultiple = pMultiple*pvalue
                # if pMultiple > clusterDistance:
                    cluster=-1
                if cluster==-1:
                    break
            if cluster==-1:
                break
        if clusterDistance >200:
            cluster = -1
        print(clusterDistance)
        # change the new image data to
        newdata=[]
        if cluster!=-1:
            for j in bestCombn:
                newdata.append(data[0][j])
        else:
            newdata = data[0]
        
        # if  Save and (cluster != -1):
        #     saveData(newdata,cluster)
        saveData(newdata,5)


        # return the meassage informing type of bug
        if cluster != -1:
            numberofBug[cluster-1] = numberofBug[cluster-1]+1
            # path = "C:/Users/master/Desktop/20190629/Smarf/Result/" +str(cluster)
            # cv2.imwrite(os.path.join(path , str(numberofBug[cluster-1])+'.jpg'), data) 
        clusterData.append(cluster)
        print(str(progress)+ "/" + str(length) + "....")
        progress = progress + 1
    # print("finish!")
    # for i in range(0,4):
    #     print("--------------------------")
    #     print(dist_avg_data_total[i])
    #     print("--------------------------")
    #     print(dist_var_data_total[i])
    #     print("--------------------------")
    returnmessage = ""
    for i,j in enumerate(BugName):
        if i!=0:
            returnmessage=returnmessage + " and "
        returnmessage=returnmessage + j + ": " +str(numberofBug[i])
    return (returnmessage,numberofBug,clusterData,True)
    # except Exception as e:
    #     return (e,0,0,False)

def classifyMoth_distance(datalist,Save=False,BugName=["1","2","3","4"]):

    NumberofType=len(BugName)

    # get dir list by os dir function
    filedir=os.getcwd()

    strlen=len(filedir)

    filedir=os.getcwd()[0:strlen-6]+'/MothDataHsv/'

    dirlist=os.listdir(filedir)

    fileList=[]

    for i in dirlist:

        if i.find('csv') is not -1:

            if i.find('Mothdata') is not -1:

                fileList.append(filedir+i)

        # print(filedir+i)

    # roi("./test.png",5000)
    # print (fileList) #:: current directory
    # Get Saved Moth data

    dist_data_total=readData(fileList)

    # Get Color from moth data

    dist_avg_data_total=[]

    #nonfileList=["/Users/moojin/Dropbox/Codes/python/code_combining/NonBugData/NonBugData01.csv"]  ##change later

    _filedir=os.getcwd()[0:strlen-6]+'/NonBugData/'

    if platform.system() == "Windows":
        _filedir=  _filedir.replace("\\","/")

    _dirlist=os.listdir(_filedir)
    nonfileList=[]

    for i in _dirlist:
        if i.find('csv') is not -1:
            if i.find('NonBug') is not -1:
                nonfileList.append(_filedir+i)

    #if nonfileList is empty -> error message

    dist_non_data_total=readData(nonfileList)

    # dist_non_data_total=[[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]]
    ##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##
    ##########################################################
    ##change below part using url to get image from python,
    ## or get dir?##
    ## getColor2(filename, clusternum, sizethreshold) \

    dist_avg_data_total=[]
    dist_avg_non_data_total=[]
    numberofBug=[]
    for i in range(0,NumberofType):
        numberofBug.append(0)

    clusterData=[]
    for data in datalist:

        # Calculate the avearage of the existing data.

        for dist_data in dist_data_total:
            dist_avg_data=[]
            if dist_data[0]==[]:
                print("Empty Distribution")
                break
            y = dist_data.astype(np.float)
            dist_avg_data=np.average(y,axis=0)
            avglist =[]
            # Change the scala row data to point row data
            for j in range(0,5):
                avglist.append(dist_avg_data[j*3:j*3+3])
            dist_avg_data_total.append(avglist)


        for dist_non_data in dist_non_data_total:
            dist_avg_non_data=[]
            if dist_non_data[0]==[]:
                print("")
                break
            # print(dist_non_data)
            y = dist_non_data.astype(np.float)
            dist_avg_non_data=np.average(y,axis=0)
            avglist =[]
            # Change the scala row data to point row data
            for j in range(0,5):
                avglist.append(dist_avg_non_data[j*3:j*3+3])
            dist_avg_non_data_total.append(avglist)

        # Set initial value
        lowdist=1
        k=0

        # Set a very very high value
        origin=10000000
        clusterDistance=1000000000
        cluster=-1
        # Calculte all combination between 5-point of exsisting average data and 5-point of new data
        # Find the order of 5-point data that has the smallest distance value.
        for l,r in enumerate(dist_avg_data_total):
            for i in itertools.permutations([1,2,3,4,0],5):
                distsum=0
                for j,k in enumerate(i):
                    # Sum of square of distances between two points.
                    distsum=distsum+distanceHSV(r[j],data[0][k])
                if distsum < origin:
                    origin = distsum
                    bestCombn = i
            if origin < clusterDistance:
                clusterDistance=origin
                cluster=l+1


        for l,r in enumerate(dist_avg_non_data_total):
            for i in itertools.permutations([1,2,3,4,0],5):
                distsum=0
                for j,k in enumerate(i):
                    # Sum of square of distances between two points.
                    distsum=distsum+distanceHSV(r[j],data[0][k])
                if distsum < clusterDistance:
                    cluster=-1
                    print("white")
                if cluster==-1:
                    break
            if cluster==-1:
                break

        # change the new image data to
        if clusterDistance>7000:
            cluster =-1
        newdata=[]

        for j in bestCombn:
            newdata.append(data[0][j])

        if  Save and (cluster != -1):
            saveData(newdata,cluster)

        # return the meassage informing type of bug

        if cluster != -1:
            numberofBug[cluster-1] = numberofBug[cluster-1]+1
            # path = "C:/Users/master/Desktop/20190629/Smarf/Result/" +str(cluster)
            # cv2.imwrite(os.path.join(path , str(numberofBug[cluster-1])+'.jpg'), data) 

        clusterData.append(cluster)
    returnmessage = ""
    for i,j in enumerate(BugName):
        if i!=0:
            returnmessage=returnmessage + " and "
        returnmessage=returnmessage + j + ": " +str(numberofBug[i])

    return (returnmessage,numberofBug,clusterData,True)
