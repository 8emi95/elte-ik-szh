import socket

udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_address = ('localhost', 10002)
udpSock.bind(udp_address)

data, address = udpSock.recvfrom(4096)

print "Incoming message from", address
print "Message:", data

udpSock.sendto('Hello kliens', address)

