#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Készíts olyan server-kliens socket alkalmazást,
# ahol a kliens elküld egy bitsorozatot (max 16) és egy kódolást (’NRZ-L’,’RZ’,’Manchester’,’DiffManchester’),
# amire a szerver kiszámolja a kódolt jelerőséget!
# A jelerőségek hármasok: az intervallum eleje, közepe és vége.

# pl:
# – kliens küldi: („NRZ-L”, 1100)
# – server válasza: (1,1,1),(1,1,1),(0,0,0),(0,0,0)

# help:
# x00-k eltüntetése egy string végéről: szoveg.rstrip('\x00')

# változó hosszúságú üzenetet is kezeljen, ne egészítse ki 16 hosszúra

import socket
import struct

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10001)
connection.connect(server_address)

# data = 'NRZ-L,110011'
# data = 'RZ,110011'
# data = 'Manchester,110011'
data = 'DiffManchester,110011'

connection.sendall(data.encode('utf-8'))

result = connection.recv(1024)

connection.close()