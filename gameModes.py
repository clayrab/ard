#webpage
#SSL
#registration
#distribution
#general instructions page
#how to host instructions page

#server:
#*,|, and - cannot be allowed in roomnames
#record wins/losses
#report game state(to look for cheaters/bugs)

#ISSUES
#proper quit and options menus
#menu: resume, quit, help
#create email form/database table
#teams
#handle disconnections/reconnections gracefully
#draw roads properly
#map name clickable to view map
#keyboard shortcuts(s skip, a auto-select, g gather, u start summoning)
#testing connection timeout
#sound effects
#change selected node to white hex and next unit to a flag
#mouseover effects
#racial bonuses
#red wood/blue wood as resources. green wood for elf racial bonuses.
#show move speed and attack speed
#icons for green and blue wood
#healing animation

#BUGS
#replace open() on map files with mapdatas data
#sending " to chat as first character doesn't work... 
#fix py_decrefs in fonts.h
#make sure text edit boxes only allow chars and not shift/enter
#make sure room and/or map names do not contain *
#aStar heuristic is slowest possible heuristic(also finds ideal solution, but it's slow)

############# MINIMUM VIABLE PRODUCT AT THIS POINT ##############

#potential units:
#eagle. gains bonus vision range.
#giant eagle. gains bonus vision, has decent HP and attack.
#unit which 'becomes' a defensive structure and can't move like gatherer and summoner and auto-attacks
#unit could also drop mines and then become normal unit(like SC vulture)

#BONUS FEATURES
#sort room columns
#player rewards
#auto return view: after auto-scrolling to nextunit, return view to previous spot, player can turn this on/off with a checkbox in the UI.
#anti-alias text

#POLISH
#existing movePath and new movePath need to be distinguishable
#some C optimization inside drawTile() and maybe draw()... make lists, reduce mallocs in draw loop, etc
#move gameplay viewport back to entire window. make UI less intrusive, small elements at the corners, encircle map with mountains
#right-justifiable text
#add odd/even columns. i.e. every other column will get a new node with you hit +
#number keys auto-focus cities
#modals should be dismissed by esc, space, or enter

#BUGS
#send chat button should refocus chat box
#quickplay map selection only supports 10ish maps
#when you create a new map in map editor the player start location buttons are broken and cause crashes
#clicking playerstartlocation button #1 repeatedly causes a crash
#make zoomspeed(in main.c) and focusspeed non-framerate dependant
#map editor: nodes created after the ui render the ui unclickable since clicks go 'thru' to the new nodes
#check new/edited city names for duplicates
# + Buttons In map edit mode are wrong

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
import socket
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

sys.setrecursionlimit(10000)
#sys.setrecursionlimit(800)
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
		self.scrolledDistance = 0.0
		self.maxTranslateZ = 0.0-cDefines.defines["maxZoom"]
		uiElements.viewer.theViewer = None
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
		if(keycode == "t"):
			pass
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
#		gameLogic.aStarProcess.join()
		if(gameState.getClient() != None):
			gameState.getClient().socket.close()
		server.shutdownServer()
		gameLogic.aStarSearch.parentPipe.send(["kill"])#this causes the thread to quit
		gameLogic.aStarProcess.terminate()
		gameLogic.aStarProcess.join()
	def setMaxTranslateZ(self,transZ):
		if(transZ > self.maxTranslateZ):
			self.maxTranslateZ = transZ
		self.map.translateZ = transZ
	def onDraw(self,deltaTicks):
		if(self.scrolledDistance != 0.0):
			self.map.translateZ = self.map.translateZ + self.scrolledDistance*deltaTicks
			if(self.map.translateZ < (1.0-cDefines.defines['maxZoom'])):
				self.map.translateZ = 1.0-cDefines.defines['maxZoom']
			if(self.map.translateZ > (-10.0-cDefines.defines['minZoom'])):
				self.map.translateZ = -10.0-cDefines.defines['minZoom']
			if(self.map.translateZ < self.maxTranslateZ):
				self.map.translateZ = self.maxTranslateZ
		self.scrolledDistance = 0.0
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
		self.doFocus = 0
		self.doFocusTemp = 0
	def getFocusNextUnit(self):
		return self.doFocus
#		self.doFocusTemp = self.doFocus
#		self.doFocus = 0
#		return self.doFocusTemp
	def onDoneFocusing(self):
		self.doFocus = 0
		if(hasattr(self,"nextUnit") and self.nextUnit != None and len(self.nextUnit.movePath) > 0 and self.nextUnit.isControlled()):
			self.nextUnit.move()
#		elif(hasattr(self,"nextUnit") and hasattr(self,"autoSelect") and self.nextUnit != None and self.nextUnit.isControlled() and self.autoSelect):
#			gameLogic.selectNode(self.nextUnit.node)
		elif(hasattr(gameState.getGameMode().mousedOverObject,"toggleCursor")):
			gameState.getGameMode().mousedOverObject.toggleCursor()
			
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
	def handleScrollUp(self,name):
		if(self.modal == None):
			if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollUp")):
				self.elementsDict[name].onScrollUp()
			else:
				self.scrolledDistance = self.scrolledDistance + gameLogic.ZOOM_SPEED
	def handleScrollDown(self,name):
		if(self.modal == None):
			if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollDown")):
				self.elementsDict[name].onScrollDown()
			else:
				self.scrolledDistance = self.scrolledDistance - gameLogic.ZOOM_SPEED
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
		tiledGameMode.__init__(self)
		self.units = []
		self.elementalEffects = []
		self.nextUnit = None
		self.selectedNode = None
		self.shiftDown = False
		self.focusing = False
		self.blueWoodUIElem = None
		self.greenWoodUIElem = None
		self.players = []
		self.focusXPos = 0.0
		self.focusYPos = 0.0
		self.chooseNextDelayed = False
		#self.backgroundImageIndex = texIndex("CREATE_GAME_BACKGROUND")
		self.ticks = 0#set in main.c
		self.previousTicks = 0
		self.timeToMove = 60000
		self.firstTurn = True
		self.autoSelect = False
	def getChooseNextDelayed(self):
		if(self.chooseNextDelayed):
			retVal = self.chooseNextDelayed
			self.chooseNextDelayed = False
			return retVal
		else:
			return False
	def sendChooseNextUnit(self):
		gameState.getClient().sendCommand("chooseNextUnit")
	def loadMap(self):
		self.map = gameLogic.mapp(gameLogic.playModeNode)
		gameLogic.aStarSearch.parentPipe.send(['map',gameState.getMapName()])
	def unitComparater(self,unit):
		if (unit.waiting or unit.isMeditating or (unit.attackPoints > 0.0)):
			return 1000.0
		else:
			return unit.movementPoints
	def orderUnits(self):
		self.units.sort(key=self.unitComparater)
	def chooseNextUnit(self):
		winner = None
		for player in self.players:
			player.hasSummoners = False
		for unit in self.units:
			if(unit.unitType.name == "summoner"):
				self.players[unit.player-1].hasSummoners = True
		for player in self.players:
			if(winner != None and player.hasSummoners):
				winner = None
				break
			if(player.hasSummoners):
				winner = player
		if(winner != None):
			if(gameState.getPlayerNumber() == winner.playerNumber):
				uiElements.winModal()
			else:
				uiElements.loseModal()
			return
		if(len(self.units) <= 1):
			   print 'ERROR: ONLY ONE UNIT ON THE BOARD, THE GAME SHOULD HAVE ENDED, THIS WILL CAUSE AN INFINITE LOOP'
			   return
		self.orderUnits()
		while(self.units[0].movementPoints > 0.0 or self.units[0].attackPoints > 0.0):
# or self.units[0].waiting or self.units[0].isMeditating):
			self.orderUnits()
			for elementalEffect in self.elementalEffects:
				elementalEffect.movePoints = elementalEffect.movePoints - elementalEffect.speed
#				print fire
			for unit in self.units:
				if(unit.unitType.name == "gatherer" and unit.isMeditating and (unit.node.tileValue == cDefines.defines['FOREST_TILE_INDEX'] or unit.node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX'])):
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
						unit.movementPoints = 0.0#for waiting/meditating units
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
#		eligibleUnits.append(self.units[0])
		for unit in self.units:
			if(len(eligibleUnits) > 0):
				if((unit.movementPoints == eligibleUnits[0].movementPoints) and (not unit.waiting) and (not unit.isMeditating) and (unit.attackPoints <= 0.0)):
					eligibleUnits.append(unit)
			else:
				if(unit.movementPoints <= 0.0 and unit.attackPoints <= 0.0 and not unit.waiting and not unit.isMeditating):
					eligibleUnits.append(unit)

		if(len(eligibleUnits) == 0):#all units are waiting/meditating!!!
			for unit in self.units:#add movementpoints to each unit
				#unit.movementPoints = unit.movementPoints + (gameLogic.INITIATIVE_ACTION_DEPLETION/5.0)
				unit.skip()
			if(gameState.getPlayerNumber() <= 1):
				self.chooseNextDelayed = True
			self.nextUnit = None
		else:
			self.nextUnit = random.choice(eligibleUnits)
			if(self.firstTurn):
				if(self.nextUnit.isControlled()):
					gameLogic.selectNode(self.nextUnit.node)
					self.focusXPos = self.nextUnit.node.xPos
					self.focusYPos = self.nextUnit.node.yPos
					self.doFocus = 1
				else:
					for unit in self.units:
						if(unit.unitType.name == "summoner" and unit.isControlled()):
							gameLogic.selectNode(unit.node)
							self.focusXPos = unit.node.xPos
							self.focusYPos = unit.node.yPos
							self.doFocus = 1
							break
				self.firstTurn = False
			else:
				if(self.autoSelect and self.nextUnit.isControlled()):
					gameLogic.selectNode(self.nextUnit.node)
					self.focusXPos = self.nextUnit.node.xPos
					self.focusYPos = self.nextUnit.node.yPos
					self.doFocus = 1
				elif(len(self.nextUnit.movePath) > 0 and self.nextUnit.isControlled()):
					self.focusXPos = self.nextUnit.node.xPos
					self.focusYPos = self.nextUnit.node.yPos
					self.doFocus = 1				
			if(hasattr(gameState.getGameMode().mousedOverObject,"toggleCursor")):
				gameState.getGameMode().mousedOverObject.toggleCursor()
		if(self.nextUnit != None and self.nextUnit.isControlled()):
			self.waitingElem.hidden = True
			self.timeToMove = self.timeToMove + 5000
			if(self.timeToMove > 60000):
				self.timeToMove = 60000
		else:
			self.waitingElem.hidden = False
		if(gameState.getGameMode().selectedNode != None and uiElements.viewer.theViewer != None):
			if(hasattr(uiElements.viewer.theViewer,"isCityViewer")):
				uiElements.viewer.theViewer.destroy()
				uiElements.viewer.theViewer = uiElements.cityViewer(gameState.getGameMode().selectedNode)
			elif(gameState.getGameMode().selectedNode.unit != None):
				uiElements.viewer.theViewer.destroy()
				uiElements.viewer.theViewer = uiElements.unitViewer(gameState.getGameMode().selectedNode)
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
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["dragon"],node.playerStartValue,rowCount,columnCount,node,1))
					node.addUnit(gameLogic.unit(gameState.theUnitTypes["gatherer"],node.playerStartValue,rowCount,columnCount,node,1))
					node.addUnit(gameLogic.unit(gameState.theUnitTypes["gatherer"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["gatherer"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["gatherer"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["swordsman"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["wolf"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["blue mage"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["white mage"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["red mage"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addUnit(gameLogic.unit(gameState.theUnitTypes["archer"],node.playerStartValue,rowCount,columnCount,node,1))
#					node.addFire(gameLogic.fire(node))
#					node.addIce(gameLogic.ice(node))
	
	def keyDown(self,keycode):
		if(keycode == "left shift" or keycode == "right shift"):
			self.shiftDown = True
		if(keycode == "space"):
			if(self.nextUnit != None):
				gameLogic.selectNode(self.nextUnit.node)
				self.focusXPos = self.nextUnit.node.xPos
				self.focusYPos = self.nextUnit.node.yPos
				self.doFocus = 1
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
			if(self.nextUnit != None):
				number = self.nextUnit.player
			else:
				number = 1
		return number
	def onDraw(self,deltaTicks):
#		with gameLogic.aStarSearch.searchCompleteLock:
#		print 'astarseach:' + str(gameLogic.aStarSearch)
#		print gameLogic.aStarSearch.map
		
		if(gameLogic.aStarSearch.searchComplete):
			with gameLogic.aStarSearch.aStarLock:
				gameLogic.playModeNode.movePath = []
				for node in gameLogic.aStarSearch.movePath:
					gameLogic.playModeNode.movePath.append(node)
					node.onMovePath = True
				gameLogic.aStarSearch.searchComplete = False
				gameLogic.aStarSearch.movePath = []
		if(gameLogic.aStarSearch.parentPipe.poll()):
			for node in gameLogic.playModeNode.movePath:
				node.onMovePath = False
			gameLogic.playModeNode.movePath = []
			data = gameLogic.aStarSearch.parentPipe.recv()
			for arr in data:
				node = gameState.getGameMode().map.nodes[arr[1]][arr[0]]
				gameLogic.playModeNode.movePath.append(node)
				node.onMovePath = True
		if(self.timeToMove <= 0 and self.nextUnit != None and self.nextUnit.isControlled()):
			gameState.getClient().sendCommand("skip")
			gameState.getClient().sendCommand("chooseNextUnit")
			self.nextUnit = None
		self.greenWoodUIElem.text = str(int(math.floor(self.players[self.getPlayerNumber()-1].greenWood)))
		self.blueWoodUIElem.text = str(int(math.floor(self.players[self.getPlayerNumber()-1].blueWood)))
		if(self.previousTicks != 0 and self.nextUnit != None and self.nextUnit.isControlled()):
			self.timeToMove = self.timeToMove - (self.ticks - self.previousTicks)
		self.timeToMoveElem.text = "{0:.2f}".format(self.timeToMove/1000.0)
		self.previousTicks = self.ticks		
		gameMode.onDraw(self,deltaTicks)

	def addUIElements(self):
		if(gameState.getClient() == None):#single player game
			server.startServer('')
			client.startClient('127.0.0.1')
# 			client.startClient('192.168.0.102')
# 			client.startClient('84.73.77.222')
			gameState.setPlayerNumber(-2)
			gameState.addPlayer(1).isOwnPlayer = True
			gameState.addPlayer(2).isOwnPlayer = True
		self.players = gameState.getPlayers()

		uiElements.uiElement(0.635,0.965,textureIndex=texIndex("TIME_ICON"),width=texWidth("TIME_ICON"),height=texHeight("TIME_ICON"))
		self.timeToMoveElem = uiElements.uiElement(0.659,0.942,text="",textSize=0.00045)
		uiElements.uiElement(0.755,0.965,textureIndex=texIndex("GREEN_WOOD_ICON"),width=texWidth("GREEN_WOOD_ICON"),height=texHeight("GREEN_WOOD_ICON"))
		self.greenWoodUIElem = uiElements.uiElement(0.779,0.942,text=str(self.players[0].greenWood),textSize=0.00045)
		uiElements.uiElement(0.875,0.965,textureIndex=texIndex("BLUE_WOOD_ICON"),width=texWidth("BLUE_WOOD_ICON"),height=texHeight("BLUE_WOOD_ICON"))
		self.blueWoodUIElem = uiElements.uiElement(0.899,0.942,text=str(self.players[0].blueWood),textSize=0.00045)

		self.waitingElem = uiElements.uiElement(-0.2,0.93,text="waiting for another player",textColor="ee ed 9b",textSize=0.00055,hidden=True)

		uiElements.uiElement(0.718,-0.932,textureIndex=texIndex("CHECKBOXES_BACKGROUND"),width=texWidth("CHECKBOXES_BACKGROUND"),height=texHeight("CHECKBOXES_BACKGROUND"))
		uiElements.autoSelectCheckBox(0.735,-0.94)
#		uiElements.watchFriendlyMovesCheckBox(0.455,-0.94)
#		uiElements.watchEnemyMovesCheckBox(0.675,-0.94)

	def startGame(self):
		self.loadSummoners()
		for unit in self.units:
			if(unit.node.visible):
				gameLogic.aStarSearch.parentPipe.send(["unitAdd",unit.node.xPos,unit.node.yPos])
		self.orderUnits()
		self.chooseNextUnit()

class mapEditorMode(tiledGameMode):	
	def __init__(self,args):
		self.selectedButton = None
		self.selectedCityNode = None
		tiledGameMode.__init__(self)
	def loadMap(self):
		self.map = gameLogic.mapp(gameLogic.mapEditorNode)
		self.focusXPos = int(len(self.map.nodes[0])/2)
		self.focusYPos = int(len(self.map.nodes)/2)
		self.doFocus = 1
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

		uiElements.uiElement(-0.50,0.98,textureIndex=texIndex("UI_CITY_EDITOR_BACKGROUND_BACKGROUND"),height=0.12,width=0.7)
		uiElements.mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines.defines['DESERT_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.37,0.92,tileType=cDefines.defines['GRASS_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.29,0.92,tileType=cDefines.defines['MOUNTAIN_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.21,0.92,tileType=cDefines.defines['FOREST_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.13,0.92,tileType=cDefines.defines['BLUE_FOREST_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(-0.05,0.92,tileType=cDefines.defines['WATER_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(0.03,0.92,tileType=cDefines.defines['ROAD_TILE_INDEX'])
		uiElements.mapEditorTileSelectUIElement(0.11,0.92,tileType=cDefines.defines['CITY_TILE_INDEX'])
		for col in range(0,2):
			for row in range(0,4):
				if((4*(col))+(row+1) <= self.map.numPlayers):

					uiElements.playerStartLocationButton(0.17+(0.05*col),0.972-(0.038*row),playerNumber=col*4+row+1,width=2.0*cDefines.defines['PLAYER_START_BUTTON_WIDTH']/cDefines.defines['SCREEN_WIDTH'],height=2.0*cDefines.defines['PLAYER_START_BUTTON_HEIGHT']/cDefines.defines['SCREEN_HEIGHT'],textureIndex=cDefines.defines['PLAYER_START_BUTTON_INDEX'])
					uiElements.uiElement(0.19+(0.05*col),0.948-(0.04*row),text=str((col*4)+row+1),textSize=0.0004)
				
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
		uiElements.uiElement(-0.5*texWidth("TITLE"),0.35,textureIndex=texIndex("TITLE"),width=texWidth("TITLE"),height=texHeight("TITLE"))
		uiElements.menuButton(-0.18,-0.48,quickPlayMapSelectMode,text="Quick Play")
		uiElements.menuButton(-0.28,-0.58,joinLANGameScreenMode,text="Join LAN Game")
		uiElements.menuButton(-0.30,-0.70,hostGameMode,text="Host LAN Game")
		uiElements.menuButton(-0.19,-0.82,loginMode,text="Play Online")
		uiElements.menuButton(-0.19,-0.94,mapEditorSelectMode,text="Map Editor")

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
		uiElements.uiElement(-0.15,0.165,text="Host IP Address",textSize=0.0007,textColor="ee ed 9b")
		self.hostIPInputElem = uiElements.hostIPInputElement(-0.15,0.15)
		self.setFocus(self.hostIPInputElem)
		uiElements.hostIPConnectButton(-0.15,0.07)

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
#		server.startServer('')
#		client.startClient('127.0.0.1')
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		uiElements.uiElement(-0.15,0.9,text="lan game")
		uiElements.uiElement(-0.85,0.8,text="players")
		uiElements.mapField(-0.85,-0.1,uiElements.mapSelector,text="choose map")
		uiElements.startButton(0.65,-0.8,playMode,text="start")

class loginMode(gameMode):
	def __init__(self,args):
		gameMode.__init__(self)
			
	def addUIElements(self):
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		self.setFocus(uiElements.loginUserName(-0.12,0.02))
		uiElements.loginPassword(-0.12,-0.06)
		uiElements.loginButton(-0.12,-0.14)
		try:
			gameFindClient.startClient()
		except socket.error:
			gameState.setGameMode(newGameScreenMode)
			uiElements.smallModal("Cannot connect to server.")

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
	def roomCountUpdate(self,roomName,subscriberCount,teamSize):
		for elem in self.roomSelector.textFields:
			if(elem.roomNameElem.text == roomName):
				elem.roomCountElem.text = subscriberCount + "/" + str(2*int(teamSize))
				break
	def addUIElements(self):
#		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=texIndex("GAME_FIND_BACKGROUND"))
		uiElements.uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=texIndex("UI_NEW_GAME_SCREEN"))
#cDefines.defines['UI_NEW_GAME_SCREEN_INDEX'])	
		self.roomSelector = uiElements.roomSelector(-0.930,0.82,self.rooms,textSize=0.0005)
		self.chatDisplay = uiElements.chatDisplay(0.556,0.82)
		self.chatBox = uiElements.chatBox(0.556,-0.738,gameState.getGameFindClient())
		uiElements.sendChatButton(0.858,-0.82)
		self.setFocus(self.chatBox)
		uiElements.da1v1Button(-0.930,-0.82)
		uiElements.da2v2Button(-0.840,-0.82)
		uiElements.da3v3Button(-0.750,-0.82)
		uiElements.da4v4Button(-0.660,-0.82)
		uiElements.createRoomButton(-0.930,-0.885)
		
class joinGameMode(tiledGameMode):
	def __init__(self,args):
		tiledGameMode.__init__(self)
		self.roomName = args[0]
		self.mapName = args[1]
		self.hostIP = args[2]
		self.hostPort = int(args[3])
		self.teamSize = int(args[4])
		self.joinGameMode = True
		self.backgroundImageIndex = texIndex("JOIN_GAME_BACKGROUND")
		self.selectedNode = None
		self.playerElements = []
	def addPlayer(self,playerName):
		for elem in self.playerElements:
			if(elem.text == "empty"):
				elem.text = playerName
				elem.textColor = "FF FF FF"
				elem.mouseOverColor = "FF FF FF"
				break
	def removePlayer(self,playerName):
		previousElem = None
		self.playerElements[len(self.playerElements)-1].text = "empty"
		self.playerElements[len(self.playerElements)-1].textColor = "55 55 55"
		self.playerElements[len(self.playerElements)-1].mouseOverColor = "55 55 55"
		for elem in self.playerElements[:len(self.playerElements)-1]:
			if(previousElem != None):
				previousElem.text = elem.text
				if(elem.text == "empty"):
					previousElem.textColor = "55 55 55"
					previousElem.mouseOverColor = "55 55 55"
				else:
					previousElem.textColor = "ff ff ff"
					previousElem.mouseOverColor = "ff ff ff"
			if(elem.text == playerName):
				previousElem = elem
	def setMap(self,mapName):
		self.maxTranslateZ = 0.0-cDefines.defines["maxZoom"]
		gameState.setMapName(mapName)
		self.map = gameLogic.mapp(gameLogic.mapViewNode,-50.0)
		self.mapNameElem.text = mapName
		self.focusXPos = int(len(self.map.nodes[0])/2)
		self.focusYPos = int(len(self.map.nodes)/2)
		self.doFocus = 1
	def addUIElements(self):
#		uiElements.uiElement(0.0,0.9,text=gameState.getMapName())
		self.mapNameElem = uiElements.uiElement(0.0,0.9,text="")
		uiElements.backButton(-0.930,0.9)
		uiElements.uiElement(0.35,0.813,width=texWidth("JOIN_GAME_PLAYERS"),height=texHeight("JOIN_GAME_PLAYERS"),textureIndex=texIndex("JOIN_GAME_PLAYERS"))
		self.chatDisplay = uiElements.chatDisplay(0.35,0.4,textureName="JOIN_GAME_CHAT")
		self.chatBox = uiElements.chatBox(0.35,-0.514,gameState.getClient(),textureName="JOIN_GAME_CHAT_BOX")
		uiElements.sendChatButton(0.842,-0.595)
		for i in range(0,2*self.teamSize):
			self.playerElements.append(uiElements.uiElement(0.36,0.775-(0.033*i),text="empty",textSize=0.0005,textColor="55 55 55",mouseOverColor="55 55 55"))
		if(gameState.getClient() == None):#host connects to itself early at 127.0.0.1
			try:
				client.startClient(self.hostIP,self.hostPort)
			except socket.error:
				uiElements.lanConnectErrorModal()
				return
		else:
			uiElements.startGameButton(0.795,0.504)

class joinLANGameMode(joinGameMode):
	def __init__(self,args):
		if(len(args) == 0):
			joinGameMode.__init__(self,["LAN game","map name","127.0.0.1","6666","1"])
		else:
			joinGameMode.__init__(self,["LAN game","map name",args[0],"6666","1"])

	
class createGameMode(tiledGameMode):
	def __init__(self,args):
		tiledGameMode.__init__(self)
		self.createGameMode = True
		self.teamSize = 1
		self.mapSelector = None
		self.backgroundImageIndex = texIndex("CREATE_GAME_BACKGROUND")
		self.selectedNode = None
	def setMap(self,mapName):
		gameState.setMapName(mapName)
		if(self.map != None):
			self.map = gameLogic.mapp(gameLogic.mapViewNode,self.map.translateZ)
		else:
			self.map = gameLogic.mapp(gameLogic.mapViewNode,-50.0)			
		self.maxTranslateZ = 0.0-cDefines.defines["maxZoom"]
		if(self.mapSelector != None):
			self.mapSelector.destroy()
		self.mapNameField.text = mapName
		if(hasattr(self,"roomNameField")):
			self.roomNameField.setText(gameState.getUserName() + "'s " + str(self.teamSize) + "v" + str(self.teamSize) + "(" + mapName + ")")
		self.mapSelector = uiElements.mapSelector(-0.93,0.813,[],self.mapNameField)
		for mapData in gameState.getMapDatas()[self.teamSize-1]:
			gameState.getGameMode().mapSelector.textFields.append(uiElements.mapSelect(-0.93,0.0,gameState.getGameMode().mapSelector,mapData.name))
		gameState.getGameMode().mapSelector.redraw()
		self.focusXPos = int(len(self.map.nodes[0])/2)
		self.focusYPos = int(len(self.map.nodes)/2)
		self.doFocus = 1
	def addUIElements(self):
		self.mapNameField = uiElements.uiElement(-1.0+texWidth("CREATE_GAME_BACKGROUND_LEFT"),0.85,fontIndex=3,textColor="ee ed 9b")
		self.roomNameField = uiElements.textInputElement(0.31,-0.616)
		uiElements.createGameButton(0.717,-0.616)		
		uiElements.backButton(-0.930,0.9)

class hostGameMode(createGameMode):
	def __init__(self,args):
		createGameMode.__init__(self,args)
		self.hostGameMode = True
		self.createGameMode = True
	def addUIElements(self):
		self.mapNameField = uiElements.uiElement(-1.0+texWidth("CREATE_GAME_BACKGROUND_LEFT"),0.85,fontIndex=3,textColor="ee ed 9b")
		uiElements.backButtun(-0.930,0.9,newGameScreenMode)
		uiElements.createGameButtun(0.717,-0.616)		
		uiElements.da1v1Button(-0.710,0.9,offColor="AA AA AA")
		uiElements.da2v2Button(-0.620,0.9,offColor="AA AA AA")
		uiElements.da3v3Button(-0.530,0.9,offColor="AA AA AA")
		uiElements.da4v4Button(-0.440,0.9,offColor="AA AA AA")
		gameState.getGameMode().setMap(gameState.getMapDatas()[0][0].name)

gameState.setGameMode(newGameScreenMode)
