import sys, select
from client import Client
from crypt import Crypt

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
    print "Parancssori parameter (kliens neve) hianyzik!"
except ValueError: 
    client.close()
    print "Server full"