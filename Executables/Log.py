#-*- encoding:UTF-8 -*-
import os,sys,time,re

allpacklist={}

def logpatch():
    path=os.path.join(os.getcwd(),'Logs')
    packlist = os.popen('adb shell getprop ro.build.display.id')
    b= packlist.read()
    list = b.replace('\n','')
    list = list.split('-')
    title = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    title = title.replace(' ','-')
    title = title.replace(':','-')
    newpath = os.path.join(path,os.path.join(list[0],title))
    if not os.path.isdir(newpath):
        os.makedirs(newpath)
    return newpath

def filterPack(command):
    newlist=[]
    packlist = os.popen(command)
    b= packlist.read()
    if b==[]:
        newlist=[]
    else:
        pat = re.compile('\s+')
        list = re.sub(pat," ",b).split(' ')
        for pack in list:
            re.findall( r'^[A-Z]' , pack)
            if re.findall( r'^[A-Z]' , pack ) :
                newlist.append(pack)
                newlist.sort()
    return newlist

def clearpackage(command):
    cleralist=[]
    datalist = os.popen(command)
    b= datalist.read()
    if b==[]:
        cleralist=[]
    else:
        pat = re.compile('\s+')
        list = re.sub(pat," ",b).split(' ')
        for datanum in list:
            datanum=datanum.replace('package:','')
            cleralist.append(datanum)
            if datanum =='android':
                cleralist.remove(datanum) 
    return cleralist

def cleardata(command):
    cleralist=[]
    datalist = os.popen(command)
    b= datalist.read()
    if b==[]:
        cleralist=[]
    else:
        pat = re.compile('\s+')
        list = re.sub(pat," ",b).split(' ')
        for datanum in list:
            cleralist.append(datanum)
            if datanum =='data':
                cleralist.remove(datanum)
            elif datanum =='user':
                cleralist.remove(datanum)
            elif datanum =='app-regional':
                cleralist.remove(datanum)   
    return cleralist

def dirlist():
    newlist=filterPack('adb shell ls /system/vendor')
    allpacklist['vendor']=newlist
    newlist=[]
    newlist=filterPack('adb shell ls /oem')
    allpacklist['oem']=newlist
    return allpacklist


def checkadb():
    deviceid=os.popen('adb get-serialno').read()
    deviceid = deviceid.replace('\n','')
    while deviceid =='':
        os.system('adb kill-server')
        time.sleep(5)
        os.system('adb start-server')
        deviceid=os.popen('adb get-serialno').read()
        deviceid = deviceid.replace('\n','')

