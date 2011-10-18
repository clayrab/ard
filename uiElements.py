import os
import copy
import gameState
import gameLogic
import nameGenerator
import cDefines
import shutil
import client
import server
from textureFunctions import texWidth, texHeight, texIndex

cityCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
unitCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
startingManas = ["5","10","15","20","30","40","50","60","70","80","90","100"]
unitBuildTimes = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]


class uiElement:
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor=None,textSize=0.001,color=None,mouseOverColor=None,textXPos=0.0,textYPos=0.0):
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
		self.textXPos = textXPos
		self.textYPos = textYPos
		if(mouseOverColor != None):
			self.mouseOverColor = mouseOverColor
		elif(color != None):
			self.mouseOverColor = color
		elif(textColor != None):
			self.mouseOverColor = textColor
		else:
			self.mouseOverColor = "FF FF FF"
		if(self.color == None):
			self.color = "FF FF FF"
		if(self.textColor == None):
			self.textColor = "FF FF FF"
		gameState.getGameMode().elementsDict[self.name] = self
		gameState.getGameMode().resortElems = True
	def onScrollDown(self):
		return None
	def onScrollUp(self):
		return None


class clickableElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)

class saveButton(clickableElement):	
	def onClick(self):
		gameState.getGameMode().map.save()

#TODO: MAKE SURE YOU CAN'T REMOVE THE LAST ROW OR COLUMN!!
class addColumnButton(clickableElement):
	def onClick(self):
		for row in gameState.getGameMode().map.nodes:
			row.append(gameLogic.mapEditorNode(0,0))

class removeColumnButton(clickableElement):
	def onClick(self):
		for row in gameState.getGameMode().map.nodes:
			row.pop()

class addFirstColumnButton(clickableElement):
	def onClick(self):
		for count in range(0,len(gameState.getGameMode().map.nodes)):
			rowCopy = gameState.getGameMode().map.nodes[count][:]
			rowCopy.reverse()
			rowCopy.append(gameLogic.mapEditorNode(0,0))
			rowCopy.reverse()
			gameState.getGameMode().map.nodes[count] = rowCopy

class removeFirstColumnButton(clickableElement):
	def onClick(self):
		for count in range(0,len(gameState.getGameMode().map.nodes)):
			rowCopy = gameState.getGameMode().map.nodes[count][:]
			rowCopy.reverse()
			rowCopy.pop()
			rowCopy.reverse()
			gameState.getGameMode().map.nodes[count] = rowCopy

class addRowButton(clickableElement):
	def onClick(self):
		newRow = []
		for count in range(0,len(gameState.getGameMode().map.nodes[0])):
			newRow.append(gameLogic.mapEditorNode(0,0))
		gameState.getGameMode().map.nodes.append(newRow)

class removeRowButton(clickableElement):
	def onClick(self):
		gameState.getGameMode().map.nodes.pop()

class addFirstRowButton(clickableElement):
	def onClick(self):
		nodesCopy = gameState.getGameMode().map.nodes[:]
		newRow = []
		for count in range(0,len(gameState.getGameMode().map.nodes[0])):
			newRow.append(gameLogic.mapEditorNode(0,0))
		nodesCopy.reverse()
		nodesCopy.append(newRow)
		nodesCopy.reverse()
		gameState.getGameMode().map.polarity = (~gameState.getGameMode().map.polarity)&1
		gameState.getGameMode().map.nodes = nodesCopy

class removeFirstRowButton(clickableElement):
	def onClick(self):
		nodesCopy = gameState.getGameMode().map.nodes[:]
		nodesCopy.reverse()
		nodesCopy.pop()
		nodesCopy.reverse()
		gameState.getGameMode().map.polarity = (~gameState.getGameMode().map.polarity)&1
		gameState.getGameMode().map.nodes = nodesCopy

class textInputElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
	def onKeyDown(self,keycode):
		if(keycode == "backspace"):
			self.text = self.text.rstrip(self.text[len(self.text)-1])
		elif(keycode == "space"):
			self.text = self.text + " "
		else:
			self.text = self.text + keycode

class cityNameInputElement(textInputElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
	def onKeyDown(self,keycode):
		textInputElement.onKeyDown(self,keycode)
		cityEditor.theCityEditor.city.name = self.text

class newMapNameInputElement(textInputElement):
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
		self.gameMode = gameMode
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			if(len(self.text) > 0):
				shutil.copyfile("maps/defaultMap","maps/" + self.text + ".map")
				gameState.setMapName(self.text)
				gameState.setGameMode(self.gameMode)
		else:
			textInputElement.onKeyDown(self,keycode)

class hostIPInputElement(textInputElement):
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,text="192.168.1.5",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
		self.gameMode = gameMode
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			if(len(self.text) > 0):
				gameState.setGameMode(self.gameMode)
				gameState.setHostIP(self.text)
				client.startClient(self.text)
		else:
			textInputElement.onKeyDown(self,keycode)

class startSummoningButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		gameState.getClient().sendCommand("startSummoning " + str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.movePath[0].yPos) + " " + self.unitType.name + "|")

class cancelUnitButton(clickableElement):
       	def __init__(self,xPos,yPos,node,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.node = node
	def onClick(self):
		if(len(self.node.city.unitBuildQueue) > 0):
			self.node.city.unitBuildQueue.pop()
		elif(self.node.city.unitBeingBuilt != None):
			self.node.city.unitBeingBuilt = None
		actionViewer.theActionViewer.reset()

class startResearchButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
#		self.node = node
	def onClick(self):
		actionViewer.theActionViewer.node.city.researching = True
		actionViewer.theActionViewer.node.city.researchUnitType = self.unitType
		actionViewer.theActionViewer.node.unit.unitAction = gameLogic.unitAction.WAIT
		actionViewer.theActionViewer.node.unit.moveTo(actionViewer.theActionViewer.node)
		gameState.getGameMode().chooseNextUnit()

class viewResearchButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,node,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
		self.node = node
	def onClick(self):
		unitTypeResearchViewer.destroy()
		unitTypeResearchViewer.theUnitTypeResearchViewer = unitTypeResearchViewer(self.unitType)

class viewUnitTypeButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		unitTypeBuildViewer.destroy()
		unitTypeBuildViewer.theUnitTypeBuildViewer = unitTypeBuildViewer(self.unitType)

class stopWaitingButton(clickableElement):
	def onClick(self):
		actionViewer.theActionViewer.node.unit.unitAction = gameLogic.unitAction.MOVE
		unitViewer.reset()

class attackButton(clickableElement):
	def onClick(self):
		actionViewer.theActionViewer.node.unit.unitAction = gameLogic.unitAction.ATTACK
		unitViewer.reset()

class waitButton(clickableElement):
	def onClick(self):
		actionViewer.theActionViewer.node.unit.unitAction = gameLogic.unitAction.WAIT
		gameState.getGameMode().chooseNextUnit()

class skipButton(clickableElement):
       	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
	def onClick(self):
		if(gameState.getGameMode().nextUnit.player == gameState.getPlayerNumber() or gameState.getPlayerNumber() == -1):
			gameState.getClient().sendCommand("nodeClick " + str(gameState.getGameMode().nextUnit.node.xPos) + " " + str(gameState.getGameMode().nextUnit.node.yPos) + "|")
#		unitViewer.reset()

class actionViewer(uiElement):
	theActionViewer = None
	def __init__(self,node,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.node = node
		self.names = []
		self.names.append(uiElement(-0.978,-0.085,textureIndex=texIndex('CITY_VIEWER_BOX'),width=texWidth('CITY_VIEWER_BOX'),height=texHeight('CITY_VIEWER_BOX'),textSize=0.0007).name)
		self.names.append(uiElement(-0.964,-0.13,text=self.node.city.name,textSize=0.0007).name)
		if(self.node.city.researching):
			self.names.append(uiElement(-0.964,-0.19,text="researching",textSize=0.0005).name)
			self.names.append(uiElement(-0.964,-0.23,text=self.node.city.researchUnitType.name,textSize=0.0005).name)
			self.names.append(uiElement(-0.964,-0.25,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
			self.names.append(uiElement(-0.964,-0.25,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(float(self.node.city.researchProgress)/gameLogic.researchBuildTime),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
			if(self.node.city.researchLevel > 0):
				self.names.append(uiElement(-0.964,-0.32,text="level "+str(self.node.city.researchLevel) + " complete",textSize=0.0005).name)
				self.names.append(startResearchButton(-0.964,-0.89,self.node.city.researchUnitType,text="research level " + str(self.node.city.researchLevel+1),textSize=0.0005).name)
		elif(self.node.city.unitBeingBuilt != None):
			self.names.append(uiElement(-0.972,-0.19,text=self.node.city.unitBeingBuilt.unitType.name,textSize=0.0005).name)
			self.names.append(uiElement(-0.972,-0.21,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
			self.names.append(uiElement(-0.972,-0.21,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(self.node.city.unitBeingBuilt.unitType.buildTime-self.node.city.unitBeingBuilt.buildPoints)/self.node.city.unitBeingBuilt.unitType.buildTime,textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
			height = -0.25
			for unit in self.node.city.unitBuildQueue:
				height = height - 0.04
				self.names.append(uiElement(-0.972,height,text=str(unit.unitType.name),textSize=0.0005).name)
		elif(not self.node.city.doneResearching):
			self.names.append(uiElement(-0.88,-0.19,text="research",textSize=0.0005).name)
			if(self.node.city.researchLevel > 0):
				self.names.append(viewResearchButton(-0.964,-0.25,self.node.city.researchUnitType,self.node,text=self.node.city.researchUnitType.name + " lvl " + str(self.node.city.researchLevel+1),textSize=0.0005).name)
			else:
				height = -0.25
				for unitType in self.node.city.unitTypes:
					if(unitType.name != "summoner" and unitType.name != "gatherer"): 
						self.names.append(viewResearchButton(-0.964,height,unitType,self.node,text=unitType.name,textSize=0.0005).name)
						self.names.append(uiElement(-0.72,height,text=str(unitType.cost),textSize=0.0005).name)
						height = height - 0.04
		self.names.append(uiElement(-0.88,-0.51,text="summon",textSize=0.0005).name)
		self.names.append(viewUnitTypeButton(-0.94,-0.55,gameState.theUnitTypes["gatherer"],text="gatherer",textSize=0.0005).name)
		if(self.node.unit != None and self.node.unit.unitType.name == "summoner"):
			self.names.append(startSummoningButton(-0.97,-0.525,gameState.theUnitTypes["gatherer"],textureIndex=texIndex("ADD_BUTTON_SMALL"),width=texWidth("ADD_BUTTON_SMALL"),height=texHeight("ADD_BUTTON_SMALL")).name)
		self.names.append(viewUnitTypeButton(-0.94,-0.59,gameState.theUnitTypes["summoner"],text="summoner",textSize=0.0005).name)
		if(self.node.unit != None and self.node.unit.unitType.name == "summoner"):
			self.names.append(startSummoningButton(-0.97,-0.565,gameState.theUnitTypes["summoner"],textureIndex=texIndex("ADD_BUTTON_SMALL"),width=texWidth("ADD_BUTTON_SMALL"),height=texHeight("ADD_BUTTON_SMALL")).name)
		if(self.node.city.researchLevel > 0):
			self.names.append(viewUnitTypeButton(-0.94,-0.63,self.node.city.researchUnitType,text=self.node.city.researchUnitType.name + "(lvl " + str(self.node.city.researchLevel) + ")",textSize=0.0005).name)
			if(self.node.unit != None and self.node.unit.unitType.name == "summoner"):
				self.names.append(startSummoningButton(-0.97,-0.605,self.node.city.researchUnitType,textureIndex=texIndex("ADD_BUTTON_SMALL"),width=texWidth("ADD_BUTTON_SMALL"),height=texHeight("ADD_BUTTON_SMALL")).name)

#				self.names.append(cancelUnitButton(-0.972,-0.85,self.node,text="cancel " + self.node.city.unitBuildQueue[-1].unitType.name,textSize=0.0005).name)				
		if(self.node.unit == gameState.getGameMode().nextUnit):
			self.names.append(skipButton(-0.964,-0.89,text="skip",textSize=0.0005).name)
			self.names.append(waitButton(-0.964,-0.93,text="wait",textSize=0.0005).name)

	@staticmethod
	def destroy():
		if(actionViewer.theActionViewer != None):
			actionViewer.theActionViewer._destroy()
			actionViewer.theActionViewer = None
	def _destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True
	def reset(self):
		self._destroy()
		actionViewer.theActionViewer = actionViewer(self.node)

class unitViewer(uiElement):
	theUnitViewer = None
	def __init__(self,unit,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.unit = unit
		self.names = []
		self.names.append(uiElement(-0.978,0.79,textXPos=0.01,textYPos=-0.035,height=texHeight('UNIT_VIEWER_BOX'),width=texWidth('UNIT_VIEWER_BOX'),textureIndex=texIndex('UNIT_VIEWER_BOX'),textSize=0.0005).name)	
		self.names.append(uiElement(-0.96,0.73,text=self.unit.unitType.name,textSize=0.0007).name)
		self.names.append(stopWaitingButton(-0.947,0.68,text="move",textSize=0.0005).name)
		self.names.append(attackButton(-0.95,0.63,text="attack",textSize=0.0005).name)
		self.names.append(waitButton(-0.940,0.58,text="wait",textSize=0.0005).name)
		if(self.unit.unitAction == gameLogic.unitAction.MOVE):
			self.names.append(uiElement(-0.958,0.715,textureIndex=texIndex("SELECTION_BRACKET"),width=texWidth("SELECTION_BRACKET"),height=texHeight("SELECTION_BRACKET"),textSize=0.0005).name)
		elif(self.unit.unitAction == gameLogic.unitAction.ATTACK):
			self.names.append(uiElement(-0.958,0.665,textureIndex=texIndex("SELECTION_BRACKET"),width=texWidth("SELECTION_BRACKET"),height=texHeight("SELECTION_BRACKET"),textSize=0.0005).name)
		else:
			self.names.append(uiElement(-0.958,0.615,textureIndex=texIndex("SELECTION_BRACKET"),width=texWidth("SELECTION_BRACKET"),height=texHeight("SELECTION_BRACKET"),textSize=0.0005).name)
	@staticmethod
	def destroy():
		if(unitViewer.theUnitViewer != None):
			unitViewer.theUnitViewer._destroy()
			unitViewer.theUnitViewer = None

	def _destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True
	@staticmethod
	def reset():
		unitViewer.theUnitViewer._destroy()
		unitViewer.theUnitViewer = unitViewer(unitViewer.theUnitViewer.unit)

class unitTypeResearchViewer(uiElement):
	theUnitTypeResearchViewer = None
	@staticmethod
	def destroy():
		if(unitTypeResearchViewer.theUnitTypeResearchViewer != None):
			unitTypeResearchViewer.theUnitTypeResearchViewer._destroy()
			unitTypeResearchViewer.theUnitTypeResearchViewer = None
	def __init__(self,unitType,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.unitType = unitType
		self.names = []
		self.names.append(uiElement(-0.978,0.53,textXPos=0.01,textYPos=-0.035,height=texHeight('UNIT_TYPE_VIEWER_BOX'),width=texWidth('UNIT_TYPE_VIEWER_BOX'),textureIndex=texIndex('UNIT_TYPE_VIEWER_BOX'),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.48,text=self.unitType.name,textSize=0.0007).name)
		self.names.append(uiElement(-0.96,0.44,text="attack power",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.44,text=str(self.unitType.attackPower),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.40,text="attack speed",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.40,text=str(self.unitType.attackSpeed),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.36,text="move speed",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.36,text=str(self.unitType.movementSpeed),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.32,text="health",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.32,text=str(self.unitType.health),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.28,text="range",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.28,text=str(self.unitType.range),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.24,text="can fly",textSize=0.0005).name)
		if(self.unitType.canFly):
			self.names.append(uiElement(-0.75,0.24,text="[x]",textSize=0.0005).name)
		else:
			self.names.append(uiElement(-0.75,0.24,text="[ ]",textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.20,text="can swim",textSize=0.0005).name)
		if(self.unitType.canSwim):
			self.names.append(uiElement(-0.75,0.20,text="[x]",textSize=0.0005).name)
		else:
			self.names.append(uiElement(-0.75,0.20,text="[ ]",textSize=0.0005).name)
		if(actionViewer.theActionViewer.node.unit != None and actionViewer.theActionViewer.node.unit.unitType.name == "summoner"):

			self.names.append(startResearchButton(-0.96,0.00,self.unitType,text="start research",textSize=0.0005).name)


	def _destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True

class unitTypeBuildViewer(uiElement):
	theUnitTypeBuildViewer = None
	def __init__(self,unitType,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.unitType = unitType
		self.names = []
		self.names.append(uiElement(-0.978,0.53,textXPos=0.01,textYPos=-0.035,height=texHeight('UNIT_TYPE_VIEWER_BOX'),width=texWidth('UNIT_TYPE_VIEWER_BOX'),textureIndex=texIndex('UNIT_TYPE_VIEWER_BOX'),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.48,text=self.unitType.name,textSize=0.0007).name)
		self.names.append(uiElement(-0.96,0.44,text="attack power",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.44,text=str(self.unitType.attackPower),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.40,text="attack speed",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.40,text=str(self.unitType.attackSpeed),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.36,text="move speed",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.36,text=str(self.unitType.movementSpeed),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.32,text="health",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.32,text=str(self.unitType.health),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.28,text="range",textSize=0.0005).name)
		self.names.append(uiElement(-0.75,0.28,text=str(self.unitType.range),textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.24,text="can fly",textSize=0.0005).name)
		if(self.unitType.canFly):
			self.names.append(uiElement(-0.75,0.24,text="[x]",textSize=0.0005).name)
		else:
			self.names.append(uiElement(-0.75,0.24,text="[ ]",textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.20,text="can swim",textSize=0.0005).name)
		if(self.unitType.canSwim):
			self.names.append(uiElement(-0.75,0.20,text="[x]",textSize=0.0005).name)
		else:
			self.names.append(uiElement(-0.75,0.20,text="[ ]",textSize=0.0005).name)
		if(actionViewer.theActionViewer.node.unit != None and actionViewer.theActionViewer.node.unit.unitType.name == "summoner"):
			self.names.append(startSummoningButton(-0.96,0.00,self.unitType,text="summon",textSize=0.0005).name)

	@staticmethod
	def destroy():
		if(unitTypeBuildViewer.theUnitTypeBuildViewer != None):
			unitTypeBuildViewer.theUnitTypeBuildViewer._destroy()
			unitTypeBuildViewer.theUnitTypeBuildViewer = None
	def _destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True

class cityEditor(uiElement):
	theCityEditor = None
	def __init__(self,city,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		mapOptionsEditor.destroy()
		self.names = []
		self.city = city
		self.names.append(cityNameInputElement(-0.972,0.746,width=texWidth('UI_TEXT_INPUT_IMAGE'),height=texHeight('UI_TEXT_INPUT_IMAGE'),text=self.city.name,textSize=0.0005,textColor='00 00 00',textureIndex=texIndex('UI_TEXT_INPUT'),textYPos=-0.035,textXPos=0.01).name)
		self.names.append(cityCostField(-0.972,0.66,width=texWidth('UI_TEXT_INPUT_IMAGE'),height=texHeight('UI_TEXT_INPUT_IMAGE'),text=str(self.city.costOfOwnership),textSize=0.0005,textColor='00 00 00',mouseOverColor='00 00 00',textureIndex=texIndex('UI_TEXT_INPUT'),textYPos=-0.035,textXPos=0.01).name)
		height = 0.56
		for unitType in self.city.unitTypes:
			self.names.append(uiElement(-0.95,height,text=unitType.name,textSize=0.0005).name)
			self.names.append(uiElement(-0.75,height,text=str(unitType.cost),textSize=0.0005).name)
			if(unitType.name != "summoner" and unitType.name != "gatherer"):
				self.names.append(removeUnitTypeButton(-0.97,height+0.03,unitType,textureIndex=texIndex("REMOVE_BUTTON_SMALL"),width=texWidth("REMOVE_BUTTON_SMALL"),height=texHeight("REMOVE_BUTTON_SMALL")).name)
			height = height - 0.04
		self.names.append(addUnitTypeButton(-0.972,height,width=0.0,height=0.0,text="+unit",textSize=0.0005).name)
		self.names.append(deleteCityButton(-0.972,-0.9,width=0.0,height=0.0,text="delete city",textSize=0.0005).name)
	def addUnitType(self,unitType):
		self.city.unitTypes.append(unitType)
		self.reset()
	def removeUnitType(self,unitType):
		self.city.unitTypes.append(unitType)
		cityEditor.reset()
	@staticmethod
	def destroy():
		if(cityEditor.theCityEditor != None):
			cityEditor.theCityEditor._destroy()
			cityEditor.theCityEditor.city = None
			cityEditor.theCityEditor = None
	def _destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True
	@staticmethod
	def reset():
		if(cityEditor.theCityEditor != None):
                        cityEditor.theCityEditor._destroy()
		cityEditor.theCityEditor = cityEditor(cityEditor.theCityEditor.city)
class mapEditorTileSelectUIElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,tileType=0,playerNumber=-1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,cursorIndex=texIndex('CURSOR_POINTER_ON'))
		self.tileType = tileType
		self.selected = False
		self.playerNumber = playerNumber

		self.toolTipElement = uiElement(self.xPosition+0.00,self.yPosition+0.04,width=0.0,height=0.0,text="asdf",textSize=0.0005,hidden=True)
	def onClick(self):
		if(gameState.getGameMode().selectedButton != None):
			gameState.getGameMode().selectedButton.selected = False
			gameState.getGameMode().selectedButton.color = "FF FF FF"
		self.selected = True
		gameState.getGameMode().selectedButton = self
	def onMouseOver(self):
		self.toolTipElement.hidden = False
	def onMouseOut(self):
		self.toolTipElement.hidden = True

class mapEditorMapOptionsButton(uiElement):
	def onClick(self):
		mapOptionsEditor.theMapOptionsEditor = mapOptionsEditor(0.0,0.0)

class mapOptionsEditor(uiElement):
	theMapOptionsEditor = None
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		mapOptionsEditor.destroy()
		cityEditor.destroy()
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cursorIndex,color=color,mouseOverColor=mouseOverColor,hidden=True)
		self.names = []
		self.names.append(uiElement(-0.96,0.73,text="map options",textSize=0.0008).name)
		self.names.append(uiElement(-0.96,0.63,text="starting mana",textSize=0.0005).name)
		self.names.append(startingManaField(-0.96,0.53,text="10",textSize=0.0005).name)
	@staticmethod
	def destroy():
		if(mapOptionsEditor.theMapOptionsEditor != None):
			mapOptionsEditor.theMapOptionsEditor._destroy()
	def _destroy(self):
		mapOptionsEditor.theMapOptionsEditor = None
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		del gameState.getGameMode().elementsDict[self.name]
		gameState.getGameMode().resortElems = True

class scrollPadElement(uiElement):
	def __init__(self,xPos,yPos,scrollableElement,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,topOffset=0.016,bottomOffset=0.020,rightOffset=0.012):
		uiElement.__init__(self,xPos-rightOffset,yPos-topOffset,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=texIndex('CURSOR_POINTER_ON'),color=color,mouseOverColor=mouseOverColor)
		self.scrolling = False
		self.initMouseYPos = 0
		self.initYPos = 0
		self.topOffset = topOffset
		self.bottomOffset = bottomOffset
		self.rightOffset = rightOffset
		self.scrollableElement = scrollableElement
		self.numScrollableElements = len(self.scrollableElement.textFieldElements) - self.scrollableElement.numFields
		self.totalScrollableHeight = self.scrollableElement.height - self.topOffset - self.bottomOffset - self.height
	def onLeftClickDown(self):
		self.scrolling = True
		self.initMouseYPos = gameState.getGameMode().mouseY
		self.initYPos = self.yPosition
	def onLeftClickUp(self):
		self.scrolling = False
	def onMouseMovement(self):
		if(self.scrolling):
			self.yPosition = self.initYPos-(2.0*(gameState.getGameMode().mouseY-self.initMouseYPos)/cDefines.defines['SCREEN_HEIGHT'])
			if(self.yPosition > self.scrollableElement.yPosition - self.topOffset):
				self.yPosition = self.scrollableElement.yPosition - self.topOffset
			elif(self.yPosition < self.scrollableElement.yPosition - self.scrollableElement.height + self.height + self.bottomOffset):
				self.yPosition = self.scrollableElement.yPosition - self.scrollableElement.height + self.height + self.bottomOffset


		self.scrollableElement.scrollPosition = int((1+self.numScrollableElements)*(self.scrollableElement.yPosition-self.topOffset-self.yPosition)/self.totalScrollableHeight)
		self.scrollableElement.hideAndShowTextFields()
	def setScrollPosition(self,scrollPos):
		self.yPosition = 0.0-((self.totalScrollableHeight*scrollPos/(1+self.numScrollableElements))+self.topOffset-self.scrollableElement.yPosition)
#		self.yPosition = (self.totalScrollableHeight*scrollPos/(1+self.numScrollableElements))+self.topOffset-self.scrollableElement.yPosition

class scrollingTextElement(uiElement):
	def __init__(self,xPos,yPos,scrollableElement,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'])
		self.scrollableElement = scrollableElement
	def onClick(self):
		self.scrollableElement.handleClick(self)

class scrollableTextFieldsElement(uiElement):
	def __init__(self,xPos,yPos,textFields,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)

		self.yPositionOffset = yPositionOffset
		self.yOffset = yOffset
		self.numFields = numFields
		self.scrollSpeed = scrollSpeed
		self.scrollPosition = 0
		self.textFields = textFields
		self.textFieldElements = []
		self.names = []
		for field in self.textFields:
			text = ""
			if(hasattr(field,"name")):
				text = field.name
			else:
				text=field
			textFieldElem = scrollingTextElement(self.xPosition,0.0,width=0.2,height=0.1,text=text,textureIndex=-1,textSize=self.textSize,hidden=True,scrollableElement=self)
			textFieldElem.onScrollUp = self.onScrollUp
			textFieldElem.onScrollDown = self.onScrollDown
			self.names.append(textFieldElem.name)
			self.textFieldElements.append(textFieldElem)

		self.hideAndShowTextFields()
		if(len(self.textFields) < self.numFields):
			self.scrollPadElem = None
		else:
			self.scrollPadElem = scrollPadElement(self.xPosition + self.width - (2.0*cDefines.defines['UI_SCROLL_PAD_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),self.yPosition,scrollableElement=self,width=(2.0*cDefines.defines['UI_SCROLL_PAD_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLL_PAD_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_SCROLL_PAD_INDEX'])
			self.names.append(self.scrollPadElem.name)
#			self.scrollPadElem.hidden = True
	def hideAndShowTextFields(self):
		count = 0
		yPosOffset = self.yPositionOffset
		for textFieldElement in self.textFieldElements:
			count = count + 1
			textFieldElement.yPosition = self.yPosition+yPosOffset
			if(count < self.numFields + self.scrollPosition and count > self.scrollPosition):
				textFieldElement.hidden = False
				yPosOffset = yPosOffset + self.yOffset
			else:
				textFieldElement.hidden = True
	def onScrollUp(self):
		if(self.scrollPadElem != None):
			self.scrollPosition = self.scrollPosition - self.scrollSpeed
			if(self.scrollPosition < 0):
				self.scrollPosition = 0
			self.hideAndShowTextFields()
			self.scrollPadElem.setScrollPosition(self.scrollPosition)
	def onScrollDown(self):
		if(self.scrollPadElem != None):
			self.scrollPosition =self.scrollPosition + self.scrollSpeed
			if(self.scrollPosition > len(self.textFieldElements) - self.numFields + 1):
				self.scrollPosition = len(self.textFieldElements) - self.numFields + 1
			self.hideAndShowTextFields()
			self.scrollPadElem.setScrollPosition(self.scrollPosition)
	def destroy(self):
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		del gameState.getGameMode().elementsDict[self.name]
		gameState.getGameMode().resortElems = True

class unitTypeSelector(scrollableTextFieldsElement):
	def handleClick(self,textFieldElem):
		for unitType in gameState.theUnitTypes.values():
			if(unitType.name == textFieldElem.text):
				cityEditor.theCityEditor.addUnitType(unitType)
		self.destroy()

class cityCostSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,cityCostField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.cityCostField = cityCostField
	def handleClick(self,textFieldElem):
		self.cityCostField.text = textFieldElem.text
		cityEditor.theCityEditor.city.costOfOwnership = int(textFieldElem.text)
		self.destroy()

class unitCostSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,unitCostField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.unitCostField = unitCostField
	def handleClick(self,textFieldElem):
		self.unitCostField.text = textFieldElem.text
		self.unitCostField.unitType.cost = int(textFieldElem.text)
		self.destroy()

class startingManaSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,startingManaField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
	 	self.startingManaField = startingManaField
	def handleClick(self,textFieldElem):
		self.startingManaField.text = textFieldElem.text
		#TODO: Save this data to the map and update save/load
#		self.unitCostField.unitType.cost = int(textFieldElem.text)
		self.destroy()

#class unitBuildTimeSelector(scrollableTextFieldsElement):
#	def __init__(self,xPos,yPos,textFields,unitBuildTimeField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
#		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
#		self.unitBuildTimeField = unitBuildTimeField
#	def handleClick(self,textFieldElem):
#		self.unitBuildTimeField.text = textFieldElem.text
#		self.unitBuildTimeField.unitType.cost = int(textFieldElem.text)
#		self.destroy()

class playerStartLocationButton(clickableElement):
	playerStartLocationButtons = []
	def __init__(self,xPos,yPos,playerNumber,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,color="FF FF FF"):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,color=color)
		self.playerNumber = playerNumber
		self.selected = False
		playerStartLocationButton.playerStartLocationButtons.append(self)
	def onClick(self):
#		if(self.playerNumber <= gameState.getGameMode().map.numPlayers + 1):
		if(gameState.getGameMode().selectedButton != None):
			gameState.getGameMode().selectedButton.selected = False
			gameState.getGameMode().selectedButton.color = "FF FF FF"
		gameState.getGameMode().selectedButton = self
		self.selected = True
		self.color = "99 99 99"
class deleteCityButton(clickableElement):
	def onClick(self):
		cityEditor.theCityEditor.destroy()
		gameState.getGameMode().selectedCityNode.city = None
		gameState.getGameMode().selectedCityNode.selected = False
		gameState.getGameMode().selectedCityNode = None

class addUnitTypeButton(clickableElement):	
	def onClick(self):
		unitTypes = gameState.theUnitTypes.copy()
#		del unitTypes["summoner"]
#		del unitTypes[gameState.theUnitTypes["summo"]]
		for unitType in cityEditor.theCityEditor.city.unitTypes:
			del unitTypes[unitType.name]
		unitTypeSelector(self.xPosition,self.yPosition-0.06,unitTypes.values(),text="select unit",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class removeUnitTypeButton(clickableElement):
	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)

		self.unitType = unitType
	def onClick(self):
		cityEditor.theCityEditor.city.unitTypes.remove(self.unitType)
		cityEditor.reset()

class cityCostField(clickableElement):
	def onClick(self):
		cityCostSelector(self.xPosition,self.yPosition-0.06,cityCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class unitCostField(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		unitCostSelector(self.xPosition,self.yPosition-0.06,unitCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class startingManaField(clickableElement):
       	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
	def onClick(self):
		startingManaSelector(self.xPosition,self.yPosition-0.06,startingManas,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))


#class unitBuildTimeField(clickableElement):
#       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
#		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
#		self.unitType = unitType
#	def onClick(self):
#		unitBuildTimeSelector(self.xPosition,self.yPosition-0.06,unitBuildTimes,self,text="select build timeGET RID OF THIS",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))



class menuButton(clickableElement):
	index = 0
	buttonsList = []
	selectedIndex = 0
	selectedTextColor = "55 55 55"
	normalTextColor = "33 33 33"
	gameMode = None
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=menuButton.normalTextColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],mouseOverColor="66 66 66")
		if(menuButton.gameMode != gameState.getGameMode()):
			menuButton.index = 0
			menuButton.buttonsList = []
			menuButton.selectedIndex = 0
		self.gameMode = gameMode
		self.selected = selected
		self.index = menuButton.index
		menuButton.gameMode = gameState.getGameMode()
		menuButton.buttonsList.append(self)
		menuButton.index = menuButton.index + 1
		if(self.index == menuButton.selectedIndex):
			self.textColor = menuButton.selectedTextColor
	def onClick(self):
		gameState.setGameMode(self.gameMode)

class mapEditSelectButton(menuButton):
	def onClick(self):
		if(self.text == "create new map"):#TODO: someone naming a map "create new map" would fuck this up
			gameState.setGameMode(self.gameMode)
		else:
			gameState.setMapName(self.text)
			gameState.setGameMode(self.gameMode)

class mapPlaySelectButton(menuButton):
	def onClick(self):
		gameState.setMapName(self.text)
		gameState.setGameMode(self.gameMode)

class mapSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,mapField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.mapField = mapField
	def handleClick(self,textFieldElem):
		server.setMap(textFieldElem.text)
		self.mapField.text = textFieldElem.text
		self.destroy()

class mapField(clickableElement):
       	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
	def onClick(self):
		dirList=os.listdir("maps")
		mapNames = []
		for fileName in dirList:
			if(fileName.endswith(".map")):
				mapNames.append(fileName[0:len(fileName)-4])
		mapSelector(self.xPosition,self.yPosition-0.06,mapNames,self,text="select build time",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class startButton(menuButton):
	def onClick(self):
		if(gameState.getMapName() != None):
			server.stopAcceptingConnections()
			for player in gameState.getNetworkPlayers():
				player.dispatchCommand("startGame|")
		else:
			#TODO: show host a friendly message
			print 'choose a map!!'

