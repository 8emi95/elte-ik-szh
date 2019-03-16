import socket
import struct
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

multicast_group_address = ('224.3.29.71', 10000)

sock.settimeout(3) # idotullepesi ertek: multicast uzenet kuldoje nem tudja hany valasz lesz

# ttl: 1 csak sajat gepen fut a szerver es kliends, 2 tanari gepen szerver es mindenki feliratkozhat
ttl = struct.pack('b', 1) # '\x01'
# adott socket-opcio beallitasa
sock.setsockopt(socket.IPPROTO_IP,        # jelzi ip szintu beallitas
                socket.IP_MULTICAST_TTL,  # TTL (Time To Live): kontrollalja hany halozat kaphatja meg a csomagot
                ttl                       # biztositja a hivonak h a megfelelo biteket tartalmazza (struct)
)

try:
  sock.sendto('Hello clients', multicast_group_address)
  
  while True:
    try:
      data, client_address = sock.recvfrom(4096)
    except socket.timeout:
       print >>sys.stderr, 'timed out, no more responses'
       break
    else: # executed code if there is no exception in the try clause
       print "Incoming message from", client_address
       print "Message:", data
finally:
  print >>sys.stderr, 'closing socket'
  sock.close()