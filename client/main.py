import client_net_module
from ui import *
from file_send import *
from file_receive import *
from delete import *
from compare import *
from createFilelist import *
import threading


def send():
    s = SendFile('test')
    s.send()


def getDownLoadRepo():
    x = len(remoteList)
    for i in range(x):
        if app.remote_list.selection_includes(i):
            c = comp()
            n.getDir(remoteList[i][0])
            file_name = str(remoteList[i][0]) + '_' + str(remoteList[i][1])
            ip = n.requireHost(remoteList[i][0])
            print(ip)
            c.md5mfile(file_name)
            c.md5ufile(file_name)
            delete().dele()
            fo = open('file_diffdown.txt', 'r')
            rec = receiveFile((ip,9998), 'E:/test')
            for line in fo:
                if len(line) == 0:
                    continue
                if line[-1] == '\n':
                    line = line[:len(line) - 1]
                rec.add_file(line)
            rec.receive()

            print(ip)
            return 0

def upload():
    localRepo = open('local.txt', 'r')
    r_contentID = int(input())
    r_path = input()
    r_name = input()
    r_commit = input()
    n.addRepo(r_path, r_contentID)

root = Tk()
root.geometry('800x700')
app = Application(root)
n = client_net_module.Net()
sf = SendFile('')
n.login('xxxx', 'xxxx')
getList('test', 'Test', 'A test directory')
#n.delRepo(79)
#n.addRepo('file_info.txt', 6)
localeList = n.getRepo('me')
remoteList = n.getRepo('all')


app.download.config(command=getDownLoadRepo)
app.upload.config(command=upload)
for each in localeList:
    app.addItem(app.locale_list, each[3])
for each in remoteList:
    app.addItem(app.remote_list, each[3])

sendf = threading.Thread(target=send)
sendf.start()

app.show_widgets()
root.mainloop()
