from twisted.protocols import basic
from twisted.internet import protocol
from twisted.application import service, internet
from twisted.cred.portal import IRealm
from zope.interface import implements
import rsa
import MySQLdb
import hashlib
import time
import sys
from pprint import pprint as pp

privKey = rsa.PrivateKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537, 6977264057202623443995841153775681866813605135283831723778907294830864861810642621995438195929805731219864983148755866749414123928269010901281896813845553, 6795004418806002701275892780554702381414286837297772798037030472995866173266951571, 1073557403510678821257076760372205704035248017469579525573290803741034843)

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
    databaseConnection = MySQLdb.connect(host = "localhost",user = "clay",passwd = "maskboat",db = "ard")
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
#        strArgs = str(rsaKey.decrypt(args))
        strArgs = rsa.decrypt(args, privKey)
        tokens = strArgs.split(" ",1)
        hashFunc = hashlib.sha256()
        hashFunc.update(tokens[1])
        Connection.databaseCursor.execute("SELECT * from users WHERE username = '" + tokens[0] + "' and passhash = '" + hashFunc.digest() + "'")
        if(Connection.databaseCursor.rowcount > 0):
            users[tokens[0]] = self
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
