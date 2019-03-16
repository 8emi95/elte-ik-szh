import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10001)
udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_address = ('localhost', 10002)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the serverPort
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

connection, client_address = server.accept()

msgFromClient = connection.recv(4096)

print "Incoming message from", client_address
print "Message:", msgFromClient

udpSock.sendto(msgFromClient, udp_address)

msgFromServer, address = udpSock.recvfrom(4096)

print "Incoming message from", address
print "Message:", msgFromServer

connection.send(msgFromServer)

udpSock.close()
server.close()
connection.close()