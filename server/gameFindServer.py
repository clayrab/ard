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
import socket

gameFindPort = 26303 
privKey = rsa.PrivateKey(7294827300696961467825209649910612955544688273739654133132828909790861956391138768640249164939907033611860365075051236361359042803639003856587767504588353, 65537, 6977264057202623443995841153775681866813605135283831723778907294830864861810642621995438195929805731219864983148755866749414123928269010901281896813845553, 6795004418806002701275892780554702381414286837297772798037030472995866173266951571, 1073557403510678821257076760372205704035248017469579525573290803741034843)

rooms = {}
users = {}
#self.ownedRoom = Room(tokens[0],self.currentRoom,tokens[2],tokens[1],self.transport.getPeer().host + ":" + str(self.transport.getPeer().port))
class Room:
    def __init__(self,name,parent,mapName=None,teamSize=None,hostIP=None,hostPort=None):
        self.name = name
        self.parent = parent
        self.mapName = mapName
        self.teamSize = teamSize
        self.hostIP = hostIP
        self.hostPort = hostPort
        self.childRooms = []
        self.subscribers = []
        rooms[name] = self
        if(self.parent != None):
            self.parent.childRooms.append(self)
class Connection(basic.LineReceiver):
    databaseConnection = MySQLdb.connect(host = "localhost",user = "clayrab_ard",passwd = "96c91f98",db = "clayrab_ard")
    databaseCursor = databaseConnection.cursor()
    def connectionMade(self):
        self.userName = None
        self.loggedIn = False
        self.currentRoom = None
        self.ownedRoom = None
        print "Got new client!"
        print self.transport.getPeer().host
        self.factory.clients.append(self)
        self.authenticated = False
    def connectionLost(self, reason):
        print "Lost a client!"
        if(self.currentRoom != None):
            rooms[self.currentRoom.name].subscribers.remove(self)
        if(self.ownedRoom != None):
            self.destroyRoom(self.ownedRoom)
        if(self.userName != None):
            del users[self.userName]
        self.factory.clients.remove(self)
    def destroyRoom(self,room):
        room.parent.childRooms.remove(room)
        for subscriber in room.subscribers:
            subscriber.subscribe(room.parent.name)
            subscriber.sendCommand("showMessage","The game you are in no longer exists")
        for subscriber in room.parent.subscribers:
            subscriber.sendCommand("removeRoom",room.name)
        del rooms[room.name]
    #BEGIN COMMANDS
    def subscribe(self,roomName):
        if(not roomName in rooms):
            self.sendCommand("showMessage","This room no longer exists.")
            return
        daRoom = rooms[roomName]
        if((daRoom.teamSize != None) and (len(daRoom.subscribers) >= (2*int(daRoom.teamSize)))):
            self.sendCommand("showMessage","This room is full.")
            return            
        if(self.currentRoom != None):
            rooms[self.currentRoom.name].subscribers.remove(self)
            for subscriber in rooms[self.currentRoom.name].subscribers:
                subscriber.sendCommand("removePlayer",self.userName)
        if(self.ownedRoom != None and self.ownedRoom.name != roomName):
            self.destroyRoom(self.ownedRoom)
            self.ownedRoom = None
        self.currentRoom = daRoom
        if(daRoom.mapName != None):
            for subscriber in self.currentRoom.subscribers:
                subscriber.sendCommand("addPlayer",self.userName)
        daRoom.subscribers.append(self)
        if(daRoom.parent != None):
            for subscriber in daRoom.parent.subscribers:
                subscriber.sendCommand("roomCount",roomName + "*" + str(len(daRoom.subscribers)) + "*" + str(daRoom.teamSize))
        if(daRoom.mapName != None):
            response = roomName + "*" + daRoom.mapName + "*" + daRoom.hostIP + "*" + daRoom.hostPort + "*" + daRoom.teamSize
            self.sendCommand("showGameRoom",response)
            for subscriber in self.currentRoom.subscribers:
                self.sendCommand("addPlayer",subscriber.userName)
        else:
            response = ""
            for room in daRoom.childRooms:
                response = response + "|" + room.name + "-" + room.mapName + "-" + str(len(room.subscribers)) + "-" + str(room.teamSize)
            self.sendCommand("showRoom",roomName + response)
    def chat(self, args):
        for subscriber in self.currentRoom.subscribers:
            subscriber.sendCommand("showChat",args)
    def testServer(self,args):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((self.transport.getPeer().host,int(args)))
            self.sendCommand("testConnectSuccess","")
#            sock.shutdown()
            sock.close()
            self.hostPort = args
        except:
            self.subscribe("lobby")
            self.sendCommand("testConnectFail","")
    def createGameRoom(self,args):
        tokens = args.split("|")
        if tokens[0] in rooms:
            self.sendCommand("showMessage","This game name is already taken.")
            return
        if(self.ownedRoom != None):
            self.destroyRoom(self.ownedRoom)
        self.ownedRoom = Room(tokens[0],self.currentRoom,tokens[2],tokens[1],self.transport.getPeer().host,self.hostPort)
        self.subscribe(self.ownedRoom.name)
        for subscriber in self.ownedRoom.parent.subscribers:
            subscriber.sendCommand("addRoom",self.ownedRoom.name + "-" + str(len(self.ownedRoom.subscribers)))
    def verifyVersion(self,args):
        print args
        self.sendCommand("versionFailed","")
        #self.sendCommand("versionPassed","")
    def login(self,args):
#        strArgs = " ".join(args)
#        strArgs = str(rsaKey.decrypt(args))
        strArgs = rsa.decrypt(args, privKey)
        tokens = strArgs.split(" ",1)
        hashFunc = hashlib.sha256()
        hashFunc.update(tokens[1])
        print tokens[1]
        print hashFunc.hexdigest()
        Connection.databaseCursor.execute("SELECT * from users WHERE username = '" + tokens[0] + "' and passhash = '" + hashFunc.hexdigest() + "'")
        if(Connection.databaseCursor.rowcount > 0 and not users.has_key(tokens[0])):
            users[tokens[0]] = self
            self.loggedIn = True
            self.userName = tokens[0]
            self.subscribe("lobby")
        else:
            self.sendCommand("showLoginFailed","")
                
            print "TODO: Send failed login message to client!"
    #END COMMANDS
    def doCommand(self,commandName,arguments=None):
        print commandName
#        if((self.loggedIn or commandName == "login") and commandName != "seedRNG" and commandName != "setPlayerNumber" and commandName != "setMap"):#when testing the host, these commands will come back
        if((self.loggedIn or commandName == "login" or commandName == "verifyVersion")):
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
#Room("1v1",lobby)
#Room("2v2",lobby)
#Room("3v3",lobby)

application = service.Application("gameFindServer")
internet.TCPServer(gameFindPort, factory).setServiceParent(application)
