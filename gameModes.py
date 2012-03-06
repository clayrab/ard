#ALL GRAPHICS SHOULD BE CREATED BASED ON 1600x1200 RESOLUTION WHICH WILL BE RENDERED DOWN TO 1280x960 FOR NOW
#icons for each unit

#webpage
#SSL
#registration
#distribution
#general instructions page
#how to host instructions page

#server:
#player count
#room player count
#chat
#player count
#kick player from room if it's full when they join
#polish gameroom view
#    show each player status (connecting, connected, ready)
#show map info(perhaps just size, units available, and city count would be sufficient for now?)

#MISSING FEATURES
#testing connection timeout
#gatherers and summoners should not be able to move once they begin gathering or summoning. summoners don't get turns, they can build at any time.
#proper quit and options menus
#draw roads properly
#mountains should be impassable, hills less passable, hills give defense bonus
#sound effects
#mouseover effects
#limited time to move
#modals should be dismissed by esc, space, or enter
#handle disconnections/reconnections gracefully
#player stats(wins,losses,rank,etc)

#BUGS
#movepaths are not cleared properly
#sending " to chat as first character doesn't work... 
#clickscroll is shakey 
#fix py_decrefs in fonts.h
#scrolling map breaks after zoom out from near edge of map
#make sure text edit boxes only allow chars and not shift/enter
#check new/edited city names for duplicates
#uiElements startingManaSelector needs to be removed
#map editor: nodes created after the ui render the ui unclickable since clicks go 'thru' to the new nodes
#make sure room and/or map names do not contain *
# + buttons in map edit mode are wrong

#DESIGN
#cancel movement if any enemy is seen
#show move speed and attack speed
#icons for green and blue wood

#potential units:
#eagle. gains bonus vision range.
#giant eagle. gains bonus vision, has decent HP and attack.
#unit which 'becomes' a defensive structure and can't move like gatherer and summoner and auto-attacks
#unit could also drop mines and then become normal unit(like SC vulture)

############# MINIMUM VIABLE PRODUCT AT THIS POINT ##############

#BONUS FEATURES
#sort room columns
#player rewards
#auto return view: after auto-scrolling to nextunit, return view to previous spot, player can turn this on/off with a checkbox in the UI.

#POLISH
#existing movePath and new movePath need to be distinguishable
#some C optimization inside drawTile() and maybe draw()... make lists, reduce mallocs in draw loop, etc
#move gameplay viewport back to entire window. make UI less intrusive, small elements at the corners, encircle map with mountains
#right-justifiable text
#add odd/even columns. i.e. every other column will get a new node with you hit +

#MINOR BUGS
#when you create a new map in map editor the player start location buttons are broken and cause crashes
#clicking playerstartlocation button #1 repeatedly causes a crash
#make zoomspeed(in main.c) and focusspeed non-framerate dependant

#OPTIONAL FEATURES
#save and resume games
#music
#AI
#campaign
#unit editor

import sys
#print sys.path
#sys.path.insert(0,"python26.zip")
#sys.path.insert(0,".")
import os
import random
import math
import copy
import time
import traceback
import gameState
import nameGenerator
import cDefines
import gameLogic
import uiElements
import server
import client
import gameFindClient
from textureFunctions import texWidth, texHeight, texIndex

print random.__file__


sys.setrecursionlimit(100000)
#need this to allow deep recursion for AStar
#defaults to 1000... may cause crash on systems where 1000000 is too large...
def printTraceBack(excType,excValue,tb=None):
	print excType
	print excValue
	if(tb!=None):
		traceback.print_tb(tb)

class gameMode:
	sortedElements = []
	def __init__(self,args=[]):
		self.elementsDict = {}
		self.map = None
		self.elementWithFocus = None
		self.resortElems = True
		self.mouseTextPosition = -1
		self.modal = None
		self.mouseX = 0
		self.mouseY = 0
	def handleMouseMovement(self,name,mouseX,mouseY):
		self.mouseX = mouseX
		self.mouseY = mouseY
		if(self.elementsDict.has_key(name)):
			if(hasattr(self.elementsDict[name],"onMouseMovement")):
				self.elementsDict[name].onMouseMovement()
			elif(hasattr(self.elementWithFocus,"onMouseMovement")):
				self.elementWithFocus.onMouseMovement()

	def setFocus(self,elem):
		if(self.elementWithFocus != None):
			self.elementWithFocus.focused = False
		self.elementWithFocus = elem
		if(self.elementWithFocus != None):#no idea how this would occur but it did... TODO: figure out how
			self.elementWithFocus.focused = True
	def getUIElementsIterator(self):
		if(self.resortElems):
			self.resortElems = False
#			gameMode.sortedElements = sorted(self.elementsDict.values(),key=lambda x:x.name)
			gameMode.sortedElements = self.elementsDict.values()
			gameMode.sortedElements.sort(lambda x,y:x.name-y.name)
		return gameMode.sortedElements.__iter__()
#		return self.elementsDict.values().__iter__()
	def handleLeftClickDown(self,name):
		if(self.modal != None):
			if(self.elementsDict.has_key(name)):
				if(hasattr(self.elementsDict[name],"modal")):#only modalButton instances should have a modal attribute
					self.elementsDict[name].onClick()
				
		else:
			if(self.elementsDict.has_key(name)):
				self.setFocus(self.elementsDict[name])
				if(hasattr(self.elementsDict[name],"onClick")):
					self.elementsDict[name].onClick()
				elif(hasattr(self.elementsDict[name],"onLeftClickDown")):
					self.elementsDict[name].onLeftClickDown()
			else:
				self.setFocus(None)
	def handleLeftClickUp(self,name):
		if(self.modal == None):
			if(self.elementsDict.has_key(name)):
				if(hasattr(self.elementsDict[name],"onLeftClickUp")):
					self.elementsDict[name].onLeftClickUp()
				elif(hasattr(self.elementWithFocus,"onLeftClickUp")):
					self.elementWithFocus.onLeftClickUp()
	def handleKeyDown(self,keycode):
		if(keycode == "t" and False):
			print 'test'
		if(keycode == "y"):
			gameState.getGameMode().changeMap("Clay's Map")
		if(keycode == "u"):
			gameState.getGameMode().changeMap("test4")
		if(self.modal == None):
			if(hasattr(self,"keyDown")):
				self.keyDown(keycode)
			else:
				if(hasattr(self,"mousedOverObject") and hasattr(self.mousedOverObject,"onKeyDown")):
					self.mousedOverObject.onKeyDown(keycode)
				elif(hasattr(self.elementWithFocus,"onKeyDown")):
					self.elementWithFocus.onKeyDown(keycode)
	def handleKeyUp(self,keycode):
		if(keycode == "`"):
			if(hasattr(self,"clickScroll")):
				self.clickScroll = False
		if(self.modal == None):
			if(hasattr(self,"keyUp")):
				self.keyUp(keycode)
			else:
				if(hasattr(self.elementWithFocus,"onKeyUp")):
					self.elementWithFocus.onKeyUp(keycode)
	def setMouseTextPosition(self,position):
		self.mouseTextPosition = position
	def onQuit(self):
		if(gameState.getClient() != None):
			gameState.getClient().socket.close()
		server.shutdownServer()
	def onDraw(self):
		if(gameState.getClient() != None):
			if(hasattr(gameState.getClient(),"checkSocket")):
				gameState.getClient().checkSocket()
		if(gameState.getGameFindClient() != None):
			if(hasattr(gameState.getGameFindClient(),"checkSocket")):
				gameState.getGameFindClient().checkSocket()
			
class tiledGameMode(gameMode):
	def __init__(self,args=[]):
		self.mousedOverObject = None
		self.clickScroll = False
		gameMode.__init__(self)
	def handleRightClick(self,name):
		if(self.modal == None):
			rightClickable = False
			if(self.elementsDict.has_key(name)):
				if(hasattr(self.elementsDict[name],"onRightClick")):
					rightClickable = True
					self.elementsDict[name].onRightClick()
			if(hasattr(self,"selectedCityNode")):
				if(not rightClickable):
					self.selectedCityNode.selected = False
					self.selectedCityNode = None
	def handleRightClickUp(self,name):
		self.clickScroll = False
	def handleScrollUp(self,name,deltaTicks):
		if(self.modal == None):
			if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollUp")):
				self.elementsDict[name].onScrollUp()
			else:
				self.map.translateZ = self.map.translateZ + gameLogic.ZOOM_SPEED*deltaTicks;
				if(self.map.translateZ > (-10.0-cDefines.defines['minZoom'])):
					self.map.translateZ = -10.0-cDefines.defines['minZoom']
	def handleScrollDown(self,name,deltaTicks):
		if(self.modal == None):
			if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollDown")):
				self.elementsDict[name].onScrollDown()
			else:
				self.map.translateZ = self.map.translateZ - gameLogic.ZOOM_SPEED*deltaTicks;
				if(self.map.translateZ < (1.0-cDefines.defines['maxZoom'])):
					self.map.translateZ = 1.0-cDefines.defines['maxZoom']
	def handleMouseOver(self,name,isLeftMouseDown):
		if(self.modal != None):
			if(self.elementsDict.has_key(name)):
				if(hasattr(self.elementsDict[name],"modal")):#only modalButton should have am attribute 'modal'
					self.mousedOverObject = self.elementsDict[name]
		else:
			if(isLeftMouseDown > 0):#allows onLeftClickDown to be called for tiles when the mouse is dragged over them
				if(hasattr(gameState.getGameMode(),"selectedButton")):
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
	def __init__(self,args):
		self.units = []
		self.elementalEffects = []
		self.nextUnit = None
		self.focusNextUnit = 0
		self.focusNextUnitTemp = 0
		self.selectedNode = None
		tiledGameMode.__init__(self)
		self.shiftDown = False
		self.focusing = False
		self.blueWoodUIElem = None
		self.greenWoodUIElem = None
		self.players = []
		self.focusXPos = 0.0
		self.focusYPos = 0.0
	def loadMap(self):
		self.map = gameLogic.map(gameLogic.playModeNode)
	def getFocusNextUnit(self):
		return self.focusNextUnit
#		self.focusNextUnitTemp = self.focusNextUnit
#		self.focusNextUnit = 0
#		return self.focusNextUnitTemp
	def unitComparater(self,unit):
		if (unit.waiting or (unit.attackPoints > 0.0)):
			return 1000.0
		else:
			return unit.movementPoints
	def orderUnits(self):
		self.units.sort(key=self.unitComparater)
	def chooseNextUnit(self):
		winner = None
		for player in self.players:
			player.hasUnits = False
		for unit in self.units:
			self.players[unit.player-1].hasUnits = True
		for player in self.players:
			if(winner != None and player.hasUnits):
				winner = None
				break
			if(player.hasUnits):
				winner = player
		if(winner != None):
			print 'Winner: ' + winner.playerNumber
			return
		if(len(self.units) <= 1):
			   print 'DANGER, ONLY ONE UNIT ON THE BOARD, THE GAME SHOULD HAVE ENDED, THIS WILL CAUSE AN INFINITE LOOP'
			   return
		self.orderUnits()
		while(self.units[0].movementPoints > 0.0 or self.units[0].attackPoints > 0.0 or self.units[0].waiting):
			self.orderUnits()
			for elementalEffect in self.elementalEffects:
				elementalEffect.movePoints = elementalEffect.movePoints - elementalEffect.speed
#				print fire
			for unit in self.units:
				if(unit.unitType.name == "gatherer" and unit.gatheringNode == unit.node):
					if(unit.node.tileValue == cDefines.defines['FOREST_TILE_INDEX']):
						self.players[unit.player-1].greenWood = self.players[unit.player-1].greenWood + gameLogic.RESOURCE_COLLECTION_RATE
					elif(unit.node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX']):
						self.players[unit.player-1].blueWood = self.players[unit.player-1].blueWood + gameLogic.RESOURCE_COLLECTION_RATE
				if(unit.attackPoints > 0.0):
					unit.attackPoints = unit.attackPoints - unit.unitType.attackSpeed
				else:
#					if(unit.node.roadValue == 1):
#					unit.movementPoints = unit.movementPoints - 2.0
					if(unit.node.tileValue == cDefines.defines['MOUNTAIN_TILE_INDEX'] and not unit.unitType.canFly):
						unit.movementPoints = unit.movementPoints - ((float(unit.getMovementSpeed())+float(unit.node.roadValue))/cDefines.defines['MOUNTAIN_MOVE_COST'])
					elif(unit.node.tileValue == cDefines.defines['WATER_TILE_INDEX'] and not unit.unitType.canFly and not unit.unitType.canSwim):
						unit.movementPoints = unit.movementPoints - ((float(unit.getMovementSpeed())+float(unit.node.roadValue))/cDefines.defines['WATER_MOVE_COST'])
					elif(unit.node.tileValue == cDefines.defines['DESERT_TILE_INDEX'] and not unit.unitType.canFly):
						unit.movementPoints = unit.movementPoints - ((float(unit.getMovementSpeed())+float(unit.node.roadValue))/cDefines.defines['DESERT_MOVE_COST'])
					else:
						unit.movementPoints = unit.movementPoints - ((float(unit.getMovementSpeed())+float(unit.node.roadValue))/cDefines.defines['GRASS_MOVE_COST'])
					if(unit.movementPoints < 0.0):
						unit.movementPoints = 0.0#for waiting units
			for row in self.map.nodes:
				for node in row:
					if(node.city != None):
						node.city.incrementBuildProgress()
		#todo: sort fire and add while loop for when fire should go more than once before the next unit
		elementalEffectsMoving = True
		while(elementalEffectsMoving):
			elementalEffectsMoving = False
			for elementalEffect in self.elementalEffects:
				if(elementalEffect.movePoints < 0.0):
					elementalEffect.move()
					elementalEffectsMoving = True
		eligibleUnits = []
		eligibleUnits.append(self.units[0])
		for unit in self.units[1:]:
			if((unit.movementPoints == eligibleUnits[0].movementPoints) and (not unit.waiting) and (unit.attackPoints <= 0.0)):
				eligibleUnits.append(unit)
		self.nextUnit = random.choice(eligibleUnits)
		if(self.nextUnit.player == self.getPlayerNumber()):
			gameLogic.selectNode(self.nextUnit.node)
			self.focusXPos = self.nextUnit.node.xPos
			self.focusYPos = self.nextUnit.node.yPos
		self.focusNextUnit = 1
		if(hasattr(gameState.getGameMode().mousedOverObject,"toggleCursor")):
			gameState.getGameMode().mousedOverObject.toggleCursor()
	def onDoneFocusing(self):
		self.focusNextUnit = 0
		if(len(self.nextUnit.movePath) > 0 and gameState.getPlayers()[gameState.getGameMode().nextUnit.player-1].isOwnPlayer):
			self.nextUnit.move()
		elif(hasattr(gameState.getGameMode().mousedOverObject,"toggleCursor")):
			gameState.getGameMode().mousedOverObject.toggleCursor()
			
	def loadSummoners(self):
		rowCount = 0
		columnCount = 0
		for row in self.map.nodes:
			columnCount = 0
			rowCount = rowCount + 1
			for node in row:
				columnCount = columnCount + 1
				if(node.playerStartValue != 0):
					node.addUnit(gameLogic.unit(gameState.theUnitTypes["summoner"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["gatherer"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["gatherer"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["gatherer"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["swordsman"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["wolf"],node.playerStartValue,rowCount,columnCount,node,1))
					node.addUnit(gameLogic.unit(gameState.theUnitTypes["blue mage"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addFire(gameLogic.fire(node))
					node.addIce(gameLogic.ice(node))
	
	def keyDown(self,keycode):
		if(keycode == "left shift" or keycode == "right shift"):
			self.shiftDown = True
		if(keycode == "space"):
			gameLogic.selectNode(self.nextUnit.node)
			self.focusNextUnit = 1
		else:
			if(hasattr(self.mousedOverObject,"onKeyDown")):
				self.mousedOverObject.onKeyDown(keycode)
			elif(hasattr(self.elementWithFocus,"onKeyDown")):
				self.elementWithFocus.onKeyDown(keycode)

	def keyUp(self,keycode):
		if(keycode == "left shift" or keycode == "right shift"):
			self.shiftDown = False
		if(hasattr(self.mousedOverObject,"onKeyUp")):
			self.mousedOverObject.onKeyUp(keycode)
	def getPlayerNumber(self):#TODO: GET RID OF THIS ONCE AI IS DONE AND REPLACE WITH GAMESTATE VERSION
		number = gameState.getPlayerNumber()
		if(gameState.getPlayerNumber() == -2):
#			if(self.selectedNode != None and self.selectedNode.unit != None):
#				number = self.selectedNode.unit.player
#			else:
			number = self.nextUnit.player
		return number
	def onDraw(self):
		self.greenWoodUIElem.text = str(int(math.floor(self.players[self.getPlayerNumber()-1].greenWood)))
		self.blueWoodUIElem.text = str(int(math.floor(self.players[self.getPlayerNumber()-1].blueWood)))
		gameMode.onDraw(self)

	def addUIElements(self):
		if(gameState.getClient() == None):#single player game
			server.startServer('')
#			udpServer.startUdpServer()
#			client.startClient('127.0.0.1')
# 			client.startClient('192.168.0.102')
 			client.startClient('84.73.77.222')
#			udpClient.startUdpClient()
			gameState.setPlayerNumber(-2)
			gameState.addPlayer(1).isOwnPlayer = True
			gameState.addPlayer(2).isOwnPlayer = True
#		uiElements.uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=texHeight('UI_MAP_EDITOR_TOP_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_TOP'))
		uiElements.uiElement(xPos=-1.0,yPos=1.0-texHeight('UI_MAP_EDITOR_TOP_IMAGE'),width=texWidth('UI_MAP_EDITOR_LEFT_IMAGE'),height=texHeight('UI_MAP_EDITOR_LEFT_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_LEFT'))
#		uiElements.uiElement(xPos=1.0-texWidth('UI_MAP_EDITOR_RIGHT_IMAGE'),yPos=1.0-texHeight('UI_MAP_EDITOR_TOP_IMAGE'),width=texWidth('UI_MAP_EDITOR_RIGHT_IMAGE'),height=texHeight('UI_MAP_EDITOR_RIGHT_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_RIGHT'))
#		uiElements.uiElement(xPos=-1.0,yPos=-1.0+texHeight('UI_MAP_EDITOR_BOTTOM_IMAGE'),width=2.0,height=texHeight('UI_MAP_EDITOR_BOTTOM_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_BOTTOM'))
		self.players = gameState.getPlayers()
		self.greenWoodUIElem = uiElements.uiElement(0.80,0.93,text=str(self.players[0].greenWood),textSize=0.0005)
		self.blueWoodUIElem = uiElements.uiElement(0.90,0.93,text=str(self.players[0].blueWood),textSize=0.0005)
	def startGame(self):
		self.loadSummoners()
		self.orderUnits()
		self.chooseNextUnit()

class mapEditorMode(tiledGameMode):	
	def __init__(self,args):
		self.selectedButton = None
		self.selectedCityNode = None
		tiledGameMode.__init__(self)
	def loadMap(self):
		self.map = gameLogic.map(gameLogic.mapEditorNode)
	def keyDown(self,keycode):
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
		uiElements.uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=texHeight('UI_MAP_EDITOR_TOP_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_TOP'))
		uiElements.uiElement(xPos=-1.0,yPos=1.0-texHeight('UI_MAP_EDITOR_TOP_IMAGE'),width=texWidth('UI_MAP_EDITOR_LEFT_IMAGE'),height=texHeight('UI_MAP_EDITOR_LEFT_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_LEFT'))
		uiElements.uiElement(xPos=1.0-texWidth('UI_MAP_EDITOR_RIGHT_IMAGE'),yPos=1.0-texHeight('UI_MAP_EDITOR_TOP_IMAGE'),width=texWidth('UI_MAP_EDITOR_RIGHT_IMAGE'),height=texHeight('UI_MAP_EDITOR_RIGHT_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_RIGHT'))
		uiElements.uiElement(xPos=-1.0,yPos=-1.0+texHeight('UI_MAP_EDITOR_BOTTOM_IMAGE'),width=2.0,height=texHeight('UI_MAP_EDITOR_BOTTOM_IMAGE'),textureIndex=texIndex('UI_MAP_EDITOR_BOTTOM'))

		uiElements.mapEditorTileSelectUIElement(-0.93,0.92,tileType=cDefines.defines['DESERT_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.85,0.92,tileType=cDefines.defines['GRASS_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.77,0.92,tileType=cDefines.defines['MOUNTAIN_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.69,0.92,tileType=cDefines.defines['FOREST_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.61,0.92,tileType=cDefines.defines['BLUE_FOREST_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.53,0.92,tileType=cDefines.defines['WATER_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines.defines['ROAD_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.37,0.92,tileType=cDefines.defines['CITY_TILE_INDEX'])
		for col in range(0,2):
			for row in range(0,4):
				if((4*(col))+(row+1) <= self.map.numPlayers):

					uiElements.playerStartLocationButton(-0.31+(0.05*col),0.972-(0.038*row),playerNumber=col*4+row+1,width=2.0*cDefines.defines['PLAYER_START_BUTTON_WIDTH']/cDefines.defines['SCREEN_WIDTH'],height=2.0*cDefines.defines['PLAYER_START_BUTTON_HEIGHT']/cDefines.defines['SCREEN_HEIGHT'],textureIndex=cDefines.defines['PLAYER_START_BUTTON_INDEX'])
					uiElements.uiElement(-0.29+(0.05*col),0.948-(0.04*row),text=str((col*4)+row+1),textSize=0.0004)
				
		uiElements.mapEditorMapOptionsButton(-0.19,0.95,width=(2.0*cDefines.defines['MAP_ICON_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['MAP_ICON_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['MAP_ICON_INDEX'],cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'])

		uiElements.addColumnButton(0.96,0.03,text="+",textureIndex=cDefines.defines['ADD_BUTTON_INDEX'])
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
	def __init__(self,args):
		gameMode.__init__(self,args)
	def keyDown(self,keycode):
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
#		else:
#			if(hasattr(self.elementWithFocus,"onKeyDown")):
#				self.elementWithFocus.onKeyDown(keycode)

class newGameScreenMode(textBasedMenuMode):
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.menuButton(-0.18,-0.4,quickPlayMapSelectMode,text="Quick Play")
		uiElements.menuButton(-0.29,-0.52,multiplayerGameScreenMode,text="Play LAN Game")
		uiElements.menuButton(-0.19,-0.64,loginMode,text="Play Online")
		uiElements.menuButton(-0.19,-0.76,mapEditorSelectMode,text="Map Editor")

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
	def __init__(self,args):
		gameMode.__init__(self)
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.uiElement(-0.15,0.2,text="map name")
		self.mapNameInputElement = uiElements.newMapNameInputElement(-0.15,0.15,mapEditorMode,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text="",textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01)
		uiElements.uiElement(-0.15,0.0,text="number of players")
		self.mapPlayerCountInputElement = uiElements.newMapPlayerCountInputElement(-0.15,-0.05,mapEditorMode,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text="",textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01)


		self.setFocus(self.mapNameInputElement)
		uiElements.createMapButton(0.0,-0.3,mapEditorMode,text="create map")

class joinLANGameScreenMode(gameMode):
	def __init__(self,args):
		gameMode.__init__(self)
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])
		uiElements.uiElement(-0.15,0.2,text="Host IP Address")
		self.setFocus(uiElements.hostIPInputElement(-0.15,0.15,joiningLANGameScreenMode,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01))

class joiningLANGameScreenMode(gameMode):
	def __init__(self,args):
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
		self.mapNameElement = uiElements.uiElement(-0.85,-0.1,text="map")
		#uiElements.menuButton(-0.45,0.0,newGameScreenMode,text="back")

class hostLANGameScreenMode(gameMode):
	def __init__(self,args):
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
		server.startServer('')
		client.startClient('127.0.0.1')
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		uiElements.uiElement(-0.15,0.9,text="lan game")
		uiElements.uiElement(-0.85,0.8,text="players")
		uiElements.mapField(-0.85,-0.1,uiElements.mapSelector,text="choose map")
		uiElements.startButton(0.65,-0.8,playMode,text="start")

class gameRoomMode(gameMode):
	def __init__(self,args):
		gameMode.__init__(self)
		self.playerElementNames = []
		self.playerNames = []
	def removePlayerElements(self):
		for name in self.playerElementNames:
			del gameState.getGameMode().elementsDict[name]
		self.playerElementNames = []
		gameState.getGameMode().resortElems = True
#	def redrawPlayers(self):
#		self.removePlayerElements()
#		self.drawPlayers()
	def redrawPlayers(self):
		self.removePlayerElements()
		height = 0.55
		for playerName in self.playerNames:
			self.playerElementNames.append(uiElements.uiElement(-0.85,height,text=playerName).name)
			height = height - 0.1
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		uiElements.uiElement(-0.85,0.65,text="players")
		uiElements.startButton(0.65,-0.8,playMode,text="start")

class loginMode(gameMode):
	def __init__(self,args):
		gameMode.__init__(self)
		gameFindClient.startClient()
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		self.setFocus(uiElements.loginUserName(-0.12,0.0))
		uiElements.loginPassword(-0.12,-0.06)

class gameFindMode(gameMode):
	def __init__(self,args):
		self.roomName = args[0]
		self.rooms = []
		if(len(args) > 1):
			tokens = args[1].split('|')
			for token in tokens:
				self.rooms.append(tuple(token.split("-")))
		gameMode.__init__(self)
	def setMapName(self,mapName):
		self.mapName = mapName
		uiElements.uiElement(-0.15,0.9,text=mapName)
	def addUIElements(self):
#		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=texIndex("GAME_FIND_BACKGROUND"))
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=texIndex("UI_NEW_GAME_SCREEN"))
#cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		self.roomSelector = uiElements.roomSelector(-0.930,0.82,self.rooms,textSize=0.0005)
		self.chatDisplay = uiElements.chatDisplay(0.556,0.82)
		self.chatBox = uiElements.chatBox(0.556,-0.756,gameState.getGameFindClient())
		uiElements.sendChatButton(0.858,-0.82)
		self.setFocus(self.chatBox)
		uiElements.uiElement(-0.930,0.9,width=texWidth("BACK_BUTTON"),height=texHeight("BACK_BUTTON"),textureIndex=texIndex("BACK_BUTTON"))
		uiElements.da1v1Button(-0.930,-0.82)
		uiElements.da2v2Button(-0.840,-0.82)
		uiElements.da3v3Button(-0.750,-0.82)
		uiElements.da4v4Button(-0.660,-0.82)
		uiElements.createRoomButton(-0.930,-0.885)
		
class createGameMode(tiledGameMode):
	def __init__(self,args):
		tiledGameMode.__init__(self)
		self.createGameMode = True
		self.teamSize = 0
		self.mapSelector = None
		self.mapNameField = None
	def setMap(self,mapName):
		gameState.setMapName(mapName)
		self.map = gameLogic.map(gameLogic.mapViewNode,-60.0)
		if(self.mapNameField != None):
			self.mapNameField.destroy()
		if(self.mapSelector != None):
			self.mapSelector.destroy()
		self.mapNameField = uiElements.uiElement(-1.0+texWidth("CREATE_GAME_BACKGROUND_LEFT"),0.85,text="map name",fontIndex=3,textColor="ee ed 9b")
		self.mapSelector = uiElements.mapSelector(-0.93,1.0-texHeight("CREATE_GAME_BACKGROUND_TOP")+0.012,[],self.mapNameField)
		for mapData in gameState.getMapDatas()[self.teamSize-1]:
			gameState.getGameMode().mapSelector.textFields.append(uiElements.mapSelect(-0.93,0.0,gameState.getGameMode().mapSelector,mapData.name))
		gameState.getGameMode().mapSelector.redraw()
	def addUIElements(self):
		uiElements.uiElement(xPos=-1.0,yPos=1.0,width=texWidth("CREATE_GAME_BACKGROUND_TOP"),height=texHeight('CREATE_GAME_BACKGROUND_TOP'),textureIndex=texIndex('CREATE_GAME_BACKGROUND_TOP'))
		uiElements.uiElement(xPos=-1.0,yPos=1.0-texHeight('CREATE_GAME_BACKGROUND_TOP')+0.0018,width=texWidth("CREATE_GAME_BACKGROUND_LEFT"),height=texHeight('CREATE_GAME_BACKGROUND_LEFT'),textureIndex=texIndex('CREATE_GAME_BACKGROUND_LEFT'))
		uiElements.uiElement(xPos=1.0-texWidth("CREATE_GAME_BACKGROUND_RIGHT"),yPos=1.0-texHeight('CREATE_GAME_BACKGROUND_TOP'),width=texWidth("CREATE_GAME_BACKGROUND_RIGHT"),height=texHeight('CREATE_GAME_BACKGROUND_RIGHT'),textureIndex=texIndex('CREATE_GAME_BACKGROUND_RIGHT'))
		uiElements.uiElement(xPos=-1.0,yPos=-1.0+texHeight("CREATE_GAME_BACKGROUND_BOTTOM")+0.0034,width=2.0,height=texHeight('CREATE_GAME_BACKGROUND_BOTTOM'),textureIndex=texIndex('CREATE_GAME_BACKGROUND_BOTTOM'))


gameState.setGameMode(newGameScreenMode)

