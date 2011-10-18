import socket
import threading
import random
import gameState
import gameModes
import gameLogic

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
        node = gameState.getGameMode().map.nodens[int(tokens[1])][int(tokens[0])]
       	gameState.getGameMode().nextUnit.moveTo(node)
        gameState.getGameMode().chooseNextUnit()
    def startSummoning(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodens[int(tokens[1])][int(tokens[0])]
        print node        
	#	actionViewer.theActionViewer.node.city.doneResearching = True
	#	actionViewer.theActionViewer.node.city.queueUnit(gameLogic.unit(self.unitType,actionViewer.theActionViewer.node.city.player,actionViewer.theActionViewer.node.city.researchLevel,actionViewer.theActionViewer.node.xPos,actionViewer.theActionViewer.node.yPos,actionViewer.theActionViewer.node))
	#	actionViewer.theActionViewer.node.unit.unitAction = gameLogic.unitAction.WAIT
	#	if(gameState.getGameMode().nextUnit == actionViewer.theActionViewer.node.unit):
	#		gameState.getGameMode().chooseNextUnit()
	#	else:
	#		actionViewer.theActionViewer.reset()
	#		unitTypeBuildViewer.destroy()





        

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

