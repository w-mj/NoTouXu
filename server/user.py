import os


class ConnectingUser(object):
    def __init__(self):
        self.connecting = False
        self.name = ''
        self.password = ''
        self.address = ()
        self.repo = []
        self.ip = ''
        self.port = 0

    def set_info(self, username, password, useraddress):
        self.name = username.decode()
        self.password = password.decode()

        self.address = useraddress
        self.ip = useraddress[0]
        self.port = useraddress[1]

    def remove_repo(self, repoID):
        self.repo.remove(repoID)
        self.__update__file()

    def add_repo(self, repoID, contentID):
        self.repo.append(str(repoID) + '_' + str(contentID))
        self.__update__file()

    def __update__file(self):
        current = os.getcwd()
        os.chdir('users')
        fw = open(self.name+'.txt', 'w')
        for each in self.repo:
            fw.write(each)
            fw.write('\n')
        os.chdir(current)

    def __get_data(self):
        current = os.getcwd()
        os.chdir('users')
        fr = open(self.name + '.txt', 'r')
        for each in fr:
            if each[-1] == '\n':
                each = each[:len(each) - 1]
            self.repo.append(each)
        os.chdir(current)

    def login(self):  # 返回1为登录成功，2为密码错误，3为无此用户, 4为已经登录
        fr = open('userlist.txt', 'r')
        print("## start login")

        username = ''
        password = ''
        for line in fr:
            sp = line.split(' ')
            username = sp[0]
            if username == self.name:
                password = sp[1]
                break

        if username == self.name:
            if password == self.password:
                self.__get_data()
                self.connecting = True
                return 1
            else:
                return 2
        else:
            return 3

    def new_account(self):
        fw = open('userlist.txt', 'a')
        number_of_user = 0
        for line in fw:
            number_of_user += 1
        fw.write("%s %s %d" % (self.name, self.password, number_of_user))


class Repository(object):
    def __init__(self):
        pass


class Communication(object):
    def __init__(self):
        pass


