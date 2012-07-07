import socket
import threading
import SocketServer
import time
import gameState
import client
import uiElements

serverLock = threading.Lock()
server = None

class NetworkPlayer:
    nextPlayerNumber = 1
    def __init__(self,requestHandler):
        self.requestHandler = requestHandler
        self.playerNumber = NetworkPlayer.nextPlayerNumber
        NetworkPlayer.nextPlayerNumber = NetworkPlayer.nextPlayerNumber + 1
    def dispatchCommand(self,command):
        try:
            self.requestHandler.wfile.write(command + "|")
        except:
            return
            
class RequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while 1:
            try:
                data = self.request.recv(1024)
                if not data:
                    break
                else:
                    for player in gameState.getNetworkPlayers():
                        player.dispatchCommand(data)
            except:
                break
    def setup(self):
        with server.acceptingConnectionsLock:
            if(server.acceptingConnections):
                print 'setup new player: ' + str(self.client_address)
                SocketServer.StreamRequestHandler.setup(self)
                self.player = gameState.addNetworkPlayer(self)
                self.player.dispatchCommand("setPlayerNumber -1 " + str(self.player.playerNumber))
                if(gameState.getMapName() != None):
                    self.player.dispatchCommand("setMap -1 " + gameState.getMapName())
                seed = time.time() * 256
                for player in gameState.getNetworkPlayers():
                    player.dispatchCommand("seedRNG -1 " + str(seed))
                    self.player.dispatchCommand("addPlayer -1 " + str(player.playerNumber))
                    if(player.playerNumber != self.player.playerNumber):
                        player.dispatchCommand("addPlayer -1 " + str(self.player.playerNumber))
                print str(self.client_address) + " setup done."
            else:
            #TODO: send command to client indicating game has started or host is no longer accepting connections...
                print 'host is not accepting connections'
    def finish(self):
#        SocketServer.StreamRequestHandler.finish(self)
        gameState.removeNetworkPlayer(self.player)
        print str(self.client_address) + " disconnected."

class Server(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    def __init__(self,serverAddress):
#        try:
        SocketServer.TCPServer.__init__(self,serverAddress,RequestHandler)
        self.acceptingConnections = True
        self.acceptingConnectionsLock = threading.Lock()
#        except:
#            uiElements.smallModal("There was an error hosting the game.")

def setMap(mapName):
    with server.acceptingConnectionsLock:    
        gameState.setMapName(mapName)#need this in case host's client doesn't recieve new mapname before another player connects
        for player in gameState.getNetworkPlayers():
            player.dispatchCommand("setMap -1 " + mapName)

def startAcceptingConnections():
    with server.acceptingConnectionsLock:
        server.acceptingConnections = True
def stopAcceptingConnections():
    with server.acceptingConnectionsLock:
        server.acceptingConnections = False

serverStarted = False        
def shutdownServer():
#    with serverLock:
#        global server
#        if(server != None):
#            server.shutdown()
    return
def startServer(serverIP,port=0):
    with serverLock:
        global server
        gameState.resetNetworkPlayers()
        if(server == None):
            if(port == 0):
                port = int(gameState.getConfig()["serverPort"])
            server = Server((serverIP,port))
            server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,0)
            serverThread = threading.Thread(target=server.serve_forever)
            serverThread.daemon = True
            serverThread.start()
            serverStarted = True
            print 'server started...'
