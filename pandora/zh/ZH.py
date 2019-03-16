import socket
import sys


host="oktnb16.inf.elte.hu"
port=12045

#TODO: toltsd ki
neptun = 'T6ESML'

#TODO: csatlakozz a serverre TCP kapcsolattal
serverSocket = None


def callServer(serverSocket,msg):
	print "Call server with msg:",msg
	#TODO: kuld a msg-t a szervernek es fogadj tole 1024 hosszu uzenetet, amit adj vissza visszateresi erteknek

def getInfo(serverSocket,feladatSzam):
	print callServer(serverSocket,"info#"+neptun+"#"+feladatSzam)

callServer(serverSocket,neptun)

if sys.argv[1][:4] == 'info':
	#informacio lekeres
	getInfo(serverSocket,sys.argv[1][4])
else:
	print "Hibas parameter: ",sys.argv[1]

serverSocket.close()
