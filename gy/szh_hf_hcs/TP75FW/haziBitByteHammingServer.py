import select, sys

from server import Server
from framer import Framer

class HammingServer(Server):
    """ The server """
    handlers = []
    framer = Framer()
    
    def __init__(self, host = 'localhost', port = 10000): 
        Server.__init__(self, host, port)
        self.handlers = [self.socket, sys.stdin]

    def _accept(self):
        client, addr = self.socket.accept()
        self.handlers = [self.socket, sys.stdin, client]
    
    def _handleClient(self, client):
        msg = client.recv(1024).split(' ')
        print 'server received mode:' + msg[0]
        print 'server received msg:' + msg[1]
        print 'decoded msg: ' + self.framer.unframe(msg[1], msg[0])
        client.close()
        self.handlers = [self.socket, sys.stdin]

    def run(self):
        print 'server running'
        while True:
            readable, writeable, ex = select.select(self.handlers, [], [])
            for handler in readable:
                if handler is sys.stdin:
                    self.close()
                elif handler is self.socket:
                    self._accept()
                else:
                    self._handleClient(handler)

                
server = HammingServer()
server.run()