import socket, select, sys

from logger import Logger
from client_store import ClientStore
from haziCRCCalculator import HaziCRCCalculator

class Proxy(Logger):
    """ A UDP to TCP proxy"""

    client_store = ClientStore()
    handlers = []
    crcCalc = HaziCRCCalculator()

    def __init__(self, client_addr = ('localhost', 10000), server_addr = ('localhost', 10001), name = "UDP to TCP proxy", debug = False):
        Logger.__init__(self, debug)

        self.name = name
        self.address = client_addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(1)

        self.udp_server_address = server_addr
        self.udp_server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.handlers = [self.socket, sys.stdin]
        print "%s is up and running" % (self.name)

    def accept(self):
        connection, address = self.socket.accept()
        name = connection.recv(1024)
        connection.send("OK")

        self.log("(%s): accepted connection: %s - %s" % (self.name, address, name))
        self.client_store.addClient(name, connection)
        self.handlers = [self.socket, sys.stdin] + self.client_store.getClientHandlers()
        return (connection, address)

    def close(self):
        self.log("(%s): closing the connection" % (self.name))
        for client in ClientStore.getClientHandlers():
            client.close()
        
        self.socket.close()
        self.udp_server_sock.close()

    def handleClient(self, client):
        client_msg = client.recv(1024)
        self.log("(%s): received '%s' from %s" % (self.name, client_msg, self.client_store.getClientNameBySocket(client)))
        self.udp_server_sock.sendto(self.crcCalc.getWithCrc(client_msg), self.udp_server_address)
        response, addr = self.udp_server_sock.recvfrom(1024)
        self.log("(%s): received '%s' from %s" % (self.name, response, self.udp_server_address))
        client.send(response)

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
