
import os

import cv2 

import numpy as np

import itertools

import platform

from readcsv import saveData

from readcsv import readData

from getColor import getColor

from getColor import getColor2

from callee import roi









# return value (a,b,c)

# a: Message

# b: The number of Specific bug in the Picture -[1,0,0,5]

# c: if the function is failed to run completely - return False.

#    if the function is succeed to run           - return True



# print(os.getcwd())

def classifyMoth_distance(datalist,Save=False,BugName=["1","2","3","4"]):

    

    NumberofType=len(BugName)



    # get dir list by os dir function

    

    filedir=os.getcwd()

    strlen=len(filedir)

    filedir=os.getcwd()[0:strlen-11]+'/MothData/'

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

    _filedir=os.getcwd()[0:strlen-11]+'/NonBugData/'

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

        newdata=np.array(data)

        

        # Calculate the avearage of the existing data.

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



        # Calculte all combination between 5-point of exsisting average data and 5-point of new data

        # Find the order of 5-point data that has the smallest distance value.

        for l,r in enumerate(dist_avg_data_total):

            for i in itertools.permutations([1,2,3,4,0],5):

                distsum=0

                for j,k in enumerate(i):

                    # Sum of square of distances between two points.

                    distsum=distsum+np.linalg.norm(r[j]-data[k])**2

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

                    distsum=distsum+np.linalg.norm(r[j]-data[k])**2

                if distsum < clusterDistance:

                    cluster=-1

                if cluster==-1:

                    break

            if cluster==-1:

                break



        # change the new image data to

        if clusterDistance>15000:

            cluster =-1

        newdata=[]

        for j in bestCombn:

            newdata.append(data[j])

        

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
