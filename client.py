import gameModes
import socket
import threading
import gameState


class Commands:
    @staticmethod
    def setMap(mapName):
        print 'setting map... '
        gameState.setMapName(mapName)
        print gameState.getMapName()
    @staticmethod
    def setPlayerNumber(playerNumber):
        print 'setting player num'
        gameState.setPlayerNumber(playerNumber)
        print gameState.getPlayerNumber()
    @staticmethod
    def addPlayer(playerNumber):
        print 'adding player...'
        player = gameState.addPlayer(playerNumber)
        if(gameState.getPlayerNumber() == player.playerNumber):
            print 'it me!'
            player.isOwnPlayer = True
    @staticmethod
    def startGame():
        print 'starting game...'
        gameState.setGameMode(gameModes.playMode)

def doCommand(commandName,args=None):
    print 'doing ' + commandName 
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
        while(self.isAlive()):
            print 'run...'
            receivedData = self.socket.recv(1024)
            print "receivedData: " + receivedData
            for command in receivedData.split("|"):
                if(len(command) > 0):
                    tokens = command.split(" ",1)
                    if(len(tokens) > 1):
                        doCommand(tokens[0],args=tokens[1])                    
                    else:
                        doCommand(tokens[0])
        else:
            #TODO: create a socketLock and call these explicitely
            print '*****SOCKET SHUTTING DOWN*****'
            self.socket.shutdown()
            self.socket.close()
            print '*****SOCKET SHUT DOWN*****'
    
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
        gameState.setClient(self)
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
        
def startClient(hostIP):
    Client(hostIP)
#    clientThread = ClientThread(hostIP)
#    clientThread.daemon = True
#    clientThread.start()

