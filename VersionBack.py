#!/usr/bin/python
import os,sys
date=sys.argv[1]+"24:00:00"
allProjectPath=[]
pwd=os.getcwd();
def copyFile(dir):
    com="cat "+dir+">"+dir+".tmp"
    os.system(com)
    com=dir+".tmp"
    Path=""
    SrcDest=[]
    try:
        file = open(com)
    except Exception,e:
        print e
        print "\n"
        return 0

    while 1:
        line=file.readline()
        if line:
            L=[]
            L=line.split()
            if len(L)!=0:
                if L[0]=="<project":
                    Path=L[1].split('"')[1]
                elif L[0]=="<copyfile":
                    KK=[]
                    KK.append(L[1].split('"')[1])
                    KK.append(L[2].split('"')[1])
                    SrcDest.append(KK)
        else:
            break
    file.close()
    comd="rm "+com
    os.system(comd)
    print Path
    for i in SrcDest:
        Src=Path+"/"+i[0]
        Dest=i[1]
        comd="sudo cp "+Src+" "+Dest
        os.system(comd) 
    return 1

def getProjectPath(dir):
    com="cat "+dir+">"+dir+".tmp"
    os.system(com)
    com=dir+".tmp"
    file = open(com)
    while 1:
        line = file.readline()
        if line:
            L=[]
            L=line.split()
            if len(L)!=0:
               if L[0]=="<project":
                  LL=[]
                  LL=L[1].split('"')
                  allProjectPath.append(LL[1])
        else:
            break
    file.close();
    comd="rm "+com
    os.system(comd);

def attemptChDir():
    for l in allProjectPath:
        com=pwd+"/"+l
        try:
            os.chdir(com)
        except Exception,e:
            print e
            print "\n"
            print "No "+com+" repo please download\n"
            return 0
    return 1


def versionBack(dir):
    dir=pwd+"/"+dir
    os.chdir(dir)
    os.system("git log --pretty=format:'%ai %H' > log_tmp")
    LogList=[]
    file = open ("log_tmp")
    while 1:
        line = file.readline()
        if line:
             L=[]
             L=line.split()
             LogLine=[]
             LogLine.append(L[0]+L[1])
             LogLine.append(L[3])
             LogList.append(LogLine)
        else:
            break
    LogList.sort()
    LogList.reverse()
    for l in LogList:
        if l[0]<=date:
            print "\n"
            print "==================================================================================="
            print "|   Reset "+dir+" to "+l[0]+" |"                                                 
            print "==================================================================================="
            print "\n"
            com = "git reset --hard "+l[1]
            os.system(com)
            break
    file.close()
    comd="rm log_tmp"
    os.system(comd)
    os.chdir(pwd)

def Init():
    cdir0=".repo/manifests"
    versionBack(cdir0)
    cdir=[]
    cdir1=os.getcwd()+"/.repo/manifests/"+sys.argv[2]+".xml"
    cdir2=os.getcwd()+"/.repo/manifests/internal/_gaia.xml"
    cdir3=os.getcwd()+"/.repo/manifests/internal/_prebuilts.xml"
    cdir4=os.getcwd()+"/.repo/manifests/internal/_external.xml"
    cdir5=os.getcwd()+"/.repo/manifests/internal/_device.xml"
    cdir.append(cdir1)
    cdir.append(cdir2)
    cdir.append(cdir3)
    cdir.append(cdir4)
    cdir.append(cdir5)
    for i in cdir:
        getProjectPath(i)

def main():
    Init()
    if attemptChDir()==1:
        for i in allProjectPath:
            versionBack(i)
        print "\n"
        print "============================================================="
        print "|             Congratulation VersionBack Success            |"
        print "============================================================="
    else:
        print "\n"
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        print "X             I am sorry VersionBack Unsuccess               X"
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        return 0 
    cdir1=pwd+"/.repo/manifests/"+sys.argv[2]+".xml"
    if copyFile(cdir1)==1:    
        print "============================================================="
        print "|             CopyFile OK  Now you can build                |"
        print "============================================================="
    else:
        print "============================================================="
        print "|     CopyFile Failed  Please do it by yourself              |"
        print "============================================================="

main()
