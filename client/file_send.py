# server send file
import struct
import socket
import hashlib
import os


class SendFile(object):
    def __init__(self, pathlist, address=('', 9998)):
        self.client_address = address
        self.file_path_list = pathlist
        self.HEAD_STRUCT = b'1024sIq32s'
        self.BUFFER_SIZE = 1024
        self. sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def add_file(self, path):
        self.file_path_list.append(path)

    def __start_server(self):
        self.sock.bind(self.client_address)
        self.sock.listen(5)
        print('service start success')
        return self

    def __connect(self):
        print('Waiting for connect...')
        client, client_address = self.sock.accept()
        print('Success connect to %s:%s' % (client_address[0], client_address[1]))
        n = client.recv(struct.calcsize(b'I'))
        n, = struct.unpack(b'I', n)
        for i in range(n):
            fname = client.recv(struct.calcsize(b'1024s'))
            fname, = struct.unpack(b'1024s', fname)
            self.add_file(fname)
        return client
        # Connect to client

    def __get_file(self, file_path):
        sp = file_path.split('\\')
        file_name = sp[-1]
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
        self.__start_server()
        client = self.__connect()
        file_count = struct.pack(b'I', len(self.file_path_list))

        try:
            client.send(file_count)
            print('Sending data....')
            for file_path in self.file_path_list:
                file_name, file_head, file_size, fr = self.__get_file(file_path)
                client.send(file_head)
                send_size = 0
                while send_size<file_size:
                    if file_size - send_size < self.BUFFER_SIZE:
                        file_data = fr.read(file_size - send_size)
                        send_size = file_size
                    else:
                        file_data = fr.read(self.BUFFER_SIZE)
                        send_size += self.BUFFER_SIZE
                    client.send(file_data)
                print('File send success.')
                fr.close()
            client.close()
            self.sock.close()
        finally:
            print("Closing connect")
            

if __name__ == '__main__':
    HOST = ''
    PORT = 9999
    # char fname[128], unsigned int fnamesize, long long fsize, char MD5[32]
    file_path = ['E:\\Downloads\\C++  Primer中文版  第5版 [（美）李普曼，（美）拉乔伊，（美）默著][电子工业出版社][2013.08][838页]_cropped.pdf',
                 'E:\\Downloads\\2068-Python之tkinter中文教程.pdf']
    s = SendFile(file_path)
    # print(s.file_size)
    s.send()
