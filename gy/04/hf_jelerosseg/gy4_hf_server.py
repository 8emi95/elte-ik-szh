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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10001)
sock.bind(server_address)

sock.listen(1)

connection, client_address = sock.accept()

data = connection.recv(1024)
split_data = data.decode("utf-8").split(",")
coding = split_data[0]
bits = split_data[1]

def calculate(coding, bits):
    result = ''
    if (coding == 'NRZ-L'):
        for i in bits:
            if (i == '1'):
                result += '111'
            if (i == '0'):
                result += '000'
    elif (coding == 'RZ'):
        for i in bits:
            if (i == '1'):
                result += '100'
            if (i == '0'):
                result += '000'
    elif (coding == 'Manchester'):
        for i in bits:
            if (i == '1'):
                result += '100'
            if (i == '0'):
                result += '011'
    elif (coding == 'DiffManchester'):
        for i in bits:
            if (i == '1'):
                if (result.endswith('1') or len(result) == 0):
                    result += '100'
                elif (result.endswith('0') or len(result) == 0):
                    result += '011'
            elif (i == '0'):
                if (result.endswith('1') or len(result) == 0):
                    result += '011'
                elif (result.endswith('0') or len(result) == 0):
                    result += '100'
    return result.encode('utf-8')

result = calculate(coding, bits)

print("coding: ", coding, "\nbits: ", bits, "\nresult: ", result.decode('utf-8'))

connection.sendall(result)