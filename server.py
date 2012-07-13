import copy
import socket
import threading
import SocketServer
import time
import gameState
import client
import uiElements
import gameFindClient

serverLock = threading.Lock()
server = None
networkPlayersLock = threading.Lock()
theNetworkPlayers = []
def addNetworkPlayer(requestHandler):
       	player = NetworkPlayer(requestHandler)
	with networkPlayersLock:
		global theNetworkPlayers
		theNetworkPlayers.append(player)
	return player
def removeNetworkPlayer(player):
    #todo: need ot notify players of playernumber changes too
	NetworkPlayer.nextPlayerNumber = NetworkPlayer.nextPlayerNumber - 1
	with networkPlayersLock:
		global theNetworkPlayers
		for aPlayer in theNetworkPlayers:
			if(aPlayer.playerNumber > player.playerNumber):
				aPlayer.playerNumber = aPlayer.playerNumber - 1
		theNetworkPlayers.remove(player)
def getNetworkPlayers():
	playersCopy = []
	with networkPlayersLock:
		global theNetworkPlayers
		playersCopy = copy.copy(theNetworkPlayers)
	return playersCopy

def resetNetworkPlayers():
	with networkPlayersLock:
		global theNetworkPlayers
		theNetworkPlayers = []
		NetworkPlayer.nextPlayerNumber = 1

def setupAI(aiPlayer):
    for player in getNetworkPlayers():
        player.dispatchCommand("addPlayer -1 " + str(aiPlayer.playerNumber))

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
            print 'ERROR writing to network handler'
            return
            
class RequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while 1:
            try:
                data = self.request.recv(1024)
                if not data:
                    break
                else:
                    for player in getNetworkPlayers():
                        player.dispatchCommand(data)
            except:
                break
    def setup(self):
        with server.acceptingConnectionsLock:
            if(server.acceptingConnections):
                print 'setup new player: ' + str(self.client_address)
                if(self.client_address[0] == "94.75.235.221"):
                    print 'just testing'
                    #TODO: send a confirmation back to the server
                else:                    
                    SocketServer.StreamRequestHandler.setup(self)
                    self.player = addNetworkPlayer(self)
                    self.player.dispatchCommand("setTeamSize -1 " + str(gameState.getTeamSize()))
                    self.player.dispatchCommand("setPlayerNumber -1 " + str(self.player.playerNumber))
                    if(gameState.getMapName() != None):
                        self.player.dispatchCommand("setMap -1 " + gameState.getMapName())
                    seed = time.time() * 256
                    for player in getNetworkPlayers():
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
        if(self.client_address[0] == "94.75.235.221"):
            return#just testing
        else:
            removeNetworkPlayer(self.player)
            print str(self.client_address) + " disconnected."

class Server(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    def __init__(self,serverAddress):
        try:
            SocketServer.TCPServer.__init__(self,serverAddress,RequestHandler)
        except:
            uiElements.smallModal("There was an error hosting the game.")
        self.acceptingConnections = True
        self.acceptingConnectionsLock = threading.Lock()

#def setMap(mapName):
#    with server.acceptingConnectionsLock:    
#        gameState.setMapName(mapName)#need this in case host's client doesn't recieve new mapname before another player connects
#        for player in getNetworkPlayers():
#            player.dispatchCommand("setMap -1 " + mapName)

def startAcceptingConnections():
    with server.acceptingConnectionsLock:
        server.acceptingConnections = True
def stopAcceptingConnections():
    with server.acceptingConnectionsLock:
        server.acceptingConnections = False
def startGame():
    stopAcceptingConnections()
    for player in getNetworkPlayers():
        player.dispatchCommand("startGame -1")

serverStarted = False        
def shutdownServer():
#    with serverLock:
#        global server
#        if(server != None):
#            server.shutdown()
    return

import ai
def startServer(serverIP,port=0):
    with serverLock:
        global server
        resetNetworkPlayers()
        ai.resetAIs()
        if(server == None):
            if(port == 0):
                port = int(gameState.getConfig()["serverPort"])
            server = Server((serverIP,port))
            server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,0)
            serverThread = threading.Thread(target=server.serve_forever)
            serverThread.daemon = True
            serverThread.start()
            serverStarted = True
