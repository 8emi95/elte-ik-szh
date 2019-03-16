import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('localhost', int(sys.argv[1]))
#server_address = ('', 0)        #any interface, any port

sock.bind(server_address)

sock.listen(1)

connection, client_address = sock.accept()

data = connection.recv(16)

print data

connection.sendall('Hello kliens')
