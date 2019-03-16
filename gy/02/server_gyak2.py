# socket-ek: kommunikacios vegpontok kulonbozo programok kozti adatcsere esetén
# socket-azonosito (ip + port): ip / domainhez tartozo ip lekerese (inf.elte.hu / 157.181.1.232) + port (ftp-21, ssh-22, http-80)

import socket

sock = socket.socket(socket.AF_INET,    # family: IPv4
                     socket.SOCK_STREAM # type: TCP
                                        # proto: 0 (alapertelmezett protokoll lesz)
)

server_address = ('localhost', 10000)
sock.bind(server_address) # bindolas porthoz, erre a portra kuldi a kliens az adatot h a programom megkapja

sock.listen(1) # megkezdi a szerver mukodeset
# 1 - ennyi kapcsolodasi igeny varakozhat (backlog)

connection, client_address = sock.accept() # csatlakozo klienst var, nem megy tovabb amig nincs kliens
# visszaadja a kliens objektumot (socket) es annak cimet

data = connection.recv(16) # fogadja az adatot amit a kliens kuldott
# 16 - max ilyen hosszu adatot kepes fogadni (bufsize)

print data

connection.sendall('Hello kliens') # adat (string) kuldese socketnek, amig az osszes at nem ment vagy hiba nem tortent
# kuldes elott csatlakoznia kell a tavoli sockethez
