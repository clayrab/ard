import copy
import socket
import threading
import SocketServer
import time
import gameState
import client
import uiElements
import gameFindClient
import gameLogic
import ai

serverLock = threading.Lock()
server = None

def addNetworkPlayer(requestHandler):
    players = gameState.getPlayers()
    for i in range(0,8):
        if(players[i] != None and not players[i].isAI and not hasattr(players[i],"dispatchCommand")):
            #modifies existing players(from a loaded game) to be network players on the server
            player = gameState.addPlayer(playerClass=gameLogic.NetworkPlayer,playerNumber=i,requestHandler=requestHandler,playerObj = players[i])
            break
        
        elif(players[i] == None):
            player = gameState.addPlayer(playerClass=gameLogic.NetworkPlayer,playerNumber=i,requestHandler=requestHandler)
            break
    return player

def addAIPlayer():
    players = gameState.getPlayers()
    for i in range(0,8):
        if(players[i] == None):
            aiPlayer = gameState.addPlayer(playerClass=gameLogic.AIPlayer,playerNumber=i,requestHandler=None)
            break
    gameState.addAIPlayer(aiPlayer)
    for player in gameState.getPlayers():
        if(player != None):
            player.dispatchCommand("addPlayer -1 " + str(aiPlayer.playerNumber) + ":" + aiPlayer.userName)
    return aiPlayer

def removeNetworkPlayer(player):
    #todo: need ot notify players of playernumber changes too
    print 'removeNetworkPlayer is completely broken at this point, reimplement'
            
class RequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while 1:
            try:
                data = self.request.recv(1024)
                if not data:
                    break
                else:
                    for player in gameState.getPlayers():
                        if(player != None):
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
                    userName = "Player ?"
                    for index in range(0,8):
                        isUsed = gameState.playerUserNames[index]
                        if(not isUsed):
                            gameState.playerUserNames[index] = True
                            userName = "Player " + str(index+1)
                            break                            
                    if(gameState.getMapName() != None):
                        self.player.dispatchCommand("setMap -1 " + gameState.getMapName())
                    seed = time.time() * 256
                    for player in gameState.getPlayers():
                        if(player != None):#AI don't have dispatchcommand
                            player.dispatchCommand("seedRNG -1 " + str(seed))
                            self.player.dispatchCommand("addPlayer -1 " + str(player.playerNumber) + ":" + player.userName)
                            if(player.playerNumber != self.player.playerNumber):
                                player.dispatchCommand("addPlayer -1 " + str(self.player.playerNumber) + ":" + self.player.userName)
                    self.player.dispatchCommand("setOwnUserName -1 " + userName)
                    print str(self.client_address) + " setup done."
            else:
            #TODO: send command to client indicating game has started or host is no longer accepting connections...
                print 'host is not accepting connections'
    def finish(self):
#        SocketServer.StreamRequestHandler.finish(self)
        if(self.client_address[0] == "94.75.235.221"):
            return#just testing
        else:
            deadPlayerNumber = self.player.playerNumber
            deadUserName = self.player.userName
#            if(gameState.getPlayers().count(self.player) > 0):#can be removed first by resetPlayers when server goes down
#                gameState.removePlayer(self.player.playerNumber)
            if(server.acceptingConnections):
                for player in gameState.getPlayers():
                    if(player != None):
                        player.dispatchCommand("removePlayer -1 " + str(deadPlayerNumber))
                for index in range(0,8):
                    if(deadUserName == "Player " + str(index+1)):
                        gameState.playerUserNames[index] = False
            else:
                for player in gameState.getPlayers():
                    if(player != None):
                        player.dispatchCommand("disconnectedPlayer -1 " + str(deadPlayerNumber))
            print str(self.client_address) + " disconnected."

class Server(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    def __init__(self,serverAddress):
        try:
            SocketServer.TCPServer.__init__(self,serverAddress,RequestHandler)
        except:
            uiElements.smallModal("There was an error hosting the game.")
        self.acceptingConnections = True
        self.acceptingConnectionsLock = threading.Lock()
    def startAcceptingConnections(self):
        print 'start accepting'
        with self.acceptingConnectionsLock:
            self.acceptingConnections = True
    def stopAcceptingConnections(self):
        print 'stop accepting'
        with self.acceptingConnectionsLock:
            self.acceptingConnections = False

def startGame():
    with serverLock:
        global server
        server.stopAcceptingConnections()
    for player in gameState.getPlayers():
        if(player != None):
            player.dispatchCommand("startGame -1")
            player.dispatchCommand("chooseNextUnit -1")

serverStarted = False        
def shutdownServer():
    with serverLock:
        global server
        if(hasattr(gameState.getGameMode(),"playerMissing")):
            gameState.getGameMode().playerMissing = True
        if(server != None):
            server.stopAcceptingConnections()
        serverStarted = False

def startServer(serverIP,port=0):
    with serverLock:
        global server
        gameState.resetPlayers()
        gameState.resetAIs()
        gameState.resetPlayerUserNames()
        gameLogic.AIPlayer.nextAINumber = 1
        if(server == None):
            if(port == 0):
                port = int(gameState.getConfig()["serverPort"])
            server = Server((serverIP,port))
            server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,0)
            serverThread = threading.Thread(target=server.serve_forever)
            serverThread.daemon = True
            serverThread.start()
        server.startAcceptingConnections()
        serverStarted = True
