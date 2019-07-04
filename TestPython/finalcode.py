from getColor import getColor2
from combined_code import classifyMoth




def combined_code (data,sizethreshold,hlist=[[0,180]],sup=254,sdown=1,vup=254,vdown=1
,Save=False,NumberofType=4,BugName=["1","2","3","4"]):


    datalist=getColor2(data,sizethreshold,hlist=hlist,sup=sup,sdown=sdown,vup=vup,vdown=vdown)
    a1,b1,c1=classifyMoth(datalist,Save,NumberofType,BugName)
    return a1,b1,c1