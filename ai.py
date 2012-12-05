import gameState
import gameLogic
import uiElements
import cDefines
#import random
print gameLogic
print gameLogic.Player


class AIPlayer(gameLogic.Player):
	def __init__(self,playerNumber,userName,requestHandler):
		if(userName == "Player ?"):
			gameLogic.Player.__init__(self,playerNumber,"AI " + str(gameState.nextAINumber),None,isAI=True)
		else:
			gameLogic.Player.__init__(self,playerNumber,userName,None,isAI=True)			
		gameState.nextAINumber = gameState.nextAINumber + 1
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
