import csv
import numpy as np

def readData(fileList):
    filenum = len(fileList)
    openList = []
    lines = []
    for i in fileList:
        f=open(i,"r")
        openList.append(f)
        output = csv.reader(f)
        y = np.array([xi+[None]*(15-len(xi)) for xi in output])
        lines.append(y)
    f.close()
    k=0
    numberBugType=4
    numberColor=5
    dataset=[]
    for i in range(0,numberBugType):
        dataset.append([])
    for n,i in enumerate(lines):
        for j in i:
            colorset=[]
            for k in range(0,numberColor):
                colorset.append(j[k*3:k*3+3])
            dataset[n].append(colorset)

    for i in openList:
        i.close()
    return dataset

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