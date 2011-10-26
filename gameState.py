import os
import copy
import re
import cDefines
import gameLogic
import threading
import server
import json

unitTypesList = []
dirList=os.listdir("units")
for fileName in dirList:
	if((not fileName.startswith(".")) and fileName != "template" and (not fileName.endswith("~"))):
		print fileName
		unitFile = open("units/"+fileName)
		obj = json.load(unitFile)
		unitTypesList.append(gameLogic.unitType(fileName.replace("_"," ").strip(),cDefines.defines[obj['textureName']+"_INDEX"],obj['movementSpeed'],obj['attackSpeed'],obj['attackPower'],obj['armor'],obj['range'],obj['health'],bool(obj['canFly']),bool(obj['canSwim']),obj['cost'],obj['buildTime'],obj['movementSpeedBonus'],obj['armorBonus'],obj['attackPowerBonus'],obj['researchCost'],obj['researchTime']))

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
