#city viewer in playMode
#unit viewer in playMode
#campaign
#fog of war
#multiplayer
#AI

import os
import random
import copy
import gameState
import nameGenerator
import cDefines
from uiElements import *
from gameLogic import *

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
		self.cites = []
		self.nextUnit = None
		self.focusNextUnit = 0
		self.focusNextUnitTemp = 0
		self.selectedNode = None
		self.cityViewer = None
		tiledGameMode.__init__(self)
	def loadMap(self):
		self.map = map(playModeNode)
		self.loadSummoners()
		self.orderUnits()
		self.chooseNextUnit()

	def getFocusNextUnit(self):
		self.focusNextUnitTemp = self.focusNextUnit
		self.focusNextUnit = 0
		return self.focusNextUnitTemp
	def orderUnits(self):
		self.units.sort(key=lambda unit:0-unit.movementPoints)
	def chooseNextUnit(self):
		self.orderUnits()
		while(self.units[0].movementPoints < 1000.0):
			self.orderUnits()
			for unit in self.units:
				if(unit.node.roadValue == 1):
					unit.movementPoints = unit.movementPoints + 2.0
				elif(unit.node.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX']):
					unit.movementPoints = unit.movementPoints + 0.1
				elif(unit.node.tileValue == cDefines.defines['WATER_TILE_INDEX'] and unit.canSwim == False):
					unit.movementPoints = unit.movementPoints + 0.5
				elif(unit.node.tileValue == cDefines.defines['DESERT_TILE_INDEX']):
					unit.movementPoints = unit.movementPoints + 0.5
				else:
					unit.movementPoints = unit.movementPoints + 1.5
		eligibleUnits = []
		eligibleUnits.append(self.units[0])
		for unit in self.units[1:]:
			if(unit.movementPoints == eligibleUnits[0].movementPoints):
				eligibleUnits.append(unit)
		self.nextUnit = random.choice(eligibleUnits)
		self.nextUnit.node.selected = True
		self.selectedNode = self.nextUnit.node
		self.focusNextUnit = 1

	def loadSummoners(self):
		rowCount = 0
		columnCount = 0
		for row in self.map.nodes:
			columnCount = 0
			rowCount = rowCount + 1
			for node in row:
				columnCount = columnCount + 1
				if(node.playerStartValue != 0):
					node.unit = unit(theUnitTypes["summoner"],node.playerStartValue,rowCount,columnCount,node)
					self.units.append(node.unit)
	def incrementInitiatives(self):
		for unit in self.units:
			unit.movementInitiative = unit.movementInitiative + 1
			unit.attackInitiative = unit.attackInitiative + 1
		for city in self.cities:
			print city
			
	def handleKeyDown(self,keycode):
		try:
			self.elementWithFocus.onKeyDown(keycode)
		except:
			if(keycode == "space"):
				self.focusNextUnit = 1
				self.selectedNode.selected = False
				self.selectedNode = self.nextUnit.node
				self.nextUnit.node.selected = True

	def addUIElements(self):
		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElement(xPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_RIGHT_INDEX'])
		uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_BOTTOM_INDEX'])
		if(self.nextUnit.node.city != None):
			self.cityViewer = cityViewer(0.0,0.0,self.nextUnit.node.city)


class mapEditorMode(tiledGameMode):	
	def __init__(self):
		self.selectedButton = None
		self.selectedCityNode = None
		self.cityEditor = None
		self.mapOptionsEditor = None
		tiledGameMode.__init__(self)
	def loadMap(self):
		self.map = map(mapEditorNode)
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

		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElement(xPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines.defines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines.defines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines.defines['UI_MAP_EDITOR_RIGHT_INDEX'])

		uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines.defines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_MAP_EDITOR_BOTTOM_INDEX'])
#		self.cityEditor = cityEditor(0.0,0.0)

		mapEditorTileSelectUIElement(-0.93,0.92,tileType=cDefines.defines['DESERT_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.85,0.92,tileType=cDefines.defines['GRASS_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.77,0.92,tileType=cDefines.defines['MOUNTAIN_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.69,0.92,tileType=cDefines.defines['FOREST_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.61,0.92,tileType=cDefines.defines['WATER_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.53,0.92,tileType=cDefines.defines['ROAD_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines.defines['CITY_TILE_INDEX'])
		for col in range(0,2):
			for row in range(0,4):

				playerStartLocationButton(-0.39+(0.05*col),0.972-(0.038*row),playerNumber=col*4+row+1,width=2.0*cDefines.defines['PLAYER_START_BUTTON_WIDTH']/cDefines.defines['SCREEN_WIDTH'],height=2.0*cDefines.defines['PLAYER_START_BUTTON_HEIGHT']/cDefines.defines['SCREEN_HEIGHT'],textureIndex=cDefines.defines['PLAYER_START_BUTTON_INDEX'])
				uiElement(-0.370+(0.05*col),0.948-(0.04*row),text=str((col*4)+row+1),textSize=0.0004)
				
		mapEditorMapOptionsButton(-0.25,0.95,width=(2.0*cDefines.defines['MAP_ICON_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['MAP_ICON_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['MAP_ICON_INDEX'],cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'])

		addColumnButton(0.96,0.03,text="+",textureIndex=-1)
		removeColumnButton(0.96,-0.03,text="-",textureIndex=-1)

		addFirstColumnButton(-0.63,0.03,text="+",textureIndex=-1)
		removeFirstColumnButton(-0.63,-0.03,text="-",textureIndex=-1)

		addRowButton(0.18,-0.98,text="+",textureIndex=-1)
		removeRowButton(0.21,-0.98,text="-",textureIndex=-1)

		addFirstRowButton(0.18,0.77,text="+",textureIndex=-1)
		removeFirstRowButton(0.21,0.77,text="-",textureIndex=-1)

		uiElement(0.8,0.925,text="asdf",textSize=0.0005)
		saveButton(0.9,0.925,text="save",textSize=0.0005)

class textBasedMenuMode(gameMode):
	def __init__(self):
		gameMode.__init__(self)
	def handleKeyDown(self,keycode):
		if(keycode == "up"):
			if(menuButton.selectedIndex == 0):
				menuButton.buttonsList[menuButton.selectedIndex].textColor  = menuButton.normalTextColor
				menuButton.selectedIndex = menuButton.index - 1
				menuButton.buttonsList[menuButton.selectedIndex].textColor  =menuButton.selectedTextColor
			else:
				menuButton.buttonsList[menuButton.selectedIndex].textColor  = menuButton.normalTextColor
				menuButton.selectedIndex = menuButton.selectedIndex - 1
				menuButton.buttonsList[menuButton.selectedIndex].textColor  =menuButton.selectedTextColor
		elif(keycode == "down"):
			if(menuButton.selectedIndex == menuButton.index - 1):
				menuButton.buttonsList[menuButton.selectedIndex].textColor  = menuButton.normalTextColor
				menuButton.selectedIndex = 0
				menuButton.buttonsList[menuButton.selectedIndex].textColor  =menuButton.selectedTextColor
			else:
				menuButton.buttonsList[menuButton.selectedIndex].textColor  = menuButton.normalTextColor
				menuButton.selectedIndex = menuButton.selectedIndex + 1
				menuButton.buttonsList[menuButton.selectedIndex].textColor  =menuButton.selectedTextColor
		elif(keycode == "return"):
			menuButton.buttonsList[menuButton.selectedIndex].onClick()
					
class newGameScreenMode(textBasedMenuMode):
	def addUIElements(self):
		uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		newGameScreenButton(-0.16,0.2,quickPlayMapSelectMode,text="quick play")
		newGameScreenButton(-0.165,0.1,mapEditorSelectMode,text="map editor")

class quickPlayMapSelectMode(textBasedMenuMode):
	def addUIElements(self):
		uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		dirList=os.listdir("maps")
		heightDelta = 0.0
		for fileName in dirList:
			if(fileName.endswith(".map")):
				heightDelta = heightDelta - 0.1
				mapPlaySelectButton(-0.16,0.3+heightDelta,playMode,text=fileName[0:len(fileName)-4])

class mapEditorSelectMode(textBasedMenuMode):
	def addUIElements(self):
		uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		mapEditSelectButton(-0.16,0.2,newMapMode,text="create new map")
		dirList=os.listdir("maps")
		heightDelta = 0.0
		for fileName in dirList:
			if(fileName.endswith(".map")):
				heightDelta = heightDelta - 0.1
				mapEditSelectButton(-0.16,0.2+heightDelta,mapEditorMode,text=fileName[0:len(fileName)-4])

class newMapMode(gameMode):
	def __init__(self):
		gameMode.__init__(self)
	def addUIElements(self):
		uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		self.elementWithFocus = newMapNameInputElement(-0.2,0.2,mapEditorMode,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text="",textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01)
		uiElement(-0.2,0.0,text="asdf")

gameState.setGameMode(newGameScreenMode)
