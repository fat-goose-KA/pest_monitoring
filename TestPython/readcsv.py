import os
import csv
import numpy as np


def readData(fileList):
    # set the number of file
    filenum = len(fileList) 
    
    # set the initial value
    # openList is the list that has the opened files.
    # lines is the list that has one nparrays for each files.    
    openList = []
    lines = []

    # Save the data in the openList and lines.
    for i in fileList:
        f=open(i,"r")
        openList.append(f)
        x = csv.reader(f)
        xlist=[]
        for j in x:
            if j!=[]:
                xlist.append(j)

        # change the list of list to nparray
        y = np.array([xi+[None]*(15-len(xi)) for xi in xlist])
        lines.append(y)

    # close the file
    for i in openList:
        i.close()

    # return the list 
    return lines

#save file
def saveData(data, clusterNum,dirName=os.getcwd()):

    # Set the file dierectory
    k=clusterNum+1
    if k<10:
        openFileName = dirName +"/MothData/MothData" +"0" + str(k) + ".csv"
    else:
        openFileName = dirName +"/MothData/MothData" + str(k) + ".csv"
    f=open(openFileName, 'a')#,newline='')
    
    wr = csv.writer(f)
    # Conver the data to one row data.
    output=[]
    for i in data:
        for j in i:
            print(j)
            output.append(j)

    # Write the data to a file.
    wr.writerow(output)
    

    f.close()   