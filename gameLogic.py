import gameState
import nameGenerator
import cDefines
from uiElements import *

class city:
	def __init__(self,name,unitTypes=[],costOfOwnership=10):
		self.name = name
		self.costOfOwnership = costOfOwnership
		self.unitTypes = unitTypes
		self.unitBeingProduced = None
		self.unitProductionProgress = 0

class unitType:
	def __init__(self,name,textureIndex,movementInitiative,attackInitiative,health,canFly=False,canSwim=False,defaultCost=10,defaultBuildTime=1000):
		self.name = name
		self.textureIndex = textureIndex
		self.movementInitiative = movementInitiative
		self.attackInitiative = attackInitiative
		self.health = health
		self.canFly = canFly
		self.canSwim = canSwim
		self.cost = defaultCost
		self.buildTime = defaultBuildTime

class unit:
	def __init__(self,unitType,player,xPos,yPos,node):
		self.unitType = unitType
		self.player = player
		self.xPos = xPos
		self.yPos = yPos
		self.node = node
		self.movementPoints = 0.0
		self.attackPoints = 0.0
		self.health = self.unitType.health

unitTypesList = []
unitTypesList.append(unitType("summoner",cDefines.defines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("beaver",cDefines.defines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("catapult",cDefines.defines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("fire elemental",cDefines.defines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("dragon",cDefines.defines["MEEPLE_INDEX"],1.0,1.0,100))

theUnitTypes = {}
for unitType in unitTypesList:
	theUnitTypes[unitType.name] = unitType

class node:
	def __init__(self,xPos,yPos,tileValue=cDefines.defines['GRASS_TILE_INDEX'],roadValue=0,city=None,playerStartValue=0):
		self.xPos = xPos
		self.yPos = yPos
		self.name = nameGenerator.getNextName()
		self.tileValue = tileValue
		self.roadValue = roadValue
		self.city = city
#		self.cityViewer = None
		self.playerStartValue = playerStartValue
		self.selected = False
		gameState.getGameMode().elementsDict[self.name] = self
		self.unit = None
		self.neighbors = []
	def getValue(self):
		return self.tileValue

class map:
	def __init__(self,nodeType):
		self.polarity = 0
		self.nodeType = nodeType
		self.translateZ = 0-cDefines.defines['initZoom']
		self.load()
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
							theUnitType = copy.copy(theUnitTypes[unitTypeTokens[0]])
							theUnitType.cost = unitTypeTokens[1]
							unitTypes.append(theUnitType)
					costOfOwnership = tokens[3]
					self.nodes[int(coords[1])][int(coords[0])].city = city(cityName,unitTypes,costOfOwnership)
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
		print numPlayers
		self.numPlayers = numPlayers





class playModeNode(node):
	def onLeftClickDown(self):
		if(gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):#move unit
			if(self.unit != None):
				print "attack!!!!..?"
			else:
				gameState.getGameMode().selectedNode.selected = False
				gameState.getGameMode().nextUnit.node.unit = None
				gameState.getGameMode().nextUnit.node = self
				self.unit = gameState.getGameMode().nextUnit
				gameState.getGameMode().nextUnit.movementPoints = gameState.getGameMode().nextUnit.movementPoints - 1000.0
				gameState.getGameMode().chooseNextUnit()
		else:#select node
			if(gameState.getGameMode().cityViewer != None):
				gameState.getGameMode().cityViewer.destroy()
			gameState.getGameMode().selectedNode.selected = False
			gameState.getGameMode().selectedNode = self
			self.selected = True
			if(self.city != None):
				gameState.getGameMode().cityViewer = cityViewer(0.0,0.0,self.city)
				
	def onMouseOver(self):
		if(gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):
			print "display 'move' cursor here"
	def onMouseOut(self):
		if(gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):
			print "remove 'move' cursor here"
		

class mapEditorNode(node):
	def onLeftClickUp(self):
		if(gameState.getGameMode().selectedCityNode != None):
			if(gameState.getGameMode().selectedCityNode != self):
				if(gameState.getGameMode().selectedCityNode.city != None):
					self.city = gameState.getGameMode().selectedCityNode.city
					gameState.getGameMode().selectedCityNode.city = None
					gameState.getGameMode().selectedCityNode.selected = False
					self.selected = True
					gameState.getGameMode().selectedCityNode = self
	def onLeftClickDown(self):
		if(gameState.getGameMode().selectedButton != None):
			if(hasattr(gameState.getGameMode().selectedButton,"tileType")):
				if(gameState.getGameMode().selectedButton.tileType == cDefines.defines['ROAD_TILE_INDEX']):#new road
					self.roadValue = (~self.roadValue)&1
				elif(gameState.getGameMode().selectedButton.tileType == cDefines.defines['CITY_TILE_INDEX']):#new city
					if(self.city == None):
						self.city = city(random.choice(cityNames))
					gameState.getGameMode().cityEditor = cityEditor(0.0,0.0,self.city)
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

