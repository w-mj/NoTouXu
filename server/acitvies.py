from repository import *
from file_send_server import *
from file_receive_server import *
from user import *
import struct

accepted_users = []  # 储存已经连接到服务器的用户，每一个元素为一个ConnectingUser类


def belong(target, source):
    for each in target:
        #print('1')
        each = each.split('_')
        #print(type(each[0]), type(source))
        if int(each[0]) == source:
            return True
    return False


def login(user_sock, address, u):
    userinfo = user_sock.recv(struct.calcsize(b'32s32s2i'))  # 接收用户信息
    name, psd, nn, np = struct.unpack(b'32s32s2i', userinfo)
    name = name[:nn]
    psd = name[:np]
    isLogined = False
    u.set_info(name, psd, address)
    print(accepted_users)
    for each in accepted_users:
        if each.name == u.name:
            isLogined = True
    if not isLogined:
        result = u.login()  # 登录
    else:
        result = 4
    ret_value = struct.pack(b'i', result)  # 获得返回值，# 返回1为登录成功，2为密码错误，3为无此用户, 4为已经登录
    user_sock.send(ret_value)  # 把返回值发送回客户端
    if result != 1:
        return result
    else:
        accepted_users.append(u)  # 把登录的用户添加到表里


def getRepo(user_sock, range = all):
    repository = Repo()
    if range == all:
        repoList = repository.getall()  # 获取库列表
    else:
        repoList = range
    user_sock.send(struct.pack('I', len(repoList)))  # 发送列表长度
    current = os.getcwd()
    os.chdir('repository')
    for each in repoList:
        print(len(repoList))
        if each[-1] == '\n':
            each = each[:len(each) - 1]
        fr = open(each, 'r')
        text = fr.readline()
        name, commit, date = text.split('@')
        repoID, contentID = each.split('_')  # 发送每一个库
        sendData = struct.pack(b'2if64s256s2i', int(repoID), int(contentID), float(date), name.encode(), commit.encode(), len(name), len(commit))
        user_sock.send(sendData)
    os.chdir(current)


def getMyRepo(user_sock, u):
    getRepo(user_sock, u.repo)


def delRepo(user_sock, u):
    # getRepo(user_sock, u.repo)  #向客户端发送自己的库
    repoID = user_sock.recv(struct.calcsize(b'I'))  # 接收要删除的库ID
    repoID, = struct.unpack(b'I', repoID)
    repository = Repo()
    allrepo = repository.getall()
    print(allrepo)
    p = ''
    for i in allrepo:
        if str(repoID) == i.split('_')[0]:
            print(i.split('_')[0])
            p = i
            break
    current = os.getcwd()


    os.chdir('repository')
    os.remove(p)
    os.chdir(current)
    u.remove_repo(p)


def getDir(user_sock):
    repoID = user_sock.recv(struct.calcsize(b'I'))  # 获得请求的库ID
    target, = struct.unpack(b'I', repoID)
    repository = Repo()
    repoList = repository.getall()  # 获得全部库列表
    repoFile = ''
    for each in repoList:
        repoID, contentID= each.split('_')

        if repoID == str(target):
            repoFile = each  # 找到库ID的文件名

    sf = SendFile(user_sock)  # 把相应的文件发送至客户端
    print(repoFile)
    sf.add_file('repository\\' + repoFile)
    sf.send()


def requireHost(user_sock):
    repoID = user_sock.recv(struct.calcsize(b'I'))  # 获得请求的库ID
    target, = struct.unpack(b'I', repoID)
    print(target)
    for i in range(len(accepted_users)):
        print(accepted_users[i].repo)
        if belong(accepted_users[i].repo, target):  # 如果请求的库ID属于某个在线用户，返回该用户的地址
            retData = struct.pack(b'15s3i', accepted_users[i].ip.encode(), accepted_users[i].port, 1, len(accepted_users[i].ip))
            user_sock.send(retData)
            return 0
    retData = struct.pack(b'15s3i', b'000.000.000.000', 0, 2, 0)  # 用户不在线
    user_sock.send(retData)


def addRepo(user_sock, u):  # 添加库
    contentID = user_sock.recv(struct.calcsize(b'I'))  # 接收内容ID，
    contentID, = struct.unpack(b'I', contentID)
    repository = Repo()
    if contentID == 0:
        repoID, contentID = repository.getCount()  # 如果内容ID为0， 则分配内容ID
        repoID += 1
        contentID += 1
    else:
        repoID, ding = repository.getCount()
        repoID += 1
    # retData = struct.pack(b'2I', repoID, contentID)
    # user_sock.send(retData)
    re = reciveFile(user_sock, 'repository', str(repoID)+'_'+str(contentID))  # 接收数据
    u.add_repo(repoID, contentID)
    re.receive()
