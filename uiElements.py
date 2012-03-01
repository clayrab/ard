import os
import copy
import gameState
import gameLogic
import gameModes
import nameGenerator
import cDefines
import shutil
import client
import server
from textureFunctions import texWidth, texHeight, texIndex
from Queue import Queue
#print pubKey.decrypt(cipher)

cityCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
unitCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
startingManas = ["5","10","15","20","30","40","50","60","70","80","90","100"]
unitBuildTimes = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]

class uiElement:
#	focusedElem = None
#	@staticmethod
#	def setFocused(elem):
#		if(uiElement.focusedElem != None):
#			uiElement.focusedElem.focused = False
#		uiElement.focusedElem = elem
#		uiElement.focusedElem.focused = True
	def __init__(self,xPos,yPos,width=1.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor=None,textSize=0.001,color=None,mouseOverColor=None,textXPos=0.0,textYPos=0.0,cursorPosition=-1,fontIndex=0):
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
		self.cursorPosition = cursorPosition
		self.fontIndex = fontIndex
		self.focused = False
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
	def destroy(self):
		if(hasattr(self,"names")):
			for name in self.names:
				gameState.getGameMode().elementsDict[name].destroy()
			self.names = []
		del gameState.getGameMode().elementsDict[self.name]
		gameState.getGameMode().resortElems = True
				

class clickableElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0,fontIndex=0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos,fontIndex=fontIndex)

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
	elements = []
	def __init__(self,xPos,yPos,width=texWidth('UI_TEXT_INPUT_IMAGE'),height=texHeight('UI_TEXT_INPUT_IMAGE'),text="",textSize=0.0004,textureIndex=texIndex('UI_TEXT_INPUT'),textColor='00 00 00',textXPos=0.0,textYPos=-0.05):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos,cursorPosition=len(text))
		textInputElement.elements.append(self)
		self.realText = text
		self.leftmostCharPosition = 0
		self.rightmostCharPosition = 0
		self.recalculateText = 0
	def __del__(self):
		textInputElement.elements.remove(self)
	def textOkay(self):
		self.text = self.realText
		self.leftmostCharPosition = 0
		self.rightmostCharPosition = self.cursorPosition
	def positionText(self,leftmostCharPosition,rightmostCharPosition):
		self.recalculateText = 0
		self.leftmostCharPosition = leftmostCharPosition
		self.rightmostCharPosition = rightmostCharPosition
		if(self.leftmostCharPosition < 0):
			self.leftmostCharPosition = 0
		self.text = self.realText[leftmostCharPosition:rightmostCharPosition]
		if(self.cursorPosition > len(self.text)):
			self.cursorPosition = len(self.text)
	def onKeyDown(self,keycode):
		if(keycode == "backspace"):
			if(self.cursorPosition > 0 or self.leftmostCharPosition > 0):
				self.realText = self.realText[0:self.leftmostCharPosition+self.cursorPosition-1] + self.realText[self.leftmostCharPosition+self.cursorPosition:]
				self.recalculateText = 1
				self.cursorPosition = self.cursorPosition - 1
				if(self.leftmostCharPosition >= 1):
					self.leftmostCharPosition = self.leftmostCharPosition - 1
		elif(keycode == "delete"):
			print 'delete'
		elif(keycode == "left"):
			if(self.cursorPosition > 0):
				self.cursorPosition = self.cursorPosition - 1
			elif(self.leftmostCharPosition >= 0):
				self.leftmostCharPosition = self.leftmostCharPosition - 1
				self.recalculateText = 1
		elif(keycode == "right"):
			if(self.cursorPosition < len(self.text)):
				self.cursorPosition = self.cursorPosition + 1
				self.recalculateText = 0
			elif(self.leftmostCharPosition + self.cursorPosition < len(self.realText)):
				self.rightmostCharPosition = self.rightmostCharPosition + 1
				self.recalculateText = -1
		elif(keycode == "up" or keycode == "down" or keycode == "left shift" or keycode == "right shift"):
			self.realText = self.realText
		else:
			if(keycode == "space"):
				keycode = " "
			self.realText = self.realText[0:self.leftmostCharPosition+self.cursorPosition] + keycode + self.realText[self.leftmostCharPosition+self.cursorPosition:]
			if(self.cursorPosition < len(self.text)):
				self.cursorPosition = self.cursorPosition + 1
                                self.recalculateText = 1
			else:
                                self.cursorPosition = self.cursorPosition + 1
				self.rightmostCharPosition = self.rightmostCharPosition + 1
                                self.recalculateText = -1
			
	def onClick(self):
#		uiElement.setFocused(self)
		if(gameState.getGameMode().mouseTextPosition >=0):
			self.cursorPosition = gameState.getGameMode().mouseTextPosition
		else:
			self.cursorPosition = len(self.text)

class cityNameInputElement(textInputElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
	def onKeyDown(self,keycode):
		textInputElement.onKeyDown(self,keycode)
		cityEditor.theCityEditor.city.name = self.text


class hostIPInputElement(textInputElement):
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,text="127.0.0.1",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
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

class startGatheringButton(clickableElement):
	def onClick(self):
		gameState.getClient().sendCommand("gatherTo",str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos) + " " + str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos))
		gameState.getClient().sendCommand("wait",str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")
		if(unitViewer.theUnitViewer != None):
			unitViewer.theUnitViewer.reset()

class startSummoningButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		gameState.getClient().sendCommand("startSummoning",str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos) + " " + self.unitType.name)
		if(actionViewer.theActionViewer.node.unit == gameState.getGameMode().nextUnit):
			gameState.getClient().sendCommand("chooseNextUnit")

class cancelUnitButton(clickableElement):
	def onClick(self):
		gameState.getClient().sendCommand("cancelSummoning",str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos))
		
class startResearchButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		gameState.getClient().sendCommand("startResearch",str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos) + " " + self.unitType.name)
		if(gameState.getGameMode().nextUnit == actionViewer.theActionViewer.node.unit):
			gameState.getClient().sendCommand("chooseNextUnit")

class viewResearchButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		unitTypeResearchViewer.destroy()
		unitTypeResearchViewer.theUnitTypeResearchViewer = unitTypeResearchViewer(self.unitType)

class viewUnitTypeButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.3,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		unitTypeBuildViewer.destroy()
		unitTypeBuildViewer.theUnitTypeBuildViewer = unitTypeBuildViewer(self.unitType)

class stopWaitingButton(clickableElement):
	def onClick(self):
		gameState.getClient().sendCommand("stopWaiting",str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos))
		
class waitButton(clickableElement):
	def onClick(self):
		gameState.getClient().sendCommand("wait",str(actionViewer.theActionViewer.node.xPos) + " " + str(actionViewer.theActionViewer.node.yPos))
		if(gameState.getGameMode().nextUnit == actionViewer.theActionViewer.node.unit):
			gameState.getClient().sendCommand("chooseNextUnit")

class cancelMovementButton(clickableElement):
	def onClick(self):
		for pathNode in unitViewer.theUnitViewer.unit.movePath:
			pathNode.onMovePath = False
		unitViewer.theUnitViewer.unit.movePath = []

class skipButton(clickableElement):
       	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
	def onClick(self):
		gameState.getClient().sendCommand("skip")
#,str(gameState.getGameMode().nextUnit.node.xPos) + " " + str(gameState.getGameMode().nextUnit.node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")

class actionViewer(uiElement):
	theActionViewer = None
	def __init__(self,node,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.node = node
		self.names = []
		self.names.append(uiElement(-0.978,-0.085,textureIndex=texIndex('CITY_VIEWER_BOX'),width=texWidth('CITY_VIEWER_BOX'),height=texHeight('CITY_VIEWER_BOX'),textSize=0.0007).name)
		if(self.node.city != None):
			self.names.append(uiElement(-0.964,-0.13,text=self.node.city.name,textSize=0.0007).name)
			if(self.node.city.researching):
				self.names.append(uiElement(-0.964,-0.19,text="researching",textSize=0.0005).name)
				self.names.append(uiElement(-0.964,-0.23,text=self.node.city.researchUnitType.name,textSize=0.0005).name)
				self.names.append(uiElement(-0.964,-0.25,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
				self.names.append(uiElement(-0.964,-0.25,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(float(self.node.city.researchProgress[self.node.city.researchUnitType][1])/gameLogic.researchBuildTime),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
				#			if(self.node.city.researchLevel > 0):
#				self.names.append(uiElement(-0.964,-0.32,text="level "+str(self.node.city.researchLevel) + " complete",textSize=0.0005).name)
			else:
				if(self.node.city.unitBeingBuilt != None):
					height = -0.55
					self.names.append(uiElement(-0.972,height,text=self.node.city.unitBeingBuilt.unitType.name,textSize=0.0005).name)
					self.names.append(uiElement(-0.972,height-0.02,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
					self.names.append(uiElement(-0.972,height-0.02,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(self.node.city.unitBeingBuilt.unitType.buildTime-self.node.city.unitBeingBuilt.buildPoints)/self.node.city.unitBeingBuilt.unitType.buildTime,textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
					height = height - 0.06
					for unit in self.node.city.unitBuildQueue:
						height = height - 0.04
						self.names.append(uiElement(-0.972,height,text=str(unit.unitType.name),textSize=0.0005).name)
					height = height - 0.04
					if(len(node.city.unitBuildQueue) > 0):
						self.names.append(cancelUnitButton(-0.972,height,text="cancel " + self.node.city.unitBuildQueue[-1].unitType.name,textSize=0.0005).name)
				else:
					height = -0.55					
					self.names.append(uiElement(-0.9,-0.51,text="research",textSize=0.0007).name)
					for unitType in self.node.city.unitTypes:
						if(unitType.name != "summoner" and unitType.name != "gatherer"): 
							if(self.node.unit != None and self.node.unit.unitType.name == "summoner" and self.node.unit.player == gameState.getGameMode().getPlayerNumber() and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()-1].greenWood >= unitType.researchCostGreen and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()-1].blueWood >= unitType.researchCostBlue):
								self.names.append(startResearchButton(-0.68,height+0.025,unitType,textureIndex=texIndex("ADD_BUTTON_SMALL"),width=texWidth("ADD_BUTTON_SMALL"),height=texHeight("ADD_BUTTON_SMALL")).name)
							self.names.append(viewResearchButton(-0.965,height,unitType,self.node,text=unitType.name + " lvl " + str(self.node.city.researchProgress[unitType][0]+1),textSize=0.0005).name)
							self.names.append(uiElement(-0.93,height-0.04,text=str(unitType.researchCostGreen),textSize=0.0005).name)
							self.names.append(uiElement(-0.83,height-0.04,text=str(unitType.researchCostBlue),textSize=0.0005).name)
							self.names.append(uiElement(-0.73,height-0.04,text=str(unitType.researchTime),textSize=0.0005).name)
							height = height - 0.08
				self.names.append(uiElement(-0.9,-0.19,text="summon",textSize=0.0007).name)
				height = -0.23
				for unitType in self.node.city.researchProgress:
					if(self.node.city.researchProgress[unitType][0] > 0):
						
						self.names.append(viewUnitTypeButton(-0.965,height,unitType,text=unitType.name + " lvl " + str(self.node.city.researchProgress[unitType][0]),textSize=0.0005).name)
						self.names.append(uiElement(-0.93,height-0.04,text=str(unitType.costGreen*self.node.city.researchProgress[unitType][0]),textSize=0.0005).name)
						self.names.append(uiElement(-0.83,height-0.04,text=str(unitType.costBlue*self.node.city.researchProgress[unitType][0]),textSize=0.0005).name)
						self.names.append(uiElement(-0.73,height-0.04,text=str(unitType.buildTime),textSize=0.0005).name)
						if(self.node.unit != None and self.node.unit.unitType.name == "summoner" and self.node.unit.player == gameState.getGameMode().getPlayerNumber() and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()-1].greenWood >= unitType.costGreen and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()-1].blueWood >= unitType.costBlue):
							self.names.append(startSummoningButton(-0.68,height+0.028,unitType,textureIndex=texIndex("ADD_BUTTON_SMALL"),width=texWidth("ADD_BUTTON_SMALL"),height=texHeight("ADD_BUTTON_SMALL")).name)
						height = height - 0.08
			
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
		self.names.append(uiElement(-0.96,0.69,text=self.unit.unitType.name,textSize=0.0005).name)
		self.names.append(uiElement(-0.96,0.65,text="lvl " + str(self.unit.level),textSize=0.0005).name)
		self.names.append(uiElement(-0.964,0.76,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
		self.names.append(uiElement(-0.964,0.76,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(float(self.unit.health)/self.unit.getMaxHealth()),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
		self.names.append(uiElement(-0.96,0.735,text=str(self.unit.health)+"/"+str(self.unit.getMaxHealth()),textSize=0.0005).name)
		height = 0.565
		if(len(self.unit.movePath) > 0):
			self.names.append(cancelMovementButton(-0.964,height,text="cancel move",textSize=0.0005).name)
			height = height + 0.04
		elif(self.unit == gameState.getGameMode().nextUnit and (gameState.getPlayerNumber() == self.unit.player or gameState.getPlayerNumber() == -2)):
			self.names.append(skipButton(-0.964,height,text="skip",textSize=0.0005).name)
			height = height + 0.04

		if(self.unit.unitType.name == "gatherer"):
			if(self.unit.gatheringNode == self.unit.node):
				self.names.append(uiElement(-0.964,height,text="gathering",textSize=0.0005).name)
				height = height + 0.04
			elif(self.unit.node.tileValue == cDefines.defines['FOREST_TILE_INDEX'] or self.unit.node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX']):
				self.names.append(startGatheringButton(-0.964,height,text="start gathering",textSize=0.0005).name)
				height = height + 0.04
		if(self.unit.waiting and self.unit.unitType.name == "summoner" and self.unit.node.city != None):
			if(self.unit.node.city.unitBeingBuilt != None):
				self.names.append(uiElement(-0.964,height,text="summoning",textSize=0.0005).name)
			elif(self.unit.node.city.researching):
				self.names.append(uiElement(-0.964,height,text="researching",textSize=0.0005).name)
			else:
				self.names.append(uiElement(-0.964,height,text="waiting",textSize=0.0005).name)
			
			
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
			self.names.append(uiElement(-0.75,height,text=str(unitType.costGreen),textSize=0.0005).name)
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

class scrollableElement(uiElement):
	def onClick(self):
		self.scrollableElement.handleClick(self)	
	def setYPosition(self,yPos):
		if(hasattr(self,"names")):
			for name in self.names:
				gameState.getGameMode().elementsDict[name].yPosition = yPos
		self.yPosition = yPos

class scrollingTextElement(scrollableElement):
	def __init__(self,xPos,yPos,scrollableElement,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'])
		self.hidden = True
		self.lineHeight = 0
		self.scrollableElement = scrollableElement
		
class scrollableRoomNameElement(uiElement):
	def onClick(self):
		gameState.getGameFindClient().sendCommand("subscribe",self.text)

class scrollableMapNameElement(uiElement):
	def onClick(self):
		print 'click'

class scrollableRoomElement(scrollableElement):
	def __init__(self,xPos,yPos,roomName,mapName,playerCount,maxPlayerCount,text="",textSize=0.0005):
		scrollableElement.__init__(self,xPos,yPos,text="",textSize=textSize)
		self.names = []
		self.names.append(scrollableRoomNameElement(xPos+0.008,yPos,text=roomName,textSize=textSize).name)
		self.names.append(scrollableMapNameElement(xPos+0.9,yPos,text=mapName,textSize=textSize).name)
		self.names.append(uiElement(xPos+1.36,yPos,text=str(playerCount) + "/" + str(maxPlayerCount),textSize=textSize).name)

class scrollableTextFieldsElement(uiElement):
	def __init__(self,xPos,yPos,textFields,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,xPositionOffset=0.0,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.xPositionOffset = xPositionOffset
		self.yPositionOffset = yPositionOffset
		self.yOffset = yOffset
		self.numFields = numFields
		self.scrollSpeed = scrollSpeed
		self.scrollPosition = 0
		self.textFields = textFields
		self.names = []
		self.redraw()
	def redraw(self):
		self.reset()
		for field in self.textFields:
			textFieldElem = None
			if(hasattr(field,"onClick")):
				textFieldElem = field
				textFieldElem.scrollableElement = self
			else:
				text = ""
				if(hasattr(field,"name")):
					text = field.name
				else:
					text=field
				textFieldElem = scrollingTextElement(self.xPosition+self.xPositionOffset,0.0,self,width=2.0,height=0.1,text=text,textureIndex=-1,textSize=self.textSize,hidden=True)
			textFieldElem.onScrollUp = self.onScrollUp
			textFieldElem.onScrollDown = self.onScrollDown
			self.names.append(textFieldElem.name)
			self.textFieldElements.append(textFieldElem)
		self.hideAndShowTextFields()
		if(len(self.textFields) < self.numFields):
			self.scrollPadElem = None
		else:
			self.scrollPadElem = scrollPadElement(self.xPosition + self.width - (2.0*cDefines.defines['UI_SCROLL_PAD_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),self.yPosition,scrollableElement=self,width=(2.0*cDefines.defines['UI_SCROLL_PAD_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLL_PAD_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),textureIndex=cDefines.defines['UI_SCROLL_PAD_INDEX'],hidden=True)
			self.names.append(self.scrollPadElem.name)
			self.scrollPadElem.setScrollPosition(self.scrollPosition)
	def hideAndShowTextFields(self):
		count = 0
		yPosOffset = self.yPositionOffset
		for textFieldElement in self.textFieldElements:
			count = count + 1
			textFieldElement.setYPosition(self.yPosition+yPosOffset)
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
	def reset(self):
		for name in self.names:
			if(hasattr(gameState.getGameMode().elementsDict[name],"destroy")):
				gameState.getGameMode().elementsDict[name].destroy()
			#it appears this line is no longer needed because uiElement.destroy dels the elem from elementsDict
			#del gameState.getGameMode().elementsDict[name]
		self.names = []
#		self.textFields = []
		self.textFieldElements = []

class chatDisplay(scrollableTextFieldsElement):
	#The goal here is to hold lines of text that are too long in textQueue and run them thru a function in fonts.h which will tell us how many words will constitute one line. This way we can add the text as a textFieldElement in order to reuse all the scrollableTextFields code.
	def __init__(self):
		scrollableTextFieldsElement.__init__(self,0.55,0.9,[],textSize=0.0005,textureIndex=texIndex("CHAT_DISPLAY"),width=texWidth("CHAT_DISPLAY"),height=texHeight("CHAT_DISPLAY"),numFields=40)
		print texHeight("CHAT_DISPLAY")
		print texHeight("ROOMS_DISPLAY")

		self.textQueue = Queue()
		self.linesQueue = Queue()
		self.currentText = ""
	def addLine(self,wordLength):
		if(self.currentText != "" and wordLength > 0):
			wordTokens = self.currentText.split(" ",wordLength)
			if(len(wordTokens) > wordLength):
				self.currentText = wordTokens[wordLength]
			else:
				self.currentText = ""
			self.textFields.append(" ".join(wordTokens[:wordLength]))
			self.redraw()
			if(self.scrollPadElem != None and self.scrollPosition >= self.scrollPadElem.numScrollableElements):
				self.scrollPosition = self.scrollPadElem.numScrollableElements+1
				self.redraw()
	def addText(self,text):
		self.textQueue.put(text)
	def getText(self):
		if(self.currentText == "" and not self.textQueue.empty()):
			self.currentText = self.textQueue.get()
		return self.currentText

class roomSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,rooms,width=0.0,height=0.0,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,[],width=texWidth("ROOMS_DISPLAY"),height=texHeight("ROOMS_DISPLAY"),textureIndex=texIndex("ROOMS_DISPLAY"),text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor,xPositionOffset=0.01,yPositionOffset=-0.06,yOffset=-0.041)
		self.rooms = rooms
		for room in rooms:
			self.textFields.append(scrollableRoomElement(self.xPosition+self.xPositionOffset,0.0,room[0],"mapname",0,8))
		self.redraw()
	def handleClick(self,textFieldElem):
		print textFieldElem
	def addRoom(self,roomStr):
		roomTokens = roomStr.split("-")
		self.rooms.append(tuple(roomTokens))
		self.textFields = []
		for room in self.rooms:
			self.textFields.append(scrollableRoomElement(self.xPosition+self.xPositionOffset,0.0,room[0],"mapname",0,8))
		self.redraw()
	def removeRoom(self,roomName):
		for room in self.rooms:
			if(room[0] == roomName):
				self.rooms.remove(room)
		self.textFields = []
		for room in self.rooms:
			self.textFields.append(scrollableRoomElement(self.xPosition+self.xPositionOffset,0.0,room[0],"mapname",0,8))
		self.redraw()

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
		text="DELETEME"
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.unitCostField = unitCostField
	def handleClick(self,textFieldElem):
		self.unitCostField.text = textFieldElem.text
		self.unitCostField.unitType.costGreen = int(textFieldElem.text)
		self.destroy()

class startingManaSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,startingManaField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
	 	self.startingManaField = startingManaField
	def handleClick(self,textFieldElem):
		self.startingManaField.text = textFieldElem.text
		#TODO: Save this data to the map and update save/load
#		self.unitCostField.unitType.costGreen = int(textFieldElem.text)
		self.destroy()

class createRoomButton(clickableElement):
	def onClick(self):
		server.startServer('')
		gameState.getGameFindClient().sendCommand("testServer",gameState.getConfig()["serverPort"])
		gameState.setGameMode(gameModes.createGameMode)
		smallModal("testing connection...",dismissable=False)


class chatBox(textInputElement):
	def __init__(self):
		textInputElement.__init__(self,0.55,-0.678,text="",textSize=0.0005,textureIndex=texIndex("CHAT_BOX"),width=texWidth("CHAT_BOX"),textColor="FF FF FF",textXPos=0.02,textYPos=-0.035)
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			print 'return'
			return
		elif(keycode == "tab"):
			return
		else:
			textInputElement.onKeyDown(self,keycode)

class sendChatButton(clickableElement):	
	def onClick(self):
		print 'send chat command'

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
#		unitTypes = gameState.theUnitTypes.copy()
#		del unitTypes["summoner"]
#		del unitTypes[gameState.theUnitTypes["summo"]]
#		for unitType in cityEditor.theCityEditor.city.unitTypes:
#			del unitTypes[unitType.name]
		unitTypeSelector(self.xPosition,self.yPosition-0.06,gameState.theUnitTypes.values(),text="select unit",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

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
	selectedTextColor = "AA AA AA"
	normalTextColor = "EE EE EE"
	gameMode = None
	def __init__(self,xPos,yPos,gameMode,width=1.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=menuButton.normalTextColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],mouseOverColor="66 66 66",textSize=0.0013,fontIndex=1)
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
		if(self.text == "create new map"):#TODO: someone naming a map "create new map" would fuck this up, break this into separate classes
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

class onlineMapSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,mapField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.mapField = mapField
	def handleClick(self,fieldElem):
		self.mapField.text = fieldElem.text
		self.mapField.mapName = fieldElem.text
		self.destroy()

class mapField(clickableElement):
       	def __init__(self,xPos,yPos,selector,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.selector = selector
		self.mapName = None
	def onClick(self):
		dirList=os.listdir("maps")
		mapNames = []
		for fileName in dirList:
			if(fileName.endswith(".map")):
				mapNames.append(fileName[0:len(fileName)-4])
		self.selector(self.xPosition,self.yPosition-0.06,mapNames,self,text="select build time",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class maxPlayersSelector(scrollableTextFieldsElement):
	def handleClick(self,fieldElem):
		gameState.getGameMode().maxPlayersField.text = fieldElem.text + " players"
		self.destroy()

class maxPlayersField(clickableElement):
	def onClick(self):
		maxPlayersSelector(self.xPosition,self.yPosition-0.06,["1","2","4","8"],textSize=0.0006)

class createButton(menuButton):
	def onClick(self):
		if(gameState.getGameMode().mapField.mapName != None):
			gameState.getGameFindClient().sendCommand("createGameRoom",gameState.getGameMode().titleField.text + "|" + gameState.getGameMode().maxPlayersField.text.split(" ")[0] + "|" + gameState.getGameMode().mapField.mapName)
		else:
			smallModal("Choose a map!")

class roomTitleInputElement(textInputElement):
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			return
		elif(keycode == "tab"):
			return
		elif(keycode == "space"):
			return
		else:
			textInputElement.onKeyDown(self,keycode)

class startButton(menuButton):
	def onClick(self):
		if(gameState.getMapName() != None):
			server.stopAcceptingConnections()
			for player in gameState.getNetworkPlayers():
				player.dispatchCommand("startGame -1")
		else:
			#TODO: show host a friendly message
			print 'choose a map!!'		

class loginInputElement(textInputElement):
	usernameElem = None
	passwordElem = None
	def __init__(self,xPos,yPos,text,textXPos,textYPos):
		textInputElement.__init__(self,xPos,yPos,text=text,textSize=0.0006,textXPos=textXPos,textYPos=textYPos)
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			
			gameState.getGameFindClient().sendCommand("login",loginInputElement.usernameElem.text + " " + loginInputElement.passwordElem.text)
		elif(keycode == "tab"):
			for index,elem in enumerate(textInputElement.elements):
				if(elem.focused):
					if(index >= len(textInputElement.elements)-1):
						gameState.getGameMode().setFocus(textInputElement.elements[0])
					else:
						gameState.getGameMode().setFocus(textInputElement.elements[index+1])
					break
		elif(keycode == "space"):
			return
		else:
			textInputElement.onKeyDown(self,keycode)

class loginUserName(loginInputElement):
	def __init__(self,xPos,yPos,text="clayrab"):
		loginInputElement.__init__(self,xPos,yPos,text=text,textXPos=0.005,textYPos=-0.04)
		loginInputElement.usernameElem = self
class loginPassword(loginInputElement):
	def __init__(self,xPos,yPos,text="maskmask"):
		loginInputElement.__init__(self,xPos,yPos,text=text,textXPos=0.005,textYPos=-0.04)
		loginInputElement.passwordElem = self

class modalButton(clickableElement):
	def __init__(self,modal,yPos=-0.05,text="ok",textureIndex=cDefines.defines["OK_BUTTON_INDEX"]):
		self.modal = modal
		clickableElement.__init__(self,texWidth("OK_BUTTON")/-2.0,yPos,text=text,width=texWidth("OK_BUTTON"),height=texHeight("OK_BUTTON"),textureIndex=textureIndex,textXPos=0.1,textYPos=-0.1)
	def onClick(self):
		self.modal.destroy()

class modal(uiElement):
	def destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		del gameState.getGameMode().elementsDict[self.textElem.name]
		del gameState.getGameMode().elementsDict[self.backgroundElem.name]
		if(self.dismissable):
			del gameState.getGameMode().elementsDict[self.buttonElem.name]
		gameState.getGameMode().resortElems = True
		gameState.getGameMode().modal = None

class smallModal(modal):
	def __init__(self,text,dismissable=True):
		uiElement.__init__(self,texWidth("MODAL_SMALL")/-2.0,texHeight("MODAL_SMALL")/2.0,width=texWidth("MODAL_SMALL"),height=texHeight("MODAL_SMALL"),textureIndex=cDefines.defines["MODAL_SMALL_INDEX"])
		self.dismissable = dismissable
		self.backgroundElem = uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines["MODAL_BACKGROUND_INDEX"])
		self.textElem = uiElement((texWidth("MODAL_SMALL")/-2.0)+0.03,0.1,width=texWidth("MODAL_SMALL")-0.06,text=text,textSize=0.0007)
		if(self.dismissable):
			self.buttonElem = modalButton(self)
		gameState.getGameMode().modal = self

class createMapButton(clickableElement):
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=menuButton.normalTextColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],mouseOverColor="66 66 66",textSize=0.0013,fontIndex=1)
		self.gameMode = gameMode
	def onClick(self):
		mapName = gameState.getGameMode().mapNameInputElement.text
		try:
			numPlayers = int(gameState.getGameMode().mapPlayerCountInputElement.text)
		except:
			numPlayers = -1
		if(numPlayers < 2 or numPlayers > 8):
			smallModal("player count must be between 2 and 8")
		else:
			if(len(mapName) < 1):
				smallModal("you must enter a map name")
			else:
				shutil.copyfile("maps/defaultMap","maps/" + mapName + ".map")
				gameState.setMapName(mapName)
				gameState.setGameMode(self.gameMode)
				for playerNum in range(0,numPlayers+1):
					gameState.getGameMode().map.nodes[0][playerNum-1].playerStartValue = playerNum

class newMapNameInputElement(textInputElement):
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
		self.gameMode = gameMode
	def onKeyDown(self,keycode):
		if(keycode == "tab"):
			gameState.getGameMode().setFocus(gameState.getGameMode().mapPlayerCountInputElement)
		else:
			if(keycode != "return"):
				textInputElement.onKeyDown(self,keycode)

class newMapPlayerCountInputElement(textInputElement):
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
		self.gameMode = gameMode
	def onKeyDown(self,keycode):
		if(keycode == "tab"):
			gameState.getGameMode().setFocus(gameState.getGameMode().mapNameInputElement)
		else:
			if(keycode == "0" or keycode == "1" or keycode == "2" or keycode == "3" or keycode == "4" or keycode == "5" or keycode == "6" or keycode == "7" or keycode == "8" or keycode == "9" or keycode == "backspace"):
				textInputElement.onKeyDown(self,keycode)
