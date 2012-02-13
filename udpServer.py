import socket
import threading
import time
import gameState
import client
import Queue

SERVER_PORT = 6666
CLIENT_PORT = 6667
SERVER_IP = "127.0.0.1"
CLIENT_IP = "127.0.0.1"

class MESSAGES:
    CONNECT = 0
    HANDSHAKE = 1    

class client:
    def __init__(self,id):
        self.id = id
        self.roundTripCount = 0
        self.roundTripTimeAvg = 5.0
        self.sendCommands = {}

class udpServer:
    theUdpServer = None
    def __init__(self,socket):
        self.socketLock  = threading.Lock()
        with self.socketLock:
            self.socket = socket
            self.socket.setblocking(0)
            self.socket.bind(("",SERVER_PORT))
        self.clients = []
        self.connectingClients = Queue.Queue()
        self.connecting = False 
        self.clientConnecting = False
        self.clientConnected = False
        print self
    def connect(self,clientIp):
        self.connecting = True
        self.connectingClients.put(client(clientIp))
        print clientIp
    def run(self):
        while(True):
            time.sleep(0.100)#yield
#            if(self.clientConnected):
#                print 'connected'
#            elif(self.clientConnecting):
#                sock.sendto(str(MESSAGES.HANDSHAKE), (CLIENT_IP, SERVER_PORT))
            try:
                with self.socketLock:
                    data,address = self.socket.recvfrom(1024)
                    print "data " + data
                    print "address " + address
            except:
                data = ''
#            if(data == str(MESSAGES.CONNECT)):
#                print 'start connecting...'
#                self.clientConnecting = True
#            elif(data == str(MESSAGES.HANDSHAKE)):
#                print 'connecting...'
#                self.clientConnected = True
#            print "received message:", data
def startUdpServer():
    udpServer.theUdpServer = udpServer(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    serverThread = threading.Thread(target=udpServer.theUdpServer.run)
    serverThread.daemon = True
    serverThread.start()

