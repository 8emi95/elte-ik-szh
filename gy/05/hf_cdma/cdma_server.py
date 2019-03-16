import select, sys, time, threading, socket

from collections import deque
from cdma_client_store import CDMAClientStore
from message_helper import MessageHelper

class Server:
    """ A server """
    def __init__(self, host = 'localhost', port = 10000):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(1)

    def accept(self):
        return self.socket.accept()

    def close(self):
        return self.socket.close()

class CDMAServer(Server):
    """ The CDMA server """
    store = CDMAClientStore()
    messageHelper = MessageHelper()

    handlers = []
    interferedMsg = ''
    msgLock = threading.Lock()

    def __init__(self, host = 'localhost', port = 10000): 
        Server.__init__(self, host, port)
        self.handlers = [self.socket, sys.stdin]

    def accept(self):
        client, addr = self.socket.accept()
        name = client.recv(1024)
        if self.store.getClientNum() >= 4:
            client.send('NNNN')
            client.close()
        else:
            client.send(self.store.addClient(name, client))
            self.handlers = [self.socket, sys.stdin] + self.store.getClientHandlers()

    def startDispatcher(self):
        t = threading.Timer(30.0, self.startDispatcher)
        t.daemon = True
        t.start()
        self.dispatchMsg()

    def dispatchMsg(self):
        self.msgLock.acquire()
        try:
            if self.interferedMsg and self.store.getClientHandlers():
                print 'dispatching message: ' + self.interferedMsg
            else:
                print 'no message or clients, restarting timer...'

            for client in self.store.getClientHandlers():
                client.send(self.interferedMsg)
            self.interferedMsg = ''
        finally:
            self.msgLock.release()

    def addMsg(self, msg):
        self.msgLock.acquire()
        try:
            if self.interferedMsg == '':
                self.interferedMsg = msg
            else:
                self.interferedMsg = self.messageHelper.interfere(self.interferedMsg, msg)
        finally:
            self.msgLock.release()

    def handleClient(self, handler):
        addressee = handler.recv(1024)
        if not addressee:
            self.store.remove(handler)
            handler.close()
        else:
            addresseeChip = self.store.getClientChipByName(addressee)
            if addresseeChip:
                handler.send(addresseeChip)
                self.addMsg(handler.recv(1024))

    def run(self):
        print 'server running'
        self.startDispatcher()

        while True:
            readable, writeable, ex = select.select(self.handlers, [], [])
            for handler in readable:
                if handler is sys.stdin:
                    self.close()
                elif handler is self.socket:
                    self.accept()
                else:
                    self.handleClient(handler)

server = CDMAServer()
server.run()