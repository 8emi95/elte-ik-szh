import socket
import struct
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,      # jelzi h api szintu beallitas
                socket.SO_REUSEADDR,    # kapcsolat bontasa utan a port ujrahasznositasa
                1                       # 0 hamis, 1 igaz a SO_REUSEADDR "tulajdonsag"
)

multicast_group = '224.3.29.71'
server_address = ('', 10000) # '' = INADDR_ANY, osszes lokalis interfeszhez kotve lesz / osszes halozati interfeszen figyel a fogado
# fontos h a szerver altal hasznalt portot adjuk meg
sock.bind(server_address)

group = socket.inet_aton(multicast_group)           # '\xe0\x03\x1dG'
mreq = struct.pack('4sL', group, socket.INADDR_ANY) # '\xe0\x03\x1dG\x00\x00\x00\x00'
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # fogado oldalon a socketet hozzaadjuk a multicast csoporthoz (IP_ADD_MEMBERSHIP)

print >>sys.stderr, '\nwaiting to receive message'
data, server_address = sock.recvfrom(4096)
print "Incoming message from", server_address
print "Message:", data

sock.sendto('Acknowledgement', server_address)

sock.close()