import socket
import threading
import gameState

class ClientThread(threading.Thread):
    def run(self):
        print 'running client...'
        if(self.isAlive()):
            receivedData = self.socket.recv(1024)
        else:
            print 'closing socket...'
            self.socket.close()
            print 'closed socket.'
        print receivedData
    def __init__(self,hostIP):
        print 'init client thread...'
        threading.Thread.__init__(self)
        print '1'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print '2'
        gameState.setClient(self)
        print 'connecting...'
        self.socket.connect((hostIP,8080))
        print 'connected...'
    def sendCommand(self):
        print self.socket
#self.socket.send("data")

def startClient(hostIP):
    clientThread = ClientThread(hostIP)
    clientThread.daemon = True
    clientThread.start()

