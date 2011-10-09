import socket
import threading
import SocketServer
import gameState
import client

class NetworkPlayer:
    nextPlayerNumber = 1
    def __init__(self,requestHandler):
        self.requestHandler = requestHandler
        self.playerNumber = NetworkPlayer.nextPlayerNumber
        NetworkPlayer.nextPlayerNumber = NetworkPlayer.nextPlayerNumber + 1
    def dispatchCommand(self,command):
        print 'dispatching...'
        self.requestHandler.wfile.write(command)
        print 'dispatched...'
            
class RequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while 1:
            line = self.rfile.readline()
            if not line:
                break
            else:
                print line
    def setup(self):
        if(gameState.getServer().acceptingConnections):
            SocketServer.StreamRequestHandler.setup(self)
            self.player = gameState.addNetworkPlayer(self)
            self.player.dispatchCommand("setPlayerNumber " + str(self.player.playerNumber) + "|")
            for player in gameState.getNetworkPlayers():
                self.player.dispatchCommand("addPlayer " + str(player.playerNumber) + "|")
                if(player.playerNumber != self.player.playerNumber):
                    player.dispatchCommand("addPlayer " + str(self.player.playerNumber) + "|")
            print str(self.client_address) + " connected."
        else:
            #TODO: send command to client indicating game has started or host is no longer accepting connections...
            print 'host is not accepting connections'
    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        gameState.removeNetworkPlayer(self.player)
        print str(self.client_address) + " disconnected."

class Server(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    def __init__(self,serverAddress):
        SocketServer.TCPServer.__init__(self,serverAddress,RequestHandler)
        self.listeners = []
        self.listenersLock = threading.Lock()
        self.acceptingConnections = True
    def addListener(self, listener):
        with self.listenersLock:
            self.listeners.append(listener)
    def removeListener(self, listener):
        with self.listenersLock:
            self.listeners.remove(listener)

def startServer(serverIP):
    server = Server((serverIP,8080))
    server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,0)
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True
    serverThread.start()
    gameState.setServer(server)
