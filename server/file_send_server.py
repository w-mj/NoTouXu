# server send file
import struct
import hashlib
import os


class SendFile(object):
    def __init__(self, user_sock):
        self.HEAD_STRUCT = b'1024sIq32s'
        self.BUFFER_SIZE = 1024
        self.client = user_sock
        self.file_path_list = []

    def add_file(self, path):
        self.file_path_list.append(path)

    def __get_file(self, file_path):
        print(file_path)
        sp = file_path.split('\\')
        file_name = sp[-1]
        file_size = os.path.getsize(file_path)
        # print('Calculating MD5...')

        fr = open(file_path, 'rb')
        md5 = hashlib.md5()
        md5.update(fr.read())
        fr.close()
       # print('Calculation success \n%s\n' % md5.hexdigest())
        # Calculate MD5
        fr = open(file_path, 'rb')
        file_head = struct.pack(self.HEAD_STRUCT, file_name.encode(), len(file_name), file_size,
                                md5.hexdigest().encode())
        return file_name, file_head, file_size, fr

    def send(self):
        try:
            for file_path in self.file_path_list:
                file_name, file_head, file_size, fr = self.__get_file(file_path)
                self.client.send(file_head)
                send_size = 0
                while send_size<file_size:
                    if file_size - send_size < self.BUFFER_SIZE:
                        file_data = fr.read(file_size - send_size)
                        send_size = file_size
                    else:
                        file_data = fr.read(self.BUFFER_SIZE)
                        send_size += self.BUFFER_SIZE
                    self.client.send(file_data)
                # print('File send success.')
                fr.close()
        finally:
            pass
