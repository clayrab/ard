import cDefines
import gameLogic
import threading
import copy
import server

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

thePlayerNumber = 0
def setPlayerNumber(playerNumber):
	global thePlayerNumber
	thePlayerNumber = playerNumber
def getPlayerNumber():
	global thePlayerNumber
	return thePlayerNumber

class Player:
	def __init__(self,playerNumber):
		self.playerNumber = playerNumber
		self.isOwnPlayer = False

thePlayersLock = threading.Lock()
thePlayers = []
def addPlayer(playerNumber):
       	player = Player(playerNumber)
	with thePlayersLock:
		thePlayers.append(player)		
	getGameMode().redrawPlayers()
	return player
def removePlayer(playerNumber):
	with thePlayersLock:
		for aPlayer in theNetworkPlayers:
			if(aPlayer.playerNumber == player.playerNumber):
				theNetworkPlayers.remove(player)
def getPlayers():
	playersCopy = []
	with thePlayersLock:
		playersCopy = copy.copy(thePlayers)
	return playersCopy

networkPlayersLock = threading.Lock()
theNetworkPlayers = []
def addNetworkPlayer(requestHandler):
       	player = server.NetworkPlayer(requestHandler)
	with networkPlayersLock:
		theNetworkPlayers.append(player)
	return player
def removeNetworkPlayer(player):
	server.NetworkPlayer.nextPlayerNumber = server.NetworkPlayer.nextPlayerNumber - 1
	with networkPlayersLock:
		for aPlayer in theNetworkPlayers:
			if(aPlayer.playerNumber > player.playerNumber):
				aPlayer.playerNumber = aPlayer.playerNumber - 1
		theNetworkPlayers.remove(player)
def getNetworkPlayers():
	playersCopy = []
	with networkPlayersLock:
		playersCopy = copy.copy(theNetworkPlayers)
	return playersCopy
