def isFloat(str):
	try:
		float(str)
		return True
	except ValueError:
		return False
def isInt(str):
	try:
		int(str)
		return True
	except ValueError:
		return False

cDefines = {}
cFile =  open('main.c','r')
for line in cFile:
	if(line.strip().startswith("#define")):
		tokens = line.split()
		if(isInt(tokens[2])):
			cDefines[tokens[1]] = int(tokens[2])
		elif(isFloat(tokens[2])):
			cDefines[tokens[1]] = float(tokens[2])
		else:
			cDefines[tokens[1]] = tokens[2]
cFile.close()
class intNameGenerator:
	def __init__(self):
		self.nextName = -1
	def getNextName(self):
		self.nextName = self.nextName + 1
		return self.nextName

nameGenerator = intNameGenerator()

class uiElement:
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		self.name = nameGenerator.getNextName()
		self.xPosition = xPos
		self.yPosition = yPos
		self.width = width
		self.height = height
		self.textureIndex = textureIndex
		self.hidden=hidden
		self.cursorIndex=cursorIndex
		self.text = text
		self.textColor = textColor
		self.textSize = textSize
		self.color = color
		if(mouseOverColor != None):
			self.mouseOverColor = mouseOverColor
		else:
			self.mouseOverColor = color
		theGameMode.uiElements.append(self)

class clickableElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor)
		theGameMode.clickableObjsDict[self.name] = self

class newGameScreenButton(clickableElement):
	index = 0
	buttonsList = []
	selectedIndex = 1
	#selectedIndex = 0
	selectedTextColor = "55 55 55"
	normalTextColor = "33 33 33"
	def __init__(self,xPos,yPos,gameMode,width=1.0,height=1.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=newGameScreenButton.normalTextColor,cursorIndex=cDefines['CURSOR_HAND_INDEX'],mouseOverColor="66 66 66")
		theGameMode.clickableObjsDict[self.name] = self
		self.gameMode = gameMode
		self.selected = selected
		self.index = newGameScreenButton.index
		newGameScreenButton.buttonsList.append(self)
		newGameScreenButton.index = newGameScreenButton.index + 1
		if(self.index == newGameScreenButton.selectedIndex):
			self.textColor = newGameScreenButton.selectedTextColor
	def onClick(self):
		global theGameMode
		theGameMode = self.gameMode()
		if(hasattr(theGameMode,"loadMap")):
			theGameMode.loadMap()
		theGameMode.addUIElements()
class saveButton(clickableElement):	
	def onClick(self):
		theGameMode.map.save()

#TODO: MAKE SURE YOU CAN'T REMOVE THE LAST ROW OR COLUMN!!
class addColumnButton(clickableElement):
	def onClick(self):
		for row in theGameMode.map.nodes:
			row.append(node(0,0,0))
class removeColumnButton(clickableElement):
	def onClick(self):
		for row in theGameMode.map.nodes:
			row.pop()
class addFirstColumnButton(clickableElement):
	def onClick(self):
		for count in range(0,len(theGameMode.map.nodes)):
			rowCopy = theGameMode.map.nodes[count][:]
			rowCopy.reverse()
			rowCopy.append(node(0,0,0))
			rowCopy.reverse()
			theGameMode.map.nodes[count] = rowCopy
class removeFirstColumnButton(clickableElement):
	def onClick(self):
		for count in range(0,len(theGameMode.map.nodes)):
			rowCopy = theGameMode.map.nodes[count][:]
			rowCopy.reverse()
			rowCopy.pop()
			rowCopy.reverse()
			theGameMode.map.nodes[count] = rowCopy

class addRowButton(clickableElement):
	def onClick(self):
		newRow = []
		for count in range(0,len(theGameMode.map.nodes[0])):
			newRow.append(node(0,0,0))
		theGameMode.map.nodes.append(newRow)
class removeRowButton(clickableElement):
	def onClick(self):
		theGameMode.map.nodes.pop()
class addFirstRowButton(clickableElement):
	def onClick(self):
		nodesCopy = theGameMode.map.nodes[:]
		newRow = []
		for count in range(0,len(theGameMode.map.nodes[0])):
			newRow.append(node(0,0,0))
		nodesCopy.reverse()
		nodesCopy.append(newRow)
		nodesCopy.reverse()
		theGameMode.map.polarity = (~theGameMode.map.polarity)&1
		theGameMode.map.nodes = nodesCopy

class removeFirstRowButton(clickableElement):
	def onClick(self):
		nodesCopy = theGameMode.map.nodes[:]
		nodesCopy.reverse()
		nodesCopy.pop()
		nodesCopy.reverse()
		theGameMode.map.polarity = (~theGameMode.map.polarity)&1
		theGameMode.map.nodes = nodesCopy

class textInputUIElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,text="",textSize=0.001,textureIndex=-1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize)
		theGameMode.clickableObjsDict[self.name] = self
	def onKeyDown(self,keycode):
		if(keycode == "backspace"):
			self.text = self.text.rstrip(self.text[len(self.text)-1])
		else:
			self.text = self.text + keycode

class mapEditorTileSelectUIElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False,tileType=0,playerNumber=-1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,cursorIndex=cDefines['CURSOR_HAND_INDEX'])
		self.tileType = tileType
		self.selected = False
		theGameMode.clickableObjsDict[self.name] = self
		self.playerNumber = playerNumber
	def onClick(self):
		if(theGameMode.selectedButton != None):
			theGameMode.selectedButton.selected = False
			theGameMode.selectedButton.color = "FF FF FF"
		self.selected = True
		theGameMode.selectedButton = self

class playerStartLocationButton(clickableElement):
	playerStartLocationButtons = []
	def __init__(self,xPos,yPos,playerNumber,width=1.0,height=1.0,text="",textSize=0.001,textureIndex=-1,color="FF FF FF"):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,color=color)
		self.playerNumber = playerNumber
		self.selected = False
		theGameMode.clickableObjsDict[self.name] = self
		playerStartLocationButton.playerStartLocationButtons.append(self)
	def onClick(self):
#		if(self.playerNumber <= theGameMode.map.numPlayers + 1):
		if(theGameMode.selectedButton != None):
			theGameMode.selectedButton.selected = False
			theGameMode.selectedButton.color = "FF FF FF"
		theGameMode.selectedButton = self
		self.selected = True
		self.color = "99 99 99"

class node:
	def __init__(self,tileValue,roadValue,cityValue,playerStartValue=0):
		self.name = nameGenerator.getNextName()
		self.tileValue = tileValue
		self.roadValue = roadValue
		self.cityValue = cityValue
		self.playerStartValue = playerStartValue
		self.selected = False
		theGameMode.clickableObjsDict[self.name] = self

	def getValue(self):
		return self.tileValue
	def onClick(self):
		if(theGameMode.selectedButton != None):
			if(hasattr(theGameMode.selectedButton,"tileType")):
				if(theGameMode.selectedButton.tileType == cDefines['ROAD_TILE_INDEX']):
					self.roadValue = (~self.roadValue)&1
				elif(theGameMode.selectedButton.tileType == cDefines['CITY_TILE_INDEX']):
					self.cityValue = (~self.cityValue)&1
				else:
					self.tileValue = theGameMode.selectedButton.tileType
			else:
				if(self.playerStartValue == theGameMode.selectedButton.playerNumber):
					self.playerStartValue = 0
					if(theGameMode.map.numPlayers == theGameMode.selectedButton.playerNumber and theGameMode.map.numPlayers != 1):
						for button in playerStartLocationButton.playerStartLocationButtons:
							if(button.playerNumber == theGameMode.map.numPlayers + 1):
								button.color = "55 55 55"
						theGameMode.map.numPlayers = theGameMode.map.numPlayers - 1
				else:
#					if(theGameMode.map.numPlayers == theGameMode.selectedButton.playerNumber):
						
					for row in theGameMode.map.nodes:
						for node in row:
							if(node.playerStartValue == theGameMode.selectedButton.playerNumber):
								node.playerStartValue = 0
					self.playerStartValue = theGameMode.selectedButton.playerNumber

	def onRightClick(self):
		if(theGameMode.selectedNode != None):
			theGameMode.selectedNode.selected = False
		self.selected = True
		theGameMode.selectedNode = self
		if(self.cityValue > 0):
			print "show city editor"


class map:
	def __init__(self,mapEditorMode):
		self.polarity = 0
		self.load(mapEditorMode)
	def load(self,mapEditorMode):
		mapFile = open('map1','r')
		self.nodes = []
		count = 0
		for line in mapFile:
			if(count == 0):
				#TODO add players and starting positions to map data
				self.polarity = int(line)
				self.numPlayers = 2
			else:
				newRow = []
				for char in line:
					if(char != '\n'):
						intValue = ord(char)
						tileValue = intValue & 15
						roadValue = (intValue & 16)>>4
						cityValue = (intValue & 32)>>5
						playerStartValue = (intValue & (64+128+256))>>6
						newNode = node(tileValue,roadValue,cityValue,playerStartValue=playerStartValue)
						newRow.append(newNode)
				self.nodes.append(newRow)
			count = count + 1
		mapFile.close()
	def save(self):
		mapFile = open('map1','w')
		lines = []
		lines.append(str(self.polarity) + "\n")
		for row in self.nodes:
			line = ""
			for node in row:
				line = line + chr(node.tileValue + (16*node.roadValue) + (32*node.cityValue) + (64*node.playerStartValue) + (512*0))#USE 512 NEXT BECAUSE 8 PLAYERS NEEDS 3 BITS
			lines.append(line + "\n")
		mapFile.writelines(lines)
		mapFile.close()
		print "saved"
	def getNodes(self):
		return self.nodes
	def getIterator(self):
		return self.nodes.__iter__()
	def setNumPlayers(self,numPlayers):
		print numPlayers
	#	done = False
#		for count in range(0,len(theGameMode.uiElements)):
#			uiElem = theGameMode.uiElements[count]
#			if(hasattr(uiElem,"playerNumber")):
#				if(uiElem.playerNumber > numPlayers):
#					del theGameMode.uiElements[count+1]
#					del theGameMode.uiElements[count]
##					theGameMode.uiElements = theGameMode.uiElements[:count:]
#					done = True
#		if(not done):
			
#			mapEditorTileSelectUIElement(-0.37 + (0.08*(numPlayers-1)),0.92,tileType=cDefines['PLAYER_START_TILE_INDEX'],playerNumber=numPlayers)
#			uiElement(-0.39 + (0.08*(numPlayers-1)),0.90,text=str(numPlayers),textSize=0.0005)

		self.numPlayers = numPlayers

class mapEditorMode:
	def __init__(self):
		self.clickableObjsDict = {}
		self.elementWithFocus = None
		self.selectedButton = None
		self.uiElements = []
		self.selectedNode = None
	def loadMap(self):
		self.map = map(self)
	def getUIElementsIterator(self):
		return self.uiElements.__iter__()
	def handleRightClick(self,name):
		rightClickable = False
		if(self.clickableObjsDict.has_key(name)):
			if(hasattr(self.clickableObjsDict[name],"onRightClick")):
				rightClickable = True
				self.clickableObjsDict[name].onRightClick()
		if(not rightClickable):
			self.selectedNode.selected = False
			self.selectedNode = None
	def handleClick(self,name):
		if(self.clickableObjsDict.has_key(name)):
			self.elementWithFocus = self.clickableObjsDict[name]
			self.clickableObjsDict[name].onClick()
		else:
			self.elementWithFocus = None
	def handleKeyDown(self,keycode):
		try:
			self.elementWithFocus.onKeyDown(keycode)
		except:
			try:
				intKeycode = int(keycode)
				for key,value in self.clickableObjsDict.iteritems():
					if(hasattr(value,'tileType')):
						if(value.tileType == intKeycode-1):
							if(self.selectedButton != None):
								self.selectedButton.selected = False
							value.selected = True
							self.selectedButton = value
			except:
				return
	def addUIElements(self):
		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElement(xPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_RIGHT_INDEX'])
#-
		uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_BOTTOM_INDEX'])

		mapEditorTileSelectUIElement(-0.93,0.92,tileType=cDefines['DESERT_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.85,0.92,tileType=cDefines['GRASS_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.77,0.92,tileType=cDefines['MOUNTAIN_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.69,0.92,tileType=cDefines['JUNGLE_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.61,0.92,tileType=cDefines['WATER_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.53,0.92,tileType=cDefines['ROAD_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines['CITY_TILE_INDEX'])
		for col in range(0,2):
			for row in range(0,4):

				playerStartLocationButton(-0.39+(0.05*col),0.972-(0.038*row),playerNumber=col*4+row+1,width=2.0*cDefines['PLAYER_START_BUTTON_WIDTH']/cDefines['SCREEN_WIDTH'],height=2.0*cDefines['PLAYER_START_BUTTON_HEIGHT']/cDefines['SCREEN_HEIGHT'],textureIndex=cDefines['PLAYER_START_BUTTON_INDEX'])
				uiElement(-0.370+(0.05*col),0.948-(0.04*row),text=str((col*4)+row+1),textSize=0.0004)



		addColumnButton(0.98,0.03,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeColumnButton(0.98,-0.03,width=1.0,height=1.0,text="-",textureIndex=-1)

		addFirstColumnButton(-0.63,0.03,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeFirstColumnButton(-0.63,-0.03,width=1.0,height=1.0,text="-",textureIndex=-1)

		addRowButton(0.18,-0.98,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeRowButton(0.21,-0.98,width=1.0,height=1.0,text="-",textureIndex=-1)

		addFirstRowButton(0.18,0.77,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeFirstRowButton(0.21,0.77,width=1.0,height=1.0,text="-",textureIndex=-1)

#		textInputUIElement(0.8,0.885,text="input",textSize=0.0005)
		uiElement(0.8,0.925,width=1.0,height=1.0,text="asdf",textSize=0.0005)
		saveButton(0.9,0.925,width=1.0,height=1.0,text="save",textSize=0.0005)

class newGameScreenMode:
	def __init__(self):
		self.clickableObjsDict = {}
		self.elementWithFocus = None
		self.uiElements = []
		self.map = None
	def getUIElementsIterator(self):
		return self.uiElements.__iter__()
	def handleClick(self,name):
		if(self.clickableObjsDict.has_key(name)):
			self.elementWithFocus = self.clickableObjsDict[name]
			self.clickableObjsDict[name].onClick()
		else:
			self.elementWithFocus = None
	def handleKeyDown(self,keycode):
		if(keycode == "up"):
			if(newGameScreenButton.selectedIndex == 0):
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = newGameScreenButton.index - 1
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
			else:
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = newGameScreenButton.selectedIndex - 1
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
		elif(keycode == "down"):
			if(newGameScreenButton.selectedIndex == newGameScreenButton.index - 1):
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = 0
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
			else:
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = newGameScreenButton.selectedIndex + 1
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
		elif(keycode == "return"):
			newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].onClick()
					
	def addUIElements(self):
		uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines['UI_NEW_GAME_SCREEN_INDEX'])
		newGameScreenButton(-0.16,0.2,text="new game",gameMode=gameMode)
		newGameScreenButton(-0.165,0.1,text="map editor",gameMode=mapEditorMode)
		newGameScreenButton(-0.16,0.0,text="test test te",gameMode=gameMode)
		newGameScreenButton(-0.17,-0.1,text="test test tes",gameMode=mapEditorMode)
#		uiElement(-0.21,0.0,width=1.0,height=1.0,text="creature editor",textColor="DD DD DD")
#		uiElement(-0.12,-0.1,width=1.0,height=1.0,text="options",textColor="DD DD DD")
#		startNewGameButton(

class gameMode:
	def __init__(self):
		self.clickableObjsDict = {}
		self.elementWithFocus = None
		self.selectedButton = None
		self.uiElements = []
		self.selectedNode = None
		self.creatures = []
		self.cites = []
	def stepInitiatives(self):
		for creature in self.creatures:
			creature.movementInitiative = creature.movementInitiative + 1
			creature.attackInitiative = creature.attackInitiative + 1
		for city in self.cities:
			print city
	def loadMap(self):
		self.map = map(self)
	def getUIElementsIterator(self):
		return self.uiElements.__iter__()
	def handleRightClick(self,name):
		rightClickable = False
		if(self.clickableObjsDict.has_key(name)):
			if(hasattr(self.clickableObjsDict[name],"onRightClick")):
				rightClickable = True
				self.clickableObjsDict[name].onRightClick()
		if(not rightClickable):
			self.selectedNode.selected = False
			self.selectedNode = None
	def handleClick(self,name):
		if(self.clickableObjsDict.has_key(name)):
			self.elementWithFocus = self.clickableObjsDict[name]
			self.clickableObjsDict[name].onClick()
		else:
			self.elementWithFocus = None
	def handleKeyDown(self,keycode):
		try:
			self.elementWithFocus.onKeyDown(keycode)
		except:
			try:
				intKeycode = int(keycode)
			except:
				return
	def addUIElements(self):
		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElement(xPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_RIGHT_INDEX'])
#-
		uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_BOTTOM_INDEX'])

		mapEditorTileSelectUIElement(-0.93,0.92,tileType=cDefines['DESERT_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.85,0.92,tileType=cDefines['GRASS_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.77,0.92,tileType=cDefines['MOUNTAIN_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.69,0.92,tileType=cDefines['JUNGLE_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.61,0.92,tileType=cDefines['WATER_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.53,0.92,tileType=cDefines['ROAD_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines['CITY_TILE_INDEX'])

		addColumnButton(0.98,0.03,width=1.0,height=1.0,text="+")
		removeColumnButton(0.98,-0.03,width=1.0,height=1.0,text="-")

		addFirstColumnButton(-0.63,0.03,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeFirstColumnButton(-0.63,-0.03,width=1.0,height=1.0,text="-",textureIndex=-1)

		addRowButton(0.18,-0.98,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeRowButton(0.21,-0.98,width=1.0,height=1.0,text="-",textureIndex=-1)

		addFirstRowButton(0.18,0.77,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeFirstRowButton(0.21,0.77,width=1.0,height=1.0,text="-",textureIndex=-1)

		uiElement(0.8,0.925,width=1.0,height=1.0,text="asdf",textSize=0.0005)

class creature:
	def __init__(self):
		self.movementInitiative = 0
		self.attackInitiative = 0
		print 'creature'

class city:
	def __init__(self):
		print "city"

global theGameMode
theGameMode = newGameScreenMode()
theGameMode.addUIElements()

#theGameMode = mapEditorMode()
#theGameMode.loadMap()
#theGameMode.addUIElements()
#print theGameMode
