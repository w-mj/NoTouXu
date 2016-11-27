import socket
import struct

import file_receive_from_server
import file_send_to_server

command_list = {'login': 0, 'getRepo': 1, 'addRepo': 2, 'delRepo': 3, 'getDir': 4, 'requireHost': 5, 'getMyRepo': 6}

def command(sock, command):
    data = struct.pack(b'i', command_list[command])
    sock.send(data)

class Net(object):
    def __init__(self):
        self.username = ''
        self.password = ''
        self.localRepo = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote = ('127.0.0.1', 9999)
        self.sock.connect(self.remote)

    def login(self, username, password):
        command(self.sock, 'login')

        sdata = struct.pack(b'32s32s2i', username.encode(), password.encode(), len(username), len(password))
        self.sock.send(sdata)

        result = self.sock.recv(struct.calcsize(b'i'))
        result, = struct.unpack(b'i', result)
        return result

    def getRepo(self, target = 'all'):
        if target == 'all':
            command(self.sock, 'getRepo')
        else:
            command(self.sock, 'getMyRepo')
        n = self.sock.recv(struct.calcsize(b'i'))
        n, = struct.unpack(b'i', n)
        repoList = []
        for i in range(n):
            data = self.sock.recv(struct.calcsize(b'2if64s256s2i'))
            repoID, cotentID, data, name, commit, nn, nc = struct.unpack(b'2if64s256s2i', data)
            name = name[:nn]
            commit = commit[:nc]
            data = (repoID, cotentID, data, name.decode(), commit.decode())
            repoList.append(data)
        return repoList

    def delRepo(self, repoID):
        command(self.sock, 'delRepo')
        self.sock.send(struct.pack(b'I', repoID))

    def getDir(self, repoID):
        command(self.sock, 'getDir')
        self.sock.send(struct.pack(b'I', repoID))
        r = file_receive_from_server.ReceiveFileFromServer(self.sock)
        r.receive()

    def requireHost(self, repoID):
        command(self.sock, 'requireHost')
        self.sock.send(struct.pack(b'I', repoID))
        r = self.sock.recv(struct.calcsize(b'15s3i'))
        ip, potr, status, nip = struct.unpack(b'15s3i', r)
        ip = ip[:nip]
        if status == 2:
            return '000.000.000.000'
        else:
            return ip.decode()

    def addRepo(self, repoFilePath, contentID = 0):
        command(self.sock, 'addRepo')
        self.sock.send(struct.pack(b'I', contentID))
        s = file_send_to_server.SendFileToServer(self.sock, repoFilePath)
        s.send()
