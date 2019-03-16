import socket
import urllib.parse
socket.gethostname()

# socket.gethostbyname('homer')
socket.gethostbyname('www.python.org')
print(socket.gethostbyname('inf.elte.hu'))

socket.gethostbyaddr('157.181.161.79')
socket.gethostbyaddr('185.43.207.92')

parsed_url = urllib.parse.urlparse('http://www.example.com')
port = socket.getservbyname(parsed_url.scheme)

urls = ['http://www.example.com', 'https://www.example.com', 'ftp://example.com', 'gopher://gopher.example.com', 'smtp://mail.example.com', 'smtp://mail.example.com', 'imap://mail.example.com', 'imaps://mail.example.com', 'pop3://pop.example.com', 'pop3s://pop.example.com']
for u in urls:
  parsed_url = urllib.parse.urlparse(u)
  socket.getservbyname(parsed_url.scheme)

# ports = [80,443,21,70,25,143,993,110,995]
# for p in ports:
#   print(urlparse.urlunparse(
#     (socket.getservbyport(p), 'example.com', '/', '', '', '')
#   ))

for port in range(1,101):
  try:
   name = socket.getservbyport(port)
   print((port, name))
  except Exception:
   pass

for name in [ 'icmp', 'udp', 'tcp' ]:
  proto_num = socket.getprotobyname(name)
  print(proto_num)

for response in socket.getaddrinfo('www.python.org', 'http'):
   family, socktype, proto, canonname, sockaddr = response
   print((family, socktype, proto, canonname, sockaddr))

print((socket.AF_INET, socket.AF_INET6, socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.getprotobyname('tcp'), socket.getprotobyname('udp')))

for response in socket.getaddrinfo('www.python.org', 'http', socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP,  socket.AI_CANONNAME):
   family, socktype, proto, canonname, sockaddr = response
   print((family, socktype, proto, canonname, sockaddr))

for response in socket.getaddrinfo('www.inf.elte.hu', 'http', socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP,  socket.AI_CANONNAME):
   family, socktype, proto, canonname, sockaddr = response
   print((family, socktype, proto, canonname, sockaddr))
