import csv
import numpy as np

def readData(fileList):
    filenum = len(fileList) 
    openList = []
    lines = []
    for i in fileList:
        f=open(i,"r")
        openList.append(f)
        x = csv.reader(f)
        xlist=[]
        for j in x:
            xlist.append(j)
        print("=================")
        print(xlist)
        print("=================")
        y = np.array([xi+[None]*(15-len(xi)) for xi in xlist])
        lines.append(y)

    for i in openList:
        i.close()
    return lines

#파일 저장
def saveData(data, clusterNum):
    dirName = "C:/Users/master/Desktop/20190629/Smarf/MothData/Mothdata"
    k=clusterNum+1
    if k<10:
        openFileName = dirName + "0" + str(k) + ".csv"
    else:
        openFileName = dirName + str(k) + ".csv"
    print("================")
    print(k)
    print("================")
    print(openFileName)
    print("================")

    f=open(openFileName, 'a')
    wr = csv.writer(f)
    output=[]
    for i in data:
        for j in i:
            print(j)
            output.append(j)
    print(output)
    wr.writerow(output)
    

    f.close()   