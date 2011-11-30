import socket
import threading
import random
import gameState
import gameModes
import gameLogic
import uiElements
import udpServer

SERVER_PORT = 6666
CLIENT_PORT = 6667
SERVER_IP = "127.0.0.1"
CLIENT_IP = "127.0.0.1"

class MESSAGES:
    CONNECT = 0
    HANDSHAKE = 1    

class udpClient:
    theUdpClient = None
    def __init__(self,udpServer=None):
        self.socketLock = udpServer.socketLock
        with self.socketLock:
            self.socket = udpServer.socket
            self.socket.sendto(str(MESSAGES.CONNECT), (SERVER_IP, SERVER_PORT))
    def checkSocket(self):
        try:
            with udpServer.udpServer.theUdpServer.socketLock:
                receivedData,address = self.socket.recvfrom(1024,socket.MSG_PEEK)
        except:
            receivedData = ''
            address = ''
    def send(self):
        with self.socketLock:
            self.socket.sendto(str(MESSAGES.CONNECT), (SERVER_IP, SERVER_PORT))        

def startUdpClient():
    if(udpServer.udpServer.theUdpServer != None):
        udpClient.theUdpClient = udpClient(udpServer.udpServer.theUdpServer)
    else:
        print '1'
#    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    sock.bind(("",SERVER_PORT))
#    sock.setblocking(0)
#    print 'sending...'

