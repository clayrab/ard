import gameState
import nameGenerator
import cDefines
import copy
import uiElements
import gameModes
import client
import server
import random
import threading
import thread
import time
import sys
import socket
import ai
import rendererUpdates
import uuid
from multiprocessing import Process, Queue, Pipe
#import aStar

#thread.stack_size(32768)
#thread.stack_size(1024*1024)
#print "thread stack size: " + str(thread.stack_size())
#sys.setcheckinterval(10)

#researchBuildTime = 100
#unitBuildSpeed = 0.1
STARTING_RED_WOOD = 250.0
STARTING_BLUE_WOOD = 0.0
#STARTING_RED_WOOD = 8000.0
#STARTING_BLUE_WOOD = 8000.0
INITIATIVE_ACTION_DEPLETION = 100.0
RESOURCE_COLLECTION_RATE = 0.15
#at RESOURCE_COLLECTION_RATE = 0.15 one gatherer will gather 15 green wood per 100 'ticks'(i.e. the build time of a gatherer)
ZOOM_SPEED = 0.15 
#MOUNTAIN_ATTACK_BONUS_MULTIPLIER = 1.0
FIRE_SPEED = 10
FIRE_POWER = 3
FIRE_SPREAD_CHANCE = 0.99
FIRE_LIVE_CHANCE = 0.99
FIRE_VITALITIY_SPREAD_EFFECT = 0.9
FIRE_VITALITIY_LIVE_EFFECT = 0.01
FIRE_ATTACK_POWER = 3.0
ICE_SPEED = 10
UNIT_SLIDE_SPEED = 2.20
class MODES:
	MOVE_MODE = 0
	ATTACK_MODE = 1
	SELECT_MODE = 2
	HEAL_MODE = 3
SIN60 = 0.86602540378
COS60 = 0.5
cityNames = ["Eshnunna","Tutub","Der","Sippar","Sippar-Amnanum","Kutha","Jemde Nasr","Kish","Babilim","Borsippa","Mashkan-shapir","Dilbat","Nippur","Marad","Adab","Isin","Kisurra","Shuruppak","Bad-tibira","Zabalam","Umma","Girsu","Lagash","Urum","Uruk","Larsa","Ur","Kuara","Eridu","Akshak","Akkad","Urfa","Shanidar cave","Urkesh","Shekhna","Arbid","Harran","Chagar Bazar","Kahat","El Fakhariya","Arslan Tash","Carchemish","Til Barsip","Nabada","Nagar","Telul eth-Thalathat","Tepe Gawra","Tell Arpachiyah","Shibaniba","Tarbisu","Ninua","Qatara","Dur Sharrukin","Tell Shemshara","Arbil","Imgur-Enlil","Nimrud","Emar","Arrapha","Kar-Tukulti-Ninurta","Ashur","Nuzi","al-Fakhar","Terqa","Mari","Haradum","Nerebtum","Agrab","Dur-Kurigalzu","Shaduppum","Seleucia","Ctesiphon","Zenobia","Zalabiye","Hasanlu","Takht-i-Suleiman","Behistun","Godin Tepe","Chogha Mish","Tepe Sialk","Susa","Kabnak","Dur Untash","Pasargadai","Naqsh-e Rustam","Parsa","Anshan","Konar Sandal","Tepe Yahya","Miletus","Sfard","Nicaea","Sapinuwa","Yazilikaya","Alaca Hoyuk","Masat Hoyuk","Hattusa","Ilios","Kanesh","Arslantepe","Sam'al","Beycesultan","Adana","Karatepe","Tarsus","Sultantepe","Attalia","Acre","Adoraim","Alalah","Aleppo","Al-Sinnabra","Aphek","Arad Rabbah","Ashdod","Ashkelon","Baalbek","Batroun","Beersheba","Beth Shean","Bet Shemesh","Bethany","Bet-el","Bezer","Byblos","Capernaum","Dan","Dimashq","Deir Alla","Dhiban","Dor","Ebla","En Gedi","Enfeh","Ekron","Et-Tell","Gath","Gezer","Gibeah","Gilgal Refaim","Gubla","Hamath","Hazor","Hebron","Herodion","Jezreel","Kadesh Barnea","Kedesh","Kumidi","Lachish","Megiddo","Qatna","Qumran","Rabat Amon","Samaria","Sarepta","Sharuhen","Shiloh","Sidon","Tadmor","Tirzah","Tyros","Ugarit","Umm el-Marra"]


def translateTilesXToPositionX(tileX,tileY):
	returnVal = -tileX*-(2.0*SIN60)
	if(abs(tileY)%2 == gameState.getGameMode().map.polarity):
		returnVal = returnVal + SIN60
#	return 0.0
	return returnVal;

def translateTilesYToPositionY(tileY):
#	return 0.0
	return (tileY*1.5);

class Player:
	def __init__(self,playerNumber,userName,requestHandler,isAI=False):
		self.userName = userName
		self.playerNumber = playerNumber
		self.isOwnPlayer = False
		self.redWood = STARTING_RED_WOOD
		self.blueWood = STARTING_BLUE_WOOD
		self.hasSummoners = True
		self.team = (self.playerNumber)/gameState.getTeamSize()
		self.isAI = isAI
class NetworkPlayer(Player):
	def __init__(self,playerNumber,userName,requestHandler,player=None):
		self.requestHandler = requestHandler
		Player.__init__(self,playerNumber,userName,None)
		if(player != None):
			self.isOwnPlayer = player.isOwnPlayer
			self.redWood = player.redWood
			self.blueWood = player.blueWood
			self.team = player.team
	def dispatchCommand(self,command):
		try:
			self.requestHandler.wfile.write(command + "|")
		except:
			print 'ERROR writing to network handler'
			return


class AIPlayer(Player):
	nextAINumber = 1
	def __init__(self,playerNumber,userName,requestHandler):
		if(userName == "Player ?"):
			Player.__init__(self,playerNumber,"AI " + str(AIPlayer.nextAINumber),None,isAI=True)
		else:
			Player.__init__(self,playerNumber,userName,None,isAI=True)
			
		AIPlayer.nextAINumber = AIPlayer.nextAINumber + 1
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
class unitType:
	def __init__(self,name,textureIndex,movementSpeed,attackSpeed,attackPower,armor,range,health,canFly,canSwim,costRed,costBlue,buildTime,movementSpeedBonus,researchCostRed,researchCostBlue,researchTime,canAttackGround=False):
		self.name = name
		self.textureIndex = textureIndex
		self.movementSpeed = movementSpeed
		self.attackSpeed = attackSpeed
		self.attackPower = attackPower
		self.armor = armor
		self.range = range
		self.health = health
		self.canFly = canFly
		self.canSwim = canSwim
		self.costRed = costRed
		self.costBlue = costBlue
		self.buildTime = buildTime
		self.movementSpeedBonus = movementSpeedBonus
#		self.armorBonus = armorBonus
#		self.attackPowerBonus = attackPowerBonus
		self.researchCostRed = researchCostRed
		self.researchCostBlue = researchCostBlue
		self.researchTime = researchTime
		self.canAttackGround = canAttackGround
#		print self.name
		if(self.name == "_archer"):
			print self.name
			print "attackpower:"+str(self.attackPower)
			print "armor:"+str(self.armor)
			print "range:"+str(self.range)
			print "health:"+str(self.health)
			print "canFly:"+str(self.canFly)
			print "canSwim:"+str(self.canSwim)
			print "cost:"+str(self.cost)
			print "buildTime:"+str(self.buildTime)
			print "movementSpeedBonus:"+str(self.movementSpeedBonus)
			print "armorBonus:"+str(self.armorBonus)
			print "attackPowerBonus:"+str(self.attackPowerBonus)
			print "researchCost:"+str(self.researchCost)
			print "researchTime:"+str(self.researchTime)
	def stringify(self):
		return self.name
class ice:
	def __init__(self,node):
		self.node = node
		self.movePoints = 0
		self.speed = ICE_SPEED
	def move(self):
		self.movePoints = self.movePoints + INITIATIVE_ACTION_DEPLETION
		print 'ice move'

class fire:
	def __init__(self,node,vitality=1.0):
		self.speed = FIRE_SPEED
		self.power = FIRE_POWER
		self.vitality = vitality
		self.node = node
		self.movePoints = 0
		self.weight = 1.0
	def move(self,vitality=0.0):
		self.movePoints = self.movePoints + INITIATIVE_ACTION_DEPLETION
		liveChanceMultiplier = 1-(FIRE_VITALITIY_LIVE_EFFECT/(FIRE_VITALITIY_LIVE_EFFECT+self.vitality))
		spreadChanceMultiplier = 1-(FIRE_VITALITIY_SPREAD_EFFECT/(FIRE_VITALITIY_SPREAD_EFFECT+self.vitality))
#		print str(self.vitality) + " " + str(spreadChanceMultiplier) + " " + str(liveChanceMultiplier)
		if(random.random() < FIRE_SPREAD_CHANCE*spreadChanceMultiplier):
#		if(random.random() < FIRE_SPREAD_CHANCE*self.vitality or True):
			eligibleNodes = []
			for node in self.node.neighbors:
				if(node.tileValue == cDefines.defines['WATER_TILE_INDEX']):
					return
				if(node.tileValue == cDefines.defines['RED_FOREST_TILE_INDEX'] or node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX']):
					eligibleNodes.append(node)
					eligibleNodes.append(node)
					eligibleNodes.append(node)
					##forest tiles get spread to easily
				eligibleNodes.append(node)
			spreadToNode = random.choice(eligibleNodes)
			if(spreadToNode.fire != None):
				spreadToNode.fire.vitality = spreadToNode.fire.vitality + 0.25*self.vitality
			else:
				spreadToNode.addFire(fire(spreadToNode,0.25*self.vitality))
			self.vitality=0.75*self.vitality
		if(random.random() > FIRE_LIVE_CHANCE*liveChanceMultiplier):#die
			if(self.vitality > 0.1):
				eligibleNodes = []
				for node in self.node.neighbors:
					if node.fire != None and node.fire.vitality > self.vitality:
						eligibleNodes.append(node)
				if(len(eligibleNodes) > 0):
					dieToNode = random.choice(eligibleNodes)
					dieToNode.fire.vitality = dieToNode.fire.vitality + (self.vitality/2.0)
			gameState.getGameMode().elementalEffects.remove(self)
			self.node.fire = None

class unit(object):
	def __init__(self,unitType,player,node,level=None):
		self.id = uuid.uuid4()
		self.unitType = unitType
		self.player = player
		self.team = (self.player)/gameState.getTeamSize()
		self.ai = gameState.theAIs[self.player]
		self._node = None
		self.xPos = 0.0
		self.yPos = 0.0
		self.xPosDraw = 0.0
		self.yPosDraw = 0.0
		self.movementPoints = 0
		self.attackPoints = 0
		self.buildPoints = self.unitType.buildTime	
		self.movePath = []
		self.gotoNode = None
#		self.waiting = False
		if(level != None):
			self.level = level
		else:
			self.level = gameState.researchProgress[self.player][self.unitType][0]
		self.health = self.unitType.health*self.level
#		self.gatheringNode = None
		self.isMeditating = False
#		self.recentDamage = {}
		self.researching = False
		self.researchUnitType = None
		self.unitBeingBuilt = None
		self.cancelledUnits = []
		self.buildQueue = []

	@property
	def node(self):
		return self._node
	@node.setter
	def node(self,theNode):
		self.xPos = translateTilesXToPositionX(theNode.xPos,theNode.yPos)
		self.yPos = translateTilesYToPositionY(theNode.yPos)
		if(self._node == None):
			self.xPosDraw = translateTilesXToPositionX(theNode.xPos,theNode.yPos)
			self.yPosDraw = translateTilesYToPositionY(theNode.yPos)
		self._node = theNode
	def setPosition(self,xPos,yPos):
		return
		if(self.xPosDraw == -100000.0):
			self.xPosDraw = xPos
			self.yPosDraw = yPos
		else:
#			if(self.node.visible):
#				gameState.getGameMode().animationQueue.put((self,))
			self.xPos = xPos
			self.yPos = yPos
	def slide(self,deltaTicks):
		return
		if(self.yPosDraw == self.yPos):
			if(self.xPosDraw > self.xPos):
				self.xPosDraw = self.xPosDraw - (0.010*UNIT_SLIDE_SPEED*deltaTicks)
				if(self.xPosDraw < self.xPos):
					self.xPosDraw = self.xPos
			elif(self.xPosDraw < self.xPos):
				self.xPosDraw = self.xPosDraw + (0.010*UNIT_SLIDE_SPEED*deltaTicks)
				if(self.xPosDraw > self.xPos):
					self.xPosDraw = self.xPos
		else:
			if(self.xPosDraw > self.xPos):
				self.xPosDraw = self.xPosDraw - (0.005*UNIT_SLIDE_SPEED*deltaTicks)
				if(self.xPosDraw < self.xPos):
					self.xPosDraw = self.xPos
			elif(self.xPosDraw < self.xPos):
				self.xPosDraw = self.xPosDraw + (0.005*UNIT_SLIDE_SPEED*deltaTicks)
				if(self.xPosDraw > self.xPos):
					self.xPosDraw = self.xPos
			if(self.yPosDraw > self.yPos):
				self.yPosDraw = self.yPosDraw - (0.00806*UNIT_SLIDE_SPEED*deltaTicks)
				if(self.yPosDraw < self.yPos):
					self.yPosDraw = self.yPos
			elif(self.yPosDraw < self.yPos):
				self.yPosDraw = self.yPosDraw + (0.00806*UNIT_SLIDE_SPEED*deltaTicks)
				if(self.yPosDraw > self.yPos):
					self.yPosDraw = self.yPos
	def stringify(self):
		retStr = ""
		retStr = retStr + self.unitType.name+"|"
		retStr = retStr + str(self.player)+"|"
		retStr = retStr + str(self.team)+"|"
		retStr = retStr + str(self.node.xPos)+"|"
		retStr = retStr + str(self.node.yPos)+"|"
		retStr = retStr + str(self.movementPoints)+"|"
		retStr = retStr + str(self.attackPoints)+"|"
		retStr = retStr + str(self.buildPoints)+"|"
		if(self.gotoNode != None):
			retStr = retStr + str(self.gotoNode.xPos)+","+str(self.gotoNode.yPos)+"|"
		else:
			retStr = retStr + "None|"
		retStr = retStr + str(self.level)+"|"
		retStr = retStr + str(self.health)+"|"
		retStr = retStr + str(self.isMeditating)+"|"
		for node in self.movePath:
			retStr = retStr + str(node.xPos)+","+str(node.yPos)+"_"
		return retStr
	def isControlled(self):
		if(gameState.getPlayers()[self.player] != None):
			return gameState.getPlayers()[self.player].isOwnPlayer
		else:
			return False
	def isOwnUnit(self):
		return (gameState.getPlayerNumber() == self.player)
	def isOwnTeam(self):
		if(gameState.getPlayerNumber() == -2):
			return False
		else:
			return self.team == gameState.getTeamNumber()
	def getMaxHealth(self):
		return self.unitType.health*self.level
	def getAttackPower(self):
		return self.unitType.attackPower*self.level
	def getMovementSpeed(self):
		return self.unitType.movementSpeed + (self.unitType.movementSpeedBonus*(self.level-1))
	def getArmor(self):
		return self.unitType.armor*self.level
#	def gather(self,node):
#		gameState.getClient().sendCommand("gatherTo",str(self.node.xPos) + " " + str(self.node.yPos) + " " + str(node.xPos) + " " + str(node.yPos))
	def move(self):
#		for node in self.movePath:
#			node.onMovePath = False
#		gameState.movePath = []
#		gameState.rendererUpdateQueue.put(rendererUpdates.updateMovePath())
		gameState.aStarPath = []
		gameState.rendererUpdateQueue.put(rendererUpdates.updateAStarPath())
		if(self.movePath[0].unit != None):#ran into unit
			self.movePath = []
			gameState.rendererUpdateQueue.put(rendererUpdates.updateMovePath())
			gameState.getGameMode().focus(self.node)
		else:
			node = self.movePath[0]
			self.movePath = self.movePath[1:]
			gameState.getClient().sendCommand("moveTo",str(node.xPos) + " " + str(node.yPos))
			gameState.getClient().sendCommand("chooseNextUnit")
	def moveTo(self,node):
#		self.onMovePath = False
		for neighb in self.node.getNeighbors(5):
			neighb.stopViewing(self)
		for neighb in node.getNeighbors(5):
			neighb.startViewing(self)
		aStarSearch.parentPipe.send(["unitRemove",self.node.xPos,self.node.yPos])
		if(node.visible):
			aStarSearch.parentPipe.send(["unitAdd",node.xPos,node.yPos])
#			gameState.getGameMode().animationQueue.put((node.xPos,node.yPos,))
#			gameState.getGameMode().animationQueue.put((self,))
			gameState.rendererUpdateQueue.put(rendererUpdates.renderFocus(node.xPos,node.yPos))

		self.node.unit = None
		self.node = node
		node.unit = self
		gameState.rendererUpdateQueue.put(rendererUpdates.renderUnitChange(self))
		self.movementPoints = self.movementPoints + INITIATIVE_ACTION_DEPLETION
		gameState.getGameMode().gotoMode = False
	def heal(self,node):
		gameState.getClient().sendCommand("healTo",str(node.xPos) + " " + str(node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")
	def healTo(self,node):
#		self.waiting = False
		node.unit.health = node.unit.health + self.getAttackPower()
		self.attackPoints = self.attackPoints + INITIATIVE_ACTION_DEPLETION
		if(node.unit.health > node.unit.getMaxHealth()):
			node.unit.health = node.unit.getMaxHealth()
		gameState.getGameMode().gotoMode = False
#		selectNode(None)
	def attack(self,node):
		gameState.getClient().sendCommand("attackTo",str(node.xPos) + " " + str(node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")
	def attackTo(self,node):
#		self.waiting = False
		if(node.unit != None and node.unit.player != self.player):
			multiplier = 1
#			if(self.node.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
#				multiplier = multiplier + MOUNTAIN_ATTACK_BONUS_MULTIPLIER
			damage = ((self.getAttackPower()-node.unit.getArmor())*multiplier)
#			node.unit.recentDamage[gameState.getGameMode().ticks] = str(int(damage))
			gameState.rendererUpdateQueue.put(rendererUpdates.renderUnitChange(node.unit))
			if(damage < 1):
				damage = 1
			node.unit.health = node.unit.health - damage
			if(node.unit.health <= 0):
				for neighb in node.getNeighbors(5):
					neighb.stopViewing(node.unit)
				gameState.getGameMode().units.remove(node.unit)
				gameState.rendererUpdateQueue.put(rendererUpdates.renderRemoveUnit(node.unit))
				if(node.unit.unitType.name == "summoner"):
					gameState.getGameMode().summoners.remove(node.unit)
				aStarSearch.parentPipe.send(["unitRemove",node.xPos,node.yPos])
				if(node.unit.unitType == "gatherer" and node.city != None):
					gameState.reevaAvailableUnitTypes()
				node.unit = None
				if(gameState.getGameMode().selectedNode == node):
					selectNode(node)
		if(self.unitType.name == "red mage"):
			node.addFire(fire(node,self.level*1.0))
		elif(self.unitType.name == "blue mage"):
			if(node.fire != None):
				gameState.getGameMode().elementalEffects.remove(node.fire)
				node.fire = None
			for neighb in node.neighbors:
				if(neighb.fire != None):
					gameState.getGameMode().elementalEffects.remove(neighb.fire)
					neighb.fire = None
		self.attackPoints = self.attackPoints + INITIATIVE_ACTION_DEPLETION
		gameState.getGameMode().gotoMode = False
		selectNode(None)
	def skip(self):
		self.movementPoints = self.movementPoints + INITIATIVE_ACTION_DEPLETION
		if(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.ai == None):
			gameState.getGameMode().gotoMode = False
			selectNode(None)
	def queueResearch(self,unitType):
		self.buildQueue.append(unitType)
		if(self.unitBeingBuilt == None and not self.researching):
			self.buildNextFromQueue()			
	def unqueueResearch(self):
		if(len(self.buildQueue) > 0):
			self.buildQueue = self.buildQueue[:-1:]
		else:
			self.researching = False
			self.researchUnitType = None
	def queueUnit(self,unit):
		self.buildQueue.append(unit)
		if(self.unitBeingBuilt == None and not self.researching):
			self.buildNextFromQueue()
	def unqueueUnit(self):
		if(len(self.buildQueue) > 0):
			self.buildQueue = self.buildQueue[:-1:]
		else:
			self.unitBeingBuilt = None
	def buildNextFromQueue(self):
#		self.unitBeingBuilt = None
#		self.researching = False
#		self.researchUnitType = None
		if(len(self.buildQueue) > 0):
			nextThing = self.buildQueue[0]
			self.buildQueue = self.buildQueue[1:]
			if(hasattr(nextThing,"unitType")):#unit
				self.unitBeingBuilt = nextThing
			else:#unitType/research
				self.researching = True
				self.researchUnitType = nextThing
		else:
			self.isMeditating = False
#		if(len(self.buildQueue) > 0):
#			self.unitBeingBuilt = self.buildQueue[0]
#			self.buildQueue = self.buildQueue[1:]
#		else:
#			self.node.unit.waiting = False#wake up summoner
	def incrementBuildProgress(self):
#		if(self.node.unit != None and self.node.unit.unitType.name == "summoner" and self.node.unit.isMeditating):
		if(self.researching):
			if(self.researchUnitType != None):
				gameState.researchProgress[self.player][self.researchUnitType][1] = gameState.getResearchProgress()[self.researchUnitType][1] + 1
				if(gameState.researchProgress[self.player][self.researchUnitType][1] >= self.researchUnitType.researchTime):
					gameState.researchProgress[self.player][self.researchUnitType][0] = gameState.getResearchProgress()[self.researchUnitType][0] + 1
					gameState.researchProgress[self.player][self.researchUnitType][1] = 0
#						self.node.unit.waiting = False#wake up summoner
					self.researching = False
					self.researchUnitType = None
					self.buildNextFromQueue()
		else:
			if(self.unitBeingBuilt != None):
				self.unitBeingBuilt.buildPoints = self.unitBeingBuilt.buildPoints - 1
				if(self.unitBeingBuilt.buildPoints <= 0.0):
					self.node.addUnit(self.unitBeingBuilt)
					self.unitBeingBuilt = None
					self.buildNextFromQueue()
			
class city:
	def __init__(self,name,node,unitTypes=[],costOfOwnership=10):
		self.name = name
		self.node = node
		self.costOfOwnership = costOfOwnership#TODO: deprecated this
		self.unitTypes = unitTypes
#		self.unitTypes.append(gameState.theUnitTypes["summoner"])
#		self.unitTypes.append(gameState.theUnitTypes["gatherer"])	
#		self.unitTypes.extend(unitTypes)
		self.player = 0
		gameState.getGameMode().cities.append(self)

class node:
	def __init__(self,xPos,yPos,tileValue=cDefines.defines['GRASS_TILE_INDEX'],roadValue=0,city=None,playerStartValue=0):
		self.xPos = xPos
		self.yPos = yPos
		self.name = nameGenerator.getNextName()
		self.tileValue = tileValue
		self.roadValue = roadValue
		self.city = city
		self.playerStartValue = playerStartValue
		self.selected = False
#		self.onMovePath = False
#		self.cursorIndex = -1
		gameState.getGameMode().elementsDict[self.name] = self
		self.neighbors = []
		self.unit = None
		self.visible = True
	def getValue(self):
		return self.tileValue
	def findDistance(self,target,polarity):
		#'even row' means map polarity = 0 and row # is even OR map polarity = 0 and row # is odd...
		#polarity 0 means 'even' rows are to the left
		#polarity 1 means 'even' rows are to the right
		#if moving from even to odd row left gives you free x at 1,3,5...
		#if moving from even to odd row right gives you free x at 3,5,7...
		#if moving from odd to even row right gives you free x at 1,3,5...
		#if moving from odd to even row left gives you free x at 3,5,7...
		distance = float(abs(self.xPos - target.xPos))
		if(abs(self.yPos-target.yPos)%2 == 1):#one row is even, other is odd...
			if(self.yPos%2 == polarity):#self is even...
				if(self.xPos > target.xPos):
					distance = distance - (abs(self.yPos-target.yPos))/2
				else:
					distance = distance - (abs(self.yPos-target.yPos)+1)/2
			else:#self is odd
				if(self.xPos > target.xPos):
					distance = distance - (abs(self.yPos-target.yPos)+1)/2
				else:
					distance = distance - (abs(self.yPos-target.yPos))/2
		else:
			distance = distance - abs(self.yPos-target.yPos)/2
		if(distance < 0.0):
			distance = 0.0
		distance = distance + abs(self.yPos - target.yPos)
		return distance
	def addUnit(self,theUnit):
		if(self.unit == None and self.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX']):
			self.unit = theUnit
			theUnit.node = self
			gameState.getGameMode().units.append(theUnit)
			gameState.rendererUpdateQueue.put(rendererUpdates.renderNewUnit(self.unit))
			if(self.visible):
				aStarSearch.parentPipe.send(["unitAdd",self.xPos,self.yPos])
			if(theUnit.unitType.name == "summoner"):
				gameState.getGameMode().summoners.append(theUnit)
			if(theUnit.isOwnTeam()):
				for neighb in self.getNeighbors(5):
					neighb.startViewing(self.unit)
		else:
			hasEmptyNeighbor = False
			for neighb in self.neighbors:
				if(neighb.unit == None and neighb.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX']):
					hasEmptyNeighbor = True
					break
			if(hasEmptyNeighbor):
				randNeighb = random.choice(self.neighbors)
#				while(randNeighb.unit != None or randNeighb.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
				while(not(randNeighb.unit == None and randNeighb.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX'])):
					randNeighb = random.choice(self.neighbors)
				randNeighb.addUnit(theUnit)
			else:		
				(random.choice(self.neighbors)).addUnit(theUnit)
	def onRightClick(self):
		gameState.getGameMode().clickScroll = True

class playModeNode(node):
	isNeighbor = False
	mode = MODES.SELECT_MODE
#	openNodes = []
#	closedNodes = []
#	movePath = []
#	aStarMap = None
	def __init__(self,xPos,yPos,tileValue=cDefines.defines['GRASS_TILE_INDEX'],roadValue=0,city=None,playerStartValue=0):
		node.__init__(self,xPos,yPos,tileValue=tileValue,roadValue=roadValue,city=city,playerStartValue=playerStartValue)
#		self.closed = False
#		self.open = False
#		self.aStarKnownCost = 0.0
#		self.aStarHeuristicCost = 0.0
#		self.aStarParent = None
		self.visible = False
#		self.visible = True
		self.viewingUnits = []
		self.fire = None
		self.ice = None
	def addFire(self,fire):
		if(self.ice != None):
			gameState.getGameMode().elementalEffects.remove(self.ice)
			self.ice = None
		if(self.fire != None):
			self.fire.vitality = self.fire.vitality + fire.vitality
		else:
			if(self.tileValue != cDefines.defines['WATER_TILE_INDEX']):
				gameState.getGameMode().elementalEffects.append(fire)
				self.fire = fire
	def addIce(self,ice):
		if(self.fire != None):
			gameState.getGameMode().elementalEffects.remove(self.fire)
			self.fire = None
		if(self.ice != None):
			gameState.getGameMode().elementalEffects.remove(self.ice)
		gameState.getGameMode().elementalEffects.append(ice)
		self.ice = ice
		
#(self.fire)
	def startViewing(self,unit):
		if(unit.isOwnTeam() or gameState.getPlayerNumber() == -2):
			self.viewingUnits.append(unit)
#this doesn't work because the algorithm is simply to stop viewing all nodes in range before move and start viewing all nodes in range after move
#			if(not self.visible and self.unit != None and not self.unit.isOwnTeam() and len(unit.movePath) > 0):
#				for node in unit.movePath:
#					node.onMovePath = False
#				unit.movePath = []
			self.visible = True
			gameState.rendererUpdateQueue.put(rendererUpdates.renderNodeChange(self))

	def stopViewing(self,unit):
		if(unit in self.viewingUnits):
			self.viewingUnits.remove(unit)
		if(len(self.viewingUnits) <= 0):
			self.visible = False
			gameState.rendererUpdateQueue.put(rendererUpdates.renderNodeChange(self))
#			self.visible = True
	def onLeftClickDown(self):
		if(gameState.getGameMode().doFocus == 0 or True):
			if(playModeNode.mode == MODES.ATTACK_MODE):
				gameState.getGameMode().nextUnit.attack(self)
			elif(playModeNode.mode == MODES.HEAL_MODE):
				gameState.getGameMode().nextUnit.heal(self)
			elif(playModeNode.mode == MODES.MOVE_MODE):
				if(gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode.unit != None and (self.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX'] or (self.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX'] and gameState.getGameMode().selectedNode.unit.unitType.canFly))):
#					if(len(gameState.getGameMode().selectedNode.unit.movePath) > 0):
#						gameState.getGameMode().selectedNode.unit.gotoNode = None
#						gameState.movePath = gameState.getGameMode().selectedNode.unit.movePath
#						gameState.rendererUpdateQueue.put(rendererUpdates.updateMovePath())

#						for node in gameState.getGameMode().selectedNode.unit.movePath:
#							node.onMovePath = False


					gameState.getGameMode().selectedNode.unit.gotoNode = None
					gameState.getGameMode().selectedNode.unit.movePath = playModeNode.movePath
					if(len(gameState.getGameMode().selectedNode.unit.movePath) == 0):#movepath wasn't done calculating						
						if(playModeNode.isNeighbor):
							gameState.getGameMode().selectedNode.unit.gotoNode = None
							gameState.getGameMode().selectedNode.unit.movePath = []
							gameState.getGameMode().selectedNode.unit.movePath.append(self)
							
						else:
							gameState.getGameMode().selectedNode.unit.gotoNode = self
#							gameState.getGameMode().selectedNode.unit.gotoNode.onMovePath = True
							gameState.getGameMode().gotoMode = False
					else:
						gameState.getGameMode().selectedNode.unit.gotoNode = None
			else:
				selectNode(self)
	def toggleCursor(self):
#		gameState.movePath = []
#		if(gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode.unit != None and len(gameState.getGameMode().selectedNode.unit.movePath) != 0):
#			gameState.movePath = gameState.getGameMode().selectedNode.unit.movePath
#		gameState.rendererUpdateQueue.put(rendererUpdates.updateMovePath())



		if(gameState.getGameMode().doFocus == 1 or gameState.getGameMode().selectedNode == None or gameState.getGameMode().selectedNode.unit == None or gameState.getGameMode().selectedNode.unit.isMeditating or not gameState.getGameMode().selectedNode.unit.isControlled()):
			gameState.cursorIndex = cDefines.defines['CURSOR_POINTER_INDEX']
			playModeNode.mode = MODES.SELECT_MODE
		else:
			state = (
				gameState.getGameMode().selectedNode.unit != None,#0
				gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit,#1
				gameState.getGameMode().selectedNode.unit.isControlled(),#2
				self.findDistance(gameState.getGameMode().selectedNode,gameState.getGameMode().map.polarity) <= float(gameState.getGameMode().selectedNode.unit.unitType.range),#3
				self.unit != None and self.visible,#4
				self.unit != None and not self.unit.isOwnTeam(),#5
				gameState.getGameMode().selectedNode.unit.unitType.name == "white mage",#6
				gameState.getGameMode().selectedNode != None and self == gameState.getGameMode().selectedNode,#7
				self.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX'],#8(8 and 9 are deprecated)
				gameState.getGameMode().selectedNode.unit.unitType.canFly,#9
				playModeNode.isNeighbor,#10
				gameState.getGameMode().shiftDown,#11
				gameState.getGameMode().gotoMode,#12
				)
			if((not state[0]) or state[7]):
				gameState.cursorIndex = cDefines.defines['CURSOR_POINTER_INDEX']
				playModeNode.mode = MODES.SELECT_MODE
			elif(state[1:7] == (True,True,True,True,True,False)):
				gameState.cursorIndex = cDefines.defines['CURSOR_ATTACK_INDEX']
				playModeNode.mode = MODES.ATTACK_MODE
			elif(state[1:7] == (True,True,True,True,False,True)):
				gameState.cursorIndex = cDefines.defines['CURSOR_HEAL_INDEX']
				playModeNode.mode = MODES.HEAL_MODE
#			elif(((not state[4]) and ( (state[2] and state[12]) or (state[1] and state[2] and state[10] and (not state[11])) ) and ( (not state[8]) or (state[6:8] == (True,True)) ) )):
			elif(((not state[4]) and ( (state[2] and state[12]) or (state[1] and state[2] and state[10] and (not state[11])) ) )):
				#is neighbor or gotoMode and not a mountain or is mountain and canFly
				gameState.cursorIndex = cDefines.defines['CURSOR_MOVE_INDEX']
				playModeNode.mode = MODES.MOVE_MODE
#				self.onMovePath = True
				aStarSearch.search(self,gameState.getGameMode().selectedNode,gameState.getGameMode().selectedNode.unit.unitType.canFly,gameState.getGameMode().selectedNode.unit.unitType.canSwim)
			else:
				gameState.cursorIndex = cDefines.defines['CURSOR_POINTER_INDEX']
				playModeNode.mode = MODES.SELECT_MODE
	def getNeighbors(self,distance):
		neighbs = []
		for xDelta in range(0-distance,distance):
			for yDelta in range(0-distance,distance):
				if((self.yPos + yDelta >= 0) and (self.yPos + yDelta < len(gameState.getGameMode().map.nodes))):
					if((self.xPos + xDelta >= 0) and (self.xPos + xDelta < len(gameState.getGameMode().map.nodes[self.yPos + yDelta]))):
						if(self.findDistance(gameState.getGameMode().map.nodes[self.yPos + yDelta][self.xPos + xDelta],gameState.getGameMode().map.polarity) < 5.0):
							neighbs.append(gameState.getGameMode().map.nodes[self.yPos + yDelta][self.xPos + xDelta])
		return neighbs
	def onMouseOver(self):
#		if(playModeNode.mode == MODES.MOVE_MODE):
#			self.onMovePath = True
		if(hasattr(gameState.getGameMode(),"selectedNode") and gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode.unit != None):
			if(gameState.getGameMode().selectedNode.unit.node.neighbors.count(self) > 0):
				playModeNode.isNeighbor = True
			else:
				playModeNode.isNeighbor = False
		self.toggleCursor()
#	def onMouseOut(self):
#		self.onMovePath = False
	def onKeyUp(self,keycode):
		self.toggleCursor()

class mapEditorNode(node):
	def onLeftClickUp(self):
		self.clicked = False
		if(gameState.getGameMode().selectedCityNode != None and gameState.getGameMode().selectedCityNode.clicked != None and gameState.getGameMode().selectedCityNode.clicked):
			if(gameState.getGameMode().selectedCityNode != self):
				if(gameState.getGameMode().selectedCityNode.city != None):
					self.city = gameState.getGameMode().selectedCityNode.city
					gameState.getGameMode().selectedCityNode.city = None
					gameState.getGameMode().selectedCityNode.selected = False
					self.selected = True
					gameState.getGameMode().selectedCityNode = self
	def onLeftClickDown(self):
		self.clicked = True
		if(gameState.getGameMode().selectedCityNode != None):
			gameState.getGameMode().selectedCityNode.selected = False
		self.selected = True
		uiElements.cityEditor.destroy()
		if(gameState.getGameMode().selectedButton != None):
			if(hasattr(gameState.getGameMode().selectedButton,"tileType")):
				if(gameState.getGameMode().selectedButton.tileType == cDefines.defines['ROAD_TILE_INDEX']):#new road
					self.roadValue = (~self.roadValue)&1
				elif(gameState.getGameMode().selectedButton.tileType == cDefines.defines['CITY_TILE_INDEX']):#new city
					if(self.city == None):
						self.city = city(random.choice(cityNames),self)
					uiElements.cityEditor.theCityEditor = uiElements.cityEditor(self.city)
					gameState.getGameMode().selectedCityNode = self
				else:
					self.tileValue = gameState.getGameMode().selectedButton.tileType
			else:
#				if(self.playerStartValue == gameState.getGameMode().selectedButton.playerNumber):
#					self.playerStartValue = 0
#					if(gameState.getGameMode().map.numPlayers == gameState.getGameMode().selectedButton.playerNumber and gameState.getGameMode().map.numPlayers != 1):
#						for button in playerStartLocationButton.playerStartLocationButtons:
#							if(button.playerNumber == gameState.getGameMode().map.numPlayers + 1):
#								button.color = "55 55 55"
#						gameState.getGameMode().map.numPlayers = gameState.getGameMode().map.numPlayers - 1
#				else:
				if(self.playerStartValue != gameState.getGameMode().selectedButton.playerNumber):	
					for row in gameState.getGameMode().map.nodes:
						for node in row:
							if(node.playerStartValue == gameState.getGameMode().selectedButton.playerNumber):
								node.playerStartValue = 0
					self.playerStartValue = gameState.getGameMode().selectedButton.playerNumber

class mapViewNode(node):
#	def __init__(self)
	def onClick(self):
		selectNode(self)			

#class aStarThread(threading.Thread):
class aStarThread():
	def __init__(self):
		self.openNodes = []
		self.closedNodes = []
		self.movePath = []
		self.map = None
		self.nodes = []
		self.polarity = 0
		self.startNode = None
		self.endNode = None
		self.canFly = False
		self.canSwim = True
		self.searchComplete = False
		self.parentPipe,self.childPipe = Pipe()
		self.queue = None
		self.keepAliveTime = time.clock()
#		self.doneSearching = True
		self.aStarLock = threading.RLock()
#		self.searchCompleteLock = threading.RLock()
#		threading.Thread.__init__(self)
#		Process.__init__(self)
	@staticmethod
	def runTarget(pipe):
		while True:
#			print aStarSearch.keepAliveTime
			if(time.clock() - aStarSearch.keepAliveTime > 30.0):
				print 'no keepalives sent, exiting.\n'
				sys.exit(0)
			if(pipe.poll()):
				data = pipe.recv()
				if(data[0] == "kill"):
					break
				elif(data[0] == "polarity"):
					aStarSearch.polarity = data[1]
				elif(data[0] == "map"):
					aStarSearch.map = mapp(aStarNode,mapName=data[1],ignoreCities=True)
				elif(data[0] == "unitAdd"):
					aStarSearch.map.nodes[data[2]][data[1]].unit = True
				elif(data[0] == "unitRemove"):
					aStarSearch.map.nodes[data[2]][data[1]].unit = False
#					aStarSearch.map.nodes[data[4]][data[3]].unit = True
				elif(data[0] == "keepalive"):
					aStarSearch.keepAliveTime = time.clock()
				else:
					if(not(aStarSearch.endNode == aStarSearch.map.nodes[data[3]][data[2]] and aStarSearch.startNode == aStarSearch.map.nodes[data[1]][data[0]])):
						aStarSearch.movePath = []
						aStarSearch.resetNodes()
						aStarSearch.canFly = data[4]
						aStarSearch.canSwim = data[5]
						aStarSearch.endNode = aStarSearch.map.nodes[data[3]][data[2]]
						aStarSearch.startNode = aStarSearch.map.nodes[data[1]][data[0]]
						aStarSearch.openNodes.append(aStarSearch.startNode)
						aStarSearch.aStarSearchRecurse()
			else:
				aStarSearch.aStarSearchRecurse()
        @staticmethod
        def search(startNode,endNode,canFly,canSwim):
		aStarSearch.parentPipe.send([startNode.xPos,startNode.yPos,endNode.xPos,endNode.yPos,canFly,canSwim])
	@staticmethod
	def keepAlive():
		aStarSearch.parentPipe.send(["keepalive"])
	def resetNodes(self):
		for node in self.openNodes:
			node.closed = False
			node.open = False
			node.aStarKnownCost = 0.0
			node.aStarHeuristicCost = 0.0
			node.aStarParent = None
		for node in self.closedNodes:
			node.closed = False
			node.open = False
			node.aStarKnownCost = 0.0
			node.aStarHeuristicCost = 0.0
			node.aStarParent = None
		self.openNodes = []
		self.closedNodes = []
	@staticmethod
	def aStarHeuristic(node1,node2,polarity):
		distance = float(abs(node1.xPos - node2.xPos))
		if(abs(node1.yPos-node2.yPos)%2 == 1):#one row is even, other is odd...
			if(node1.yPos%2 == polarity):#node1 is even...
				if(node1.xPos > node2.xPos):
					distance = distance - (abs(node1.yPos-node2.yPos))/2
				else:
					distance = distance - (abs(node1.yPos-node2.yPos)+1)/2
			else:#node1 is odd
				if(node1.xPos > node2.xPos):
					distance = distance - (abs(node1.yPos-node2.yPos)+1)/2
				else:
					distance = distance - (abs(node1.yPos-node2.yPos))/2
		else:
			distance = distance - abs(node1.yPos-node2.yPos)/2
		if(distance < 0.0):
			distance = 0.0
		distance = distance + abs(node1.yPos - node2.yPos)
		return distance

	def aStarSearchRecurse(self,count=0):
		if(len(aStarSearch.openNodes) == 0):
#			aStarSearch.searching = False
			return
		node = None
		for openNode in aStarSearch.openNodes:
			if(not openNode.closed):
				if(node == None):
					node = openNode
				if((openNode.aStarKnownCost + openNode.aStarHeuristicCost) < (node.aStarKnownCost + node.aStarHeuristicCost)):
					node = openNode
		if(node == aStarSearch.endNode):
			foundNodes = []
			nextNode = aStarSearch.endNode.aStarParent
			while nextNode != None:
				foundNodes.append([nextNode.xPos,nextNode.yPos])
				nextNode = nextNode.aStarParent
			aStarSearch.childPipe.send(foundNodes)
			aStarSearch.resetNodes()
			return
		node.closed = True
		aStarSearch.closedNodes.append(node)
		for neighbor in node.neighbors:
			if(not neighbor.closed):
				if(not neighbor.open):
					aStarSearch.openNodes.append(neighbor)
					neighbor.open = True
					neighbor.aStarParent = node
					aStarThread.aStarHeuristic(neighbor,aStarSearch.endNode,aStarSearch.polarity)
#					Neighbor.findAStarHeuristicCost(aStarSearch.endNode)
					if(neighbor.unit):
						neighbor.aStarKnownCost = node.aStarKnownCost + 999.9
					elif(neighbor.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX'] and not aStarSearch.canFly):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['MOUNTAIN_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['WATER_TILE_INDEX'] and not aStarSearch.canFly and not aStarSearch.canFly):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['WATER_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['FOREST_TILE_INDEX'] and not aStarSearch.canFly):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['FOREST_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					else:
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['GRASS_MOVE_COST']/(1.0+float(neighbor.roadValue)))
				else:#calculate whether new known path is shorter than old known path
					if(neighbor.unit != None):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + 999.9):
							neighbor.aStarKnownCost = node.aStarKnownCost + 999.9
					elif(neighbor.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['MOUNTAIN_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['MOUNTAIN_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['WATER_TILE_INDEX'] and aStarSearch.canSwim == False):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['WATER_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['WATER_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['FOREST_TILE_INDEX']):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['FOREST_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['FOREST_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					else:
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['GRASS_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['GRASS_MOVE_COST']/(1.0+float(neighbor.roadValue)))
		return

class aStarNode():
	def __init__(self,xPos,yPos,tileValue=cDefines.defines['GRASS_TILE_INDEX'],roadValue=0,city=None,playerStartValue=0):
		self.xPos = xPos
		self.yPos = yPos
		self.tileValue = tileValue
		self.roadValue = roadValue
		self.neighbors = []
		self.unit = False
		self.closed = False
		self.open = False
		self.aStarKnownCost = 0.0
		self.aStarHeuristicCost = 0.0
		self.aStarParent = None
#	def aStarSearch(self):
#		#start at end point so we can just track back and insert into an array in order
#		self.findAStarHeuristicCost(aStarSearch.endNode.unit.node)
#		aStarSearch.openNodes.append(self)
#		aStarSearch.aStarSearchRecurse(aStarSearch.endNode.unit.node)
#	def findAStarHeuristicCost(self,target):
		#current 'heuristic' is just the distance assuming everything is grass
		#I might want to change this to assume that everything is mountain... or somewhere in between... gotta think about it.
#		self.aStarHeuristicCost = self.findDistance(target,aStarSearch.map.polarity)


#aStarProcess.join()

class mapData:
	def __init__(self,name,mapDataString):
		self.dataString = mapDataString
		self.name = name[:len(name)-4]
		lineTokens = self.dataString.split("\n")
		self.teamSize = int(lineTokens[1])/2

class mapp:
	def __init__(self,nodeType,mapName="",ignoreCities=False):
		if(mapName == ""):
			self.mapName = gameState.getMapName()
		else:
			self.mapName = mapName
		self.ignoreCities = ignoreCities
		self.polarity = 0
		self.nodeType = nodeType
#		self.translateZ = 0.0-cDefines.defines['initZoom']#translateZ
		self.load()
#		self.loaded = True
#	def getLoaded(self):
#		temp = self.loaded
#		self.loaded = False
#		return temp
	def getWidth(self):
		return len(self.nodes[0])
	def getHeight(self):
		return len(self.nodes)
	def load(self):
		mapFile = open('maps/' + self.mapName + ".map",'r')
		self.nodes = []
		count = 0
		yPos = -1
		xPos = -1
		for line in mapFile:
			if(count == 0):#header
				#TODO add players and starting positions to map data
				self.polarity = int(line)
#				self.numPlayers = 2
			elif(count == 1):
				self.numPlayers = int(line)
			else:
				yPos = yPos + 1
				xPos = -1
				if(line.startswith("#")):#node
					newRow = []
					line = line.strip("#")
					for char in line:
						xPos = xPos + 1
						if(char != '\n'):
							intValue = ord(char)
							tileValue = intValue & 15
							roadValue = (intValue & 128)>>7
#							playerStartValue = (intValue & (32+64+128))>>5)
							playerStartValue = 0
							newNode = self.nodeType(xPos,yPos,tileValue,roadValue,None,playerStartValue=playerStartValue)
							if(xPos > 0):#add neighbor to the left
								newNode.neighbors.append(newRow[len(newRow)-1])
								newRow[len(newRow)-1].neighbors.append(newNode)
							if(yPos > 0):#add neighbors below
								if(not (xPos == 0 and (self.polarity+yPos)%2 == 1)):#has bottom left neighbor
									if((self.polarity+yPos)%2 == 0):
										newNode.neighbors.append(self.nodes[yPos-1][xPos])
										self.nodes[yPos-1][xPos].neighbors.append(newNode)
									else:
										newNode.neighbors.append(self.nodes[yPos-1][xPos-1])
										self.nodes[yPos-1][xPos-1].neighbors.append(newNode)
								if(not (xPos == len(self.nodes[0])-1 and (self.polarity+yPos)%2 == 0)):#has bottom right neighbor
									if((self.polarity+yPos)%2 == 0):
										newNode.neighbors.append(self.nodes[yPos-1][xPos+1])
										self.nodes[yPos-1][xPos+1].neighbors.append(newNode)
									else:
										newNode.neighbors.append(self.nodes[yPos-1][xPos])
										self.nodes[yPos-1][xPos].neighbors.append(newNode)
							newRow.append(newNode)
					self.nodes.append(newRow)
		                elif(line.startswith("*") and not self.ignoreCities):#city
					tokens = line.split(":")
					coords = tokens[0].strip("*").split(",")
					cityName = tokens[1]
					unitTypes = []
					if(len(tokens[2].strip()) != 0):
						unitTypeStrings = tokens[2].strip().split(",")
						for unitTypeString in unitTypeStrings:
							theUnitType = gameState.theUnitTypes[unitTypeString]
							unitTypes.append(theUnitType)
					costOfOwnership = tokens[3]
					self.nodes[int(coords[1])][int(coords[0])].city = city(cityName,self.nodes[int(coords[1])][int(coords[0])],unitTypes,costOfOwnership)
				elif(line.startswith("@")):#playerStartPosition
					tokens = line.split(":")
					coords = tokens[0].strip("@").split(",")
					playerStartValue = int(tokens[1])
					self.nodes[int(coords[1])][int(coords[0])].playerStartValue = playerStartValue
			count = count + 1
		mapFile.close()
#		fauxRowTop = []
#		fauxRowBottom = []
#		fauxXPos = -1
#		for node in self.nodes[0]:
#			fauxXPos = fauxXPos + 1
#			fauxRowTop.append(self.nodeType(fauxXPos,-1,cDefines.defines['MOUNTAIN_TILE_INDEX'],0,None))
#			fauxRowBottom.append(self.nodeType(fauxXPos,-1,cDefines.defines['MOUNTAIN_TILE_INDEX'],0,None))
#		self.nodes.append(fauxRowTop)
#		self.polarity = 1 if self.polarity == 0 else 0
#		self.nodes.insert(0,fauxRowBottom)
	def save(self):
		mapFile = open('maps/' + gameState.getMapName() + ".map",'w')
		yPos = 0
		xPos = 0
		playerStartLines = []
		cityLines = []
		nodeLines = []
		nodeLines.append(str(self.polarity) + "\n")
		nodeLines.append(str(self.numPlayers) + "\n")
		for row in self.nodes:
			xPos = 0
			yPos = yPos + 1
			line = "#"
			for node in row:
				xPos = xPos + 1
				line = line + chr(node.tileValue + (128*node.roadValue))#DON'T GO PAST 256, THIS NEEDS TO FIT INTO ONE BYTE
				if(node.city != None):
					unitTypes = ""
					for unitType in node.city.unitTypes:
						if(unitType.name != "summoner" and unitType.name != "gatherer"):
							unitTypes = unitTypes + "," + unitType.name
					unitTypes = unitTypes[1:]
					cityLines.append("*" + str(xPos-1) + "," + str(yPos-1) + ":" + node.city.name + ":" + unitTypes + ":" + str(node.city.costOfOwnership) + "\n")
				if(node.playerStartValue > 0):
					playerStartLines.append("@" + str(xPos-1) + "," + str(yPos-1) + ":" + str(node.playerStartValue) + "\n")
					
			nodeLines.append(line + "\n")
		mapFile.writelines(nodeLines)
		mapFile.writelines(cityLines)
		mapFile.writelines(playerStartLines)
		mapFile.close()
		print "saved"
	def getNodes(self):
		return self.nodes
	def getIterator(self):
		return self.nodes.__iter__()
	def setNumPlayers(self,numPlayers):
		self.numPlayers = numPlayers

def selectNode(node):
#	if(node != None and node.unit != None):
#		node.unit.health = node.unit.health - 2
#		gameState.rendererUpdateQueue.put(rendererUpdates.renderUnitChange(node.unit))
#	for pnode in playModeNode.movePath:
#		pnode.onMovePath = False
	playModeNode.movePath = []
	gameState.movePath = []
	gameState.aStarPath = []
	if(gameState.getGameMode().selectedNode != None):
		gameState.getGameMode().selectedNode.selected = False
#		gameState.getGameMode().selectedNode.onMovePath = False
#		if(gameState.getGameMode().selectedNode.unit != None and len(gameState.getGameMode().selectedNode.unit.movePath) > 0):
#			for pathNode in gameState.getGameMode().selectedNode.unit.movePath:
#				pathNode.onMovePath = False
	if(node != None):
		node.selected = True
		if(node.unit != None and len(node.unit.movePath) > 0):
			gameState.movePath = node.unit.movePath
#			for pathNode in node.unit.movePath:
#				pathNode.onMovePath = True
#		if(node.unit != None and node.unit.gotoNode != None):
#			node.unit.gotoNode.onMovePath = True
	gameState.rendererUpdateQueue.put(rendererUpdates.updateAStarPath())
	gameState.rendererUpdateQueue.put(rendererUpdates.updateMovePath())
	if(gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode != node and hasattr(gameState.getGameMode(),"gotoMode") and gameState.getGameMode().gotoMode):
		gameState.getGameMode().gotoMode = False		
	gameState.getGameMode().selectedNode = node
	gameState.rendererUpdateQueue.put(rendererUpdates.setSelectedNode())	
	if(uiElements.viewer.theViewer != None):
		uiElements.viewer.theViewer.destroy()
	if(uiElements.unitTypeViewer.theViewer != None):
		uiElements.unitTypeViewer.theViewer.destroy()
	if(node != None):
		if((node.unit != None and node.visible and node.unit.unitType.name == "summoner")):
			uiElements.viewer.theViewer = uiElements.summonerViewer(node)
		elif(node.unit != None and node.visible):
			uiElements.viewer.theViewer = uiElements.unitViewer(node)
		elif(node.city != None):
			uiElements.viewer.theViewer = uiElements.cityViewer(node)
	if(hasattr(gameState.getGameMode().mousedOverObject,"toggleCursor")):
		gameState.getGameMode().mousedOverObject.toggleCursor()
#	node.toggleCursor()

def makeUnitFromString(string):
	tokens = string.split("|")
	theUnit = unit(gameState.theUnitTypes[tokens[0]],int(tokens[1]),node,1)
	theUnit.movementPoints = float(tokens[5])
	theUnit.attackPoints = float(tokens[6])
	theUnit.buildPoints = int(tokens[7])
	if(tokens[8] != "None"):
		coords = tokens[8].split(",")
		theUnit.gotoNode = gameState.getGameMode().map.nodes[int(coords[1])][int(coords[0])]
	theUnit.level = int(tokens[9])
	theUnit.health = float(tokens[10])
	theUnit.isMeditating = tokens[11]=="True"
	if(len(tokens[12]) > 0):
		coordsStrs = tokens[12].split("_")
		for coordsStr in coordsStrs:
			if(len(coordsStr) > 0):
				coords = coordsStr.split(",")
				theUnit.movePath.append(gameState.getGameMode().map.nodes[int(coords[1])][int(coords[0])])
	return theUnit

def loadGame(saveName):
	with open("saves/"+saveName+".sav","r") as saveFile:
		lines = saveFile.read().split("\n")
		gameState.setMapName(lines[0])
		gameState.setTeamSize(int(lines[1]))
		gameState.setPlayerNumber(int(lines[2]))
		try:
			server.startServer('')
		except socket.error:
			gameState.setGameMode(gameModes.newGameScreenMode)
			uiElements.smallModal("Cannot open socket. Try again in 1 minute.")
			return
		gameState.availableUnitTypes = [[],[],[],[],[],[],[],[],]
		gameState.researchProgress = [{},{},{},{},{},{},{},{},]
		for line in lines[4:12]:
			if(line != "None"):
				tokens = line.split("|")
				if(tokens[6] == "True"):#isAI
					player = gameState.addPlayer(playerClass=AIPlayer,playerNumber=int(tokens[0]),userName=tokens[1],requestHandler=None)
					gameState.addAIPlayer(player)
				else:
					player = gameState.addPlayer(playerNumber=int(tokens[0]),userName=tokens[1],requestHandler=None)
#					player = gameState.getPlayers()[int(tokens[0])]
				player.isOwnPlayer = True if tokens[2]=="True" else False
				player.redWood = float(tokens[3])
				player.blueWood = float(tokens[4])
				player.team = int(tokens[5])
				for researchProgressToken in tokens[7:]:
					if(len(researchProgressToken) > 0):
						tokens = researchProgressToken.split(",")
						gameState.availableUnitTypes[player.playerNumber].append(gameState.theUnitTypes[tokens[0]])
						gameState.researchProgress[player.playerNumber][gameState.theUnitTypes[tokens[0]]] = [int(tokens[1]),int(tokens[2])]
		try:
			client.startClient('127.0.0.1')
		except socket.error:
			gameState.setGameMode(gameModes.newGameScreenMode)
			uiElements.smallModal("Cannot connect to socket. Try again in 1 minute.")
			return
		gameState.setGameMode(gameModes.playMode)
		for line in lines[12:]:#units; some built, some building/queued
			if(len(line) > 0 and not line[0] == "*"):
				tokens = line.split("|")
				theUnit = makeUnitFromString(line)
				node = gameState.getGameMode().map.nodes[int(tokens[4])][int(tokens[3])]
				node.addUnit(theUnit)
			elif(len(line) > 0):
				summonerTokens = line.split("*")
				tokens = summonerTokens[1].split("|")
				node = gameState.getGameMode().map.nodes[int(tokens[1])][int(tokens[0])]
				node.unit.researching = tokens[2]=="True"
				if(tokens[3] == "None"):
					node.unit.researchUnitType = None
				else:
					node.unit.researchUnitType = gameState.theUnitTypes[tokens[3]]
				if(len(summonerTokens[2]) == 0):
					node.unit.unitBeingBuilt = None
				else:
					node.unit.unitBeingBuilt = makeUnitFromString(summonerTokens[2])
				
				for unitString in summonerTokens[4:]:
					if(len(unitString) > 0):
						if(unitString.count("|") > 0):
							node.unit.buildQueue.append(makeUnitFromString(unitString))
						else:
							node.unit.buildQueue.append(gameState.theUnitTypes[unitString])
		if(lines[3] != "None"):
			nextUnitCoords = lines[3].split(",")
			gameState.getGameMode().nextUnit = gameState.getGameMode().map.nodes[int(nextUnitCoords[1])][int(nextUnitCoords[0])].unit
		else:
			#TODO CALL CHOOSENEXTUNIT HERE AND TEST
			print "Error, no next unit was saved!"
		gameState.getGameMode().restartGame()
		if(gameState.getGameMode().nextUnit.isControlled()):
			selectNode(gameState.getGameMode().nextUnit.node)
			gameState.getGameMode().focus(gameState.getGameMode().nextUnit.node)
	print 'loaded'

def saveGame(saveName):
	saveFile = open('saves/' + saveName + '.sav','w')
	lines = []
	lines.append(str(gameState.getMapName())+"\n")
	lines.append(str(gameState.getTeamSize())+"\n")
	lines.append(str(gameState.getPlayerNumber())+"\n")
	if(gameState.getGameMode().nextUnit != None):
		lines.append(str(gameState.getGameMode().nextUnit.node.xPos)+","+str(gameState.getGameMode().nextUnit.node.yPos)+"\n")
	else:
		lines.append("None\n")
	for player in gameState.getPlayers():
		if(player != None):
			lines.append(str(player.playerNumber)+"|")
			lines.append(str(player.userName)+"|")
			lines.append(str(player.isOwnPlayer)+"|")
			lines.append(str(player.redWood)+"|")
			lines.append(str(player.blueWood)+"|")
			lines.append(str(player.team)+"|")
			lines.append(str(player.isAI)+"|")
			for researchUnitType in gameState.researchProgress[player.playerNumber]:
				lines.append(researchUnitType.name)
				lines.append(",")
				lines.append(str(gameState.researchProgress[player.playerNumber][researchUnitType][0]))
				lines.append(",")
				lines.append(str(gameState.researchProgress[player.playerNumber][researchUnitType][1]))
				lines.append("|")
			lines.append("\n")
		else:
			lines.append("None\n")
	for unit in gameState.getGameMode().units:
		lines.append(unit.stringify())
		lines.append("\n")
	for summoner in gameState.getGameMode().summoners:
		if(summoner.isMeditating):
			lines.append("*")
			lines.append(str(summoner.node.xPos)+"|")
			lines.append(str(summoner.node.yPos)+"|")
			lines.append(str(summoner.researching)+"|")
			lines.append(("None" if summoner.researchUnitType == None else summoner.researchUnitType.name)+"|")
			lines.append("*")
			if(summoner.unitBeingBuilt != None):
				lines.append(summoner.unitBeingBuilt.stringify())
			else:
				lines.append("None")				
			for item in summoner.buildQueue:
				lines.append("*")
				lines.append(item.stringify())
	saveFile.writelines(lines)
	saveFile.close()
	print 'saved'

global aStarSearch
aStarSearch = aStarThread()
aStarProcess = Process(target=aStarSearch.runTarget,args=(aStarSearch.childPipe,))
aStarProcess.daemon = True
aStarProcess.start()
#aStarProcess.terminate()

