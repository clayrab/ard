import time

#have gamefindserver attempt tcp connection to host
#if fails, inform the player they must open the port on their router
#

#one machine decides to host a game and begins listening on port 6666
#another machine comes along to join the game and reports its ip/port to the gamefindserver
#if the ip/port is the same as any previously joined player, it is told to discover the other machine on it's same LAN and route all
#sent a command to increment it's port and go back to previos step
#once a unique ip/port is discovered, the host is sent the ip/port info and begins the 'handshake' process(i.e. starts sending packets to the client so the clients handshake packet will get thru the NAT)
#keep alive packets must be sent
#client has status connecting/connected/ready(after the user clicks ready)


SERVER_PORT = 6666
CLIENT_PORT = 6667
SERVER_IP = "127.0.0.1"
CLIENT_IP = "127.0.0.1"

class udpService:
    def __init__(self,sendIP,sendPort,recvPort):
        self.commandsSent = {}
        print time.ctime()
        print time.time()
#    def connect(self):
#        print 'connect'
    def send(self):
        print 'send'
    def recv(self):
        print 'recv'
