import socket


class Net():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def startServer(self):
        self.s.bind(('', 9876))
        self.s.listen(5)
        return self
