import os
import copy
import re
import cDefines
import gameLogic
import threading
import server
import json
import Queue

#class gameState:
	
mapDatas = []
mapDatas.append([])
mapDatas.append([])
mapDatas.append([])
mapDatas.append([])
dirList=os.listdir("maps")
for fileName in dirList:
	if((not fileName.startswith(".")) and not fileName.startswith("defaultMap") and (fileName.endswith("map"))):
		file = open("maps/"+fileName)
		mapData = gameLogic.mapData(fileName,file.read())
		mapDatas[mapData.teamSize-1].append(mapData)
		file.close()
def getMapDatas():
	global mapDatas
	return mapDatas

playerUserNames = [False,False,False,False,False,False,False,False,]#need this because arbitrary players can leave, unlike ai players
def resetPlayerUserNames():
	global playerUserNames
	playerUserNames = [False,False,False,False,False,False,False,False,]
	
unitTypesList = []
dirList=os.listdir("units")
for fileName in dirList:
	if((not fileName.startswith(".")) and fileName != "template" and (not fileName.endswith("~"))):
		unitFile = open("units/"+fileName)
		obj = json.load(unitFile)
		unitTypesList.append(gameLogic.unitType(fileName.replace("_"," ").strip(),cDefines.defines[obj['textureName']+"_INDEX"],obj['movementSpeed'],obj['attackSpeed'],obj['attackPower'],obj['armor'],obj['range'],obj['health'],bool(obj['canFly']),bool(obj['canSwim']),obj['costRed'],obj['costBlue'],obj['buildTime'],obj['movementSpeedBonus'],obj['researchCostRed'],obj['researchCostBlue'],obj['researchTime']))
		unitFile.close()

global theUnitTypes
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
def getOwnUserName():
	global userName
	return userName
def setOwnUserName(uName):
	global userName
	userName = uName
def changeUserName(playerNumber,newUserName):
	thePlayers[playerNumber].userName = newUserName

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
    if(theGameMode != None and theGameMode.modal != None):
	    theGameMode.modal.destroy()
    theGameMode = gameModeType(args)
    if(hasattr(theGameMode,"loadMap")):
	    theGameMode.loadMap()
    theGameMode.addUIElements()
#    if(hasattr(theGameMode,"startGame")):
#	    theGameMode.startGame()

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

thePlayerNumber = -1
theTeamNumber = 0
def setPlayerNumber(playerNumber):
	global thePlayerNumber
	global theTeamNumber
	thePlayerNumber = playerNumber
	theTeamNumber = playerNumber/theTeamSize
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
def getTeamNumber():
	global theTeamNumber
	return theTeamNumber

theTeamSize = 1
def setTeamSize(teamSize):
	global theTeamSize
	theTeamSize = teamSize
def getTeamSize():
	global theTeamSize
	return theTeamSize

#thePlayersLock = threading.Lock()
thePlayers = [None]*8
def addPlayer(playerClass=gameLogic.Player,userName="Player ?",playerNumber=0,requestHandler=None,playerObj=None):
	player = None
	if(playerObj != None):
		player = playerClass(playerNumber=playerNumber,userName=userName,requestHandler=requestHandler,player=playerObj)
		thePlayers[playerNumber] = player
	elif(thePlayers[playerNumber] == None):#will be a NetworkPlayer already on the host
		player = playerClass(playerNumber=playerNumber,userName=userName,requestHandler=requestHandler)
		thePlayers[playerNumber] = player
	else:
		player = thePlayers[playerNumber]
	return player
def removePlayer(playerNumber):
	for index in range(0,8):
		player = thePlayers[index]
		if(player != None and player.playerNumber == playerNumber):
			thePlayers[index] = None
def movePlayer(oldNumber,newNumber):
	if(thePlayers[newNumber] == None):
		thePlayers[newNumber] = thePlayers[oldNumber]
		thePlayers[oldNumber] = None
		thePlayers[newNumber].playerNumber = newNumber
#		if(thePlayers[newNumber].userName == "Player " + str(oldNumber+1)):
#			thePlayers[newNumber].userName = "Player " + str(newNumber+1)
		if(oldNumber == getPlayerNumber()):
			setPlayerNumber(newNumber)
def resetPlayers():
	global thePlayers
	thePlayers = [None]*8
def getPlayers():
	global thePlayers
	return thePlayers
	
theAIs = [None]*8
def addAIPlayer(aiPlayer):
    theAIs[aiPlayer.playerNumber] = aiPlayer
def resetAIs():
    global theAIs
    theAIs = [None]*8

global nextAINumber
nextAINumber = 1

global researchProgress
researchProgress = [{},{},{},{},{},{},{},{},]
global availableUnitTypes
availableUnitTypes = [[],[],[],[],[],[],[],[],]
for i in range(0,8):
	availableUnitTypes[i].append(theUnitTypes["gatherer"])
	researchProgress[i][theUnitTypes["gatherer"]] = [1,0]
def getAvailableUnitTypes():
	global availableUnitTypes
	return availableUnitTypes[thePlayerNumber]

def getResearchProgress():
	global researchProgress
	return researchProgress[thePlayerNumber]

def reevalAvailableUnitTypes():
	global researchProgress
	global availableUnitTypes
	global theUnitTypes
	availableUnitTypes = [[],[],[],[],[],[],[],[],]
	for i in range(0,8):
		availableUnitTypes[i].append(theUnitTypes["gatherer"])
	for unit in theGameMode.units:
		if(unit.isMeditating and unit.unitType.name == "gatherer" and unit.node.city != None):
			for unitType in unit.node.city.unitTypes:
				if(availableUnitTypes[unit.player].count(unitType) == 0):
					availableUnitTypes[unit.player].append(unitType)
				if(not researchProgress[unit.player].has_key(unitType)):
					researchProgress[unit.player][unitType] = [1,0]
global doingAStarMove
doingAStarMove = False

global cursorIndex
cursorIndex = -2

global movePath
movePath = []

global aStarPath
aStarPath = []

global focusQueue
focusQueue = Queue.Queue()

global rendererUpdateQueue
rendererUpdateQueue = Queue.Queue()
