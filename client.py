import socket
import threading

import threading

class ClientThread(threading.Thread):
    def run(self):
        print self
        receivedData = self.socket.recv(1024)
        print receivedData
    def __init__(self,hostIP):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

