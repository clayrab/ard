import cDefines
import gameLogic

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
