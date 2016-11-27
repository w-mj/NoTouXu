import socket
import threading
import user
from acitvies import *


def accept_user(user_sock, address):
    STRUCT_COMMAND = b'i'
    command_list = {'login': 0, 'getRepo': 1, 'addRepo': 2, 'delRepo': 3, 'getDir': 4, 'requireHost': 5, 'getMyRepo': 6}
    u = user.ConnectingUser()
    while True:
        command = user_sock.recv(struct.calcsize(STRUCT_COMMAND))
        #while not len(command):
         #   command = user_sock.recv(struct.calcsize(STRUCT_COMMAND))
        command, = struct.unpack(STRUCT_COMMAND, command)
        if command == command_list['login']:  # 登录
            login(user_sock, address, u)
        elif command == command_list['getRepo']:  # 获取库列表
            getRepo(user_sock)
        elif command == command_list['delRepo']:  # 删除一个库
            delRepo(user_sock, u)
        elif command == command_list['getDir']:  # 获取库中的文件列表
            getDir(user_sock)
        elif command == command_list['requireHost']:  # 请求目标主机
            requireHost(user_sock)
        elif command == command_list['addRepo']:  # 添加一个库
            addRepo(user_sock, u)
        elif command == command_list['getMyRepo']:  # 获得我的库列表
            getMyRepo(user_sock, u)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 9999))
    sock.listen(5)
    print('Wating for connect')
    while True:
        userSock, userAddress = sock.accept()
        print('Connect success')
        startService = threading.Thread(target=accept_user, args=(userSock, userAddress))
        startService.start()


if __name__ == '__main__':
    main()
