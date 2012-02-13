import time

SERVER_PORT = 6666
CLIENT_PORT = 6667
SERVER_IP = "127.0.0.1"
CLIENT_IP = "127.0.0.1"

class udpService:
    def __init__(self,isServer=False):
        if(isServer):
            self.portIn = SERVER_PORT
            self.portOut = CLIENT_PORT
        else:
            self.portIn = CLIENT_PORT
            self.portOut = SERVER_PORT
        self.commandsSent = {}
        print time.ctime()
        print time.time()
    def connect(self):
        print 'connect'
    def send(self):
        print 'send'
    def recv(self):
        print 'recv'
