import socket, select, sys

from logger import Logger
from client_store import ClientStore

class Proxy(Logger):
    """ A TCP to TCP proxy"""

    client_store = ClientStore()
    handlers = []

    def __init__(self, client_addr = ('localhost', 10000), server_addr = ('localhost', 10001), name = "TCP to TCP proxy", debug = False):
        Logger.__init__(self, debug)

        self.name = name
        self.address = client_addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # toplevel import... socket wtf?
        self.socket.bind(self.address)
        self.socket.listen(1)

        self.tcp_server_addr = server_addr
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.connect(self.tcp_server_addr)

        self.handlers = [self.socket, sys.stdin]
        print "%s is up and running" % (self.name)

    def accept(self):
        connection, address = self.socket.accept()
        name = connection.recv(1024)

        self.log("(%s): accepted connection: %s - %s" % (self.name, address, name))
        self.client_store.addClient(name, connection)
        self.handlers = [self.socket, sys.stdin] + self.client_store.getClientHandlers()
        return (connection, address)

    def close(self):
        self.log("(%s): closing the connection" % (self.name))
        for client in ClientStore.getClientHandlers():
            client.close()
        
        self.socket.close()
        self.tcp_server_socket.close()

    def handleClient(self, client):
        client_msg = client.recv(1024)
        self.log("(%s): received '%s' from %s" % (self.name, client_msg, self.client_store.getClientNameBySocket(client)))

        received_parity = client_msg[len(client_msg)-1]
        client_msg = client_msg [:len(client_msg)-1]
        parity = sum(int(x) for x in client_msg if x.isdigit()) % 2
        if received_parity == str(parity):
            self.tcp_server_socket.send(client_msg)
            response = self.tcp_server_socket.recv(1024)
            self.log("(%s): received '%s' from Store" % (self.name, response))
            client.send(response)
        else:
            self.log("Invalid parity")
            client.send("0")

    def run(self):
        while True:
            readable, writeable, ex = select.select(self.handlers, [], [])
            for handler in readable:
                if handler is sys.stdin:
                    self.close()
                elif handler is self.socket:
                    self.accept()
                else:
                    self.handleClient(handler)

proxy = Proxy()
proxy.enableLogging()
proxy.run()
