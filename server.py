import threading
import SocketServer
import gameState

class RequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while 1:
            line = self.rfile.readline()
            if not line:
                break
            else:
                print line
    def setup(self):
        print 'setup'
        SocketServer.StreamRequestHandler.setup(self)
        self.player = gameState.addPlayer(self)
        print str(self.client_address) + " connected."
    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        gameState.removePlayer(self.player)
        print str(self.client_address) + " disconnected."

class Server(SocketServer.TCPServer):
    def __init__(self,serverAddress):
        SocketServer.TCPServer.__init__(self,serverAddress,RequestHandler)
        self.listeners = []
        self.listenersLock = threading.Lock()
    def addListener(self, listener):
        with self.listenersLock:
            self.listeners.append(listener)
    def removeListener(self, listener):
        with self.listenersLock:
            self.listeners.remove(listener)

class ServerThread(threading.Thread):
    def __init__(self,serverAddress):
        threading.Thread.__init__(self)
        gameState.setServer(Server(serverAddress))
    def run(self):
        gameState.getServer().serve_forever()
    def shutdown(self):
        gameState.getServer().shutdown()        

def startServer(serverIP):
    serverThread = ServerThread((serverIP,8080))
    serverThread.daemon = True
    serverThread.start()
