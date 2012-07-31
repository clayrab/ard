import socket
import threading
import random
import gameState
import gameModes
import gameLogic
import uiElements
import rsa

gameFindHost = "94.75.231.214"
#gameFindHost = "94.75.235.221"

(pubKey, privKey) = rsa.newkeys(512)
#pubKey = "PublicKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537)"

#privKey = "PrivateKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537, 6977264057202623443995841153775681866813605135283831723778907294830864861810642621995438195929805731219864983148755866749414123928269010901281896813845553, 6795004418806002701275892780554702381414286837297772798037030472995866173266951571, 1073557403510678821257076760372205704035248017469579525573290803741034843)"

pubKey = rsa.PublicKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353,65537)
privKey = rsa.PrivateKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537, 6977264057202623443995841153775681866813605135283831723778907294830864861810642621995438195929805731219864983148755866749414123928269010901281896813845553, 6795004418806002701275892780554702381414286837297772798037030472995866173266951571, 1073557403510678821257076760372205704035248017469579525573290803741034843)

SERVER = -1
class Commands:
    @staticmethod
    def showGameRoom(args):	    
        tokens = args.split("*")
        gameState.setGameMode(gameModes.gameRoomMode,tokens)
    @staticmethod
    def removePlayer(args):	    
        if(hasattr(gameState.getGameMode(),"removePlayer")):
            gameState.getGameMode().removePlayer(args)
    @staticmethod
    def roomCount(args):
        tokens = args.split("*")
        if(hasattr(gameState.getGameMode(),"roomCountUpdate")):
               gameState.getGameMode().roomCountUpdate(tokens[0],tokens[1],tokens[2])
    @staticmethod
    def showRoom(args):
        tokens = args.split("|",1)
        gameState.setGameMode(gameModes.findGameMode,tokens)
    @staticmethod
    def versionPassed(args):
#        uiElements.smallModal("Login failed.")
        return
    @staticmethod
    def versionFailed(args):
        uiElements.smallModal("There is a new version of Ard available. You must get the update to play online.")
    @staticmethod
    def showLoginFailed(args):
        uiElements.smallModal("Login failed.")
    @staticmethod
    def addRoom(args):
        gameState.getGameMode().roomSelector.addRoom(args)
    @staticmethod
    def removeRoom(args):
        gameState.getGameMode().roomSelector.removeRoom(args)        
    @staticmethod    
    def showMessage(args):
        uiElements.smallModal(args)
    @staticmethod    
    def testConnectSuccess(args):
#        gameState.resetNetworkPlayers()
        gameState.getGameMode().modal.destroy()
    @staticmethod    
    def testConnectFail(args):
        uiElements.smallModal("Host test failed. Try again in 30 seconds or visit http://naqala.com/ard/hosting for details")
    @staticmethod
    def showChat(args):
        gameState.getGameMode().chatDisplay.addText(args)
        
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
        host = gameFindHost
        port = 26303
        self.socket.connect((host,port))
        self.socket.setblocking(0)
        self.commandLog = []
        self.delayedCommands = []
        self.sendCommand("verifyVersion",str(gameModes.version))
    def checkSocket(self):
        try:
            receivedData = self.socket.recv(1024)
        except:
            receivedData = ''
        for command in receivedData.split("\r\n"):
            if(len(command) > 0):
                tokens = command.split("~",1)
                if(len(tokens) > 1):
                    doCommand(tokens[0],args=tokens[1])
                else:
                    doCommand(tokens[0])
    def sendCommand(self,command,argsString=""):
        if(command == "login"):
            argsString = rsa.encrypt(argsString, pubKey)
        self.socket.send(command + " " + str(argsString) + "\r\n")
def startClient():
    gameState.setGameFindClient(Client())
def stopClient():
    gameState.getGameFindClient().socket.close()
    gameState.setGameFindClient(None)
#    clientThread = ClientThread(hostIP)
#    clientThread.daemon = True
#    clientThread.start()

