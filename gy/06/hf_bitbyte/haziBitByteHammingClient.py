import sys, select, socket

from framer import Framer

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

class HammingClient(Client):
    """ The client """
    framer = Framer()

    def __init__(self, mode, msg, host = 'localhost', port = 10000):
        Client.__init__(self, host, port)
        print 'mode: ' + mode
        print 'msg: ' + msg

        self.mode = mode
        self.msg = msg

    def run(self):
        self.send(self.mode + ' ' + self.framer.frame(self.msg, self.mode))
        self.close()

try:
    client = HammingClient(sys.argv[1], sys.argv[2])
    client.run()
except IndexError:
    print "Missing commandline argument!"
except ValueError:
    client.close()
    print "Server full"