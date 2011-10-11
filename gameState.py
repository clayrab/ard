import os
import copy
import re
import cDefines
import gameLogic
import threading
import server

unitTypesList = []
		
dirList=os.listdir("units")
for fileName in dirList:
	if(fileName != "template"):
		unitFile = open("units/"+fileName)
		tokens = unitFile.read().split("\n")
		tokens[0] = cDefines.defines[tokens[0]+"_INDEX"]
		tokens[1] = float(tokens[1])
		tokens[2] = float(tokens[2])
		tokens[3] = int(tokens[3])
		tokens[4] = int(tokens[4])
		tokens[5] = int(tokens[5])
		tokens[6] = bool(tokens[6])
		tokens[7] = bool(int(tokens[7]))
		tokens[8] = int(int(tokens[8]))
		tokens[9] = int(tokens[9])
		tokens[10] = int(tokens[10])
		tokens[11] = int(tokens[11])
		tokens[12] = int(tokens[12])
		unitTypesList.append(gameLogic.unitType(fileName.replace("_"," "),tokens[0],tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6],tokens[7],tokens[8],tokens[9],tokens[10],tokens[11],tokens[12]))

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

#theServer = None
#def setServer(server):
#	global theServer
#	theServer = server
#def getServer():
#	global theServer
#	return theServer

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
