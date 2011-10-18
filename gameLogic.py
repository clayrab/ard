import gameState
import nameGenerator
import cDefines
import copy
import uiElements
import random

researchBuildTime = 100
unitBuildSpeed = 0.1

cityNames = ["Eshnunna","Tutub","Der","Sippar","Sippar-Amnanum","Kutha","Jemde Nasr","Kish","Babilim","Borsippa","Mashkan-shapir","Dilbat","Nippur","Marad","Adab","Isin","Kisurra","Shuruppak","Bad-tibira","Zabalam","Umma","Girsu","Lagash","Urum","Uruk","Larsa","Ur","Kuara","Eridu","Akshak","Akkad","Urfa","Shanidar cave","Urkesh","Shekhna","Arbid","Harran","Chagar Bazar","Kahat","el Fakhariya (Washukanni?)","Arslan Tash","Carchemish","Til Barsip","Nabada","Nagar","Telul eth-Thalathat","Tepe Gawra","Tell Arpachiyah","Shibaniba","Tarbisu","Ninua","Qatara","Dur Sharrukin","Tell Shemshara","Arbil","Imgur-Enlil","Nimrud","Emar","Arrapha","Kar-Tukulti-Ninurta","Ashur","Nuzi","al-Fakhar","Terqa","Mari","Haradum","Nerebtum","Agrab","Dur-Kurigalzu","Shaduppum","Seleucia","Ctesiphon","Zenobia","Zalabiye","Hasanlu","Takht-i-Suleiman","Behistun","Godin Tepe","Chogha Mish","Tepe Sialk","Susa","Kabnak","Dur Untash","Pasargadai","Naqsh-e Rustam","Parsa","Anshan","Konar Sandal","Tepe Yahya","Miletus","Sfard","Nicaea","Sapinuwa","Yazilikaya","Alaca Hoyuk","Masat Hoyuk","Hattusa","Ilios","Kanesh","Arslantepe","Sam'al","Beycesultan","Adana","Karatepe","Tarsus","Sultantepe","Attalia","Acre","Adoraim","Alalah","Aleppo","Al-Sinnabra","Aphek","Arad Rabbah","Ashdod","Ashkelon","Baalbek","Batroun","Beersheba","Beth Shean","Bet Shemesh","Bethany","Bet-el","Bezer","Byblos","Capernaum","Dan","Dimashq","Deir Alla","Dhiban","Dor","Ebla","En Gedi","Enfeh","Ekron","Et-Tell","Gath","Gezer","Gibeah","Gilgal Refaim","Gubla","Hamath","Hazor","Hebron","Herodion","Jezreel","Kadesh Barnea","Kedesh","Kumidi","Lachish","Megiddo","Qatna","Qumran","Rabat Amon","Samaria","Sarepta","Sharuhen","Shiloh","Sidon","Tadmor","Tirzah","Tyros","Ugarit","Umm el-Marra"]

class unitAction:
	MOVE = 1
	ATTACK = 2
	WAIT = 3

class unitType:
	def __init__(self,name,textureIndex,movementSpeed,attackSpeed,attackPower,armor,range,health,canFly,canSwim,cost,buildTime,movementSpeedBonus,armorBonus,attackPowerBonus,researchCost,researchTime):
		self.name = name
		self.textureIndex = textureIndex
		self.movementSpeed = movementSpeed
		self.attackSpeed = attackSpeed
		self.attackPower = attackPower
		self.range = range
		self.health = health
		self.canFly = canFly
		self.canSwim = canSwim
		self.cost = cost
		self.buildTime = buildTime
		self.movementSpeedBonus = movementSpeedBonus
		self.armorBonus = armorBonus
		self.attackPowerBonus = attackPowerBonus
		self.researchCost = researchCost
		self.researchTime = researchTime
class unit:
	def __init__(self,unitType,player,level,xPos,yPos,node):
		self.unitType = unitType
		self.player = player
		self.xPos = xPos
		self.yPos = yPos
		self.node = node
		self.movementPoints = self.unitType.movementSpeed
		self.attackPoints = 0.0
		self.buildPoints = self.unitType.buildTime
		self.health = self.unitType.health
		self.movePath = []
		self.unitAction = unitAction.MOVE
		self.level = level
	def moveTo(self,node):
		if(node.unit != None and self.node != node):
			if(node.unit.player != self.player):
				print 'attack!!??'
			else:
				print 'own unit... do nothing or if were on a movepath, recalc movepath and move'
		else:
			self.node.unit = None
			self.node = node
			node.unit = self
			if(node.city != None):
				node.city.player = node.unit.player
       			self.movementPoints = self.movementPoints + self.unitType.movementSpeed
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
		self.researching = False
		self.doneResearching = False
		self.researchUnitType = None
		self.researchLevel = 0
		self.researchProgress = 0
		self.unitBeingBuilt = None
		self.unitBuildQueue = []
		self.player = 0
	def queueUnit(self,unit):
		self.unitBuildQueue.append(unit)
		if(self.unitBeingBuilt == None):
			self.buildNextUnit()
	def buildNextUnit(self):
		if(len(self.unitBuildQueue) > 0):
			self.unitBeingBuilt = self.unitBuildQueue[0]
			self.unitBuildQueue = self.unitBuildQueue[1:]
		else:
			self.node.unit.unitAction = unitAction.MOVE#wake up summoner
	def incrementBuildProgress(self):
		if(self.node.unit != None and self.node.unit.unitType.name == "summoner"):
			if(self.researching):
				if(self.researchUnitType != None):
					self.researchProgress = self.researchProgress + 1
					if(self.researchProgress >= researchBuildTime):
						self.researchLevel = self.researchLevel + 1
						self.researchProgress = 0
						self.node.unit.unitAction = unitAction.MOVE
						self.researching = False
			else:
				if(self.unitBeingBuilt != None):
					self.unitBeingBuilt.buildPoints = self.unitBeingBuilt.buildPoints - unitBuildSpeed
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
		else:
			(random.choice(self.neighbors)).addUnit(unit)

class playModeNode(node):
	isNeighbor = False
	moveMode = False
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
	def onLeftClickDown(self):
		if(True or len(gameState.getPlayers()) > 1):#multiplayer game
			if(gameState.getPlayers()[gameState.getGameMode().nextUnit.player-1].isOwnPlayer):
				if(playModeNode.moveMode):
					print '1'
					gameState.getGameMode().nextUnit.movePath = gameState.getGameMode().nextUnit.node.movePath[1:]
					print '1'
					gameState.getClient().sendCommand("nodeClick " + str(gameState.getGameMode().nextUnit.node.movePath[0].xPos) + " " + str(gameState.getGameMode().nextUnit.node.movePath[0].yPos) + "|")
					print '1'
				else:
					selectNode(self)
		elif(len(gameState.getPlayers()) > 0):#single player network game...
			print 'here...'
			gameState.getGameMode().nextUnit.movePath = gameState.getGameMode().nextUnit.node.movePath[1:]
			gameState.getClient().sendCommand("nodeClick " + str(gameState.getGameMode().nextUnit.node.movePath[0].xPos) + " " + str(gameState.getGameMode().nextUnit.node.movePath[0].yPos) + "|")

		else:
			if(playModeNode.moveMode):
				gameState.getGameMode().nextUnit.movePath = gameState.getGameMode().nextUnit.node.movePath[1:]
				gameState.getGameMode().nextUnit.moveTo(gameState.getGameMode().nextUnit.node.movePath[0])
				gameState.getGameMode().chooseNextUnit()
			else:
				selectNode(self)
	def toggleCursor(self):
		for node in playModeNode.movePath:
			node.onMovePath = False
		playModeNode.movePath = []
		if((gameState.getGameMode().nextUnit.node == self) or (playModeNode.isNeighbor and gameState.getGameMode().shiftDown) or ((not playModeNode.isNeighbor) and (not gameState.getGameMode().shiftDown))):
			self.cursorIndex = -1
			playModeNode.moveMode = False
		else:
			self.cursorIndex = cDefines.defines['CURSOR_MOVE_INDEX']
			playModeNode.moveMode = True
			self.aStarSearch()
	def aStarSearch(self):
		#start at end point so we can just track back and insert into an array in order
		self.findAStarHeuristicCost(gameState.getGameMode().nextUnit.node)
		playModeNode.openNodes.append(self)
		playModeNode.aStarSearchRecurse(gameState.getGameMode().nextUnit.node)
	def findAStarHeuristicCost(self,target):
		#This is just a heuristic that guesses the cost to the target by assuming everything is grass
		#current 'heuristic' is just the distance assuming everything is grass
		#I might want to change this to assume that everything is mountain... or somewhere in between... gotta think about it.
		#'even row' means map polarity = 0 and row # is even OR map polarity = 0 and row # is odd...
		#polarity 0 means 'even' rows are to the left
		#polarity 1 means 'even' rows are to the right
		#if moving from even to odd row left gives you free x at 1,3,5...
		#if moving from even to odd row right gives you free x at 3,5,7...
		#if moving from odd to even row right gives you free x at 1,3,5...
		#if moving from odd to even row left gives you free x at 3,5,7...
		heuristicCost = float(abs(self.xPos - target.xPos))
		if(abs(self.yPos-target.yPos)%2 == 1):#one row is even, other is odd...
			if(self.yPos%2 == gameState.getGameMode().map.polarity):#self is even...
				if(self.xPos > target.xPos):
					heuristicCost = heuristicCost - (abs(self.yPos-target.yPos)+1)/2
				else:
					heuristicCost = heuristicCost - (abs(self.yPos-target.yPos)-1)/2
			else:#self is odd
				if(self.xPos > target.xPos):
					heuristicCost = heuristicCost - (abs(self.yPos-target.yPos)-1)/2
				else:
					heuristicCost = heuristicCost - (abs(self.yPos-target.yPos)+1)/2
		else:
			heuristicCost = heuristicCost - abs(self.yPos-target.yPos)/2
		if(heuristicCost < 0.0):
			heuristicCost = 0.0
		heuristicCost = heuristicCost + abs(self.yPos - target.yPos)
		self.aStarHeuristicCost = heuristicCost
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
			nextNode = gameState.getGameMode().nextUnit.node.aStarParent
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
					if(neighbor.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['MOUNTAIN_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['WATER_TILE_INDEX'] and target.unit.unitType.canSwim == False):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['WATER_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					elif(neighbor.tileValue == cDefines.defines['DESERT_TILE_INDEX']):
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['DESERT_MOVE_COST']/(1.0+float(neighbor.roadValue)))
					else:
						neighbor.aStarKnownCost = node.aStarKnownCost + (cDefines.defines['GRASS_MOVE_COST']/(1.0+float(neighbor.roadValue)))
				else:
					if(neighbor.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
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
#		print "count:"+str(count)
		playModeNode.aStarSearchRecurse(target,count)
	def onMouseOver(self):
		if(gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):
			playModeNode.isNeighbor = True
		else:
			playModeNode.isNeighbor = False
		self.toggleCursor()
#	def onMouseOut(self):
#		if(gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):
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
				if(self.playerStartValue == gameState.getGameMode().selectedButton.playerNumber):
					self.playerStartValue = 0
					if(gameState.getGameMode().map.numPlayers == gameState.getGameMode().selectedButton.playerNumber and gameState.getGameMode().map.numPlayers != 1):
						for button in playerStartLocationButton.playerStartLocationButtons:
							if(button.playerNumber == gameState.getGameMode().map.numPlayers + 1):
								button.color = "55 55 55"
						gameState.getGameMode().map.numPlayers = gameState.getGameMode().map.numPlayers - 1
				else:
					for row in gameState.getGameMode().map.nodes:
						for node in row:
							if(node.playerStartValue == gameState.getGameMode().selectedButton.playerNumber):
								node.playerStartValue = 0
					self.playerStartValue = gameState.getGameMode().selectedButton.playerNumber

class map:
	def __init__(self,nodeType):
		self.polarity = 0
		self.nodeType = nodeType
		self.translateZ = 0-cDefines.defines['initZoom']
		self.load()
	def getWidth(self):
		return len(self.nodes)
	def getHeight(self):
		return len(self.nodes[0])
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
				self.numPlayers = 2
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
							roadValue = (intValue & 16)>>4
							playerStartValue = (intValue & (32+64+128))>>5
							newNode = self.nodeType(xPos,yPos,tileValue,roadValue,None,playerStartValue=playerStartValue)
							if(xPos > 0):#add neighbor to the left
								newNode.neighbors.append(newRow[len(newRow)-1])
								newRow[len(newRow)-1].neighbors.append(newNode)
							if(yPos > 0):#add neighbors above
								if(not (xPos == 0 and (self.polarity+yPos)%2 == 0)):#has top left neighbor
									if((self.polarity+yPos)%2 == 0):
										newNode.neighbors.append(self.nodes[yPos-1][xPos-1])
										self.nodes[yPos-1][xPos-1].neighbors.append(newNode)
									else:
										newNode.neighbors.append(self.nodes[yPos-1][xPos])
										self.nodes[yPos-1][xPos].neighbors.append(newNode)
								
								if(not (xPos == len(self.nodes[0])-1 and (self.polarity+yPos)%2 == 1)):#has top right neighbor
									if((self.polarity+yPos)%2 == 0):
										newNode.neighbors.append(self.nodes[yPos-1][xPos])
										self.nodes[yPos-1][xPos].neighbors.append(newNode)
									else:
										newNode.neighbors.append(self.nodes[yPos-1][xPos+1])
										self.nodes[yPos-1][xPos+1].neighbors.append(newNode)
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
							unitTypeTokens = unitTypeString.split("|")
							theUnitType = copy.copy(gameState.theUnitTypes[unitTypeTokens[0]])
							theUnitType.cost = unitTypeTokens[1]
							unitTypes.append(theUnitType)
					costOfOwnership = tokens[3]
					self.nodes[int(coords[1])][int(coords[0])].city = city(cityName,self.nodes[int(coords[1])][int(coords[0])],unitTypes,costOfOwnership)
			count = count + 1
		mapFile.close()
	def save(self):
		mapFile = open('maps/' + gameState.getMapName() + ".map",'w')
		yPos = 0
		xPos = 0
		cityLines = []
		nodeLines = []
		nodeLines.append(str(self.polarity) + "\n")
		for row in self.nodes:
			xPos = 0
			yPos = yPos + 1
			line = "#"
			for node in row:
				xPos = xPos + 1
				line = line + chr(node.tileValue + (16*node.roadValue)+ (32*node.playerStartValue) + (512*0))#USE 512 NEXT BECAUSE 8 PLAYERS NEEDS 3 BITS
				if(node.city != None):
					unitTypes = ""
					for unitType in node.city.unitTypes:
						unitTypes = unitTypes + "," + unitType.name + "|" + str(unitType.cost)
					unitTypes = unitTypes[1:]
					cityLines.append("*" + str(xPos-1) + "," + str(yPos-1) + ":" + node.city.name + ":" + unitTypes + ":" + str(node.city.costOfOwnership) + "\n")
			nodeLines.append(line + "\n")
		mapFile.writelines(nodeLines)
		mapFile.writelines(cityLines)
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
	gameState.getGameMode().selectedNode = node
	node.selected = True
	uiElements.actionViewer.destroy()
	uiElements.unitTypeResearchViewer.destroy()
	uiElements.unitTypeBuildViewer.destroy()
	if(node.city != None):
		uiElements.actionViewer.theActionViewer = uiElements.actionViewer(node)
#	if(node.unit != None):
#		uiElements.unitViewer.theUnitViewer = uiElements.unitViewer(node.unit)
	node.toggleCursor()


