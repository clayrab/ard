import gameState
import gameLogic
import uiElements
import cDefines
#import random

class AIPlayer(gameLogic.Player):
    AIAStar = gameLogic.aStarThread()
    def __init__(self,playerNumber,userName,requestHandler):
        if(userName == "Player ?"):
            gameLogic.Player.__init__(self,playerNumber,"AI " + str(gameState.nextAINumber),None,isAI=True)
        else:
            gameLogic.Player.__init__(self,playerNumber,userName,None,isAI=True)
        gameState.nextAINumber = gameState.nextAINumber + 1
        self.rankedCities = []
        self.startingNode = None
    def analyzeMap(self):
        self.rankedCities = []        
        AIPlayer.AIAStar.map = gameLogic.mapp(gameLogic.aStarNode,mapName=gameState.getMapName(),ignoreCities=True)
        for row in gameState.getGameMode().map.nodes:
            for node in row:
                if node.playerStartValue != 0:
                    print node.playerStartValue
                if node.playerStartValue == self.playerNumber+1:
                    self.startingNode = node
                    break
        for city in gameState.getGameMode().cities:
            print 'city'
            print city.node.yPos
            print city.node.xPos
            AIPlayer.AIAStar.startSearch(AIPlayer.AIAStar.map.nodes[city.node.yPos][city.node.xPos],AIPlayer.AIAStar.map.nodes[self.startingNode.yPos][self.startingNode.xPos],False,False)
            foundNodes = []
#            while(len(foundNodes) == 0):
#                foundNodes = AIPlayer.AIAStar.aStarSearchRecurse(True)
#            print foundNodes
#            print len(foundNodes)
#            self.rankedCities.append((len(foundNodes),city,))
 #       print self.rankedCities
#            print AIPlayer.AIAStar.closedNodes
#            print AIPlayer.AIAStar.openNodes
    def dispatchCommand(self,command):
        return
    def takeTurn(self):
        eligibleMoveNodes = []
        for neighb in gameState.getGameMode().nextUnit.node.neighbors:
            if(neighb.unit == None):
                if(neighb.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX'] or (gameState.getGameMode().nextUnit.unitType.canFly)):
                    eligibleMoveNodes.append(neighb)
        if(len(eligibleMoveNodes) > 0):
            moveToNode = eligibleMoveNodes[0]
            gameState.getClient().sendCommand("moveTo",str(moveToNode.xPos) + " " + str(moveToNode.yPos))
        else:
            gameState.getClient().sendCommand("skip")
        gameState.getClient().sendCommand("chooseNextUnit")

def analyzeMap():
    for player in gameState.getPlayers():
        if player != None and player.isAI:
            player.analyzeMap()
def addAIPlayer():
    players = gameState.getPlayers()
    for i in range(0,8):
        if(players[i] == None):
            aiPlayer = gameState.addPlayer(playerClass=AIPlayer,playerNumber=i,requestHandler=None)
            break
    gameState.addAIPlayer(aiPlayer)
    for player in gameState.getPlayers():
        if(player != None):
            player.dispatchCommand("addPlayer -1 " + str(aiPlayer.playerNumber) + ":" + aiPlayer.userName)
    return aiPlayer

class addAIButton(uiElements.clickableElement):
	def __init__(self,xPos,yPos):
		uiElements.clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("ADD_AI_BUTTON"),width=texWidth("ADD_AI_BUTTON"),height=texHeight("ADD_AI_BUTTON"))
	def onClick(self):
		addAIPlayer()
		gameState.getGameMode().soundIndeces.append(cDefines.defines["FINGER_CYMBALS_HIT_INDEX"])
