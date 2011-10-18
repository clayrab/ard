import socket
import threading
import random
import gameState
import gameModes
import gameLogic
import uiElements

class Commands:
    @staticmethod
    def seedRNG(seed):
        print seed
        random.seed(seed)
    @staticmethod
    def setMap(mapName):
        gameState.setMapName(mapName)
    @staticmethod
    def setPlayerNumber(playerNumber):
        if(gameState.getPlayerNumber() != -1):
            gameState.setPlayerNumber(int(playerNumber))
    @staticmethod
    def addPlayer(playerNumber):
        player = gameState.addPlayer(playerNumber)
        if(gameState.getPlayerNumber() == player.playerNumber or gameState.getPlayerNumber() == -1):
            player.isOwnPlayer = True
        gameState.getGameMode().redrawPlayers()
    @staticmethod
    def startGame():
        gameState.setGameMode(gameModes.playMode)
    @staticmethod
    def nodeClick(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
       	gameState.getGameMode().nextUnit.moveTo(node)
        gameState.getGameMode().chooseNextUnit()
    @staticmethod
    def startSummoning(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        if(node.unit != None and node.unit.unitType.name == "summoner"):#don't trust the other client...
            node.city.doneResearching = True
            node.city.queueUnit(gameLogic.unit(unitType,node.city.player,node.city.researchLevel,node.xPos,node.yPos,node))
            node.unit.waiting = True
            if(gameState.getGameMode().nextUnit == node.unit):
                gameState.getGameMode().chooseNextUnit()
            elif(uiElements.actionViewer.theActionViewer.node == node):
                uiElements.actionViewer.theActionViewer.reset()
                uiElements.unitTypeBuildViewer.destroy()
    @staticmethod
    def cancelSummoning(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        if(len(node.city.unitBuildQueue) > 0):
            node.city.unitBuildQueue.pop()
        elif(node.city.unitBeingBuilt != None):
            node.city.unitBeingBuilt = None
        if(uiElements.actionViewer.theActionViewer.node == node):
            uiElements.actionViewer.theActionViewer.reset()
    @staticmethod
    def startResearch(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        node.city.researching = True
	node.city.researchUnitType = unitType
	node.unit.waiting = True
#	node.unit.moveTo(node)
        if(gameState.getGameMode().nextUnit == node.unit):
            gameState.getGameMode().chooseNextUnit()


def doCommand(commandName,args=None):
    commandFunc = getattr(Commands,commandName)
    if(commandFunc != None):
        if(args != None):
            commandFunc(args)
        else:
            commandFunc()
    else:
        print "ERROR: COMMAND " + commandName + " does not exist"

class ClientThread(threading.Thread):
    def run(self):
        while(1):
            receivedData = self.socket.recv(1024)
            print "receivedData: " + receivedData
            for command in receivedData.split("|"):
                if(len(command) > 0):
                    tokens = command.split(" ",1)
                    if(len(tokens) > 1):
                        doCommand(tokens[0],args=tokens[1])                    
                    else:
                        doCommand(tokens[0])
#        else:
            #TODO: create a socketLock and call these explicitely
#            print '*****SOCKET SHUTTING DOWN*****'
#            self.socket.shutdown()
#            self.socket.close()
#            print '*****SOCKET SHUT DOWN*****'
    
    def __init__(self,hostIP):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1)
#        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,1)
#        print self.socket.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
        gameState.setClient(self)
        self.socket.connect((hostIP,8080))

class Client:
    def __init__(self,hostIP):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((hostIP,8080))
        self.socket.setblocking(0)
    def checkSocket(self):
        receivedData = self.socket.recv(1024)
        print "receivedData: " + receivedData
        for command in receivedData.split("|"):
            if(len(command) > 0):
                tokens = command.split(" ",1)
                if(len(tokens) > 1):
                    doCommand(tokens[0],args=tokens[1])                    
                else:
                    doCommand(tokens[0])
    def sendCommand(self,command):
        print 'sending... ' + command
        self.socket.send(command)
        print 'sent...'
def startClient(hostIP):
    gameState.setClient(Client(hostIP))
#    clientThread = ClientThread(hostIP)
#    clientThread.daemon = True
#    clientThread.start()

