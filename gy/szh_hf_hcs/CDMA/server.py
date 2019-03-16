import socket

class Server:
    """ A server"""
    def __init__(self, host = 'localhost', port = 10000):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(1)

    def accept(self):
        return self.socket.accept()

    def close(self):
        return self.socket.close()