import datetime 
import csv
import os
import platform
import numpy as np


def saveDataAsCsv(id, data ,bugName,newFile=False):
    # Find or create a csv file
    originBugName=bugName
    bugName.sort()
    newdata=[]
    for i in bugName:   
        newdata.append(data[originBugName.index(i)])

    data=newdata
    now = datetime.datetime.now()
    year = now.strftime('%Y')

    filedir=os.getcwd()
    strlen=len(filedir)

    filedir=os.getcwd()[0:strlen-6]+'/Client_data/'+id

    if not os.path.exists(filedir):
        os.mkdir(filedir)

    filedir=filedir+'/TimeData/'  

    if platform.system() == "Windows":
        filedir=  filedir.replace("\\","/")

    if not os.path.exists(filedir):
        os.mkdir(filedir)

    dirlist=os.listdir(filedir)
    fileList=[]
    for i in dirlist:
        if i.find('csv') is not -1:
            if i.find('Bug_'+year+'_' ) is not -1:
                fileList.append(filedir+i)
    fileList.sort(reverse=True)
    if fileList!=[]:
        bugNameSet=set(bugName)
        exist=False
        for i in fileList:
            f = open(i,"r")
            nameline = f.readline().replace("\r\n","")
            nameline=nameline.replace("\n","")
            
            nameline = nameline.replace("Time,","")    
            nameline = nameline.split(",")
            datasplit = set(nameline)
            # print(i)
            lines = f.read().splitlines()
            last_line = lines[-1]
            last_line=last_line.replace("/r/n","") 
            last_line=last_line.replace("/n","")
            last_line=last_line.split(",")
            del last_line[0]
            beforeData = np.array(last_line,dtype=int)

            f.close()
            if datasplit == bugNameSet:
                exist=True
                break
        
        # There is no file with same bugs name.
        if exist == False or newFile == True :
            fileList.sort()
            #setting BugName

            fileList.sort()
            dirName = fileList[len(fileList)-1]

            dirName = dirName.replace(filedir,"")
            front = dirName[:9]
            num = dirName[9:].replace(".csv","")
            num = int(num)
            num = num+1
            dirName = front+ str(num)+".csv"
            dirName = filedir+dirName
            if platform.system() == "Windows":
                f = open(dirName,"a",newline="") 
            else :
                f = open(dirName,"a")
            fwriter = csv.writer(f)
            bugName.insert(0,"Time")
            fwriter.writerow(bugName)
        else:  
            data = np.array(data)
            data= beforeData+data
            dirName=i
            if platform.system() == "Windows":
                f= open(dirName,"a",newline="") 
            else :
                f= open(dirName,"a")
            fwriter=csv.writer(f)
    else:
        dirName = filedir + "Bug_"+year+"_0.csv"
        if platform.system() == "Windows":
            f= open(dirName,"a",newline="") 
        else :
            f= open(dirName,"a")    
        fwriter=csv.writer(f)
        bugName.insert(0,"Time")
        fwriter.writerow(bugName)

    nowTime = now.strftime('%m/%d %H:%M:%S')
    # print(data, nowTime)
    data = np.array(data)
    data=data.tolist()    
    data.insert(0,nowTime)
    # print(data)
    fwriter.writerow(data)
    f.close()
    
    
# data=[1,3,4,1,1234]
# bugName=["kim","Moo","alim","Jin","bzxv"]
# saveDataAsCsv(data,bugName)

