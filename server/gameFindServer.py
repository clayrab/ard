from twisted.protocols import basic
from twisted.internet import protocol
from twisted.application import service, internet
from twisted.cred.portal import IRealm
from zope.interface import implements
from Crypto.PublicKey import RSA
import MySQLdb
import hashlib
import time
import sys
from pprint import pprint as pp

rsaKey = RSA.importKey("""-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCJ5JSy/apuQQJ4OzsbT1EcnocXjNbdUgxGoUkDBq6QVwebGAon
i8aLd/vdyw90Q5dAxelJlTAKgvA7e1DmXlNaPRZ9CuwkfHcIAEeVoMnEmc0Enfwz
2PaA5dFCdsyifeiLjxH852sNcRQJjis5uCO/qRBIHxhGho31ggCgs/6qcQIDAQAB
AoGAEKjrRkzbgIKeN8SAOaZ1mE2W6MN9WjQFg6sM1S7DfHDnXFelMm3yyPrwFTXp
YhSge5TtwJQjv8FeIPGfLpYK39jD1ghC9xYQRnPozjx7Ey/LmwA+tAmZ3V4JJVs0
8NH8v1b4AqJ1a1fvzVxYcMRcC5fh6UPmZAmqmLZamkWtOYECQQC3cQ3ddfVJ6ZKv
kJOHoBJfPgXtEhno3jgTc1fiBZqoCH6jbb2y/g088qYV/yCICx24X5t/KLFXsilK
LDVueF2JAkEAwG9ZtNVTDVPTt419bu2SEC3H7TCTGynXaAttH7prpRGamxe/We2v
p5TFCnIoKe1PXj6zjL39B5Z3izPGwqnTqQJAVet1+wyM3xmvwtuMvjGTaVi7ndak
nBW5XiLgPtUxIxMXfaSg/X1Q5gMhF5xvuEi8mubtBhohNloUTNF4FU37QQJBALqA
8QNnITgwf2hNdD03eTG+/R5vzpMsCT4onNl8VunD1wDrkiQ5Td3wPMwz+aMxAZRI
1sHYPMzG0xOR2dg+ugkCQEWDWjG/HGn/lXKzAVyA8JGe0oGNlgme2p787ya2ixWA
9x6ZS1ohXmHsMcT1Ld/6j4sX8mA78GedJTuDN4ScAfw=
-----END RSA PRIVATE KEY-----""")

rooms = {}
users = {}
class Room:
    def __init__(self,name,parent,mapName=None,maxPlayers=None):
        self.name = name
        self.parent = parent
        self.mapName = mapName
        self.maxPlayers = maxPlayers
        self.childRooms = []
        self.subscribers = []
        rooms[name] = self
        if(self.parent != None):
            self.parent.childRooms.append(self)

class Connection(basic.LineReceiver):
    databaseConnection = MySQLdb.connect(host = "localhost",user = "clay",passwd = "maskmask",db = "ard")
    databaseCursor = databaseConnection.cursor()
    def connectionMade(self):
        self.userName = ""
        self.loggedIn = False
        self.currentRoom = None
        self.ownedRoom = None
        print "Got new client!"
        self.factory.clients.append(self)
        self.authenticated = False
    def connectionLost(self, reason):
        print "Lost a client!"
        if(self.ownedRoom != None):
            self.destroyRoom(self.ownedRoom)
        if(self.currentRoom != None):
            rooms[self.currentRoom.name].subscribers.remove(self)
        self.factory.clients.remove(self)
    def destroyRoom(self,room):
        print room.name
        print room.parent.childRooms
        room.parent.childRooms.remove(self)
        del rooms[self.name]
        #TODO: dispatch message to subscribers and subscribe them to parent
    #BEGIN COMMANDS
    def subscribe(self,args):
        roomName = args
        response = ""
        if(self.currentRoom != None):
            rooms[self.currentRoom.name].subscribers.remove(self)
        print rooms[roomName].subscribers
        rooms[roomName].subscribers.append(self)
        self.currentRoom = rooms[roomName]
        print 'currentroom: ' + str(self.currentRoom)
        if(rooms[roomName].mapName != None):
            response = response + "*" + rooms[roomName].mapName
            self.sendCommand("showGameRoom",roomName + response)
        else:
            for room in rooms[roomName].childRooms:
                response = response + "|" + room.name + "-" + str(len(room.subscribers))
            self.sendCommand("showRoom",roomName + response)
    def createRoom(self,args):
        tokens = args.split("|")
        if(self.ownedRoom != None):
            self.destroyRoom(self.ownedRoom)
        self.ownedRoom = Room(tokens[0],self.currentRoom,tokens[2],tokens[1])
        self.subscribe(self.ownedRoom.name)
        for subscriber in self.ownedRoom.parent:
            print subscriber
    def login(self,args):
#        strArgs = " ".join(args)
        strArgs = str(rsaKey.decrypt(args))
        tokens = strArgs.split(" ",1)
        hashFunc = hashlib.sha256()
        hashFunc.update(tokens[1])
        Connection.databaseCursor.execute("SELECT * from users WHERE username = '" + tokens[0] + "' and passhash = '" + hashFunc.digest() + "'")
        if(Connection.databaseCursor.rowcount > 0):
            self.loggedIn = True
            self.userName = tokens[0]
            self.subscribe("lobby")
        else:
            print "TODO: Send failed login message to client!"
    #END COMMANDS
    def doCommand(self,commandName,arguments=None):
        if(self.loggedIn or commandName == "login"):
            commandFunc = getattr(self,commandName)
            if(commandFunc != None):
                commandFunc(arguments)
            else:
                print "ERROR: COMMAND " + commandName + " does not exist"

    def lineReceived(self, line):
        tokens = line.split(" ",1)
        if(len(tokens) > 1):
            self.doCommand(tokens[0],arguments=tokens[1])
        else:
            self.doCommand(tokens[0])
    def sendCommand(self,command,arg):
        self.transport.write(command + "~" + arg + "\r\n")

factory = protocol.ServerFactory()
factory.protocol = Connection
factory.clients = []
lobby = Room("lobby",None)
Room("1v1",lobby)
Room("2v2",lobby)
Room("3v3",lobby)

application = service.Application("gameFindServer")
internet.TCPServer(2222, factory).setServiceParent(application)
