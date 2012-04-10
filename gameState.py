import os
import copy
import re
import cDefines
import gameLogic
import threading
import server
import json

mapDatas = []
mapDatas.append([])
mapDatas.append([])
mapDatas.append([])
mapDatas.append([])
dirList=os.listdir("maps")
for fileName in dirList:
	if((not fileName.startswith(".")) and not fileName.startswith("defaultMap") and (not fileName.endswith("~"))):
		file = open("maps/"+fileName)
		mapData = gameLogic.mapData(fileName,file.read())
		mapDatas[mapData.teamSize-1].append(mapData)
def getMapDatas():
	global mapDatas
	return mapDatas

unitTypesList = []
dirList=os.listdir("units")
for fileName in dirList:
	if((not fileName.startswith(".")) and fileName != "template" and (not fileName.endswith("~"))):
		unitFile = open("units/"+fileName)
		obj = json.load(unitFile)
		unitTypesList.append(gameLogic.unitType(fileName.replace("_"," ").strip(),cDefines.defines[obj['textureName']+"_INDEX"],cDefines.defines[obj['textureName']+"_OVERLAY_INDEX"],obj['movementSpeed'],obj['attackSpeed'],obj['attackPower'],obj['armor'],obj['range'],obj['health'],bool(obj['canFly']),bool(obj['canSwim']),obj['costGreen'],obj['costBlue'],obj['buildTime'],obj['movementSpeedBonus'],obj['researchCostGreen'],obj['researchCostBlue'],obj['researchTime']))
		unitFile.close()

theUnitTypes = {}
for unitType in unitTypesList:
	theUnitTypes[unitType.name] = unitType

configOptions = {}

configFile = open("config.txt")
for line in configFile:
	tokens = line.split("=")
	configOptions[tokens[0]] = tokens[1].strip()
configFile.close()
def getConfig():
	global configOptions
	return configOptions

userName = None
def getUserName():
	global userName
	return userName
def setUserName(uName):
	global userName
	userName = uName

theMapName = None
def getMapName():
    global theMapName
    return theMapName
def setMapName(mapName):
    global theMapName
    theMapName = mapName
    
theGameMode = None
def setGameMode(gameModeType,args=[]):
    global theGameMode
    theGameMode = gameModeType(args)
    if(hasattr(theGameMode,"loadMap")):
        theGameMode.loadMap()
    theGameMode.addUIElements()
    if(hasattr(theGameMode,"startGame")):
        theGameMode.startGame()
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

theGameFindClient = None
def setGameFindClient(client):
	global theGameFindClient
	theGameFindClient = client
def getGameFindClient():
	global theGameFindClient
	return theGameFindClient

thePlayerNumber = 0
def setPlayerNumber(playerNumber):
	global thePlayerNumber
	thePlayerNumber = playerNumber
def getPlayerNumber():
	global thePlayerNumber
#	if(thePlayerNumber == -2):
#		if(getGameMode().selectedNode != None and getGameMode().selectedNode.unit != None):
#			return getGameMode().selectedNode.unit.player
#		elif(getGameMode().nextUnit != None):
#			return getGameMode().nextUnit.player
#		else:
#			return 1
#	else:
	return thePlayerNumber

#thePlayersLock = threading.Lock()
thePlayers = []
def addPlayer(playerNumber):
       	player = gameLogic.Player(playerNumber)
#	with thePlayersLock:
       	thePlayers.append(player)		
	return player
def removePlayer(playerNumber):
#	with thePlayersLock:
	for aPlayer in thePlayers:
		if(aPlayer.playerNumber == player.playerNumber):
			thePlayers.remove(player)
def getPlayers():
	playersCopy = []
#	with thePlayersLock:
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

def resetNetworkPlayers():
	with networkPlayersLock:
		theNetworkPlayers = []
		server.NetworkPlayer.nextPlayerNumber = 1
