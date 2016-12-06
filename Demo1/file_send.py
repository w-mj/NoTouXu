# server send file
import struct
import socket
import hashlib
import os


class SendFile(object):
    def __init__(self, sock):
        self.sock = sock
        self.file_path_list = []
        self.HEAD_STRUCT = b'1024sIq32s'
        self.BUFFER_SIZE = 1024
        self.absultePathL = 0
        self.sendPath = ''

    def add_file(self, path):
        self.file_path_list.append(path)

    def clearFileList(self):
        self.file_path_list = []

    def changeA(self, abp):
        self.sendPath = abp
        self.absultePathL = len(abp)


    def getFileList(self):

        n = self.sock.recv(struct.calcsize(b'I'))
        n, = struct.unpack(b'I', n)
        for i in range(n):
            fname= self.sock.recv(struct.calcsize(b'1024sI'))
            fname, nameLength  = struct.unpack(b'1024sI', fname)
            fname = fname.decode()
            fname = fname[:nameLength]
            fname = self.sendPath + fname
            self.add_file(fname)


        return self.sock
        # Connect to client

    def __get_file(self, file_path):

        # sp = file_path.split(self.absultePathL)

        file_name = file_path[self.absultePathL + 1:]
        print(file_path)
        file_path = os.path.abspath(file_path)

        file_size = os.path.getsize(file_path)
        print('Calculating MD5...')
        fr = open(file_path, 'rb')
        md5 = hashlib.md5()
        md5.update(fr.read())
        fr.close()
        print('Calculation success \n%s\n' % md5.hexdigest())
        # Calculate MD5
        fr = open(file_path, 'rb')
        file_head = struct.pack(self.HEAD_STRUCT, file_name.encode(), len(file_name), file_size,
                                md5.hexdigest().encode())
        return file_name, file_head, file_size, fr

    def send(self):

        client = self.sock
        #self.getFileList()
        file_count = struct.pack(b'I', len(self.file_path_list))

        try:
            #client.send(file_count)
            print('Sending data....')
            for file_path in self.file_path_list:
                if not os.path.isfile(file_path):
                    continue
                file_name, file_head, file_size, fr = self.__get_file(file_path)
                print('sending %s' % file_name)
                client.send(file_head)
                send_size = 0
                while send_size < file_size:
                    if file_size - send_size < self.BUFFER_SIZE:
                        file_data = fr.read(file_size - send_size)
                        send_size = file_size
                    else:
                        file_data = fr.read(self.BUFFER_SIZE)
                        send_size += self.BUFFER_SIZE
                    client.send(file_data)
                print('File send success.')
                fr.close()
        finally:
            pass
            

if __name__ == '__main__':
    HOST = ''
    PORT = 9999
    # char fname[128], unsigned int fnamesize, long long fsize, char MD5[32]
    file_path = ['E:\\Downloads\\C++  Primer中文版  第5版 [（美）李普曼，（美）拉乔伊，（美）默著][电子工业出版社][2013.08][838页]_cropped.pdf',
                 'E:\\Downloads\\2068-Python之tkinter中文教程.pdf']
    s = SendFile(file_path)
    # print(s.file_size)
    s.send()
