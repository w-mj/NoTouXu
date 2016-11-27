import socket
import struct
import hashlib


class ReceiveFileFromServer(object):
    def __init__(self, sock):
        self.BUFFER_SIZE = 1024
        self.HEAD_STRUCT = b'1024sIq32s'
        self.sock = sock
        self.SAVE_PATH = ''

    def receive(self):
        savepath = self.SAVE_PATH
        sock = self.sock
        try:
            info_struct = struct.calcsize(self.HEAD_STRUCT)
            file_info = sock.recv(info_struct)
            # recive file head
            fname, fname_size, fsize, fmd5 = struct.unpack(self.HEAD_STRUCT, file_info)

            fname = fname.decode()
            fname = fname[:fname_size]
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
            print('File receive success')

            fw = open(fname, 'rb')
            md5 = hashlib.md5()
            md5.update(fw.read())
            if fmd5.decode() != md5.hexdigest():
                print('MD5 error')
            fw.close()
        finally:
            pass