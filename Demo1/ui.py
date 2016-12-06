from tkinter import *
import socket

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.locale_list = Listbox(self, width=40, height=30)
        self.remote_list = Listbox(self, width=40, height=30)
        self.upload = Button(self, text='上传新目录')
        self.download = Button(self, text='同步此目录')
        self.msb = Toplevel(self)
        self.ip = ''
        self.flag = 0

    def show_widgets(self):
        self.locale_list.grid(row=1, column=0, columnspan=2, rowspan=2)
        self.remote_list.grid(row=1, column=3, columnspan=2, rowspan=2)
        self.upload.grid(row=4, column=0)
        self.download.grid(row=4, column=3)

    def addItem(self, where, item):
        where.insert(END, item)

    def getIP(self, ip1, ip2, ip3, ip4, msb):
        ip = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)
        msb.destroy()
        self.ip = ip

    def ps(self, a):
        self.flag = a

    def login(self):
        msb = self.msb
        msb.geometry('800x200')
        # bb1 = Button(msb)
        # bb2 = Button(msb)
        # bb1.config(text='发文件', command=lambda: self.ps(1))
        # bb2.config(text='收文件', command=lambda: self.ps(2))
        # bb1.grid(column=0)
        # bb2.grid(column=5)
        # while self.flag == 0:
        #    pass
        # bb1.destroy()
        # bb2.destroy()

        my_ip = socket.gethostbyname(socket.gethostname())
        print(my_ip)
        msb.attributes('-topmost', True)
        msb.positionfrom(who='program')
        mb0 = Message(msb)

        mb0.config(text='我的IP:')
        mb0.grid(row=0, column=0, columnspan=2, sticky='w')
        mb1 = Label(msb)
        mb1.config(text=my_ip)
        mb1.grid(row=0, column=2, columnspan=5, sticky='w')
        mb2 = Label(msb)
        mb2.config(text='输入对方IP地址:')
        mb2.grid(row=2, column=0, columnspan=20, sticky='w')
        e1 = Entry(msb)
        e2 = Entry(msb)
        e3 = Entry(msb)
        e4 = Entry(msb)
        d1 = Message(msb)
        d2 = Message(msb)
        d3 = Message(msb)
        d1.config(text='.')
        d2.config(text='.')
        d3.config(text='.')
        e1.grid(row=3, column=0)
        d1.grid(row=3, column=1)
        e2.grid(row=3, column=2)
        d2.grid(row=3, column=3)
        e3.grid(row=3, column=4)
        d3.grid(row=3, column=5)
        e4.grid(row=3, column=6)
        b1 = Button(msb)
        b2 = Button(msb)
        b1.config(text='OK', command=lambda: self.getIP(e1.get(), e2.get(), e3.get(), e4.get(), msb))
        b2.config(text='Cancel', command=msb.destroy)
        b1.grid(row=5, column=1)
        b2.grid(row=5, column=2)
        # msb.wait_window(msb)

