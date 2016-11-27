# server send file
import struct
import hashlib
import os


class SendFileToServer(object):
    def __init__(self, sock, filepath):
        self.sock = sock
        self.HEAD_STRUCT = b'1024sIq32s'
        self.BUFFER_SIZE = 1024
        self.path = filepath

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
        client = self.sock
        try:
            print('Sending data....')
            file_name, file_head, file_size, fr = self.__get_file(self.path)
            print(file_name)
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
            fr.close()
            print("Send finish")
        finally:
            pass

