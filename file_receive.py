import socket
import struct
import hashlib

class reciveFile():
    def __init__(self, address, savepath = ''):
        self.BUFFER_SIZE = 1024
        self.HEAD_STRUCT = b'1024sIq32s'
        self.ADDR = address
        self.SAVE_PATH = savepath

    def set_address(self, address):
        self.ADDR = address

    def receive(self):
        address = self.ADDR
        savepath = self.SAVE_PATH
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(address)
            #print(struct.calcsize(b'i'))
            file_count_b = sock.recv(struct.calcsize(b'i'))

            file_count = struct.unpack(b'i', file_count_b)
            file_names = []

            info_struct = struct.calcsize(self.HEAD_STRUCT)

            for i in range(file_count[0]):
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
