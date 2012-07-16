import socket
import threading
import random
import gameState
import gameModes
import gameLogic
import uiElements
import server

SERVER = -1
SINGLE_PLAYER = -2
class Commands:
    @staticmethod
    def seedRNG(seed):
        random.seed(seed)
    @staticmethod
    def setMap(mapName):
#        gameState.setMapName(mapName)
        if(hasattr(gameState.getGameMode(),"setMap")):
            gameState.getGameMode().setMap(mapName)
        else:
            gameState.setMapName(mapName)
    @staticmethod
    def setOwnUserName(userName):
        if(gameState.getOwnUserName() == None):#"Player X" from server, prefer real username, which would already be set
            gameState.setOwnUserName(userName)
        print gameState.getOwnUserName()
        gameState.getClient().sendCommand("changeUserName",str(gameState.getPlayerNumber()) + ":" + gameState.getOwnUserName())
        if(hasattr(gameState.getGameMode(),"redrawTeams")):
            gameState.getGameMode().redrawTeams()
    @staticmethod
    def changeUserName(args):
        tokens = args.split(":")
        oldUserName = gameState.getPlayers()[int(tokens[0])].userName
        gameState.changeUserName(int(tokens[0]),tokens[1])
        if(hasattr(gameState.getGameMode(),"redrawTeams")):
            gameState.getGameMode().redrawTeams()
        for index in range(0,8):
            if(oldUserName == "Player " + str(index+1)):
                server.playerUserNames[index] = False
    @staticmethod
    def setTeamSize(teamSize):
        gameState.setTeamSize(int(teamSize))
        if(hasattr(gameState.getGameMode(),"redrawTeams")):
            gameState.getGameMode().redrawTeams()
    @staticmethod
    def setPlayerNumber(playerNumber):
        if(gameState.getPlayerNumber() != SINGLE_PLAYER):
            gameState.setPlayerNumber(int(playerNumber))
#        if(gameState.getOwnUserName() == None):
#            gameState.setOwnUserName("Player " + playerNumber)
    @staticmethod
    def removePlayer(playerNumber):
        gameState.removePlayer(int(playerNumber))
        if(hasattr(gameState.getGameMode(),"redrawTeams")):
            gameState.getGameMode().redrawTeams()        
    @staticmethod
    def addPlayer(args):
        tokens = args.split(":")
        playerNumber = int(tokens[0])
        userName = tokens[1]
        gameState.addPlayer(playerNumber=playerNumber,userName=userName,requestHandler=None)
        for player in gameState.getPlayers():
            if(player != None):
                if(gameState.getPlayerNumber() == player.playerNumber or gameState.getPlayerNumber() == SINGLE_PLAYER):
                    player.isOwnPlayer = True
                    gameState.setPlayerNumber(player.playerNumber)
                else:
                    player.isOwnPlayer = False
        if(hasattr(gameState.getGameMode(),"redrawTeams")):
            gameState.getGameMode().redrawTeams()
    @staticmethod
    def changePlayerNumber(args):
        tokens = args.split(":")
        oldNumber = int(tokens[0])
        newNumber = int(tokens[1])
        gameState.movePlayer(oldNumber,newNumber)
        for player in gameState.getPlayers():
            if(player != None):
                if(gameState.getPlayerNumber() == player.playerNumber or gameState.getPlayerNumber() == SINGLE_PLAYER):
                    player.isOwnPlayer = True
                    gameState.setPlayerNumber(player.playerNumber)
                else:
                    player.isOwnPlayer = False
        if(hasattr(gameState.getGameMode(),"redrawTeams")):
            gameState.getGameMode().redrawTeams()
    @staticmethod
    def startGame():
        gameState.setGameMode(gameModes.playMode)
    @staticmethod
    def chooseNextUnit():
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
    def skip():
       	gameState.getGameMode().nextUnit.skip()
    @staticmethod
    def skipUndo():
        pass
#        tokens = args.split(" ")
    @staticmethod
    def skipRedo():
        pass
#        tokens = args.split(" ")
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
    def startMeditating(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.isMeditating = True
        if(node == gameState.getGameMode().selectedNode and node.unit.isOwnUnit()):
            if(uiElements.viewer.theViewer != None):
                uiElements.viewer.theViewer.destroy()
            if(gameState.getGameMode().selectedNode.city != None):
                uiElements.viewer.theViewer = uiElements.cityViewer(node)
            else:
                uiElements.viewer.theViewer = uiElements.unitViewer(node)
    @staticmethod
    def startMeditatingUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.isMeditating = False
    @staticmethod
    def startMeditatingRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        node.unit.isMeditating = True
    @staticmethod
    def startSummoning(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        gameState.getGameMode().players[node.unit.player-1].greenWood = gameState.getGameMode().players[node.unit.player-1].greenWood - (node.city.researchProgress[unitType][0]*unitType.costGreen)
        gameState.getGameMode().players[node.unit.player-1].blueWood = gameState.getGameMode().players[node.unit.player-1].blueWood - (node.city.researchProgress[unitType][0]*unitType.costBlue)
        node.city.queueUnit(gameLogic.unit(unitType,node.city.player,node.xPos,node.yPos,node))
        if(gameState.getGameMode().selectedNode == node and hasattr(uiElements.viewer.theViewer,"isCityViewer")):
            uiElements.viewer.theViewer.destroy()
            uiElements.viewer.theViewer = uiElements.cityViewer(node)
            
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
    def cancelQueuedThing(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        index = int(tokens[2])
        if(len(node.city.unitBuildQueue) > 0):
            cancelledQueuedThing = node.city.unitBuildQueue.pop(index-1)
            node.city.cancelledUnits.append((cancelledQueuedThing,index,))
            if(hasattr(cancelledQueuedThing,"unitType")):#unit
                gameState.getGameMode().players[node.unit.player-1].greenWood = gameState.getGameMode().players[node.unit.player-1].greenWood + cancelledQueuedThing.unitType.costGreen
                gameState.getGameMode().players[node.unit.player-1].blueWood = gameState.getGameMode().players[node.unit.player-1].blueWood + cancelledQueuedThing.unitType.costBlue
            else:#unittype
                gameState.getGameMode().players[node.unit.player-1].greenWood = gameState.getGameMode().players[node.unit.player-1].greenWood + cancelledQueuedThing.researchCostGreen
                gameState.getGameMode().players[node.unit.player-1].blueWood = gameState.getGameMode().players[node.unit.player-1].blueWood + cancelledQueuedThing.researchCostBlue
        if(gameState.getGameMode().selectedNode == node and hasattr(uiElements.viewer.theViewer,"isCityViewer")):
            uiElements.viewer.theViewer.destroy()
            uiElements.viewer.theViewer = uiElements.cityViewer(node)
    @staticmethod
    def cancelQueuedThingUndo(args):
        tokens = args.split(" ")
        index = int(tokens[2])
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        cancelledThing,index = node.city.cancelledUnits.pop()
        node.city.unitBuildQueue.insert(index-1,cancelledThing)
    @staticmethod
    def cancelQueuedThingRedo(args):
        tokens = args.split(" ")
        index = int(tokens[2])
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        if(len(node.city.unitBuildQueue) > 0):
            node.city.unitBuildQueue.pop(index-1)
    @staticmethod
    def startResearch(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        node.city.queueResearch(unitType)
        gameState.getGameMode().players[node.unit.player-1].greenWood = gameState.getGameMode().players[node.unit.player-1].greenWood - unitType.researchCostGreen
        gameState.getGameMode().players[node.unit.player-1].blueWood = gameState.getGameMode().players[node.unit.player-1].blueWood - unitType.researchCostBlue
        if(gameState.getGameMode().selectedNode == node and hasattr(uiElements.viewer.theViewer,"isCityViewer")):
            uiElements.viewer.theViewer.destroy()
            uiElements.viewer.theViewer = uiElements.cityViewer(node)
    @staticmethod
    def startResearchUndo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        node.city.unqueueResearch()
    @staticmethod
    def startResearchRedo(args):
        tokens = args.split(" ")
        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
        unitType = gameState.theUnitTypes[tokens[2]]
        node.city.queueResearch(unitType)
#    @staticmethod
#    def stopWaiting(args):
#        tokens = args.split(" ")
#        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
#        node.unit.waiting = False

#        if(uiElements.unitViewer.theUnitViewer != None and uiElements.unitViewer.theUnitViewer.unit == node.unit):
#            uiElements.unitViewer.reset()
#        if(uiElements.actionViewer.theViewer.node == node):
#            uiElements.actionViewer.theViewer.reset()
#    @staticmethod
#    def stopWaitingUndo(args):
 #       tokens = args.split(" ")
#        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
#        node.unit.waiting = True
#    @staticmethod
#    def stopWaitingRedo(args):
#        tokens = args.split(" ")
#        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
#        node.unit.waiting = False
#    @staticmethod
#    def wait(args):
#        tokens = args.split(" ")
#        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
#        node.unit.waiting = True
#    @staticmethod
#    def waitUndo(args):
#        tokens = args.split(" ")
#        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
#        node.unit.waiting = False
#    @staticmethod
#    def waitRedo(args):
#        tokens = args.split(" ")
#        node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
#        node.unit.waiting = True
    @staticmethod
    def chat(args):
        if(hasattr(gameState.getGameMode(),"chatDisplay")):
            gameState.getGameMode().chatDisplay.addText(args)


def doCommand(commandName,args=None):
    print commandName + ":" + str(args)
    commandFunc = getattr(Commands,commandName)
    if(commandFunc != None):
        if(args != None and args != ''):
            commandFunc(args)
        else:
            commandFunc()
    else:
        print "ERROR: COMMAND " + commandName + " does not exist"

class Client:
    def __init__(self,hostIP,port=-1):
        if(port < 0):
            port = int(gameState.getConfig()["serverPort"])
        self.hostIP = hostIP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((hostIP,port))
        self.socket.setblocking(0)
        self.commandLog = []
#        self.delayedCommands = []
#    def sendDelayedCommands(self):
#        for command in self.delayedCommands:
#             self.socket.send(command)
#        self.delayedCommands = []
    def checkSocket(self):
        try:
            receivedData = self.socket.recv(1024)
        except:
            receivedData = ''
        for command in receivedData.split("|"):
            if(len(command) > 0):
                tokens = command.split(" ",2)
                if(tokens[0] == "chooseNextUnit"):
                    if(len(self.commandLog) > 0):
                        for command in self.commandLog:
                            doCommand(command[0]+"Undo",command[1])
                    doCommand("chooseNextUnit")
                    if(len(self.commandLog) > 0):
                        for command in self.commandLog:
                            doCommand(command[0]+"Redo",command[1])
                    self.commandLog = []
                else:
                    if(gameState.getPlayerNumber() == SERVER or int(tokens[1]) != gameState.getPlayerNumber() or tokens[0] == "changePlayerNumber"):#skip our own commands, they were executed immediately
                        if(len(tokens) > 2):
                            doCommand(tokens[0],args=tokens[2])
                        else:
                            doCommand(tokens[0])
                    else:
                        self.commandLog = self.commandLog[:-1:]
                        #print "commandLog: " + str(self.commandLog)

    def sendCommand(self,command,argsString=""):
        if(command != "chooseNextUnit" and command != "changePlayerNumber"):
            self.commandLog.append((command,argsString))
            if(argsString != ""):
                doCommand(command,argsString)
#TODO: TEST THE ENTIRE GAME IN SINGLE PLAYER WITH THESE COMMANDS UNCOMMENTED
#                doCommand(command+"Undo",argsString)
#                doCommand(command+"Redo",argsString)
            else:
                doCommand(command)
        self.socket.send(command + " " + str(gameState.getPlayerNumber()) + " " + argsString + "|")

def startClient(hostIP,hostPort=-1):
    gameState.setClient(Client(hostIP,hostPort))
def stopClient():
    gameState.getClient().socket.close()
    gameState.setClient(None)
#    clientThread = ClientThread(hostIP)
#    clientThread.daemon = True
#    clientThread.start()

