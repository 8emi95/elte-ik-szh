import socket

from time import sleep
from logger import Logger
from haziCRCCalculator import HaziCRCCalculator

class UdpServer(Logger):
    """ A UDP server"""

    crcCalc = HaziCRCCalculator()

    def __init__(self, host = 'localhost', port = 10005, name = "UDP server", debug = False):
        Logger.__init__(self, debug)

        self.name = name
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP -> SOCK_DGRAM
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        socket.setdefaulttimeout(1)
        print "%s is up and running" % (self.name)

    def close(self):
        self.log("(%s): closing the connection" % (self.name))
        return self.socket.close()

    def recv(self, size):
        data, client_addr = server.socket.recvfrom(size)
        self.log("(%s): received: '%s'" % (self.name, data))
        errorInData = self.crcCalc.getAsInt(self.crcCalc.getRemainder(data, self.crcCalc.generator)) != 0
        if errorInData:
            print "(%s): CRC checksum failed --> error" % (self.name)
        else:
            print "(%s): CRC checksum OK" % (self.name)
        return (data, client_addr)

    def send(self, msg, target):
        self.log("(%s): sending: '%s' to target: '%s'" % (self.name, msg, target))
        return self.socket.sendto(msg, target)

server = UdpServer('localhost', 10007)
server.enableLogging()
while True:
    try:
        data, addr = server.recv(1024)
        server.send("OK", addr)
    except socket.timeout:
        continue