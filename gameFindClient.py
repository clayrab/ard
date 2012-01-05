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
#        host = socket.gethostbyname("cynicsymposium.com")
        host = "127.0.0.1"
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

