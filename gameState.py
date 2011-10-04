import cDefines
import gameLogic
import threading
import copy

unitTypesList = []
unitTypesList.append(gameLogic.unitType("summoner",cDefines.defines["MEEPLE_INDEX"],100.0,100.0,100))
unitTypesList.append(gameLogic.unitType("beaver",cDefines.defines["MEEPLE_INDEX"],100.0,100.0,100))
unitTypesList.append(gameLogic.unitType("catapult",cDefines.defines["MEEPLE_INDEX"],100.0,100.0,100))
unitTypesList.append(gameLogic.unitType("archer",cDefines.defines["MEEPLE_INDEX"],100.0,100.0,100))
unitTypesList.append(gameLogic.unitType("dragon",cDefines.defines["MEEPLE_INDEX"],100.0,100.0,100))

theUnitTypes = {}
for unitType in unitTypesList:
	theUnitTypes[unitType.name] = unitType

theMapName = None
def getMapName():
    global theMapName
    return theMapName
def setMapName(mapName):
    global theMapName
    theMapName = mapName
    
theGameMode = None
def setGameMode(gameModeType):
    global theGameMode
    theGameMode = gameModeType()
    if(hasattr(theGameMode,"loadMap")):
        theGameMode.loadMap()
    theGameMode.addUIElements()
def getGameMode():
    global theGameMode
    return theGameMode

theServer = None
def setServer(server):
	global theServer
	theServer = server
def getServer():
	global theServer
	return theServer

theHostIP = None
def setHostIP(hostIP):
	global theHostIP
	theHostIP = hostIP
def getHostIP():
	global theHostIP
	return theHostIP

theClient = None
def setClient(client):
	global theClient
	theClient = client
def getClient():
	global theClient
	return theClient


class Player:
	nextPlayerNumber = 1
	def __init__(self,requestHandler):
		print 'new player'
		self.requestHandler = requestHandler
		self.playerNumber = Player.nextPlayerNumber
		Player.nextPlayerNumber = Player.nextPlayerNumber + 1
	def dispatchCommand(self,command):
		self.requestHandler.wfile.write(command)

playersLock = threading.Lock()
thePlayers = []
def addPlayer(requestHandler):
	print '1'
       	player = Player(requestHandler)
	print '2'
	with playersLock:
		thePlayers.append(player)
	return player
def removePlayer(player):
	Player.nextPlayerNumber = Player.nextPlayerNumber - 1
	with playersLock:
		for aPlayer in thePlayers:
			if(aPlayer.playerNumber > player.playerNumber):
				aPlayer.playerNumber = aPlayer.playerNumber - 1
		thePlayers.remove(player)
def getPlayers():
	playersCopy = []
	with playersLock:
		playersCopy = copy.copy(thePlayers)
	return playersCopy
