import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10001)

connection.connect(server_address)

connection.send('Hello szerver')

data  = connection.recv(4096)

print "Message:", data

connection.close()