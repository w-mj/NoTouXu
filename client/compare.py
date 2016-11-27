import os
import time
import hashlib

class comp(object):
    def md5mfile(self, file):
        f = open('file_info.txt', 'r')  # 文件为1.txt
        g = open(file, 'r')  # 网络md5文件假设为2.txt
        f.readline()
        g.readline()
        localLines = f.readlines()  # 按行读出文件内容
        interlines = g.readlines()
        f.close()
        g.close()
        loc = []
        inte = []
        down = []
        up = []
        for line in localLines:
            temp1 = line.strip('\n')  # 去掉每行最后的换行符'\n'
            temp1 = temp1.split('|')
            try:
                loc.append(temp1[2])  # 添加到new
            except:
                loc.append(temp1[0])
        for line in interlines:
            temp2 = line.strip('\n')
            temp2 = temp2.split('|')
            inte.append(temp2)
            try:
                if temp2[2] not in loc:
                    temp2[1] = time.ctime(float(temp2[1]))
                    down.append(temp2[:2])  # 网上有而我没有
            except:
                if temp2[0] not in loc:
                    temp2[1] = time.ctime(float(temp2[1]))
                    down.append(temp2[:2])
        q = open('file_diffdown.txt', 'w')
        q.write("\n")
        le = []
        for le in down:
            le[0] = le[0].split('test')[-1]
            q.write(le[0])
            #q.write('|')
            #q.write(le[1])
            q.write('\n')
        q.close()

    def md5ufile(self, file):
        f = open('file_info.txt', 'r')  # 文件为1.txt
        g = open(file, 'r')  # 网络md5文件假设为2.txt
        f.readline()
        g.readline()
        localLines = f.readlines()  # 按行读出文件内容
        interlines = g.readlines()
        f.close()
        g.close()
        loc = []
        inte = []
        down = []
        up = []
        for line in interlines:
            temp2 = line.strip('\n')
            temp2 = temp2.split('|')
            try:
                inte.append(temp2[2])
            except:
                inte.append(temp2[0])
        for line in localLines:
            temp3 = line.strip('\n')
            temp3 = temp3.split('|')
            try:
                if temp3[2] not in inte:
                    temp3[1] = time.ctime(float(temp3[1]))
                    up.append(temp3[:2])
            except:
                if temp3[0] not in inte:
                    temp3[1] = time.ctime(float(temp3[1]))
                    up.append(temp3[:2])
        q = open('file_diffdelete.txt', 'w')
        q.write("\n")
        le = []
        for le in up:
            q.write(le[0])
            q.write('|')
            q.write(le[1])
            q.write('\n')
        q.close()
