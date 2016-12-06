import ui
import tkinter.filedialog
import tkinter
import threading
import createFilelist
import netserver
import file_send
import file_receive
import compare
import delete
import os

ip = ''
path = ''
done = False


def startSend(sock, caddress, path):
    s = file_send.SendFile(sock)
    s.changeA(os.getcwd())
    s.add_file(os.path.join(os.getcwd(), 'file_info.txt'))
    s.send()
    print('waiting for file List')
    s.clearFileList()
    s.changeA(path)
    s.getFileList()
    print(path)

    s.send()

def gui():
    uroot = tkinter.Tk()
    uroot.geometry('800x700')
    u = ui.Application(uroot)
    # u.show_widgets()

    global path
    global ip
    global done
    path = tkinter.filedialog.askdirectory()
    # ip = u.g()
    u.login()
    uroot.wait_window(u.msb)
    ip = u.ip
    print(ip)
    done = True
    u.mainloop()

if __name__ == '__main__':

    uis = threading.Thread(target=gui)
    uis.start()

    print('ding')
    n = netserver.Net()
    # 如果<发送>:发送文件列表

    while not done:
        pass
    print('Start progress')
    createFilelist.getList(path)  # 对path生产文件列表
    if ip == '':
        n.startServer()
        print('waiting for connect..')
        while True:
            csock, caddress = n.s.accept()
            print('connect success')
            ss = threading.Thread(target=startSend, args=(csock, caddress, path))
            ss.start()
    else:  # 接收文件
        r = file_receive.receiveFile((ip, 9876))
        r.setSavePath(os.getcwd())
        r.receive(1)
        cmf = compare.comp()
        downlist = cmf.md5mfile()
        cmf.md5ufile()
        delete.dele()
        for each in downlist:
            r.add_file(each)
        r.sendFileList()
        r.setSavePath(path)
        r.receive(len(downlist))
        print('File receive success!!!!!!!!')
