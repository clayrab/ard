from twisted.protocols import basic
from twisted.internet import protocol
from twisted.application import service, internet

class Room:
    def __init__(self):
        print 'new room'
        
class GameFinder(basic.LineReceiver):
    def connectionMade(self):
        print "Got new client!"
        self.factory.clients.append(self)
        
    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)
    def lineReceived(self, line):
        print "received", repr(line)
        for c in self.factory.clients:
            c.message(line)

    def message(self, message):
        self.transport.write(message + '\n')

factory = protocol.ServerFactory()
factory.protocol = GameFinder
factory.clients = []

application = service.Application("gameFindServer")
internet.TCPServer(2222, factory).setServiceParent(application)
