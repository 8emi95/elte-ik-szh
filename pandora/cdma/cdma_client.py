import sys, select, socket

from crypt import Crypt

class Client(object):
    """ A client """
    def __init__(self, host = 'localhost', port = 10010):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)

    def close(self):
        return self.socket.close()

    def send(self, msg):
        self.socket.send(msg)

class CDMAClient(Client):
    """ A CDMA client """
    handlers = []
    chip = ''

    def __init__(self, name, host = 'localhost', port = 10000):
        Client.__init__(self, host, port)
        self.name = name
        self.crypt = Crypt()
        self.handlers = [self.socket, sys.stdin]

    def run(self):
        self.send(sys.argv[1])
        self.chip = self.socket.recv(1024)
        if self.chip == 'NNNN':
            raise ValueError()
        else:
            print 'client ' + self.name + ' got chip ' + self.chip

        while True:
            readable, writeable, ex = select.select(self.handlers, [], [])
            for r in readable:
                if r == sys.stdin:
                    input = raw_input().split(' ')
                    self.socket.send(input[0])
                    addresseeChip = self.socket.recv(1024)
                    self.socket.send(self.crypt.encrypt(addresseeChip, input[1]))
                else:
                    data = r.recv(1024)
                    print 'received: ' + self.crypt.decrypt(self.chip, data)

try:
    client = CDMAClient(sys.argv[1])
    client.run()
except IndexError:
    print "Missing commandline argument (client name)!"
except ValueError:
    client.close()
    print "Server full"