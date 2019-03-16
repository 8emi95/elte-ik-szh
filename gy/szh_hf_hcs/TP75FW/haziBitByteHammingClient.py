import sys, select
from client import Client
from framer import Framer

class HammingClient(Client):
    """ client """
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
    print "Parancssori parameter hianyzik!"
except ValueError: 
    client.close()
    print "Server full"