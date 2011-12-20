import socket
import threading
import random
import gameState
import gameModes
import gameLogic
import uiElements
from Crypto.PublicKey import RSA

pubKey = RSA.importKey("""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCJ5JSy/apuQQJ4OzsbT1EcnocX
jNbdUgxGoUkDBq6QVwebGAoni8aLd/vdyw90Q5dAxelJlTAKgvA7e1DmXlNaPRZ9
CuwkfHcIAEeVoMnEmc0Enfwz2PaA5dFCdsyifeiLjxH852sNcRQJjis5uCO/qRBI
HxhGho31ggCgs/6qcQIDAQAB
-----END PUBLIC KEY-----""")

SERVER = -1
SINGLE_PLAYER = -2
class Commands:
    @staticmethod
    def showRoom(args):
        print 'showroom'
        gameState.setGameMode(gameModes.gameFindMode)
        roomSelector = gameState.getGameMode().roomSelector
        roomSelector.reset()
        tokens = args.split('|')
        for token in tokens:
            if(len(token) > 0):
                (roomName,subscribersCount) = tuple(token.split("-"))
                roomSelector.textFields.append(uiElements.scrollableRoomElement(roomSelector.xPosition,0.0,roomName,"mapname",0,8))
        roomSelector.redraw()
        
        print args
    @staticmethod
    def seedRNG(seed):
        random.seed(seed)
    @staticmethod
    def setMap(mapName):
        gameState.setMapName(mapName)
    @staticmethod
    def setPlayerNumber(playerNumber):
        if(gameState.getPlayerNumber() != SINGLE_PLAYER):
            gameState.setPlayerNumber(int(playerNumber))
    @staticmethod
    def addPlayer(playerNumber):
        player = gameState.addPlayer(int(playerNumber))
        if(gameState.getPlayerNumber() == player.playerNumber or gameState.getPlayerNumber() == SINGLE_PLAYER):
            player.isOwnPlayer = True
        if(hasattr(gameState.getGameMode(),"redrawPlayers")):
               gameState.getGameMode().redrawPlayers()
    @staticmethod
    def startGame(args):
        gameState.setGameMode(gameModes.playMode)
    @staticmethod
    def chooseNextUnit(args):
        gameState.getGameMode().chooseNextUnit()
    @staticmethod
    def moveTo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
       	gameState.getGameMode().nextUnit.moveTo(node)
    @staticmethod
    def moveToUndo(args):
        tokens = args.split(" ")
    @staticmethod
    def moveToRedo(args):
        tokens = args.split(" ")
    @staticmethod
    def gatherTo(args):
        tokens = args.split(" ")
        unitNode = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node = gameState.getGameMode().map.nodes[int(tokens[3])][int(tokens[2])]
        unitNode.unit.gatheringNode = node
    @staticmethod
    def gatherToUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.gatheringNode = None
    @staticmethod
    def gatherToRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.gatheringNode = node

    @staticmethod
    def skip():
       	gameState.getGameMode().nextUnit.skip()
    @staticmethod
    def skipUndo(args):
        tokens = args.split(" ")
    @staticmethod
    def skipRedo(args):
        tokens = args.split(" ")
    @staticmethod
    def attackTo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
       	gameState.getGameMode().nextUnit.attackTo(node)
    @staticmethod
    def attackToUndo(args):
        tokens = args.split(" ")
    @staticmethod
    def attackToRedo(args):
        tokens = args.split(" ")
    @staticmethod
    def healTo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
       	gameState.getGameMode().nextUnit.healTo(node)
    @staticmethod
    def healToUndo(args):
        tokens = args.split(" ")
    @staticmethod
    def healToRedo(args):
        tokens = args.split(" ")
    @staticmethod
    def startSummoning(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        if(node.unit != None and node.unit.unitType.name == "summoner"):#don't trust the other client...
            node.city.queueUnit(gameLogic.unit(unitType,node.city.player,node.xPos,node.yPos,node))
            node.unit.waiting = True
            gameState.getGameMode().players[node.unit.player-1].greenWood = gameState.getGameMode().players[node.unit.player-1].greenWood - unitType.costGreen
            gameState.getGameMode().players[node.unit.player-1].blueWood = gameState.getGameMode().players[node.unit.player-1].blueWood - unitType.costBlue
            if(uiElements.actionViewer.theActionViewer.node == node):
                uiElements.actionViewer.theActionViewer.reset()
                uiElements.unitTypeBuildViewer.destroy()
    @staticmethod
    def startSummoningUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        if(node.unit != None and node.unit.unitType.name == "summoner"):
            node.city.unqueueUnit()
    @staticmethod
    def startSummoningRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        if(node.unit != None and node.unit.unitType.name == "summoner"):
            node.city.queueUnit(gameLogic.unit(unitType,node.city.player,node.xPos,node.yPos,node))
    @staticmethod
    def cancelSummoning(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        gameState.getGameMode().players[node.unit.player-1].greenWood = gameState.getGameMode().players[node.unit.player-1].greenWood + node.city.unitBuildQueue[-1].unitType.costGreen
        gameState.getGameMode().players[node.unit.player-1].blueWood = gameState.getGameMode().players[node.unit.player-1].blueWood + node.city.unitBuildQueue[-1].unitType.costBlue

        if(len(node.city.unitBuildQueue) > 0):
            node.city.cancelledUnits.append(node.city.unitBuildQueue.pop())
        elif(node.city.unitBeingBuilt != None):
            node.city.cancelledUnits.append(node.city.unitBeingBuilt)
            node.city.unitBeingBuilt = None
        if(uiElements.actionViewer.theActionViewer.node == node):
            uiElements.actionViewer.theActionViewer.reset()
    @staticmethod
    def cancelSummoningUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        if(node.city.unitBeingBuilt == None):
            node.city.unitBeingBuilt = node.city.cancelledUnits.pop()
        else:
            node.city.unitBuildQueue.append(node.city.cancelledUnits.pop())
    @staticmethod
    def cancelSummoningRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        if(len(node.city.unitBuildQueue) > 0):
            node.city.unitBuildQueue.pop()
        elif(node.city.unitBeingBuilt != None):
            node.city.unitBeingBuilt = None
    @staticmethod
    def startResearch(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        node.city.researching = True
	node.city.researchUnitType = unitType
        gameState.getGameMode().players[node.unit.player-1].greenWood = gameState.getGameMode().players[node.unit.player-1].greenWood - unitType.researchCostGreen
        gameState.getGameMode().players[node.unit.player-1].blueWood = gameState.getGameMode().players[node.unit.player-1].blueWood - unitType.researchCostBlue
	node.unit.waiting = True
    @staticmethod
    def startResearchUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        node.city.researching = False
        node.city.researchUnitType = None
    @staticmethod
    def startResearchRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        node.city.researching = True
	node.city.researchUnitType = unitType
    @staticmethod
    def stopWaiting(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.waiting = False
        if(uiElements.unitViewer.theUnitViewer != None and uiElements.unitViewer.theUnitViewer.unit == node.unit):
            uiElements.unitViewer.reset()
        if(uiElements.actionViewer.theActionViewer.node == node):
            uiElements.actionViewer.theActionViewer.reset()
    @staticmethod
    def stopWaitingUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.waiting = True
    @staticmethod
    def stopWaitingRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.waiting = False
    @staticmethod
    def wait(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.waiting = True
    @staticmethod
    def waitUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.waiting = False
    @staticmethod
    def waitRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.waiting = True        

def doCommand(commandName,args=None):
    commandFunc = getattr(Commands,commandName)
    if(commandFunc != None):
        commandFunc(args)
    else:
        print "ERROR: COMMAND " + commandName + " does not exist"

class Client:
    def __init__(self):        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        host = socket.gethostbyname("cynicsymposium.com")
        host = "127.0.0.1"
        port = 2222
        self.socket.connect((host,port))
        self.socket.setblocking(0)
        self.commandLog = []
        self.delayedCommands = []
        self.sendCommand("subscribe",gameState.getUserName() + " lobby")
    def checkSocket(self):
        try:
            receivedData = self.socket.recv(1024)
        except:
            receivedData = ''
        for command in receivedData.split("\r\n"):
            if(len(command) > 0):
                tokens = command.split("~",1)
                print tokens
                if(len(tokens) > 1):
                    doCommand(tokens[0],args=tokens[1])
                else:
                    doCommand(tokens[0])

    def sendCommand(self,command,argsString=""):
        if(command == "login"):
            argsString = pubKey.encrypt(argsString,32)
            argsString = argsString[0]
            print argsString
        self.socket.send(command + " " + str(argsString) + "\r\n")
        print 'sent...'
def startClient():
    gameState.setGameFindClient(Client())
#    clientThread = ClientThread(hostIP)
#    clientThread.daemon = True
#    clientThread.start()

