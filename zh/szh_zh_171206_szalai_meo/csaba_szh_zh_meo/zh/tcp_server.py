import socket

from logger import Logger

class TcpServer(Logger):
    """ A TCP server"""
    store = {
        0: {"name": "kocka",     "stock": 10},
        1: {"name": "kerek",     "stock": 11},
        2: {"name": "hangszoro", "stock": 12},
        3: {"name": "elem",      "stock": 13},
        4: {"name": "kijelzo",   "stock": 14},
    }

    def __init__(self, host = "localhost", port = 10001, name = "TCP server", debug = False):
        Logger.__init__(self, debug)

        self.name = name
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(1)
        print "%s is up and running" % (self.name)

    def accept(self):
        connection, client_address = self.socket.accept()
        self.log("(%s): accepted connection: %s" % (self.name, client_address))
        return (connection, client_address)

    def close(self):
        self.log("(%s): closing the connection" % (self.name))
        return self.socket.close()

    def send(self, connection, msg):
        self.log("(%s): sending: %s"  % (self.name, msg))
        return connection.send(msg)

    def recv(self, connection, size):
        msg = connection.recv(size)
        self.log("(%s): received: %s"  % (self.name, msg))
        return msg

    def run(self):
        connection, addr = server.accept()
        while True:
            try:
                msg = connection.recv(1024)
                self.log("(%s): received: %s"  % (self.name, msg))
                if len(msg) > 5:
                    raise ValueError("invalid message")
                
                everythingPresent = True
                for i in range(len(msg)):
                    self.log("store manager requested: %s pcs of %s, in stock %d" % (msg[i], self.store[i]["name"], self.store[i]["stock"]))
                    everythingPresent = everythingPresent and self.store[i]["stock"] >= int(msg[i])
                if everythingPresent:
                    for i in range(len(msg)):
                        self.store[i]["stock"] -= int(msg[i])
                        self.log("decreasing amount of: %s with %s, remained in stock %d" % (self.store[i]["name"], msg[i], self.store[i]["stock"]))
                    connection.send("1") # OK
                else:
                    connection.send("-1") # Cannot fulfill
            except socket.timeout:
                continue
            except ValueError:
                connection.send("0") # error

server = TcpServer()
server.enableLogging()
server.run()
