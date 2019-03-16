import socket
import struct

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("localhost", 10001)
connection.connect(server_address)

data = "1,0,0,1,1"

connection.sendall(data)

result = connection.recv(20)

print result

connection.close()