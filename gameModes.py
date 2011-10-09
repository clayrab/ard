#server:
#room for finding games
#room for each game
#way to save and resume games
#icons for each unit
#fog of war
#attacking
#unit viewer in playMode
#AI
#campaign

import os
import random
import copy
import time
import gameState
import nameGenerator
import cDefines
import gameLogic
import uiElements
import server
import client

zoomSpeed = 0.3
class gameMode:
	sortedElements = []
	def __init__(self):
		self.elementsDict = {}
		self.map = None
		self.elementWithFocus = None
		self.resortElems = True
		
	def getUIElementsIterator(self):
		#TODO: remove resortElems code if it's not needed...
		if(self.resortElems):
			self.resortElems = False
#			gameMode.sortedElements = sorted(self.elementsDict.values().__iter__())
#			gameMode.sortedElements = self.elementsDict.values()
#			print "SORT"
#			print gameMode.sortedElements
#		return gameMode.sortedElements.__iter__()
		return self.elementsDict.values().__iter__()
	def handleLeftClickDown(self,name):
		if(self.elementsDict.has_key(name)):
			self.elementWithFocus = self.elementsDict[name]
			if(hasattr(self.elementsDict[name],"onClick")):
				self.elementsDict[name].onClick()
			elif(hasattr(self.elementsDict[name],"onLeftClickDown")):
				self.elementsDict[name].onLeftClickDown()
			elif(hasattr(self.elementWithFocus,"onClick")):
				self.elementWithFocus.onClick()
			elif(hasattr(self.elementWithFocus,"onLeftClickDown")):
				self.elementWithFocus.onLeftClickDown()
		else:
			self.elementWithFocus = None
	def handleLeftClickUp(self,name):
		if(self.elementsDict.has_key(name)):
			if(hasattr(self.elementsDict[name],"onLeftClickUp")):
                                self.elementsDict[name].onLeftClickUp()
			elif(hasattr(self.elementWithFocus,"onLeftClickUp")):
				self.elementWithFocus.onLeftClickUp()
	def handleKeyDown(self,keycode):
		if(hasattr(self.elementWithFocus,"onKeyDown")):
			self.elementWithFocus.onKeyDown(keycode)
	def handleKeyUp(self,keycode):
		if(hasattr(self.elementWithFocus,"onKeyUp")):
			self.elementWithFocus.onKeyUp(keycode)
	def onQuit(self):
		if(gameState.getClient() != None):
			print 'shutting down client...'
			gameState.getClient().socket.close()
			print 'done shutting down client'
		if(gameState.getServer() != None):
			print 'shutting down server...'
			gameState.getServer().shutdown()
			print 'done shutting down'
	def onDraw(self):
		if(gameState.getClient() != None):
			if(hasattr(gameState.getClient(),"checkSocket")):
				gameState.getClient().checkSocket()
			
class tiledGameMode(gameMode):
	def __init__(self):
		self.mousedOverObject = None
		self.mouseX = 0
		self.mouseY = 0
		gameMode.__init__(self)
	def handleMouseMovement(self,name,mouseX,mouseY):
		self.mouseX = mouseX
		self.mouseY = mouseY
		if(self.elementsDict.has_key(name)):
			if(hasattr(self.elementsDict[name],"onMouseMovement")):
				self.elementsDict[name].onMouseMovement()
			elif(hasattr(self.elementWithFocus,"onMouseMovement")):
				self.elementWithFocus.onMouseMovement()
	def handleRightClick(self,name):
		rightClickable = False
		if(self.elementsDict.has_key(name)):
			if(hasattr(self.elementsDict[name],"onRightClick")):
				rightClickable = True
				self.elementsDict[name].onRightClick()
		if(not rightClickable):
			self.selectedCityNode.selected = False
			self.selectedCityNode = None
	def handleScrollUp(self,name,deltaTicks):
		if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollUp")):
			self.elementsDict[name].onScrollUp()
		else:
			self.map.translateZ = self.map.translateZ + zoomSpeed*deltaTicks;
			if(self.map.translateZ > (-10.0-cDefines.defines['minZoom'])):
				self.map.translateZ = -10.0-cDefines.defines['minZoom']
	def handleScrollDown(self,name,deltaTicks):
		if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollDown")):
			self.elementsDict[name].onScrollDown()
		else:
			self.map.translateZ = self.map.translateZ - zoomSpeed*deltaTicks;
			if(self.map.translateZ < (10.0-cDefines.defines['maxZoom'])):
				self.map.translateZ = 10.0-cDefines.defines['maxZoom']
	def handleMouseOver(self,name,isLeftMouseDown):
		#TODO: keeping track of mousedOverObject might not be necessary any more since I added previousMousedoverName to the C code
		if(isLeftMouseDown > 0):#allows onLeftClickDown to be called for tiles when the mouse is dragged over them
			if(gameState.getGameMode().selectedButton != None):
				if(gameState.getGameMode().selectedButton.tileType != cDefines.defines['CITY_TILE_INDEX']):
					if(self.elementsDict.has_key(name)):
						if(hasattr(self.elementsDict[name],"tileValue")):#node
							self.elementsDict[name].onLeftClickDown()
		if(self.mousedOverObject != None):
			if(self.mousedOverObject.name != name):
				if(hasattr(self.mousedOverObject,"onMouseOut")):
					self.mousedOverObject.onMouseOut()
				self.mousedOverObject = None
		if(self.elementsDict.has_key(name)):
			if(self.mousedOverObject != None):
				if(self.mouseOverObject.name != name):
					self.mousedOverObject = self.elementsDict[name]
					if(hasattr(self.elementsDict[name],"onMouseOver")):
						self.elementsDict[name].onMouseOver()
			else:
				self.mousedOverObject = self.elementsDict[name]
				if(hasattr(self.elementsDict[name],"onMouseOver")):
					self.elementsDict[name].onMouseOver()


class playMode(tiledGameMode):
	def __init__(self):
		self.units = []
#		self.cites = []
		self.nextUnit = None
		self.focusNextUnit = 0
		self.focusNextUnitTemp = 0
		self.selectedNode = None
		self.cityViewer = None
		tiledGameMode.__init__(self)
	def loadMap(self):
		self.map = gameLogic.map(gameLogic.playModeNode)
		self.loadSummoners()
		self.orderUnits()
		self.chooseNextUnit()
	def getFocusNextUnit(self):
		self.focusNextUnitTemp = self.focusNextUnit
		self.focusNextUnit = 0
		return self.focusNextUnitTemp
	def orderUnits(self):
		self.units.sort(key=lambda unit:unit.movementPoints)
	def chooseNextUnit(self):
		self.orderUnits()
		while(self.units[0].movementPoints > 0.0):
			self.orderUnits()
			for unit in self.units:
#				if(unit.node.roadValue == 1):
#					unit.movementPoints = unit.movementPoints - 2.0
				if(unit.node.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
					unit.movementPoints = unit.movementPoints - ((1.0+float(unit.node.roadValue))/cDefines.defines['MOUNTAIN_MOVE_COST'])
				elif(unit.node.tileValue == cDefines.defines['WATER_TILE_INDEX'] and unit.canSwim == False):
					unit.movementPoints = unit.movementPoints - ((1.0+float(unit.node.roadValue))/cDefines.defines['WATER_MOVE_COST'])
				elif(unit.node.tileValue == cDefines.defines['DESERT_TILE_INDEX']):
					unit.movementPoints = unit.movementPoints - ((1.0+float(unit.node.roadValue))/cDefines.defines['DESERT_MOVE_COST'])
				else:
					unit.movementPoints = unit.movementPoints - ((1.0+float(unit.node.roadValue))/cDefines.defines['GRASS_MOVE_COST'])
			for row in self.map.nodes:
				for node in row:
					if(node.city != None and node.city.unitBeingBuilt != None and node.unit != None and node.unit.unitType.name == "summoner"):
						node.city.unitBeingBuilt.buildPoints = node.city.unitBeingBuilt.buildPoints - 1.0
						if(node.city.unitBeingBuilt.buildPoints <= 0.0):
							node.addUnit(node.city.unitBeingBuilt)
							node.city.buildNextUnit()

		eligibleUnits = []
		eligibleUnits.append(self.units[0])
		for unit in self.units[1:]:
			if(unit.movementPoints == eligibleUnits[0].movementPoints):
				eligibleUnits.append(unit)
		self.nextUnit = random.choice(eligibleUnits)
		gameLogic.selectNode(self.nextUnit.node)
		self.focusNextUnit = 1
		if(len(self.nextUnit.movePath) > 0):
			self.nextUnit.movePath = self.nextUnit.movePath[1:]
			self.nextUnit.moveTo(self.nextUnit.movePath[0])
	def loadSummoners(self):
		rowCount = 0
		columnCount = 0
		for row in self.map.nodes:
			columnCount = 0
			rowCount = rowCount + 1
			for node in row:
				columnCount = columnCount + 1
				if(node.playerStartValue != 0):
					node.addUnit(gameLogic.unit(gameState.theUnitTypes["summoner"],node.playerStartValue,rowCount,columnCount,node))
#					node.unit = gameLogic.unit(gameState.theUnitTypes["summoner"],node.playerStartValue,rowCount,columnCount,node)
#					self.units.append(node.unit)
	def handleKeyDown(self,keycode):
		if(keycode == "space"):
			self.nextUnit.moveTo(self.nextUnit.node)
		elif(keycode == "n"):
			self.focusNextUnit = 1
			self.selectedNode.selected = False
			self.selectedNode = self.nextUnit.node
			self.nextUnit.node.selected = True
		else:
			if(hasattr(self.mousedOverObject,"onKeyDown")):
				self.mousedOverObject.onKeyDown(keycode)
			elif(hasattr(self.elementWithFocus,"onKeyDown")):
				self.elementWithFocus.onKeyDown(keycode)

	def handleKeyUp(self,keycode):
		if(hasattr(self.mousedOverObject,"onKeyUp")):
			self.mousedOverObject.onKeyUp(keycode)

	def addUIElements(self):
		uiElements.uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElements.uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElements.uiElement(xPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_RIGHT_INDEX'])
		uiElements.uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_BOTTOM_INDEX'])
		gameLogic.selectNode(self.nextUnit.node)

class mapEditorMode(tiledGameMode):	
	def __init__(self):
		self.selectedButton = None
		self.selectedCityNode = None
		self.cityEditor = None
		self.mapOptionsEditor = None
		tiledGameMode.__init__(self)
	def loadMap(self):
		self.map = gameLogic.map(gameLogic.mapEditorNode)
	def handleKeyDown(self,keycode):
		if(keycode == 'r'):
			print keycode
			self.resortElems = True
		try:
			self.elementWithFocus.onKeyDown(keycode)
		except:
			try:
				intKeycode = int(keycode)
				for key,value in self.elementsDict.iteritems():
					if(hasattr(value,'tileType')):
						if(value.tileType == intKeycode-1):
							if(self.selectedButton != None):
								self.selectedButton.selected = False
							value.selected = True
							self.selectedButton = value
			except:
				return
	def addUIElements(self):

		uiElements.uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElements.uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElements.uiElement(xPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_RIGHT_INDEX'])

		uiElements.uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_BOTTOM_INDEX'])

		uiElements.mapEditorTileSelectUIElement(-0.93,0.92,tileType=cDefines.defines['DESERT_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.85,0.92,tileType=cDefines.defines['GRASS_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.77,0.92,tileType=cDefines.defines['MOUNTAIN_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.69,0.92,tileType=cDefines.defines['FOREST_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.61,0.92,tileType=cDefines.defines['WATER_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.53,0.92,tileType=cDefines.defines['ROAD_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines.defines['CITY_TILE_INDEX'])
		for col in range(0,2):
			for row in range(0,4):

				uiElements.playerStartLocationButton(-0.39+(0.05*col),0.972-(0.038*row),playerNumber=col*4+row+1,width=2.0*cDefines.defines['PLAYER_START_BUTTON_WIDTH']/cDefines.defines['SCREEN_WIDTH'],height=2.0*cDefines.defines['PLAYER_START_BUTTON_HEIGHT']/cDefines.defines['SCREEN_HEIGHT'],textureIndex=cDefines.defines['PLAYER_START_BUTTON_INDEX'])
				uiElements.uiElement(-0.370+(0.05*col),0.948-(0.04*row),text=str((col*4)+row+1),textSize=0.0004)
				
		uiElements.mapEditorMapOptionsButton(-0.25,0.95,width=(2.0*cDefines.defines['MAP_ICON_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['MAP_ICON_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['MAP_ICON_INDEX'],cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'])

		uiElements.addColumnButton(0.96,0.03,text="+",textureIndex=-1)
		uiElements.removeColumnButton(0.96,-0.03,text="-",textureIndex=-1)

		uiElements.addFirstColumnButton(-0.63,0.03,text="+",textureIndex=-1)
		uiElements.removeFirstColumnButton(-0.63,-0.03,text="-",textureIndex=-1)

		uiElements.addRowButton(0.18,-0.98,text="+",textureIndex=-1)
		uiElements.removeRowButton(0.21,-0.98,text="-",textureIndex=-1)

		uiElements.addFirstRowButton(0.18,0.77,text="+",textureIndex=-1)
		uiElements.removeFirstRowButton(0.21,0.77,text="-",textureIndex=-1)

		uiElements.uiElement(0.8,0.925,text="asdf",textSize=0.0005)
		uiElements.saveButton(0.9,0.925,text="save",textSize=0.0005)

class textBasedMenuMode(gameMode):
	def __init__(self):
		gameMode.__init__(self)
	def handleKeyDown(self,keycode):
		if(keycode == "up"):
			if(uiElements.menuButton.selectedIndex == 0):
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  = uiElements.menuButton.normalTextColor
				uiElements.menuButton.selectedIndex = uiElements.menuButton.index - 1
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  =uiElements.menuButton.selectedTextColor
			else:
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  = uiElements.menuButton.normalTextColor
				uiElements.menuButton.selectedIndex = uiElements.menuButton.selectedIndex - 1
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  =uiElements.menuButton.selectedTextColor
		elif(keycode == "down"):
			if(uiElements.menuButton.selectedIndex == uiElements.menuButton.index - 1):
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  = uiElements.menuButton.normalTextColor
				uiElements.menuButton.selectedIndex = 0
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  =uiElements.menuButton.selectedTextColor
			else:
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  = uiElements.menuButton.normalTextColor
				uiElements.menuButton.selectedIndex = uiElements.menuButton.selectedIndex + 1
				uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].textColor  =uiElements.menuButton.selectedTextColor
		elif(keycode == "return"):
			uiElements.menuButton.buttonsList[uiElements.menuButton.selectedIndex].onClick()
					
class newGameScreenMode(textBasedMenuMode):
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.menuButton(-0.16,0.2,quickPlayMapSelectMode,text="quick play")
		uiElements.menuButton(-0.155,0.1,comingSoonMode,text="campaign")
		uiElements.menuButton(-0.168,0.0,multiplayerGameScreenMode,text="multiplayer")
		uiElements.menuButton(-0.165,-0.1,mapEditorSelectMode,text="map editor")

class multiplayerGameScreenMode(textBasedMenuMode):
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.menuButton(-0.15,0.2,hostLANGameScreenMode,text="host lan game")
		uiElements.menuButton(-0.15,0.1,joinLANGameScreenMode,text="join lan game")
		uiElements.menuButton(-0.15,0.0,comingSoonMode,text="online")

class comingSoonMode(textBasedMenuMode):
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.menuButton(-0.45,0.0,newGameScreenMode,text="campaign mode coming soon!")
		
class quickPlayMapSelectMode(textBasedMenuMode):
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		dirList=os.listdir("maps")
		heightDelta = 0.0
		for fileName in dirList:
			if(fileName.endswith(".map")):
				heightDelta = heightDelta - 0.1
				uiElements.mapPlaySelectButton(-0.16,0.3+heightDelta,playMode,text=fileName[0:len(fileName)-4])

class mapEditorSelectMode(textBasedMenuMode):
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.mapEditSelectButton(-0.16,0.2,newMapMode,text="create new map")
		dirList=os.listdir("maps")
		heightDelta = 0.0
		for fileName in dirList:
			if(fileName.endswith(".map")):
				heightDelta = heightDelta - 0.1
				uiElements.mapEditSelectButton(-0.16,0.2+heightDelta,mapEditorMode,text=fileName[0:len(fileName)-4])

class newMapMode(gameMode):
	def __init__(self):
		gameMode.__init__(self)
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.uiElement(-0.15,0.2,text="map name")
		self.elementWithFocus = uiElements.newMapNameInputElement(-0.15,0.15,mapEditorMode,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text="",textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01)

class joinLANGameScreenMode(gameMode):
	def __init__(self):
		gameMode.__init__(self)
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.uiElement(-0.15,0.2,text="Host IP Address")
		self.elementWithFocus = uiElements.hostIPInputElement(-0.15,0.15,joiningLANGameScreenMode,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01)

class joiningLANGameScreenMode(gameMode):
	def __init__(self):
		gameMode.__init__(self)
		self.playerElementNames = []
	def removePlayerElements(self):
		for name in self.playerElementNames:
			del gameState.getGameMode().elementsDict[name]
		self.playerElementNames = []
		gameState.getGameMode().resortElems = True
	def redrawPlayers(self):
		self.removePlayerElements()
		height = 0.7
		for player in gameState.getPlayers():
			if(player.isOwnPlayer):
				self.playerElementNames.append(uiElements.uiElement(-0.85,height,text="*player " + str(player.playerNumber) + "*").name)
			else:
				self.playerElementNames.append(uiElements.uiElement(-0.85,height,text="player " + str(player.playerNumber)).name)
			height = height - 0.1
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.uiElement(-0.15,0.9,text="lan game")
		uiElements.uiElement(-0.85,0.8,text="players")
		self.mapNameElement = uiElements.uiElement(-0.85,-0.1,text="choose map")
		#uiElements.menuButton(-0.45,0.0,newGameScreenMode,text="back")

class hostLANGameScreenMode(gameMode):
	def __init__(self):
		gameMode.__init__(self)
		self.playerElementNames = []
	def removePlayerElements(self):
		for name in self.playerElementNames:
			del gameState.getGameMode().elementsDict[name]
		self.playerElementNames = []
		gameState.getGameMode().resortElems = True
	def redrawPlayers(self):
		self.removePlayerElements()
		height = 0.7
		for player in gameState.getPlayers():
			if(player.isOwnPlayer):
				self.playerElementNames.append(uiElements.uiElement(-0.85,height,text="*player " + str(player.playerNumber) + "*").name)
			else:
				self.playerElementNames.append(uiElements.uiElement(-0.85,height,text="player " + str(player.playerNumber)).name)
			height = height - 0.1
	def addUIElements(self):
		print 'starting server...'
		server.startServer('')
		print 'server started...'
		print 'starting client...'
		client.startClient('127.0.0.1')
		print 'client started'
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		uiElements.uiElement(-0.15,0.9,text="lan game")
		uiElements.uiElement(-0.85,0.8,text="players")
		uiElements.mapField(-0.85,-0.1,text="choose map")
		uiElements.startButton(0.65,-0.8,playMode,text="start")

gameState.setGameMode(newGameScreenMode)
