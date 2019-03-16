import socket
import select
import sys

class Client(object):
    """ A client """
    def __init__(self, host = 'localhost', port = 10000):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)

    def close(self):
        return self.socket.close()

    def send(self, msg):
        self.socket.send(msg)