import gameState
import gameLogic
import server
import cDefines
import random

theAIs = {}

def addAIPlayer():
    player = aiPlayer()
    server.setupAI(player)
    theAIs[player.playerNumber] = player
#    theAIs.append(aiPlayer)
    print 'add ai'
def resetAIs():
    global theAIs
    theAIs = {}

class aiPlayer():
    def __init__(self):
        print 'init'
#        server.NetworkPlayer.nextPlayerNumber = server.NetworkPlayer.nextPlayerNumber + 1
    def dispatchCommand(self,command):
        return
    def takeTurn(self):
        eligibleMoveNodes = []
        for neighb in gameState.getGameMode().nextUnit.node.neighbors:
            if(neighb.unit == None):
                if(neighb.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX'] or (gameState.getGameMode().nextUnit.unitType.canFly)):
                    eligibleMoveNodes.append(neighb)
        if(len(eligibleMoveNodes) > 0):
            moveToNode = random.choice(eligibleMoveNodes)
#            moveToNode = eligibleMoveNodes[0]
            gameState.getGameMode().nextUnit.moveTo(moveToNode)
        else:
            gameState.getGameMode().nextUnit.skip()

	gameState.getClient().sendCommand("chooseNextUnit")

        print 'taketurn'
