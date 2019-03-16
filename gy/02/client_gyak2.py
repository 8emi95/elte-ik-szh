import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
connection.connect(server_address) # kapcsolodas megkezdese egy tavoli sockethez cimen keresztul

connection.sendall('Hello szerver') # adat (string) kuldese socketnek, amig az osszes at nem ment vagy hiba nem tortent
# kuldes elott csatlakoznia kell a tavoli sockethez

data = connection.recv(16) # fogadja az adatot amit a szerver kuldott
# 16 - max ilyen hosszu adatot kepes fogadni (bufsize)

print data

connection.close()
