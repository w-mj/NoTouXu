import socket
import struct
import hashlib

class receiveFile():
    def __init__(self, address, savepath = ''):
        self.BUFFER_SIZE = 1024
        self.HEAD_STRUCT = b'1024sIq32s'
        self.ADDR = address
        self.SAVE_PATH = savepath
        self.file_list = []

    def set_address(self, address):
        self.ADDR = address

    def add_file(self, file_path):
        self.file_list.append(file_path)

    def receive(self):
        address = self.ADDR
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(address)
            #print(struct.calcsize(b'i'))
            file_count = len(self.file_list)
            sock.send(struct.pack(b'I', file_count))
            for each in range(file_count):
                sock.send(struct.pack(b'1024s', self.file_list[each].encode()))

            info_struct = struct.calcsize(self.HEAD_STRUCT)

            for i in range(file_count):
                file_info = sock.recv(info_struct)
                # recive file head
                fname, fname_size, fsize, fmd5 = struct.unpack(self.HEAD_STRUCT, file_info)

                fname = fname.decode()
                fname = fname[:fname_size]
                fname = self.SAVE_PATH + '\\' + fname
                fw = open(fname, 'wb')

                recv_size = 0
                print('Receiving file...')
                while recv_size < fsize:
                    if fsize - recv_size < self.BUFFER_SIZE:
                        file_data = sock.recv(fsize - recv_size)
                        recv_size = fsize
                    else:
                        file_data = sock.recv(self.BUFFER_SIZE)
                        recv_size += self.BUFFER_SIZE
                    fw.write(file_data)
                fw.close()
                file_names.append(fname)

                print('File receive success')

                fw = open(fname, 'rb')
                md5 = hashlib.md5()
                md5.update(fw.read())
                if fmd5.decode() != md5.hexdigest():
                    print('MD5 error')
                fw.close()
            sock.close()
        finally:
            pass
        


if __name__ == '__main__':
    r = reciveFile(('127.0.0.1', 9999))
    r.receive()
