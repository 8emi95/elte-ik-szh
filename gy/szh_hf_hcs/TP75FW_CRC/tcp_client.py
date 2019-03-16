import socket, select, sys

from logger import Logger

#import pdb; pdv.set.trace() - debugging

class TcpClient(Logger):
    """ A TCP client """
    handlers = []

    def __init__(self, host = 'localhost', port = 10000, name = "TCP client", debug = False):
        Logger.__init__(self, debug)

        self.name = name
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "%s created, dont forget to connect!" % (self.name)
       
    def connect(self):
        self.socket.connect(self.address) 
        self.handlers = [self.socket, sys.stdin]
        print "%s is up and running" % (self.name)
        self.send(self.name)
        client.recv(1024)

    def close(self):
        self.log("(%s): closing the connection" % (self.name))
        return self.socket.close()

    def send(self, msg):
        self.log("(%s): sending: '%s'"  % (self.name, msg))
        return self.socket.send(msg)

    def recv(self, size):
        msg = self.socket.recv(size)
        self.log("(%s): received: '%s'"  % (self.name, msg))
        return msg

    def run(self):
        try:
            self.connect()
            while True:
                readable, writeable, ex = select.select(self.handlers, [], [])
                for r in readable:
                    if r == sys.stdin:
                        input = raw_input()
                        self.socket.send(input)
                        self.recv(1024)
        except Exception: 
            print "(%s): Error - can't connect to server!" % (self.name)

try:
    client = TcpClient('localhost', 10000, sys.argv[1])
    client.enableLogging()
    client.run()
except IndexError:
    print "Parancssori parameter hianyzik!"