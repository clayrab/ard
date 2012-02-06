import socket
import threading
import random
import gameState
import gameModes
import gameLogic
import uiElements
print '1'
import rsa
import hashlib

print '2'
print rsa.__path__
(pubKey, privKey) = rsa.newkeys(512)
print pubKey
print privKey
#pubKey = "PublicKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537)"

#privKey = "PrivateKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537, 6977264057202623443995841153775681866813605135283831723778907294830864861810642621995438195929805731219864983148755866749414123928269010901281896813845553, 6795004418806002701275892780554702381414286837297772798037030472995866173266951571, 1073557403510678821257076760372205704035248017469579525573290803741034843)"

pubKey = rsa.PublicKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353,65537)
privKey = rsa.PrivateKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537, 6977264057202623443995841153775681866813605135283831723778907294830864861810642621995438195929805731219864983148755866749414123928269010901281896813845553, 6795004418806002701275892780554702381414286837297772798037030472995866173266951571, 1073557403510678821257076760372205704035248017469579525573290803741034843)

SERVER = -1
SINGLE_PLAYER = -2
class Commands:
    @staticmethod
    def showGameRoom(args):	    
        print args
        gameState.setGameMode(gameModes.gameRoomMode) 
        print 'show game room'
    @staticmethod
    def showRoom(args):
        tokens = args.split("|",1)
        gameState.setGameMode(gameModes.gameFindMode,tokens)
#        gameState.getGameMode().roomSelector.drawRooms(tokens[1])

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

def doCommand(commandName,args=None):
    commandFunc = getattr(Commands,commandName)
    if(commandFunc != None):
        commandFunc(args)
    else:
        print "ERROR: COMMAND " + commandName + " does not exist"

class Client:
    def __init__(self):        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname("cynicsymposium.com")
#        host = "127.0.0.1"
        port = 2222
        self.socket.connect((host,port))
        self.socket.setblocking(0)
        self.commandLog = []
        self.delayedCommands = []
        self.sendCommand("subscribe","lobby")
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
            argsString = rsa.encrypt(argsString, pubKey)
        self.socket.send(command + " " + str(argsString) + "\r\n")
        print 'sent...'
def startClient():
    gameState.setGameFindClient(Client())
#    clientThread = ClientThread(hostIP)
#    clientThread.daemon = True
#    clientThread.start()

