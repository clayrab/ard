import gameState
import nameGenerator
import cDefines
import copy
import uiElements
import random

#researchBuildTime = 100
#unitBuildSpeed = 0.1
STARTING_GREEN_WOOD = 250.0
STARTING_BLUE_WOOD = 0.0
#STARTING_GREEN_WOOD = 2000.0
#STARTING_BLUE_WOOD = 1000.0
INITIATIVE_ACTION_DEPLETION = 100.0
RESOURCE_COLLECTION_RATE = 0.15
#at RESOURCE_COLLECTION_RATE = 0.15 one gatherer will gather 15 green wood per 100 'ticks'(i.e. the build time of a gatherer)
ZOOM_SPEED = 0.2 
MOUNTAIN_ATTACK_BONUS_MULTIPLIER = 1.0
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
	def __init__(self,playerNumber):
		self.playerNumber = playerNumber
		self.isOwnPlayer = False
		self.greenWood = STARTING_GREEN_WOOD
		self.blueWood = STARTING_BLUE_WOOD
		self.hasUnits = True
class unitType:
	def __init__(self,name,textureIndex,movementSpeed,attackSpeed,attackPower,armor,range,health,canFly,canSwim,costGreen,costBlue,buildTime,movementSpeedBonus,researchCostGreen,researchCostBlue,researchTime):
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
		self.costGreen = costGreen
		self.costBlue = costBlue
		self.buildTime = buildTime
		self.movementSpeedBonus = movementSpeedBonus
#		self.armorBonus = armorBonus
#		self.attackPowerBonus = attackPowerBonus
		self.researchCostGreen = researchCostGreen
		self.researchCostBlue = researchCostBlue
		self.researchTime = researchTime
		print self.name
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
				if(node.tileValue == cDefines.defines['FOREST_TILE_INDEX'] or node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX']):
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
		self.gatheringNode = None
	def getMaxHealth(self):
		return self.unitType.health*self.level
	def getAttackPower(self):
		return self.unitType.attackPower*self.level
	def getMovementSpeed(self):
		return self.unitType.movementSpeed + (self.unitType.movementSpeedBonus*(self.level-1))
	def getArmor(self):
		return self.unitType.armor*self.level
	def getCostGreen(self):
		return self.unitType.costGreen*self.level
	def getCostBlue(self):
		return self.unitType.costBlue*self.level
	def gather(self,node):
		gameState.getClient().sendCommand("gatherTo",str(self.node.xPos) + " " + str(self.node.yPos) + " " + str(node.xPos) + " " + str(node.yPos))
	def move(self):
		for node in self.movePath:
			node.onMovePath = False
		if(self.movePath[0].unit != None):#ran into own unit
			self.movePath = []
			selectNode(self.node)
			gameState.getGameMode().focusNextUnit = 1
		else:
			gameState.getClient().sendCommand("moveTo",str(self.movePath[0].xPos) + " " + str(self.movePath[0].yPos))
			self.movePath = self.movePath[1:]
			gameState.getClient().sendCommand("chooseNextUnit")
	def moveTo(self,node):
		self.waiting = False
		self.gatheringNode = None
		node.onMovePath = False
		for neighb in self.node.getNeighbors(5):
			neighb.stopViewing(self)
		for neighb in node.getNeighbors(5):
			neighb.startViewing(self)
		if(node.unit != None and self.node != node):
			if(node.unit.player == self.player):
				if(len(self.movePath) > 0):
					self.movePath = []
#				#else: the player is trying to move onto their own unit, do nothing
		else:
			self.node.unit = None
			self.node = node
			node.unit = self
			if(node.city != None):
				node.city.player = node.unit.player
				for neighbor in node.neighbors:
					if(neighbor.unit != None and neighbor.unit.player != self.player):
						self.movePath = []
						#break
			if(node.unit.gatheringNode == node):
				self.waiting = True
			self.movementPoints = self.movementPoints + INITIATIVE_ACTION_DEPLETION
	def heal(self,node):
		gameState.getClient().sendCommand("healTo",str(node.xPos) + " " + str(node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")
	def healTo(self,node):
		self.waiting = False
		node.unit.health = node.unit.health + self.getAttackPower()
		self.attackPoints = self.attackPoints + INITIATIVE_ACTION_DEPLETION
		if(node.unit.health > node.unit.getMaxHealth()):
			node.unit.health + node.unit.getMaxHealth()
	def attack(self,node):
		gameState.getClient().sendCommand("attackTo",str(node.xPos) + " " + str(node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")
	def attackTo(self,node):
		self.waiting = False
		if(node.unit != None and node.unit.player != self.player):
			multiplier = 1.0		
			if(self.node.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
				multiplier = multiplier + MOUNTAIN_ATTACK_BONUS_MULTIPLIER
			damage = ((self.getAttackPower()-node.unit.getArmor())*multiplier)
			if(damage < 1):
				damage = 1
			node.unit.health = node.unit.health - damage
			if(node.unit.health < 0.0):
				for neighb in node.getNeighbors(5):
					neighb.stopViewing(node.unit)
				gameState.getGameMode().units.remove(node.unit)
				node.unit = None
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
		self.attackPoints = self.attackPoints + INITIATIVE_ACTION_DEPLETION
			
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
			self.researchProgress[unitType] = [0,0]
		self.researchProgress[gameState.theUnitTypes["summoner"]] = [1,0]
		self.researchProgress[gameState.theUnitTypes["gatherer"]] = [1,0]
		self.researching = False
		self.researchUnitType = None
		self.unitBeingBuilt = None
		self.cancelledUnits = []
		self.unitBuildQueue = []
		self.player = 0
	def queueUnit(self,unit):
		self.unitBuildQueue.append(unit)
		if(self.unitBeingBuilt == None):
			self.buildNextUnit()
	def unqueueUnit(self):
		if(len(self.unitBuildQueue) > 0):
			self.unitBuildQueue = self.unitBuildQueue[:-1:]
		else:
			self.unitBeingBuilt = None
	def buildNextUnit(self):
		if(len(self.unitBuildQueue) > 0):
			self.unitBeingBuilt = self.unitBuildQueue[0]
			self.unitBuildQueue = self.unitBuildQueue[1:]
		else:
			self.node.unit.waiting = False#wake up summoner
	def incrementBuildProgress(self):
		if(self.node.unit != None and self.node.unit.unitType.name == "summoner"):
			if(self.researching):
				if(self.researchUnitType != None):
					self.researchProgress[self.researchUnitType][1] = self.researchProgress[self.researchUnitType][1] + 1
					if(self.researchProgress[self.researchUnitType][1] >= self.researchUnitType.researchTime):
						self.researchProgress[self.researchUnitType][0] = self.researchProgress[self.researchUnitType][0] + 1
						self.researchProgress[self.researchUnitType][1] = 0
						self.node.unit.waiting = False#wake up summoner
						self.researching = False
			else:
				if(self.unitBeingBuilt != None):
					self.unitBeingBuilt.buildPoints = self.unitBeingBuilt.buildPoints - 1
					if(self.unitBeingBuilt.buildPoints <= 0.0):
						self.node.addUnit(self.unitBeingBuilt)
						self.unitBeingBuilt = None
						self.buildNextUnit()

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
	def getValue(self):
		return self.tileValue
	def addUnit(self,unit):
		if(self.unit == None):
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

class playModeNode(node):
	isNeighbor = False
	mode = MODES.SELECT_MODE
	openNodes = []
	closedNodes = []
	movePath = []
	def __init__(self,xPos,yPos,tileValue=cDefines.defines['GRASS_TILE_INDEX'],roadValue=0,city=None,playerStartValue=0):
		node.__init__(self,xPos,yPos,tileValue=tileValue,roadValue=roadValue,city=city,playerStartValue=playerStartValue)
		self.closed = False
		self.open = False
		self.aStarKnownCost = 0.0
		self.aStarHeuristicCost = 0.0
		self.aStarParent = None
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
		if(gameState.getPlayerNumber() == unit.player or gameState.getPlayerNumber() == -2):
			self.viewingUnits.append(unit)
			self.visible = True
	def stopViewing(self,unit):
		if(gameState.getPlayerNumber() == unit.player or gameState.getPlayerNumber() == -2):
			if(unit in self.viewingUnits):
				self.viewingUnits.remove(unit)
			if(len(self.viewingUnits) <= 0):
				self.visible = False
	def onLeftClickDown(self):
		if(playModeNode.mode == MODES.ATTACK_MODE):
			gameState.getGameMode().nextUnit.attack(self)
		elif(playModeNode.mode == MODES.HEAL_MODE):
			gameState.getGameMode().nextUnit.heal(self)
		elif(playModeNode.mode == MODES.MOVE_MODE):
			if(uiElements.unitViewer.theUnitViewer.unit == gameState.getGameMode().nextUnit):
				uiElements.unitViewer.theUnitViewer.unit.movePath = uiElements.unitViewer.theUnitViewer.unit.node.movePath
				uiElements.unitViewer.theUnitViewer.unit.move()
			else:
				uiElements.unitViewer.theUnitViewer.unit.movePath = uiElements.unitViewer.theUnitViewer.unit.node.movePath
				gameState.getClient().sendCommand("stopWaiting",str(uiElements.actionViewer.theActionViewer.node.xPos) + " " + str(uiElements.actionViewer.theActionViewer.node.yPos))

				uiElements.unitViewer.theUnitViewer.reset()
			for node in uiElements.unitViewer.theUnitViewer.unit.movePath:
				node.onMovePath = True
		else:
			selectNode(self)
	def toggleCursor(self):
		for node in playModeNode.movePath:
			node.onMovePath = False
		playModeNode.movePath = []
		if(uiElements.unitViewer.theUnitViewer != None):
			for node in uiElements.unitViewer.theUnitViewer.unit.movePath:
				node.onMovePath = True
		if(gameState.getGameMode().focusNextUnit == 1):
			self.cursorIndex = cDefines.defines['CURSOR_POINTER_INDEX']
			playModeNode.mode = MODES.SELECT_MODE
			return;
		if(uiElements.unitViewer.theUnitViewer != None and gameState.getGameMode().getPlayerNumber() == gameState.getGameMode().nextUnit.player):
			if((gameState.getGameMode().nextUnit == uiElements.unitViewer.theUnitViewer.unit) and self.fire != None and gameState.getGameMode().nextUnit.unitType.name == "blue mage"):
				self.cursorIndex = cDefines.defines['CURSOR_ATTACK_INDEX']
				playModeNode.mode = MODES.ATTACK_MODE				
			elif((gameState.getGameMode().nextUnit == uiElements.unitViewer.theUnitViewer.unit) and (self.unit != None and self.unit.player != uiElements.unitViewer.theUnitViewer.unit.player) and self.findDistance(uiElements.unitViewer.theUnitViewer.unit.node) <= uiElements.unitViewer.theUnitViewer.unit.unitType.range):
				self.cursorIndex = cDefines.defines['CURSOR_ATTACK_INDEX']
				playModeNode.mode = MODES.ATTACK_MODE
			elif((gameState.getGameMode().nextUnit == uiElements.unitViewer.theUnitViewer.unit) and (self.unit != None and self.unit.player == uiElements.unitViewer.theUnitViewer.unit.player) and self.findDistance(uiElements.unitViewer.theUnitViewer.unit.node) <= uiElements.unitViewer.theUnitViewer.unit.unitType.range and uiElements.unitViewer.theUnitViewer.unit.unitType.name == "white mage"):
				self.cursorIndex = cDefines.defines['CURSOR_HEAL_INDEX']
				playModeNode.mode = MODES.HEAL_MODE
#			elif(uiElements.unitViewer.theUnitViewer.unit.unitType.name == "gatherer" and (not gameState.getGameMode().shiftDown) and (self.tileValue == cDefines.defines['FOREST_TILE_INDEX'] or self.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX']) and self.unit != uiElements.unitViewer.theUnitViewer.unit):
#				self.cursorIndex = cDefines.defines['CURSOR_GATHER_INDEX']
#				playModeNode.mode = MODES.GATHER_MODE
#				self.aStarSearch()
			elif((uiElements.unitViewer.theUnitViewer.unit.node == self) or (playModeNode.isNeighbor and gameState.getGameMode().shiftDown) or ((not playModeNode.isNeighbor) and (not gameState.getGameMode().shiftDown)) or (self.unit != None) or (gameState.getGameMode().selectedNode == None) or (gameState.getGameMode().selectedNode != None and gameState.getGameMode().selectedNode.unit == None)):
				self.cursorIndex = cDefines.defines['CURSOR_POINTER_INDEX']
				playModeNode.mode = MODES.SELECT_MODE
			else:
				for node in uiElements.unitViewer.theUnitViewer.unit.movePath:
					node.onMovePath = False
				self.cursorIndex = cDefines.defines['CURSOR_MOVE_INDEX']
				playModeNode.mode = MODES.MOVE_MODE
				self.aStarSearch()
		else:
			if(uiElements.unitViewer.theUnitViewer != None and gameState.getGameMode().shiftDown and uiElements.unitViewer.theUnitViewer != None and uiElements.unitViewer.theUnitViewer.unit != None):
				for node in uiElements.unitViewer.theUnitViewer.unit.movePath:
					node.onMovePath = False
				self.cursorIndex = cDefines.defines['CURSOR_MOVE_INDEX']
				playModeNode.mode = MODES.MOVE_MODE
				self.aStarSearch()
			else:
				self.cursorIndex = -1
				playModeNode.mode = MODES.SELECT_MODE			
	def getNeighbors(self,distance):
		neighbs = []
		for xDelta in range(0-distance,distance):
			for yDelta in range(0-distance,distance):
				if((self.yPos + yDelta >= 0) and (self.yPos + yDelta < len(gameState.getGameMode().map.nodes))):
					if((self.xPos + xDelta >= 0) and (self.xPos + xDelta < len(gameState.getGameMode().map.nodes[self.yPos + yDelta]))):
						if(self.findDistance(gameState.getGameMode().map.nodes[self.yPos + yDelta][self.xPos + xDelta]) < 5.0):
							neighbs.append(gameState.getGameMode().map.nodes[self.yPos + yDelta][self.xPos + xDelta])
		return neighbs
	def aStarSearch(self):
		#start at end point so we can just track back and insert into an array in order
		self.findAStarHeuristicCost(uiElements.unitViewer.theUnitViewer.unit.node)
		playModeNode.openNodes.append(self)
		playModeNode.aStarSearchRecurse(uiElements.unitViewer.theUnitViewer.unit.node)
	def findAStarHeuristicCost(self,target):
		#current 'heuristic' is just the distance assuming everything is grass
		#I might want to change this to assume that everything is mountain... or somewhere in between... gotta think about it.
		self.aStarHeuristicCost = self.findDistance(target)
	def findDistance(self,target):
		#'even row' means map polarity = 0 and row # is even OR map polarity = 0 and row # is odd...
		#polarity 0 means 'even' rows are to the left
		#polarity 1 means 'even' rows are to the right
		#if moving from even to odd row left gives you free x at 1,3,5...
		#if moving from even to odd row right gives you free x at 3,5,7...
		#if moving from odd to even row right gives you free x at 1,3,5...
		#if moving from odd to even row left gives you free x at 3,5,7...
		distance = float(abs(self.xPos - target.xPos))
		if(abs(self.yPos-target.yPos)%2 == 1):#one row is even, other is odd...
			if(self.yPos%2 == gameState.getGameMode().map.polarity):#self is even...
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
	@staticmethod
	def aStarSearchRecurse(target,count=0):
		#TODO: remove count from here since it's really just for debugging purposes...
#		node = playModeNode.openNodes[0]
		node = None
		for openNode in playModeNode.openNodes:
			if(not openNode.closed):
				if(node == None):
					node = openNode
				if((openNode.aStarKnownCost + openNode.aStarHeuristicCost) < (node.aStarKnownCost + node.aStarHeuristicCost)):
					node = openNode
		if(node == target):
			nextNode = target.aStarParent
			while nextNode != None:
				playModeNode.movePath.append(nextNode)
				nextNode.onMovePath = True
				nextNode = nextNode.aStarParent
       			for node in playModeNode.openNodes:
				node.closed = False
				node.open = False
				node.aStarKnownCost = 0.0
				node.aStarHeuristicCost = 0.0
				node.aStarParent = None
			for node in playModeNode.closedNodes:
				node.closed = False
				node.open = False
				node.aStarKnownCost = 0.0
				node.aStarHeuristicCost = 0.0
				node.aStarParent = None
			playModeNode.openNodes = []
			playModeNode.closedNodes = []
			return
		node.closed = True
		playModeNode.closedNodes.append(node)
		for neighbor in node.neighbors:
			if(not neighbor.closed):
				if(not neighbor.open):
					playModeNode.openNodes.append(neighbor)
					neighbor.open = True
					neighbor.aStarParent = node
					neighbor.findAStarHeuristicCost(target)
					if(neighbor.unit != None):
						neighbor.aStarKnownCost = node.aStarKnownCost + 999.9
					elif(neighbor.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX'] and not target.unit.unitType.canFly):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['MOUNTAIN_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['WATER_TILE_INDEX'] and not target.unit.unitType.canFly and not target.unit.unitType.canFly):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['WATER_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['DESERT_TILE_INDEX'] and not target.unit.unitType.canFly):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['DESERT_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					else:
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['GRASS_MOVE_COST']/(1.0+float(neighbor.roadValue)))
				else:#calculate whether new known path is shorter than old known path
					if(neighbor.unit != None):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + 999.9):
							   neighbor.aStarKnownCost = node.aStarKnownCost + 999.9
					elif(neighbor.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['MOUNTAIN_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							   neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['MOUNTAIN_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['WATER_TILE_INDEX'] and target.unit.unitType.canSwim == False):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['WATER_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							   neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['WATER_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['DESERT_TILE_INDEX']):
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['DESERT_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							   neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['DESERT_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					else:
						if(neighbor.aStarKnownCost > node.aStarKnownCost + (cDefines.defines['GRASS_MOVE_COST']/(1.0+float(neighbor.roadValue)))):
							   neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['GRASS_MOVE_COST']/(1.0+float(neighbor.roadValue)))
		count = count + 1
		playModeNode.aStarSearchRecurse(target,count)
	def onMouseOver(self):
		if(uiElements.unitViewer.theUnitViewer != None):
			if(uiElements.unitViewer.theUnitViewer.unit.node.neighbors.count(self) > 0):
				playModeNode.isNeighbor = True
			else:
				playModeNode.isNeighbor = False
			self.toggleCursor()
#	def onMouseOut(self):
#		if(uiElements.unitViewer.theUnitViewer.unit.node.neighbors.count(self) > 0):
#			playModeNode.isNeighbor = False
	def onKeyDown(self,keycode):
		self.toggleCursor()
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
		if(gameState.getGameMode().selectedButton != None):
			if(hasattr(gameState.getGameMode().selectedButton,"tileType")):
				if(gameState.getGameMode().selectedButton.tileType == cDefines.defines['ROAD_TILE_INDEX']):#new road
					self.roadValue = (~self.roadValue)&1
				elif(gameState.getGameMode().selectedButton.tileType == cDefines.defines['CITY_TILE_INDEX']):#new city
					if(self.city == None):
						self.city = city(random.choice(cityNames),self)
					uiElements.cityEditor.destroy()
					uiElements.cityEditor.theCityEditor = uiElements.cityEditor(self.city)
					if(gameState.getGameMode().selectedCityNode != None):
						gameState.getGameMode().selectedCityNode.selected = False
					self.selected = True
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
	def onLeftClickDown(self):
		print 'click'

class map:
	def __init__(self,nodeType):
		self.polarity = 0
		self.nodeType = nodeType
		self.translateZ = 0.0-cDefines.defines['initZoom']
		self.load()
	def getWidth(self):
		return len(self.nodes[0])
	def getHeight(self):
		return len(self.nodes)
	def load(self):
		mapFile = open('maps/' + gameState.getMapName() + ".map",'r')
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
				print "map: " + str(self)
				self.numPlayers = int(line)
				print self.numPlayers
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
		                elif(line.startswith("*")):#city
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
				print node.tileValue + (128*node.roadValue)
				print node.tileValue
				print node.roadValue
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
	if(gameState.getGameMode().selectedNode != None):
		gameState.getGameMode().selectedNode.selected = False
		if(gameState.getGameMode().selectedNode.unit != None and len(gameState.getGameMode().selectedNode.unit.movePath) > 0):
			for pathNode in gameState.getGameMode().selectedNode.unit.movePath:
				pathNode.onMovePath = False
	gameState.getGameMode().selectedNode = node
	node.selected = True
	uiElements.actionViewer.destroy()
	uiElements.unitViewer.destroy()
	uiElements.unitTypeResearchViewer.destroy()
	uiElements.unitTypeBuildViewer.destroy()
	if(node.city != None):
		uiElements.actionViewer.theActionViewer = uiElements.actionViewer(node)
	if(node.unit != None and node.visible):
		uiElements.unitViewer.theUnitViewer = uiElements.unitViewer(node.unit)
	if(node.unit != None and len(node.unit.movePath) > 0):
		for pathNode in node.unit.movePath:
			pathNode.onMovePath = True
	if(hasattr(gameState.getGameMode().mousedOverObject,"toggleCursor")):
		   gameState.getGameMode().mousedOverObject.toggleCursor()
#	node.toggleCursor()


