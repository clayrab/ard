import gameState
import nameGenerator
import cDefines
import copy
import uiElements
import random
import threading
import thread
import time
import sys
from multiprocessing import Process, Queue, Pipe
#import aStar

#thread.stack_size(32768)
#thread.stack_size(1024*1024)
#print "thread stack size: " + str(thread.stack_size())
#sys.setcheckinterval(10)

#researchBuildTime = 100
#unitBuildSpeed = 0.1
STARTING_GREEN_WOOD = 250.0
STARTING_BLUE_WOOD = 0.0
#STARTING_GREEN_WOOD = 2000.0
#STARTING_BLUE_WOOD = 1000.0
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

class MODES:
	MOVE_MODE = 0
	ATTACK_MODE = 1
	SELECT_MODE = 2
	HEAL_MODE = 3

cityNames = ["Eshnunna","Tutub","Der","Sippar","Sippar-Amnanum","Kutha","Jemde Nasr","Kish","Babilim","Borsippa","Mashkan-shapir","Dilbat","Nippur","Marad","Adab","Isin","Kisurra","Shuruppak","Bad-tibira","Zabalam","Umma","Girsu","Lagash","Urum","Uruk","Larsa","Ur","Kuara","Eridu","Akshak","Akkad","Urfa","Shanidar cave","Urkesh","Shekhna","Arbid","Harran","Chagar Bazar","Kahat","El Fakhariya","Arslan Tash","Carchemish","Til Barsip","Nabada","Nagar","Telul eth-Thalathat","Tepe Gawra","Tell Arpachiyah","Shibaniba","Tarbisu","Ninua","Qatara","Dur Sharrukin","Tell Shemshara","Arbil","Imgur-Enlil","Nimrud","Emar","Arrapha","Kar-Tukulti-Ninurta","Ashur","Nuzi","al-Fakhar","Terqa","Mari","Haradum","Nerebtum","Agrab","Dur-Kurigalzu","Shaduppum","Seleucia","Ctesiphon","Zenobia","Zalabiye","Hasanlu","Takht-i-Suleiman","Behistun","Godin Tepe","Chogha Mish","Tepe Sialk","Susa","Kabnak","Dur Untash","Pasargadai","Naqsh-e Rustam","Parsa","Anshan","Konar Sandal","Tepe Yahya","Miletus","Sfard","Nicaea","Sapinuwa","Yazilikaya","Alaca Hoyuk","Masat Hoyuk","Hattusa","Ilios","Kanesh","Arslantepe","Sam'al","Beycesultan","Adana","Karatepe","Tarsus","Sultantepe","Attalia","Acre","Adoraim","Alalah","Aleppo","Al-Sinnabra","Aphek","Arad Rabbah","Ashdod","Ashkelon","Baalbek","Batroun","Beersheba","Beth Shean","Bet Shemesh","Bethany","Bet-el","Bezer","Byblos","Capernaum","Dan","Dimashq","Deir Alla","Dhiban","Dor","Ebla","En Gedi","Enfeh","Ekron","Et-Tell","Gath","Gezer","Gibeah","Gilgal Refaim","Gubla","Hamath","Hazor","Hebron","Herodion","Jezreel","Kadesh Barnea","Kedesh","Kumidi","Lachish","Megiddo","Qatna","Qumran","Rabat Amon","Samaria","Sarepta","Sharuhen","Shiloh","Sidon","Tadmor","Tirzah","Tyros","Ugarit","Umm el-Marra"]


class Player:
	def __init__(self,playerNumber,userName=None):
		if(userName == None):
			userName = "Player " + str(playerNumber)
		self.userName = userName
		self.playerNumber = playerNumber
		self.isOwnPlayer = False
		self.greenWood = STARTING_GREEN_WOOD
		self.blueWood = STARTING_BLUE_WOOD
		self.hasSummoners = True
class unitType:
	def __init__(self,name,textureIndex,overlayTextureIndex,movementSpeed,attackSpeed,attackPower,armor,range,health,canFly,canSwim,costGreen,costBlue,buildTime,movementSpeedBonus,researchCostGreen,researchCostBlue,researchTime,canAttackGround=False):
		self.name = name
		self.textureIndex = textureIndex
		self.overlayTextureIndex = overlayTextureIndex
		self.movementSpeed = movementSpeed
		self.attackSpeed = attackSpeed
		self.attackPower = attackPower
		self.armor = armor
		self.range = range
		self.health = health
		self.canFly = canFly
		self.canSwim = canSwim
		self.costGreen = costGreen
		self.costBlue = costBlue
		self.buildTime = buildTime
		self.movementSpeedBonus = movementSpeedBonus
#		self.armorBonus = armorBonus
#		self.attackPowerBonus = attackPowerBonus
		self.researchCostGreen = researchCostGreen
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
		
class unit:
	def __init__(self,unitType,player,xPos,yPos,node,level=None):
		self.unitType = unitType
		self.player = player
		self.node = node
		self.movementPoints = 0
		self.attackPoints = 0
		self.buildPoints = self.unitType.buildTime	
		self.movePath = []
		self.waiting = False
		if(level != None):
			self.level = level
		else:
			self.level = node.city.researchProgress[self.unitType][0]
		self.health = float(self.unitType.health*self.level)
		self.originCity = node.city
#		self.gatheringNode = None
		self.isMeditating = False
		self.recentDamage = {}
	def isControlled(self):
		return gameState.getPlayers()[self.player-1].isOwnPlayer		
	def isOwnUnit(self):
		return (gameState.getPlayerNumber() == self.player)
	def isOwnTeam(self):
		if(gameState.getPlayerNumber() == -2):
			if(gameState.getGameMode().nextUnit == None):
				return True
			else:
				return (self.player == gameState.getGameMode().nextUnit.player)
		else:
			return (gameState.getPlayerNumber() == self.player)
	def getMaxHealth(self):
		return self.unitType.health*self.level
	def getAttackPower(self):
		return self.unitType.attackPower*self.level
	def getMovementSpeed(self):
		return self.unitType.movementSpeed + (self.unitType.movementSpeedBonus*(self.level-1))
	def getArmor(self):
		return self.unitType.armor*self.level
	def getCostGreen(self):
		print 'DEPRECATED'
		return self.unitType.costGreen*self.level
	def getCostBlue(self):
		print 'DEPRECATED'
		return self.unitType.costBlue*self.level
#	def gather(self,node):
#		gameState.getClient().sendCommand("gatherTo",str(self.node.xPos) + " " + str(self.node.yPos) + " " + str(node.xPos) + " " + str(node.yPos))
	def move(self):
		for node in self.movePath:
			node.onMovePath = False
		if(self.movePath[0].unit != None):#ran into unit
			self.movePath = []
			selectNode(self.node)
			gameState.getGameMode().doFocus = 1
		else:
			gameState.getClient().sendCommand("moveTo",str(self.movePath[0].xPos) + " " + str(self.movePath[0].yPos))
			self.movePath = self.movePath[1:]
			gameState.getClient().sendCommand("chooseNextUnit")
	def moveTo(self,node):
		self.waiting = False
#		self.gatheringNode = None
		node.onMovePath = False
		for neighb in self.node.getNeighbors(5):
			neighb.stopViewing(self)
		for neighb in node.getNeighbors(5):
			neighb.startViewing(self)
#it seems that this is now dealt with in the move method
#		if(node.unit != None and self.node != node):
#			if(node.unit.player == self.player):#moved onto own unit, cancel movepath
#				if(len(self.movePath) > 0):
#					self.movePath = []
#		else:
		aStarSearch.parentPipe.send(["unitRemove",self.node.xPos,self.node.yPos])
		if(node.visible):
			aStarSearch.parentPipe.send(["unitAdd",node.xPos,node.yPos])
		self.node.unit = None
		if(gameState.getGameMode().selectedNode == self.node):
			selectNode(self.node)
		self.node = node
		node.unit = self
		if(node.city != None):
			node.city.player = node.unit.player
			for neighbor in node.neighbors:
				if(neighbor.unit != None and neighbor.unit.player != self.player):
					self.movePath = []
						#break
#			if(node.unit.gatheringNode == node):
#				self.waiting = True
		self.movementPoints = self.movementPoints + INITIATIVE_ACTION_DEPLETION
	def heal(self,node):
		gameState.getClient().sendCommand("healTo",str(node.xPos) + " " + str(node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")
	def healTo(self,node):
		self.waiting = False
		node.unit.health = node.unit.health + self.getAttackPower()
		self.attackPoints = self.attackPoints + INITIATIVE_ACTION_DEPLETION
		if(node.unit.health > node.unit.getMaxHealth()):
			node.unit.health = node.unit.getMaxHealth()
	def attack(self,node):
		gameState.getClient().sendCommand("attackTo",str(node.xPos) + " " + str(node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")
	def attackTo(self,node):
		self.waiting = False
		if(node.unit != None and node.unit.player != self.player):
			multiplier = 1.0		
#			if(self.node.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
#				multiplier = multiplier + MOUNTAIN_ATTACK_BONUS_MULTIPLIER
			damage = ((self.getAttackPower()-node.unit.getArmor())*multiplier)
			node.unit.recentDamage[gameState.getGameMode().ticks] = str(int(damage))
			if(damage < 1):
				damage = 1
			node.unit.health = node.unit.health - damage
			if(node.unit.health < 0.0):
				for neighb in node.getNeighbors(5):
					neighb.stopViewing(node.unit)
				gameState.getGameMode().units.remove(node.unit)
				gameLogic.aStarSearch.parentPipe.send(["unitRemove",unit.node.xPos,unit.node.yPos])
				if(node.unit.unitType == "summoner" and node.city != None):
					node.city.researchProgress = {}
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
	def skip(self):
		self.movementPoints = self.movementPoints + INITIATIVE_ACTION_DEPLETION
			
class city:
	def __init__(self,name,node,unitTypes=None,costOfOwnership=10):
		if(unitTypes == None):
			unitTypes = []
		self.name = name
		self.node = node
		self.costOfOwnership = costOfOwnership
		self.unitTypes = []
		self.unitTypes.append(gameState.theUnitTypes["summoner"])
		self.unitTypes.append(gameState.theUnitTypes["gatherer"])	
		self.unitTypes.extend(unitTypes)
		self.researchProgress = {}
		for unitType in unitTypes:
			self.researchProgress[unitType] = [1,0]
		self.researchProgress[gameState.theUnitTypes["summoner"]] = [1,0]
		self.researchProgress[gameState.theUnitTypes["gatherer"]] = [1,0]
		self.researching = False
		self.researchUnitType = None
		self.unitBeingBuilt = None
		self.cancelledUnits = []
		self.unitBuildQueue = []
		self.player = 0
	def queueResearch(self,unitType):
		self.unitBuildQueue.append(unitType)
		if(self.unitBeingBuilt == None and not self.researching):
			self.buildNextFromQueue()			
	def unqueueResearch(self):
		if(len(self.unitBuildQueue) > 0):
			self.unitBuildQueue = self.unitBuildQueue[:-1:]
		else:
			self.researching = False
			self.researchUnitType = None
	def queueUnit(self,unit):
		self.unitBuildQueue.append(unit)
		if(self.unitBeingBuilt == None and not self.researching):
			self.buildNextFromQueue()
	def unqueueUnit(self):
		if(len(self.unitBuildQueue) > 0):
			self.unitBuildQueue = self.unitBuildQueue[:-1:]
		else:
			self.unitBeingBuilt = None
	def buildNextFromQueue(self):
#		self.unitBeingBuilt = None
#		self.researching = False
#		self.researchUnitType = None
		if(len(self.unitBuildQueue) > 0):
			nextThing = self.unitBuildQueue[0]
			self.unitBuildQueue = self.unitBuildQueue[1:]
			if(hasattr(nextThing,"unitType")):#unit
				self.unitBeingBuilt = nextThing
			else:#unitType/research
				self.researching = True
				self.researchUnitType = nextThing
#		if(len(self.unitBuildQueue) > 0):
#			self.unitBeingBuilt = self.unitBuildQueue[0]
#			self.unitBuildQueue = self.unitBuildQueue[1:]
#		else:
#			self.node.unit.waiting = False#wake up summoner
	def incrementBuildProgress(self):
		if(self.node.unit != None and self.node.unit.unitType.name == "summoner" and self.node.unit.isMeditating):
			if(self.researching):
				if(self.researchUnitType != None):
					self.researchProgress[self.researchUnitType][1] = self.researchProgress[self.researchUnitType][1] + 1
					if(self.researchProgress[self.researchUnitType][1] >= self.researchUnitType.researchTime):
						self.researchProgress[self.researchUnitType][0] = self.researchProgress[self.researchUnitType][0] + 1
						self.researchProgress[self.researchUnitType][1] = 0
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
		self.onMovePath = False
		self.cursorIndex = -1
		gameState.getGameMode().elementsDict[self.name] = self
		self.neighbors = []
		self.unit = None
	def onKeyDown(self,keycode):
		if(keycode == "`"):
			gameState.getGameMode().clickScroll = True
 		if(hasattr(self,"toggleCursor")):
			self.toggleCursor()
	def onKeyUp(self,keycode):
		if(keycode == "`"):
			gameState.getGameMode().clickScroll = False		
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
	def addUnit(self,unit):
		if(self.unit == None and self.tileValue != cDefines.defines['MOUNTAIN_TILE_INDEX']):
			self.unit = unit
			unit.node = self
			gameState.getGameMode().units.append(unit)
			if(gameState.getPlayerNumber() == self.playerStartValue or gameState.getPlayerNumber() == -2):
				for neighb in self.getNeighbors(5):
					neighb.startViewing(self.unit)
			if(self.city != None):
				self.city.player = self.unit.player
		else:
			(random.choice(self.neighbors)).addUnit(unit)
	def onRightClick(self):
		gameState.getGameMode().clickScroll = True

class playModeNode(node):
	isNeighbor = False
	mode = MODES.SELECT_MODE
#	openNodes = []
#	closedNodes = []
	movePath = []
#	aStarMap = None
	def __init__(self,xPos,yPos,tileValue=cDefines.defines['GRASS_TILE_INDEX'],roadValue=0,city=None,playerStartValue=0):
		node.__init__(self,xPos,yPos,tileValue=tileValue,roadValue=roadValue,city=city,playerStartValue=playerStartValue)
#		self.closed = False
#		self.open = False
#		self.aStarKnownCost = 0.0
#		self.aStarHeuristicCost = 0.0
#		self.aStarParent = None
		self.visible = False
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
		if(unit.isControlled()):
			self.viewingUnits.append(unit)
#this doesn't work because the algorithm is simply to stop viewing all nodes in range before move and start viewing all nodes in range after move
#			if(not self.visible and self.unit != None and not self.unit.isOwnTeam() and len(unit.movePath) > 0):
#				for node in unit.movePath:
#					node.onMovePath = False
#				unit.movePath = []
			self.visible = True
	def stopViewing(self,unit):
		if(gameState.getPlayerNumber() == unit.player or gameState.getPlayerNumber() == -2):
			if(unit in self.viewingUnits):
				self.viewingUnits.remove(unit)
			if(len(self.viewingUnits) <= 0):
				self.visible = False
	def onLeftClickDown(self):
		if(gameState.getGameMode().doFocus == 0):
			if(playModeNode.mode == MODES.ATTACK_MODE):
				gameState.getGameMode().nextUnit.attack(self)
			elif(playModeNode.mode == MODES.HEAL_MODE):
				gameState.getGameMode().nextUnit.heal(self)
			elif(playModeNode.mode == MODES.MOVE_MODE):
				if(gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode.unit != None):
					if(len(gameState.getGameMode().selectedNode.unit.movePath) > 0):
						for node in gameState.getGameMode().selectedNode.unit.movePath:
							node.onMovePath = False
					if(gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit):
						gameState.getGameMode().selectedNode.unit.movePath = playModeNode.movePath
						if(len(gameState.getGameMode().selectedNode.unit.movePath) > 0 ):
							gameState.getGameMode().selectedNode.unit.move()
					else:
						gameState.getGameMode().selectedNode.unit.movePath = playModeNode.movePath
#						if(gameState.getGameMode().nextUnit.isControlled()):
#							selectNode(gameState.getGameMode().nextUnit.node)
			else:
				selectNode(self)
	def toggleCursor(self):
		for node in playModeNode.movePath:
			node.onMovePath = False
		playModeNode.movePath = []
		if(gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode.unit != None):
			for node in gameState.getGameMode().selectedNode.unit.movePath:
				node.onMovePath = True

		if(gameState.getGameMode().doFocus == 1 or gameState.getGameMode().selectedNode == None or gameState.getGameMode().selectedNode.unit == None or gameState.getGameMode().selectedNode.unit.isMeditating or not gameState.getGameMode().selectedNode.unit.isControlled()):
			self.cursorIndex = cDefines.defines['CURSOR_POINTER_INDEX']
			playModeNode.mode = MODES.SELECT_MODE
		else:
			state = (self.unit == None,
				 gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit,
				 self.findDistance(gameState.getGameMode().selectedNode,gameState.getGameMode().map.polarity) <= float(gameState.getGameMode().selectedNode.unit.unitType.range),
				 self.unit != None and not self.unit.isOwnTeam(),
				 gameState.getGameMode().selectedNode.unit.unitType.name == "white mage",
				 self == gameState.getGameMode().selectedNode and gameState.getGameMode().selectedNode != None,
				 self.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX'],
				 gameState.getGameMode().selectedNode.unit.unitType.canFly,)
			# playModeNode.isNeighbor
			# gameState.getGameMode().shiftDown
			if((state[0] == True and (state[6] == False or state[6:] == (True,True))) or (state[0] == False and state[5] == True)):
				self.cursorIndex = cDefines.defines['CURSOR_MOVE_INDEX']
				playModeNode.mode = MODES.MOVE_MODE
				aStarSearch.search(self,gameState.getGameMode().selectedNode,gameState.getGameMode().selectedNode.unit.unitType.canFly,gameState.getGameMode().selectedNode.unit.unitType.canSwim)
			elif(state[0:4] == (False,True,True,True)):
				self.cursorIndex = cDefines.defines['CURSOR_ATTACK_INDEX']
				playModeNode.mode = MODES.ATTACK_MODE
			elif(state[0:5] == (False,True,True,False,True)):
				self.cursorIndex = cDefines.defines['CURSOR_HEAL_INDEX']
				playModeNode.mode = MODES.HEAL_MODE
			else:
				self.cursorIndex = cDefines.defines['CURSOR_POINTER_INDEX']
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
		if(hasattr(gameState.getGameMode(),"selectedNode") and gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode.unit != None):
			if(gameState.getGameMode().selectedNode.unit.node.neighbors.count(self) > 0):
				playModeNode.isNeighbor = True
			else:
				playModeNode.isNeighbor = False
			self.toggleCursor()
#	def onMouseOut(self):
#		if(gameState.getGameMode().selectedNode.unit.node.neighbors.count(self) > 0):
#			playModeNode.isNeighbor = False
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
		selectNode(self,uiElements.cityViewerNoPlay)			

#class aStarThread(threading.Thread):
class aStarThread():
	def __init__(self):
		self.openNodes = []
		self.closedNodes = []
		self.movePath = []
		self.map = None
		self.nodes = []
		self.polarity = 0
		self.endNode = None
		self.canFly = False
		self.canSwim = True
		self.searchComplete = False
		self.parentPipe,self.childPipe = Pipe()
		self.queue = None
#		self.doneSearching = True
		self.aStarLock = threading.RLock()
#		self.searchCompleteLock = threading.RLock()
#		threading.Thread.__init__(self)
#		Process.__init__(self)
	@staticmethod
	def runTarget(pipe):
#		aStarSearch.queueFuck = queue
#	startNode.findAStarHeuristicCost(aStarSearch.endNode)
	#	aStarSearch.openNodes.append(startNode)
		while True:
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
				else:
					aStarSearch.movePath = []
					aStarSearch.resetNodes()
					aStarSearch.canFly = data[4]
					aStarSearch.canSwim = data[5]
					aStarSearch.endNode = aStarSearch.map.nodes[data[3]][data[2]]
					startNode = aStarSearch.map.nodes[data[1]][data[0]]
					aStarSearch.openNodes.append(startNode)
			else:
				aStarSearch.aStarSearchRecurse()
        @staticmethod
        def search(startNode,endNode,canFly,canSwim):
		aStarSearch.parentPipe.send([startNode.xPos,startNode.yPos,endNode.xPos,endNode.yPos,canFly,canSwim])
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
	def __init__(self,nodeType,translateZ=0.0-cDefines.defines['initZoom'],mapName="",ignoreCities=False):
		if(mapName == ""):
			self.mapName = gameState.getMapName()
		else:
			self.mapName = mapName
		self.ignoreCities = ignoreCities
		self.polarity = 0
		self.nodeType = nodeType
		self.translateZ = translateZ
		self.load()
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

def selectNode(node,theCityViewer = uiElements.cityViewer):
	for pnode in playModeNode.movePath:
		pnode.onMovePath = False
	playModeNode.movePath = []
	if(gameState.getGameMode().selectedNode != None):
		gameState.getGameMode().selectedNode.selected = False
		if(gameState.getGameMode().selectedNode.unit != None and len(gameState.getGameMode().selectedNode.unit.movePath) > 0):
			for pathNode in gameState.getGameMode().selectedNode.unit.movePath:
				pathNode.onMovePath = False
	if(node.unit != None and len(node.unit.movePath) > 0):
		for pathNode in node.unit.movePath:
			pathNode.onMovePath = True
	gameState.getGameMode().selectedNode = node
	node.selected = True
	if(uiElements.viewer.theViewer != None):
		uiElements.viewer.theViewer.destroy()
	if(uiElements.unitTypeViewer.theViewer != None):
		uiElements.unitTypeViewer.theViewer.destroy()
	if((node.unit == None and node.city !=None) or (node.unit != None and node.unit.unitType.name == "summoner" and node.unit.isMeditating and node.city != None)):
		uiElements.viewer.theViewer = theCityViewer(node)
	elif(node.unit != None):
		uiElements.viewer.theViewer = uiElements.unitViewer(node)
	if(hasattr(gameState.getGameMode().mousedOverObject,"toggleCursor")):
		gameState.getGameMode().mousedOverObject.toggleCursor()
#	node.toggleCursor()

global aStarSearch
aStarSearch = aStarThread()
aStarProcess = Process(target=aStarSearch.runTarget,args=(aStarSearch.childPipe,))
aStarProcess.daemon = True
aStarProcess.start()
#aStarProcess.terminate()
