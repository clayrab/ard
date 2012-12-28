import gameState
import gameLogic
import uiElements
import cDefines
import rendererUpdates
import random

class MODES:
    ATTACK_MODE = 0
    DEFEND_MODE = 1
    GATHER_MODE = 2
    GATHER_BLUE_MODE = 2
    RESEARCH_MODE = 4
class AIUnitData:
    def __init__(self):
        self.mode = None
        self.gotoNode = None
class AIPlayer(gameLogic.Player):
    AIAStar = gameLogic.aStarSearch
    def __init__(self,playerNumber,userName,requestHandler):
        if(userName == "Player ?"):
            gameLogic.Player.__init__(self,playerNumber,"AI " + str(gameState.nextAINumber),None,isAI=True)
        else:
            gameLogic.Player.__init__(self,playerNumber,userName,None,isAI=True)
        gameState.nextAINumber = gameState.nextAINumber + 1
        self.rankedCities = []
        self.enemyRankedCities = []        
        self.startingNode = None
        self.enemyStartingNodes = []
        self.nearestEnemyStartingNode = None
        self.nearestEnemy = None
        self.somewhatReasonableNumberOfCitiesToHaveOccupied = 0
#        self.units = []
#        self.workers = []
        self.workerCount = 0
        self.nonWorkerCount = 0
    @staticmethod
    def findPath(node1,node2):
        AIPlayer.AIAStar.startSearch(AIPlayer.AIAStar.map.nodes[node1.yPos][node1.xPos],AIPlayer.AIAStar.map.nodes[node2.yPos][node2.xPos],False,False)
        foundNodes = []
        while(len(foundNodes) == 0):
            foundNodes = AIPlayer.AIAStar.aStarSearchRecurse(True)
        return foundNodes
    @staticmethod
    def findDistance(node1,node2):
        return len(AIPlayer.findPath(node1,node2))
    def analyzeMap(self):
#        AIPlayer.AIAStar.map = gameLogic.mapp(gameLogic.aStarNode,mapName=gameState.getMapName(),ignoreCities=True)
        for row in gameState.getGameMode().map.nodes:
            for node in row:
                if node.playerStartValue != 0:
                    if gameState.getPlayers()[node.playerStartValue-1].team != self.team:
                        self.enemyStartingNodes.append(node)
                    if self.playerNumber == node.playerStartValue - 1:
                        self.startingNode = node
        #calculate distance to nearest cities and rank them:
        for city in gameState.getGameMode().cities:
            if(not(city.node.yPos == self.startingNode.yPos and city.node.xPos == self.startingNode.xPos)):
                self.rankedCities.append((AIPlayer.findDistance(city.node,self.startingNode),city,))
            else:
                self.rankedCities.append((0,city,))
        self.rankedCities.sort(lambda x,y:x[0]-y[0])
        #find nearest enemy starting node
        for startingNode in self.enemyStartingNodes:
            distance = AIPlayer.findDistance(startingNode,self.startingNode)
            if(self.nearestEnemy == None or distance < self.nearestEnemy[0]):
                self.nearestEnemy = (distance,startingNode,)
                self.nearestEnemyStartingNode = startingNode
        #calculate distance to nearest enemy's nearest cities and rank them:
        for city in gameState.getGameMode().cities:
            if(not(city.node.yPos == self.nearestEnemy[1].yPos and city.node.xPos == self.nearestEnemy[1].xPos)):
                self.enemyRankedCities.append((AIPlayer.findDistance(city.node,self.nearestEnemy[1]),city,))
            else:
                self.enemyRankedCities.append((0,city,))
        self.enemyRankedCities.sort(lambda x,y:x[0]-y[0])
        #account for units/count workers
        for unit in gameState.getGameMode().units:
            if unit.player == self.playerNumber:
                if unit.unitType.name != "gatherer":
                    self.nonWorkerCount = self.nonWorkerCount + 1
#        print "nearest enemy: " + str(self.nearestEnemy)
#        print "ranked cities: " + str(self.rankedCities)
#        print "enemy ranked cities: " + str(self.enemyRankedCities)
        print "worker count: " + str(self.workerCount)
#       print self.rankedCities
#            print AIPlayer.AIAStar.closedNodes
#            print AIPlayer.AIAStar.openNodes
    def dispatchCommand(self,command):
        return
    def moveNextUnitToRandomNode(self):
        print 'moveNextUnitToRandomNode'
        rngState = random.getstate()
        eligibleMoveNodes = []
        for neighb in gameState.getGameMode().nextUnit.node.neighbors:
            if(neighb.unit == None):
                if(neighb.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX'] or (gameState.getGameMode().nextUnit.unitType.canFly)):
                    eligibleMoveNodes.append(neighb)
        if(len(eligibleMoveNodes) > 0):
            moveToNode = random.choice(eligibleMoveNodes)
            gameState.getClient().sendCommand("moveTo",str(moveToNode.xPos) + " " + str(moveToNode.yPos))
        else:
            gameState.getClient().sendCommand("skip")
        random.setstate(rngState)
    def chooseRandomBuildableUnitType(self):
        print 'chooseRandomBuildableUnitType'
        rngState = random.getstate()
        eligibleUnitTypes = []
        for unitType in gameState.researchProgress[self.playerNumber]:
            if unitType.name != "gatherer":
                eligibleUnitTypes.append(unitType)
        if(len(eligibleUnitTypes) == 0):
            retUnitType = gameState.researchProgress[self.playerNumber].keys()[0]
        else:
            retUnitType = random.choice(eligibleUnitTypes)
        random.setstate(rngState)
        return retUnitType
    def moveNextUnitTowardNode(self,node):
        if(node == gameState.getGameMode().nextUnit.node):#just a little precaution for now, hopefully the finished AI would never run into this situation
            self.moveNextUnitToRandomNode()
        else:
            path = AIPlayer.findPath(node,gameState.getGameMode().nextUnit.node)
            nextNode = gameState.getGameMode().map.nodes[path[0][1]][path[0][0]]
            if(nextNode.unit == None):
                gameState.getClient().sendCommand("moveTo",str(nextNode.xPos) + " " + str(nextNode.yPos))
            else:#needed in case the unit is completely surrounded by friendly units.
                gameState.getClient().sendCommand("skip")
    def findNearestTile(self,tileComparitor):
        searchDistance = 1
        retNode = None
        while(True):
            neighbs = gameState.getGameMode().nextUnit.node.getNeighbors(searchDistance)
            for node in neighbs:
                if(tileComparitor(node) and node.unit == None):
                    return node
            searchDistance += 1
    
#    def findNearestRedForest(self,comparitor):
#        return self.findNearestTile(lambda x:x.tileValue == cDefines.defines['RED_FOREST_TILE_INDEX'])
#    def findNearestCity(self):
#        return self.findNearestTile(lambda x:x.city != None)
    def takeTurn(self):
        nextUnit = gameState.getGameMode().nextUnit
        if(nextUnit.aiData == None):
            nextUnit.aiData = AIUnitData()
        if(nextUnit.unitType.name == "summoner"):
            print 'summoners turn'
            if(nextUnit.node.city != None):
                self.moveNextUnitToRandomNode()
            else:
                if(self.nonWorkerCount > self.workerCount):
                    buildUnitType = gameState.theUnitTypes["gatherer"]
                    self.workerCount+=1
                else:
                    buildUnitType = self.chooseRandomBuildableUnitType()
                    
                if(self.redWood >= (gameState.researchProgress[self.playerNumber][buildUnitType][0]*buildUnitType.costRed) and self.blueWood >= (gameState.researchProgress[self.playerNumber][buildUnitType][0]*buildUnitType.costBlue)):
                    print self.redWood
                    print self.blueWood
                    gameState.researchProgress[self.playerNumber]
                    gameState.getClient().sendCommand("startSummoning",str(nextUnit.node.xPos) + " " + str(nextUnit.node.yPos) + " " + buildUnitType.name)
                else:
                    #Should the summoner move somewhere? Where?
                    gameState.getClient().sendCommand("skip")

        elif(nextUnit.unitType.name == "gatherer"):
            print 'gatherers turn'
            if(nextUnit.aiData.mode == None):
                self.workerCount = self.workerCount + 1
                if(self.workerCount%10 == 0):
                    nextUnit.aiData.mode = MODES.RESEARCH_MODE
                elif(self.workerCount%5 == 0):
                    nextUnit.aiData.mode = MODES.GATHER_BLUE_MODE
                else:
                    nextUnit.aiData.mode = MODES.GATHER_MODE
            if(nextUnit.aiData.mode == MODES.GATHER_MODE):
                comparitorFunc = lambda node:node.tileValue == cDefines.defines['RED_FOREST_TILE_INDEX']
            elif(nextUnit.aiData.mode == MODES.GATHER_BLUE_MODE):
                comparitorFunc = lambda node:node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX']
            else:
                comparitorFunc = lambda node:node.city != None
            print comparitorFunc(nextUnit.node)
            if(comparitorFunc(nextUnit.node)):
                gameState.getClient().sendCommand("startMeditating",str(nextUnit.node.xPos) + " " + str(nextUnit.node.yPos))
            else:
                if(nextUnit.aiData.gotoNode == None or nextUnit.aiData.gotoNode.unit != None):
                    nextUnit.aiData.gotoNode = self.findNearestTile(comparitorFunc)
                self.moveNextUnitTowardNode(nextUnit.aiData.gotoNode)
#             if(nextUnit.aiData.mode == MODES.GATHER_MODE):
#                 if(nextUnit.node.tileValue == cDefines.defines['RED_FOREST_TILE_INDEX']):
#                     gameState.getClient().sendCommand("startMeditating",str(nextUnit.node.xPos) + " " + str(nextUnit.node.yPos))
#                 else:
#                     if(nextUnit.aiData.gotoNode == None or nextUnit.aiData.gotoNode.unit != None):
#                         nextUnit.aiData.gotoNode = self.findNearestRedForest()
#                     self.moveNextUnitTowardNode(nextUnit.aiData.gotoNode)
#             else:#MODES.RESEARCH_MODE
#                 print 'unimplemented!!!'
#                 if(nextUnit.node.city != None):
#                     gameState.getClient().sendCommand("startMeditating",str(nextUnit.node.xPos) + " " + str(nextUnit.node.yPos))
#                 else:
#                     if(nextUnit.aiData.gotoNode == None or (nextUnit.aiData.gotoNode.unit != None and nextUnit.aiData.gotoNode.unit.isMeditating)):
#                         nextUnit.aiData.gotoNode = self.findNearestCity()
#                     self.moveNextUnitTowardNode(nextUnit.aiData.gotoNode)
        else:
            print 'units turn'
            self.moveNextUnitTowardNode(self.nearestEnemyStartingNode)
            #self.moveNextUnitToRandomNode()
        gameState.getClient().sendCommand("chooseNextUnit")
        print 'turn done'
#def analyzeMap():
#    for player in gameState.getPlayers():
#        if player != None and player.isAI:
#            player.analyzeMap()
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
