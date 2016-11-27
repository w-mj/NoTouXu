from tkinter import *


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.locale_list = Listbox(self, width=40, height=30)
        self.remote_list = Listbox(self, width=40, height=30)
        self.upload = Button(self, text='上传新目录')
        self.download = Button(self, text='同步此目录')

    def show_widgets(self):
        self.locale_list.grid(row=1, column=0, columnspan=2, rowspan=2)
        self.remote_list.grid(row=1, column=3, columnspan=2, rowspan=2)
        self.upload.grid(row=4, column=0)
        self.download.grid(row=4, column=3)

    def addItem(self, where, item):
        where.insert(END, item)




