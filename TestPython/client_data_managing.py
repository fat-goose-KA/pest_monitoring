import os
import time
import sys
# client data: username/ password? / raspberrypi ip address



        

def main() :
    print("This is client information program")
    print("Choose and write which work to do")
    print("1:make account   2:delete account    3:change account information    4:show list")
    choice=raw_input()
    try:
        int_choice=int(choice)
        if (int_choice<1) or (int_choice>4):
            print("invalid choice. choose among 1,2,3,4")
            return 0
    except:
        print("invalid choice. choose among 1,2,3,4")
        return 0
    filedir=os.getcwd()
    strlen=len(filedir)
    filedir=os.getcwd()[0:strlen-11]+'/Client_data/'
    txt_name='client_data.txt'
    try:
        f = open(filedir+txt_name, 'r')
        lines=f.readlines()
        old_id_list=[]
        old_ip_list=[]
        for i in lines:
            # print(i)
            before_list=i.split('\n')
            # print(before_list)
            before_list=before_list[0].split('\t')  
            # print(before_list)
            old_id_list.append(before_list[0])
            old_ip_list.append(before_list[1])
        f.close()
    except:
        old_id_list=[]
        old_password_list=[]
        old_ip_list=[]

    if (int_choice==4):
        print(old_id_list)
        print(old_ip_list)
        return 0
    try:
        f = open(filedir+txt_name, 'a')
    except:
        f = open(filedir+txt_name,'w')
    if (int_choice==1):
        flag=False
        while flag==False:
            print("write id: ")
            id_trial=raw_input()
            if id_trial in old_id_list:
                print("already exist name. use other name")
                return 0
            id_retry=raw_input("for check, rewrite your id: ")
            if (id_retry==id_trial):
                flag=True
            else:
                print("do not corresponding trial")
        f.write(id_trial+'\t')
        flag2=False
        while flag2==False:
            ip_address=raw_input("write ip address: ")
            print("check again, is it right? "+ip_address)
            check=raw_input("if you checked, enter yes: ")
            if (check=="yes"):
                flag2=True
        f.write(ip_address+"\n")
        f.close()
        repo=filedir+id_trial+"/"
        if not os.path.isdir(repo):
            os.mkdir(repo)
            os.mkdir(repo+"MothData/")
            os.mkdir(repo+"ImageData/")            
            os.mkdir(repo+"NonBugData/")
            os.mkdir(repo+"Picture/")
            os.mkdir(repo+"Picture/MJPG")
            os.mkdir(repo+"TimeData")


        return 0
    elif((int_choice==2) or (int_choice==3)):
        if(int_choice==3):
            print("write id: ")
            id_login=raw_input()
            try:
                index=old_id_list.index(id_login)
                new_ip_add=raw_input("write new ip address: ")
                old_ip_list[index]=new_ip_add
            except:
                print("such id does not exist")     
                return 0
        if(int_choice==2):
            print("write id: ")
            id_login=raw_input()
            try:
                index=old_id_list.index(id_login)
                length=len(old_id_list)
                old_id_list[index]=old_id_list[length-1]
                old_ip_list[index]=old_ip_list[length-1]
                old_ip_list.pop()
                old_id_list.pop()
            except:
                print("such id does not exist")     
                return 0
        print("flag1")
        os.remove(filedir+txt_name)
        print("flag2")
        f = open(filedir+txt_name,'w')
        print("flag3")
        for i in range(len(old_id_list)):
            f.write(old_id_list[i]+'\t')
            f.write(old_ip_list[i]+'\n') 
        f.close()      
        return 0
flag3=True
while flag3==True:
    main()
    inputt=raw_input("if you want to exit, enter \"exit\"")
    if (inputt=="exit"):
        flag3=False