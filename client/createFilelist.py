import os
import hashlib

def getList(path, name, commit, date = 0):
    folderpath=os.path.abspath(path)
    listpath=os.listdir(folderpath)
    file_path=open("file_info.txt","w")
    file_path.write("%s@%s@%s\n"% (name, commit, str(date)))
    start=len(folderpath)
    writepath(folderpath,listpath, file_path)
    file_path.close()

def writepath(folderpath,listpath, file_path):
    for list in listpath:
        path = os.path.join(folderpath, list)
        tem = path
        mtime=str(os.path.getmtime(tem))
        if os.path.isfile(path):
            md5 = str(getmd5(path))
            file_path.write(path)
            file_path.write("|")
            file_path.write(mtime)
            file_path.write("|")
            file_path.write(md5)
            file_path.write("\n")
        elif len(os.listdir(path))==0:
            file_path.write(path)
            file_path.write("\\")
            file_path.write("|")
            file_path.write(mtime)
            file_path.write("\n")
        if os.path.isdir(path) and len(os.listdir(path))>0:
            writepath(tem,os.listdir(tem), file_path)
            file_path.write(path)
            file_path.write("\\")
            file_path.write("|")
            file_path.write(mtime)
            file_path.write("\n")



def getmd5(filename):
    m = hashlib.md5()
    mfile = open(filename, 'rb')
    m.update(mfile.read())
    mfile.close()
    md5value = m.hexdigest()
    return md5value
