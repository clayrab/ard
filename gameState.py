
import cDefines

foo = 'bar'

unitTypesList = []
#unitTypesList.append(unitType("summoner",cDefines.defines["MEEPLE_INDEX"],1.0,1.0,100))



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
