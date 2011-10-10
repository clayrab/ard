import socket
import threading
import SocketServer
import time
import gameState
import client

serverLock = threading.Lock()
server = None

class NetworkPlayer:
    nextPlayerNumber = 1
    def __init__(self,requestHandler):
        self.requestHandler = requestHandler
        self.playerNumber = NetworkPlayer.nextPlayerNumber
        NetworkPlayer.nextPlayerNumber = NetworkPlayer.nextPlayerNumber + 1
    def dispatchCommand(self,command):
        self.requestHandler.wfile.write(command)
            
class RequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while 1:
            data = self.request.recv(1024)
            if not data:
                break
            else:
                for player in gameState.getNetworkPlayers():
                    player.dispatchCommand(data)
    def setup(self):
        with server.acceptingConnectionsLock:
            if(server.acceptingConnections):
                SocketServer.StreamRequestHandler.setup(self)
                self.player = gameState.addNetworkPlayer(self)
                self.player.dispatchCommand("setPlayerNumber " + str(self.player.playerNumber) + "|")
                if(gameState.getMapName() != None):
                    self.player.dispatchCommand("setMap " + gameState.getMapName() + "|")
                seed = time.time() * 256
                for player in gameState.getNetworkPlayers():
                    player.dispatchCommand("seedRNG " + str(seed) + "|")
                    self.player.dispatchCommand("addPlayer " + str(player.playerNumber) + "|")
                    if(player.playerNumber != self.player.playerNumber):
                        player.dispatchCommand("addPlayer " + str(self.player.playerNumber) + "|")
                print str(self.client_address) + " connected."
            else:
            #TODO: send command to client indicating game has started or host is no longer accepting connections...
                print 'host is not accepting connections'
    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        gameState.removeNetworkPlayer(self.player)
        print str(self.client_address) + " disconnected."

class Server(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    def __init__(self,serverAddress):
        SocketServer.TCPServer.__init__(self,serverAddress,RequestHandler)
        self.acceptingConnections = True
        self.acceptingConnectionsLock = threading.Lock()

def setMap(mapName):
    with server.acceptingConnectionsLock:    
        gameState.setMapName(mapName)#need this incase host's client doesn't recieve new mapname before another player connects
        for player in gameState.getNetworkPlayers():
            player.dispatchCommand("setMap " + mapName + "|")

def startAcceptingConnections():
    with server.acceptingConnectionsLock:
        server.acceptingConnections = True
def stopAcceptingConnections():
    with server.acceptingConnectionsLock:
        server.acceptingConnections = False
        
def shutdownServer():
    global server
    if(server != None):
        server.shutdown()
def startServer(serverIP):
    with serverLock:
        global server
        server = Server((serverIP,8080))
        server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,0)
        serverThread = threading.Thread(target=server.serve_forever)
        serverThread.daemon = True
        serverThread.start()
