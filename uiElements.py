import os
import copy
import gameState
import gameLogic
import gameModes
import gameFindClient
import nameGenerator
import cDefines
import shutil
import client
import server
import socket
from textureFunctions import texWidth, texHeight, texIndex
import rendererUpdates
from Queue import Queue
#print pubKey.decrypt(cipher)

cityCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
unitCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
startingManas = ["5","10","15","20","30","40","50","60","70","80","90","100"]
unitBuildTimes = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]

class uiElement(object):
	def __init__(self,xPos,yPos,width=1.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor=None,textSize=0.001,color=None,mouseOverColor=None,textXPos=0.0,textYPos=0.0,cursorPosition=-1,fontIndex=0,frameLength=10,frameCount=1):
		self.name = nameGenerator.getNextName()
		self._xPosition = xPos
		self._yPosition = yPos
		self.width = width
		self.height = height/frameCount
		self.textureIndex = textureIndex
		self._hidden=hidden
		self.cursorIndex=cursorIndex
		self._text = text
		self._textColor = textColor
		if(self._textColor == None):
			self._textColor = "FF FF FF"
		self.textSize = textSize
		self.color = color
		self.textXPos = textXPos
		self.textYPos = textYPos
		self.cursorPosition = cursorPosition
		self.fontIndex = fontIndex
		self.frameLength = frameLength
		self.frameCount = frameCount
		self.focused = False
		self.mouseOverColor = mouseOverColor
		if(self.color == None):
			self.color = "FF FF FF"
		self.names = []
		gameState.getGameMode().elementsDict[self.name] = self
		gameState.getGameMode().resortElems = True
		gameState.rendererUpdateQueue.put(rendererUpdates.addUIElem(self))
	@property
	def textColor(self): 
		return self._textColor
	@textColor.setter
	def textColor(self,val):
		gameState.rendererUpdateQueue.put(rendererUpdates.updateUIElem(self))
		self._textColor = val
	@property
	def hidden(self): 
		return self._hidden
	@hidden.setter
	def hidden(self,val):
		gameState.rendererUpdateQueue.put(rendererUpdates.updateUIElem(self))
		self._hidden = val
	@property
	def xPosition(self): 
		return self._xPosition
	@xPosition.setter
	def xPosition(self,val):
		self._xPosition = val
		gameState.rendererUpdateQueue.put(rendererUpdates.updateUIElem(self))
	@property
	def yPosition(self): 
		return self._yPosition
	@yPosition.setter
	def yPosition(self,val):
		self._yPosition = val
		gameState.rendererUpdateQueue.put(rendererUpdates.updateUIElem(self))
	@property
	def text(self): 
		return self._text
	@text.setter
	def text(self,val):
		if(self._text != val):
			self._text = val
#			gameState.rendererUpdateQueue.put(rendererUpdates.updateUIElem(self))
		
	def onScrollDown(self):
		return None
	def onScrollUp(self):
		return None
	def destroy(self):
		if(hasattr(self,"names")):
			for name in self.names:
				gameState.getGameMode().elementsDict[name].destroy()
			self.names = []
		gameState.rendererUpdateQueue.put(rendererUpdates.removeUIElem(self))			
		del gameState.getGameMode().elementsDict[self.name]
		gameState.getGameMode().resortElems = True

class clickableElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color=None,mouseOverColor=None,textXPos=0.0,textYPos=0.0,fontIndex=0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos,fontIndex=fontIndex)

class playerElement(clickableElement):
	def __init__(self,xPos,yPos,playerNumber,text="empty",textColor="55 55 55",textSize=0.0005,mouseOverColor="55 55 55"):
		clickableElement.__init__(self,xPos,yPos,text=text,textColor=textColor,textSize=textSize,mouseOverColor=mouseOverColor)
		self.playerNumber = playerNumber
	def onClick(self):
		if(self.text == "empty"):
			gameState.getClient().sendCommand("changePlayerNumber",str(gameState.getPlayerNumber()) + ":" + str(self.playerNumber))

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
	def __init__(self,xPos,yPos,isPassword=False,width=texWidth('UI_TEXT_INPUT'),height=texHeight('UI_TEXT_INPUT'),text="",textureIndex=texIndex('UI_TEXT_INPUT'),textColor='DD DD DD',textSize=0.0006,textXPos=0.010,textYPos=-0.045,fontIndex=0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos,cursorPosition=len(text),fontIndex=fontIndex)
		textInputElement.elements.append(self)
		if(isPassword):
			self.text = "*"*len(text)
		self.realText = text
		self.leftmostCharPosition = 0
		self.rightmostCharPosition = 0
		self.recalculateText = 0
		self.isPassword = isPassword
	def __del__(self):
		textInputElement.elements.remove(self)
	def setText(self,txt):
		self.realText = txt
		self.leftmostCharPosition = 0
		self.cursorPosition = 0
		self.recalculateText = 1
	def textOkay(self):
		self.recalculateText = 0
		if(self.isPassword):
			self.text = "*"*len(self.realText)
		else:
			self.text = self.realText
		self.cursorPosition = self.cursorPosition + self.leftmostCharPosition
		self.leftmostCharPosition = 0
		self.rightmostCharPosition = len(self.realText)
	def positionText(self,leftmostCharPosition,rightmostCharPosition):
		self.recalculateText = 0
		if(leftmostCharPosition < self.leftmostCharPosition):
			self.cursorPosition = self.cursorPosition - (self.leftmostCharPosition - leftmostCharPosition)
		self.leftmostCharPosition = leftmostCharPosition
		self.rightmostCharPosition = rightmostCharPosition
		if(self.leftmostCharPosition < 0):
			self.leftmostCharPosition = 0
		if(self.isPassword):
			self.text = "*"*(rightmostCharPosition-leftmostCharPosition)
		else:
			self.text = self.realText[leftmostCharPosition:rightmostCharPosition]
		if(self.cursorPosition > len(self.text)):
			self.cursorPosition = len(self.text)
	def onKeyDown(self,keycode):
		if(keycode == "backspace"):
			if(self.cursorPosition > 0 or self.leftmostCharPosition > 0):
				self.realText = self.realText[0:self.leftmostCharPosition+self.cursorPosition-1] + self.realText[self.leftmostCharPosition+self.cursorPosition:]
				self.recalculateText = 1
				if(self.cursorPosition > 1):
					self.cursorPosition = self.cursorPosition - 1
				else:
					self.leftmostCharPosition = self.leftmostCharPosition - 1
#				if(self.rightmostCharPosition > len(self.realText)):
#					   self.rightmostCharPosition = len(self.realText)
#				if(self.leftmostCharPosition >= 1):
#					self.leftmostCharPosition = self.leftmostCharPosition - 1
		elif(keycode == "delete"):
			if(self.cursorPosition < len(self.realText)):
				self.realText = self.realText[0:self.leftmostCharPosition+self.cursorPosition] + self.realText[self.leftmostCharPosition+self.cursorPosition+1:]
				self.recalculateText = 1
#				if(self.rightmostCharPosition == len(self.realText)):
#					self.rightmostCharPosition = self.rightmostCharPosition -1
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
		elif(keycode == "*" or keycode == "|" or keycode == "-"):
			return
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
#		uiElement.setFocusedElemed(self)
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

class hostIPConnectButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("CONNECT_BUTTON"),width=texWidth("CONNECT_BUTTON"),height=texHeight("CONNECT_BUTTON"))
	def onClick(self):
		if(len(gameState.getGameMode().hostIPInputElem.text) > 0):
			gameState.setHostIP(gameState.getGameMode().hostIPInputElem.text)
			gameState.setGameMode(gameModes.lanGameRoomMode,[gameState.getGameMode().hostIPInputElem.text])

class hostIPInputElement(textInputElement):
	def __init__(self,xPos,yPos):
		textInputElement.__init__(self,xPos,yPos,width=texWidth("UI_TEXT_INPUT"),height=texHeight("UI_TEXT_INPUT"),textureIndex=texIndex("UI_TEXT_INPUT"),text="192.168.1.4")
#		self.gameMode = gameMode
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			if(len(self.text) > 0):
				gameState.setGameMode(gameModes.lanGameRoomMode,[self.text])
				gameState.setHostIP(self.text)
		elif(keycode == "." or keycode == "backspace"):
			textInputElement.onKeyDown(self,str(keycode))
		else:
			try:
				keycode = int(keycode)
				textInputElement.onKeyDown(self,str(keycode))
			except:
				return

class viewUnitTypeButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.3,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		unitTypeBuildViewer.destroy()
		unitTypeBuildViewer.theUnitTypeBuildViewer = unitTypeBuildViewer(self.unitType)

class unitTypeViewerButton(clickableElement):
	def __init__(self,xPos,yPos,unitType,textureIndex=None,width=0.0,height=0.0):
		clickableElement.__init__(self,xPos,yPos,textureIndex=textureIndex,width=width,height=height)
		self.unitType = unitType
		self.dontDismiss = False
	def onMouseOver(self):
		if(unitTypeViewer.theViewer != None):
			unitTypeViewer.theViewer.destroy()
		unitTypeViewer.theViewer = unitTypeViewer(self.unitType)
	def onMouseOut(self):
		if(not self.dontDismiss):
			if(unitTypeViewer.theViewer != None):
				unitTypeViewer.theViewer.destroy()
	def onClick(self):
		self.dontDismiss = True

class summonerViewerButton(clickableElement):
	def onClick(self):
		node = viewer.theViewer.node
		viewer.theViewer.destroy()
		viewer.theViewer = summonerViewer(node)

class unitViewerButton(clickableElement):
	def onClick(self):
		node = viewer.theViewer.node
		viewer.theViewer.destroy()
		viewer.theViewer = unitViewer(node)

class cityViewerButton(clickableElement):
	def onClick(self):
		node = viewer.theViewer.node
		viewer.theViewer.destroy()
		viewer.theViewer = cityViewer(node)
#		gameState.rendererUpdateQueue.put(rendererUpdates.updateUIElem(viewer.theViewer))
class cancelButton(clickableElement):
	def __init__(self,xPos,yPos,index):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('CANCEL_BUTTON'),width=texWidth('CANCEL_BUTTON'),textureIndex=texIndex('CANCEL_BUTTON'))	
		self.index = index
	def onClick(self):
		gameState.getClient().sendCommand("cancelQueuedThing",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos) + " " + str(self.index))
#		if(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
#			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)

def startGathering():
	viewer.theViewer.destroy()
	gameState.getClient().sendCommand("startMeditating",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos))
	if(gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit):
		gameState.getClient().sendCommand("chooseNextUnit")
	
class startGatheringButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('MEDITATE_BUTTON'),width=texWidth('MEDITATE_BUTTON'),textureIndex=texIndex('MEDITATE_BUTTON'))
	def onClick(self):
		startGathering()

class cancelMovementButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('CANCEL_MOVEMENT_BUTTON'),width=texWidth('CANCEL_MOVEMENT_BUTTON'),textureIndex=texIndex('CANCEL_MOVEMENT_BUTTON'))
	def onClick(self):
		gameState.movePath = []
		gameState.getGameMode().selectedNode.unit.movePath = []
		gameState.rendererUpdateQueue.put(rendererUpdates.updateMovePath())

def skip():
	gameState.getClient().sendCommand("skip")
	gameState.getClient().sendCommand("chooseNextUnit")

class skipButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('SKIP_BUTTON'),width=texWidth('SKIP_BUTTON'),textureIndex=texIndex('SKIP_BUTTON'))
	def onClick(self):
		skip()

class doneButton(clickableElement):
	def __init__(self,xPos,yPos):
		skipButton.__init__(self,xPos,yPos,textureIndex=texIndex('SKIP_BUTTON'))

def startSummoning():
	viewer.theViewer.destroy()
	gameState.getClient().sendCommand("startMeditating",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos))
#	if(gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit):
#		gameState.getClient().sendCommand("chooseNextUnit")
	
class startSummoningButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('START_SUMMONING_BUTTON'),width=texWidth('START_SUMMONING_BUTTON'),textureIndex=texIndex('START_SUMMONING_BUTTON'))
	def onClick(self):
		startSummoning()

class summonButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BUILD_BUTTON"),width=texWidth("BUILD_BUTTON"),height=texHeight("BUILD_BUTTON"))
		self.unitType = unitType
	def onClick(self):
		gameState.getClient().sendCommand("startSummoning",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos) + " " + self.unitType.name)
		if(gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit):
			gameState.getClient().sendCommand("chooseNextUnit")
#		elif(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
#			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)
#			gameState.getGameMode().focus(gameState.getGameMode().nextUnit.node)

class researchButton(clickableElement):
	def __init__(self,xPos,yPos,unitType):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('RESEARCH_BUTTON'),width=texWidth('RESEARCH_BUTTON'),textureIndex=texIndex('RESEARCH_BUTTON'))
		self.unitType = unitType
	def onClick(self):
		gameState.getClient().sendCommand("startResearch",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos) + " " + self.unitType.name)
		if(gameState.getGameMode().nextUnit == gameState.getGameMode().selectedNode.unit):
			gameState.getClient().sendCommand("chooseNextUnit")
#		elif(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
#			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)
#			gameState.getGameMode().focus(gameState.getGameMode().nextUnit.node)

class unitTypeViewer(uiElement):
	theViewer = None
	def __init__(self,unitType):
		if(hasattr(gameState.getGameMode(),"nextUnit")):
			uiElement.__init__(self,-0.520,0.983,width=texWidth("UI_UNITTYPE_BACKGROUND"),height=texHeight("UI_UNITTYPE_BACKGROUND"),textureIndex=texIndex("UI_UNITTYPE_BACKGROUND"))
		else:
			uiElement.__init__(self,viewer.theViewer.xPosition+0.465,0.79,width=texWidth("UI_UNITTYPE_BACKGROUND"),height=0.8,textureIndex=texIndex("UI_UNITTYPE_BACKGROUND"))
		self.unitType = unitType
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.052,text=self.unitType.name,textSize=0.0006,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.092,text="health",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.092,text=str(self.unitType.health),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.132,text="attack power",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.132,text=str(self.unitType.attackPower),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.172,text="attack speed",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.172,text=str(self.unitType.attackSpeed),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.212,text="movement speed",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.212,text=str(self.unitType.movementSpeed),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.252,text="armor",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.252,text=str(self.unitType.armor),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.292,text="range",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.292,text=str(self.unitType.range),textSize=0.0005,textColor="ee ed 9b").name)
		if(self.unitType.canFly):
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.332,text="flying",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.412,text="red wood cost",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.412,text=str(self.unitType.costRed),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.452,text="blue wood cost",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.452,text=str(self.unitType.costBlue),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.492,text="build time",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.492,text=str(self.unitType.buildTime),textSize=0.0005,textColor="ee ed 9b").name)

		if(self.unitType.researchCostRed > 0):
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.572,text="red wood level cost",textSize=0.0005,textColor="ee ed 9b").name)
			self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.572,text=str(self.unitType.researchCostRed),textSize=0.0005,textColor="ee ed 9b").name)
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.612,text="red wood level cost",textSize=0.0005,textColor="ee ed 9b").name)
			self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.612,text=str(self.unitType.researchCostBlue),textSize=0.0005,textColor="ee ed 9b").name)
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.652,text="level research time",textSize=0.0005,textColor="ee ed 9b").name)
			self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.652,text=str(self.unitType.researchTime),textSize=0.0005,textColor="ee ed 9b").name)
#	self.movementSpeedBonus = movementSpeedBonus
#	self.canSwim = canSwim
	def destroy(self):
		unitTypeViewer.theViewer = None
		uiElement.destroy(self)


class viewer(uiElement):
	theViewer = None
	def __init__(self,xPos,yPos,node,width,height,textureIndex):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex)
		self.node = node
		self.names = []
		if(node.unit != None):
			self.names.append(unitViewerButton(xPos+0.047,yPos-0.044,text="unit",textSize=0.00055,textColor="ee ed 9b",width=1.0,height=1.0,fontIndex=1).name)
		else:
			self.names.append(uiElement(xPos+0.047,yPos-0.044,text="unit",textSize=0.00055,textColor="cc cc cc",width=1.0,height=1.0,fontIndex=1).name)			
		if(node.unit != None and node.unit.unitType.name == "summoner"):
			self.names.append(summonerViewerButton(xPos+0.164,yPos-0.044,text="summon",textSize=0.00055,textColor="ee ed 9b",width=1.0,height=1.0,fontIndex=1).name)
		else:
			self.names.append(uiElement(xPos+0.164,yPos-0.044,text="summon",textSize=0.00055,textColor="cc cc cc",width=1.0,height=1.0,fontIndex=1).name)
		if(node.city != None):
			self.names.append(cityViewerButton(xPos+0.335,yPos-0.044,text="stone",textSize=0.00055,textColor="ee ed 9b",width=1.0,height=1.0,fontIndex=1).name)
		else:
			self.names.append(uiElement(xPos+0.335,yPos-0.044,text="stone",textSize=0.00055,textColor="cc cc cc",width=1.0,height=1.0,fontIndex=1).name)
	def destroy(self):
		viewer.theViewer = None
		uiElement.destroy(self)

class unitViewer(viewer):
	def __init__(self,node):
		viewer.__init__(self,-0.983,0.983,node,width=texWidth("UNIT_VIEWER_BACKGROUND"),height=texHeight("UNIT_VIEWER_BACKGROUND"),textureIndex=texIndex("UNIT_VIEWER_BACKGROUND"))
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.100,textureIndex=texIndex("GREY_PEDESTAL"),width=2.0*texWidth("GREY_PEDESTAL"),height=2.0*texHeight("GREY_PEDESTAL")).name)
		self.names.append(unitTypeViewerButton(self.xPosition+0.040,self.yPosition-0.120,self.node.unit.unitType,textureIndex=self.node.unit.unitType.textureIndex,height=0.14,width=0.14*0.75).name)

		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.125,text="health",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.130,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.130,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR')*(float(self.node.unit.health)/self.node.unit.getMaxHealth()),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)

		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.185,text="move initiative",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.190,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.190,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR')*(float(gameLogic.INITIATIVE_ACTION_DEPLETION-self.node.unit.movementPoints)/float(gameLogic.INITIATIVE_ACTION_DEPLETION)),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)

		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.245,text="atk initiative",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.250,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.250,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR')*(float(gameLogic.INITIATIVE_ACTION_DEPLETION-self.node.unit.attackPoints)/float(gameLogic.INITIATIVE_ACTION_DEPLETION)),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
		
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.32,text=self.node.unit.unitType.name,textSize=0.00055,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.36,text="lvl " + str(self.node.unit.level),textSize=0.00055,textColor="ee ed 9b").name)

		if(self.node.unit.isMeditating):
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.450,text="meditating",textSize=0.00055,textColor="ee ed 9b").name)
		else:
			height = self.yPosition-1.870
			if(len(self.node.unit.movePath) > 0 and self.node.unit.isControlled()):
				self.names.append(cancelMovementButton(self.xPosition+0.126,height).name)
				height = height + 0.085
			if(self.node.unit == gameState.getGameMode().nextUnit and self.node.unit.isControlled()):
				self.names.append(skipButton(self.xPosition+0.310,height).name)
				height = height + 0.085
			if(self.node.unit == gameState.getGameMode().nextUnit and self.node.unit.unitType.name == "gatherer" and (self.node.tileValue == cDefines.defines['RED_FOREST_TILE_INDEX'] or self.node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX'] or self.node.city != None)):
				self.names.append(startGatheringButton(self.xPosition+0.262,height).name)

class cityViewer(viewer):
	def __init__(self,node):
		if(hasattr(gameState.getGameMode(),"createGameMode")):
			uiElement.__init__(self,-0.31,0.79,width=texWidth("UI_CITYVIEW_BACKGROUND"),height=texHeight("UI_CITYVIEW_BACKGROUND"),textureIndex=texIndex("UI_CITYVIEW_BACKGROUND"))
		else:
			viewer.__init__(self,-0.983,0.983,node,texWidth("STONE_VIEWER_BACKGROUND"),texHeight("STONE_VIEWER_BACKGROUND"),texIndex("STONE_VIEWER_BACKGROUND"))
		self.node = node
		height = self.yPosition-0.3
		for unitType in self.node.city.unitTypes:
			self.names.append(uiElement(self.xPosition+0.022,height,textureIndex=texIndex("GREY_PEDESTAL"),width=texWidth("GREY_PEDESTAL"),height=texHeight("GREY_PEDESTAL")).name)
			self.names.append(unitTypeViewerButton(self.xPosition+0.028,height-0.008,unitType,textureIndex=unitType.textureIndex,height=0.07,width=0.07*0.75).name)
			self.names.append(uiElement(self.xPosition+0.1,height-0.030,text=unitType.name,textSize=0.00055,textColor="ee ee ee",fontIndex=2).name)

			self.names.append(uiElement(self.xPosition+0.1,height-0.042,textureIndex=texIndex("RED_WOOD_ICON"),width=texWidth("RED_WOOD_ICON"),height=texHeight("RED_WOOD_ICON")).name)
			self.names.append(uiElement(self.xPosition+0.123,height-0.065,text=str(unitType.costRed),textSize=0.00040,textColor="ee ee ee",fontIndex=0).name)
			self.names.append(uiElement(self.xPosition+0.175,height-0.042,textureIndex=texIndex("BLUE_WOOD_ICON"),width=texWidth("BLUE_WOOD_ICON"),height=texHeight("BLUE_WOOD_ICON")).name)
			self.names.append(uiElement(self.xPosition+0.198,height-0.065,text=str(unitType.costBlue),textSize=0.00040,textColor="ee ee ee",fontIndex=0).name)
			self.names.append(uiElement(self.xPosition+0.250,height-0.042,textureIndex=texIndex("TIME_ICON"),width=texWidth("TIME_ICON"),height=texHeight("TIME_ICON")).name)
			self.names.append(uiElement(self.xPosition+0.273,height-0.065,text=str(unitType.buildTime),textSize=0.00040,textColor="ee ee ee",fontIndex=0).name)

			height = height - 0.1
	def destroy(self):
		viewer.theViewer = None
		uiElement.destroy(self)
	

class summonerViewer(viewer):
	def __init__(self,node):
		viewer.__init__(self,-0.983,0.983,node,width=texWidth("SUMMON_VIEWER_BACKGROUND"),height=texHeight("SUMMON_VIEWER_BACKGROUND"),textureIndex=texIndex("SUMMON_VIEWER_BACKGROUND"))
		self.node = node
		self.isSummonerViewer = True
		self.names.append(summonerUnitsDisplay(self.xPosition+0.012,self.yPosition-0.150,gameState.getAvailableUnitTypes(),node.unit,buildUnitElem).name)
		researchableUnitTypes = []
		for unitType in gameState.getResearchProgress():
			if(unitType.name != "gatherer"):
				researchableUnitTypes.append(unitType)
		self.names.append(summonerUnitsDisplay(self.xPosition+0.012,self.yPosition-0.738,researchableUnitTypes,node.unit,researchUnitElem).name)
		queuedThings = []
		if(self.node.unit.researching):
			queuedThings.append(self.node.unit.researchUnitType)
		elif(self.node.unit.unitBeingBuilt != None):
			queuedThings.append(self.node.unit.unitBeingBuilt)
		for thing in self.node.unit.buildQueue:
			queuedThings.append(thing)
		queuedThingElem.firstThing = True
		self.names.append(summonerUnitsDisplay(self.xPosition+0.012,self.yPosition-1.324,queuedThings,node.unit,queuedThingElem).name)
		if(gameState.getGameMode().nextUnit == self.node.unit and self.node.unit.isControlled()):
			self.names.append(skipButton(-0.673,-0.887).name)
		if(len(self.node.unit.movePath) > 0 and self.node.unit.isControlled()):
			self.names.append(cancelMovementButton(-0.857,-0.887).name)

		
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
		if(actionViewer.theViewer.node.unit != None and actionViewer.theViewer.node.unit.unitType.name == "summoner"):

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
		if(actionViewer.theViewer.node.unit != None and actionViewer.theViewer.node.unit.unitType.name == "summoner"):
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
	def __init__(self,city):
		uiElement.__init__(self,-0.983,0.983,textureIndex=texIndex("UI_CITY_EDITOR_BACKGROUND_BACKGROUND"),height=texHeight("UI_CITY_EDITOR_BACKGROUND_BACKGROUND"),width=texWidth("UI_CITY_EDITOR_BACKGROUND_BACKGROUND"))
		self.names = []
		self.city = city
		self.names.append(cityNameInputElement(-0.972,0.746,width=texWidth('UI_TEXT_INPUT'),height=texHeight('UI_TEXT_INPUT'),text=self.city.name,textSize=0.0005,textColor='FF FF FF',textureIndex=texIndex('UI_TEXT_INPUT'),textYPos=-0.035,textXPos=0.01).name)
		height = 0.56
		for unitType in self.city.unitTypes:
			self.names.append(uiElement(-0.95,height,text=unitType.name,textSize=0.0005).name)
			self.names.append(uiElement(-0.75,height,text=str(unitType.costRed),textSize=0.0005).name)
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
		self.setScrollPosition(0)
	def onLeftClickDown(self):
		self.scrolling = True
		self.initMouseYPos = gameState.getGameMode().mouseY
		self.initYPos = self.yPosition
	def onLeftClickUp(self):
		self.scrolling = False
	def onMouseMovement(self):
		if(self.scrolling and self.numScrollablePositions > 0):
			self.yPosition = self.initYPos-(2.0*(gameState.getGameMode().mouseY-self.initMouseYPos)/cDefines.defines['SCREEN_HEIGHT'])
			if(self.yPosition > self.scrollableElement.yPosition - self.topOffset):
				self.yPosition = self.scrollableElement.yPosition - self.topOffset
			elif(self.yPosition < self.scrollableElement.yPosition - self.scrollableElement.height + self.height + self.bottomOffset):
				self.yPosition = self.scrollableElement.yPosition - self.scrollableElement.height + self.height + self.bottomOffset
			self.scrollableElement.scrollPosition = int(float(self.numScrollablePositions)*(self.scrollableElement.yPosition-self.topOffset-self.yPosition+0.001)/self.totalScrollableHeight)
			self.scrollableElement.hideAndShowTextFields()
	def setScrollPosition(self,scrollPos):
		self.numScrollablePositions = len(self.scrollableElement.textFieldElements) - self.scrollableElement.numFields
#		self.numScrollablePositions = len(self.scrollableElement.textFields) - self.scrollableElement.numFields
		self.totalScrollableHeight = self.scrollableElement.height - self.topOffset - self.bottomOffset - self.height
		if(self.numScrollablePositions > 0):
			self.yPosition = 0.0-((self.totalScrollableHeight*scrollPos/(self.numScrollablePositions))+self.topOffset-self.scrollableElement.yPosition)

class scrollableElement(uiElement):
	def setYPosition(self,yPos):
		if(hasattr(self,"names")):
			for name in self.names:
				gameState.getGameMode().elementsDict[name].yPosition = gameState.getGameMode().elementsDict[name].yPosition + yPos - self.yPosition
		self.yPosition = yPos

class buildUnitElem(scrollableElement):
	def __init__(self,xPos,yPos,summoner,unitType,index):
		scrollableElement.__init__(self,xPos,yPos)
		self.unitType = unitType
		self.summoner = summoner
		self.names.append(uiElement(self.xPosition,self.yPosition,textureIndex=texIndex("UNIT_UI_BACK"),height=texHeight("UNIT_UI_BACK"),width=texWidth("UNIT_UI_BACK")).name)
		self.names.append(unitTypeViewerButton(self.xPosition+0.009,self.yPosition-0.026,self.unitType,textureIndex=self.unitType.textureIndex,height=0.07,width=0.07).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name+"("+str(gameState.getResearchProgress()[self.unitType][0])+")",textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.071,textureIndex=texIndex("RED_WOOD_ICON"),width=texWidth("RED_WOOD_ICON")/4.0,height=texHeight("RED_WOOD_ICON")/4.0).name)
		self.names.append(uiElement(self.xPosition+0.106,self.yPosition-0.092,text=str(gameState.getResearchProgress()[self.unitType][0]*self.unitType.costRed),textSize=0.00038,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.151,self.yPosition-0.071,textureIndex=texIndex("BLUE_WOOD_ICON"),width=texWidth("BLUE_WOOD_ICON")/4.0,height=texHeight("BLUE_WOOD_ICON")/4.0).name)
		self.names.append(uiElement(self.xPosition+0.172,self.yPosition-0.092,text=str(gameState.getResearchProgress()[self.unitType][0]*self.unitType.costBlue),textSize=0.00038,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.221,self.yPosition-0.071,textureIndex=texIndex("TIME_ICON"),width=texWidth("TIME_ICON")/4.0,height=texHeight("TIME_ICON")/4.0).name)
		self.names.append(uiElement(self.xPosition+0.242,self.yPosition-0.092,text=str(self.unitType.buildTime),textSize=0.00038,textColor="ee ee ee",fontIndex=0).name)
		if(gameState.getGameMode().selectedNode.unit != None and gameState.getGameMode().selectedNode.unit.isControlled() and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()].redWood >= (gameState.getResearchProgress()[self.unitType][0]*self.unitType.costRed) and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()].blueWood >= (gameState.getResearchProgress()[unitType][0]*self.unitType.costBlue)):
#		if(gameState.getGameMode().selectedNode.unit != None and gameState.getGameMode().selectedNode.unit.isMeditating and gameState.getGameMode().selectedNode.unit.isControlled()):
			self.names.append(summonButton(self.xPosition+0.293,self.yPosition-0.068,self.unitType).name)

class researchUnitElem(scrollableElement):
	def __init__(self,xPos,yPos,summoner,unitType,index):
		scrollableElement.__init__(self,xPos,yPos)
		self.summoner = summoner
		self.unitType = unitType
		self.names.append(uiElement(self.xPosition,self.yPosition,textureIndex=texIndex("UNIT_UI_BACK"),height=texHeight("UNIT_UI_BACK"),width=texWidth("UNIT_UI_BACK")).name)
		self.names.append(unitTypeViewerButton(self.xPosition+23.0/cDefines.defines["SCREEN_WIDTH"],self.yPosition-23.0/cDefines.defines["SCREEN_HEIGHT"],self.unitType,textureIndex=self.unitType.textureIndex,height=70.0/cDefines.defines["SCREEN_HEIGHT"],width=70.0/cDefines.defines["SCREEN_WIDTH"]).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name+" lv "+ str(gameState.getResearchProgress()[self.unitType][0]+1),textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.071,textureIndex=texIndex("RED_WOOD_ICON"),width=texWidth("RED_WOOD_ICON")/4.0,height=texHeight("RED_WOOD_ICON")/4.0).name)
		self.names.append(uiElement(self.xPosition+0.106,self.yPosition-0.092,text=str(self.unitType.researchCostRed),textSize=0.00038,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.151,self.yPosition-0.071,textureIndex=texIndex("BLUE_WOOD_ICON"),width=texWidth("BLUE_WOOD_ICON")/4.0,height=texHeight("BLUE_WOOD_ICON")/4.0).name)
		self.names.append(uiElement(self.xPosition+0.172,self.yPosition-0.092,text=str(self.unitType.researchCostBlue),textSize=0.00038,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.221,self.yPosition-0.071,textureIndex=texIndex("TIME_ICON"),width=texWidth("TIME_ICON")/4.0,height=texHeight("TIME_ICON")/4.0).name)
		self.names.append(uiElement(self.xPosition+0.242,self.yPosition-0.092,text=str(self.unitType.buildTime),textSize=0.00038,textColor="ee ee ee",fontIndex=0).name)
		if(gameState.getGameMode().selectedNode.unit != None and gameState.getGameMode().selectedNode.unit.isControlled() and gameState.getGameMode().players[gameState.getGameMode().selectedNode.unit.player].redWood >= self.unitType.researchCostRed and gameState.getGameMode().players[gameState.getGameMode().selectedNode.unit.player].blueWood >= self.unitType.researchCostBlue):
#		if(gameState.getGameMode().selectedNode.unit != None and gameState.getGameMode().selectedNode.unit.isMeditating and gameState.getGameMode().selectedNode.unit.isControlled()):
			self.names.append(researchButton(self.xPosition+0.293,self.yPosition-0.068,self.unitType).name)

class queuedThingElem(scrollableElement):
	firstThing = True
	def __init__(self,xPos,yPos,summoner,unitThing,index):
		scrollableElement.__init__(self,xPos,yPos)
		self.summoner = summoner
		self.unit = None
		self.unitType = None
		if(hasattr(unitThing,"unitType")):#unit
			self.unit = unitThing
			self.unitType = self.unit.unitType
		else:
			self.unitType = unitThing
		self.names.append(uiElement(self.xPosition,self.yPosition,textureIndex=texIndex("UNIT_UI_BACK"),height=texHeight("UNIT_UI_BACK"),width=texWidth("UNIT_UI_BACK")).name)
		self.names.append(unitTypeViewerButton(self.xPosition+23.0/cDefines.defines["SCREEN_WIDTH"],self.yPosition-23.0/cDefines.defines["SCREEN_HEIGHT"],self.unitType,textureIndex=self.unitType.textureIndex,height=70.0/cDefines.defines["SCREEN_HEIGHT"],width=70.0/cDefines.defines["SCREEN_WIDTH"]).name)
		if(queuedThingElem.firstThing):
			queuedThingElem.firstThing = False
			if(self.unit != None):
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name+"("+str(self.unit.level)+")",textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR')*(summoner.unitBeingBuilt.unitType.buildTime-summoner.unitBeingBuilt.buildPoints)/summoner.unitBeingBuilt.unitType.buildTime,textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
			else:
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name+" lv "+str(gameState.getResearchProgress()[self.unitType][0]+1),textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR'),width=texWidth('UNIT_BUILD_BAR')*(float(gameState.getResearchProgress()[summoner.researchUnitType][1])/summoner.researchUnitType.researchTime),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
		else:
			if(self.unit != None):
#				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text="summon",textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name+"("+str(self.unit.level)+")",textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
			else:
#				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text="research",textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name+" lv "+str(gameState.getResearchProgress()[self.unitType][0]+1),textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
			self.names.append(cancelButton(self.xPosition+0.293,self.yPosition-0.068,index).name)

class scrollingTextElement(scrollableElement):
	def __init__(self,xPos,yPos,scrollableElement,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'])
		self.hidden = True
		self.lineHeight = 0
		self.scrollableElement = scrollableElement
	def onClick(self):
		if(hasattr(self.scrollableElement,"onClick")):
			self.scrollableElement.onClick(self)
class scrollableRoomNameElement(uiElement):
	def onClick(self):
		gameState.getGameFindClient().sendCommand("subscribe",self.text)

class scrollableMapNameElement(uiElement):
	def onClick(self):
		gameState.setMapName(self.text)
		gameState.setGameMode(gameModes.mapViewMode)

class scrollableRoomElement(scrollableElement):
	def __init__(self,xPos,yPos,roomName,mapName,playerCount,maxPlayerCount,text="",textSize=0.0005):
		scrollableElement.__init__(self,xPos,yPos,text="",textSize=textSize)
		self.names = []
		self.roomNameElem = scrollableRoomNameElement(xPos+0.008,yPos,text=roomName,textSize=textSize)
		self.names.append(self.roomNameElem.name)
		self.mapNameElem = scrollableMapNameElement(xPos+0.9,yPos,text=mapName,textSize=textSize)
		self.names.append(self.mapNameElem.name)
		self.roomCountElem = uiElement(xPos+1.36,yPos,text=str(playerCount) + "/" + str(maxPlayerCount),textSize=textSize)
		self.names.append(self.roomCountElem.name)

class scrollableTextFieldsElement(uiElement):
	def __init__(self,xPos,yPos,textFields,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.0005,color="FF FF FF",mouseOverColor=None,xPositionOffset=0.0,yPositionOffset=0.04,lineHeight=0.041,numFields=25,scrollSpeed=1,scrollPadTex="UI_SCROLL_PAD"):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.xPositionOffset = xPositionOffset
		self.yPositionOffset = yPositionOffset
		self.lineHeight = lineHeight
		self.numFields = numFields
		self.scrollSpeed = scrollSpeed
		self.scrollPosition = 0
		self.textFields = textFields
		self.textFieldElements = []
		self.names = []
		self.scrollPadTex = scrollPadTex
		self.scrollPadElem = scrollPadElement(self.xPosition + self.width - texWidth(self.scrollPadTex),self.yPosition,scrollableElement=self,width=texWidth(self.scrollPadTex),height=texHeight(self.scrollPadTex),textureIndex=texIndex(self.scrollPadTex),hidden=True)
		self.scrollPadElem.onScrollUp = self.onScrollUp
		self.scrollPadElem.onScrollDown = self.onScrollDown
		self.names.append(self.scrollPadElem.name)
		self.redraw()
	def redraw(self):
#		self.reset()
		for field in self.textFields:
			textFieldElem = None
			if(hasattr(field,"xPosition")):
#			if(True):
				textFieldElem = field
				textFieldElem.scrollableElement = self
				textFieldElem.xPosition = self.xPosition+self.xPositionOffset
#				gameState.getGameMode().elementsDict[textFieldElem.name] = textFieldElem
#				gameState.rendererUpdateQueue.put(rendererUpdates.addUIElem(textFieldElem))
#			else:
#				text = ""
#				if(hasattr(field,"name")):
#					text = field.name
#				else:
#					text=field
#				textFieldElem = scrollingTextElement(self.xPosition+self.xPositionOffset,0.0,self,width=2.0,height=0.1,text=text,textureIndex=-1,textSize=self.textSize,hidden=True)
				textFieldElem.onScrollUp = self.onScrollUp
				textFieldElem.onScrollDown = self.onScrollDown
				for name in textFieldElem.names:
					gameState.getGameMode().elementsDict[name].onScrollUp = self.onScrollUp
					gameState.getGameMode().elementsDict[name].onScrollDown = self.onScrollDown
#			self.names.append(textFieldElem.name)
			self.textFieldElements.append(textFieldElem)
		self.hideAndShowTextFields()
#		self.scrollPadElem = scrollPadElement(self.xPosition + self.width - texWidth(self.scrollPadTex),self.yPosition,scrollableElement=self,width=texWidth(self.scrollPadTex),height=texHeight(self.scrollPadTex),textureIndex=texIndex(self.scrollPadTex),hidden=True)

#			self.scrollPadElem = None
#		else:
#			self.scrollPadElem = scrollPadElement(self.xPosition + self.width - texWidth(self.scrollPadTex),self.yPosition,scrollableElement=self,width=texWidth(self.scrollPadTex),height=texHeight(self.scrollPadTex),textureIndex=texIndex(self.scrollPadTex),hidden=True)
#		if(len(self.textFields) > self.numFields):
		self.scrollPadElem.setScrollPosition(self.scrollPosition)
	def hideAndShowTextFields(self):
		count = 0
		yPosOffset = 0-self.yPositionOffset
		for textFieldElement in self.textFieldElements:
			textFieldElement.setYPosition(self.yPosition+yPosOffset)
			if(not self.hidden and count < self.numFields + self.scrollPosition and count > self.scrollPosition - 1):
				yPosOffset = yPosOffset - self.lineHeight
				textFieldElement.hidden = False
				for name in textFieldElement.names:
					gameState.getGameMode().elementsDict[name].hidden = False
			else:
				textFieldElement.hidden = True
				for name in textFieldElement.names:
					gameState.getGameMode().elementsDict[name].hidden = True
			count = count + 1
	def onScrollUp(self):
		if(self.scrollPadElem != None):
			self.scrollPosition = self.scrollPosition - self.scrollSpeed
			if(self.scrollPosition < 0):
				self.scrollPosition = 0
			self.hideAndShowTextFields()
			self.scrollPadElem.setScrollPosition(self.scrollPosition)
	def onScrollDown(self):
		if(self.scrollPadElem != None):
			self.scrollPosition = self.scrollPosition + self.scrollSpeed
			if(self.scrollPosition > len(self.textFieldElements) - self.numFields):
				self.scrollPosition = len(self.textFieldElements) - self.numFields
			self.hideAndShowTextFields()
			self.scrollPadElem.setScrollPosition(self.scrollPosition)
	def reset(self):
#		for name in self.names:
#			print gameState.getGameMode().elementsDict[name].names
#			gameState.getGameMode().elementsDict[name].destroy()
			#del gameState.getGameMode().elementsDict[name]
#		self.names = []
#		self.textFields = []
		self.textFieldElements = []

class summonerUnitsDisplay(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,unitTypes,summoner,unitElemClass):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,[],height=texHeight("QUEUE_BORDER")-0.015,width=texWidth("QUEUE_BORDER"),xPositionOffset=0.01,yPositionOffset=0.014,lineHeight=0.127,numFields=4,scrollPadTex="SCROLL_BAR")
		self.unitTypes = unitTypes
		self.summoner = summoner
		index = 0
		for unitType in self.unitTypes:
			elem = unitElemClass(self.xPosition+self.xPositionOffset,0.0,summoner,unitType,index)
			self.textFields.append(elem)
			self.names.append(elem.name)
			index = index + 1
		self.redraw()

class chatDisplay(scrollableTextFieldsElement):
	#The goal here is to hold lines of text that are too long in textQueue and run them thru a function in fonts.h which will tell us how many words will constitute one line. This way we can add the text as a textFieldElement in order to reuse all the scrollableTextFields code.
	def __init__(self,xPos,yPos,textureName="CHAT_DISPLAY"):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,[],textSize=0.0005,textureIndex=texIndex(textureName),width=texWidth(textureName),height=texHeight(textureName),numFields=36,xPositionOffset=0.02,yPositionOffset=0.05)
		self.textQueue = Queue()
		self.linesQueue = Queue()
		self.currentText = ""
	def addLine(self,wordLength):
		if(wordLength == 0):
			wordLength = 1
		if(self.currentText != "" and wordLength > 0):
			wordTokens = self.currentText.split(" ",wordLength)
			if(len(wordTokens) > wordLength):
				self.currentText = wordTokens[wordLength]
			else:
				self.currentText = ""
			self.textFields.append(" ".join(wordTokens[:wordLength]))
			self.redraw()
			if(self.scrollPadElem != None and self.scrollPosition <= self.scrollPadElem.numScrollablePositions):
				self.scrollPosition = self.scrollPadElem.numScrollablePositions+1
				self.redraw()
	def addText(self,text):
		self.textQueue.put(text)
		if(hasattr(gameState.getGameMode(),"lastChatTicks")):
			gameState.getGameMode().lastChatTicks = gameState.getGameMode().ticks
			self.hidden = False
			self.hideAndShowTextFields()
		   
	def getText(self):
		if(self.currentText == "" and not self.textQueue.empty()):
			self.currentText = self.textQueue.get()
		return self.currentText

class inGameChatDisplay(chatDisplay):
	def __init__(self,xPos,yPos):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,[],hidden=True,textSize=0.0005,numFields=3,width=0.980-xPos,scrollPadTex="UI_SCROLL_PAD_DUMMY")
		self.textQueue = Queue()
		self.linesQueue = Queue()
		self.currentText = ""
	

class roomSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,rooms,width=0.0,height=0.0,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,[],width=texWidth("ROOMS_DISPLAY"),height=texHeight("ROOMS_DISPLAY"),textureIndex=texIndex("ROOMS_DISPLAY"),text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor,xPositionOffset=0.01,yPositionOffset=0.06,lineHeight=0.041)
		self.rooms = rooms
		for room in rooms:
			self.textFields.append(scrollableRoomElement(self.xPosition+self.xPositionOffset,0.0,room[0],room[1],room[2],2*int(room[3])))
		self.redraw()
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
	def onClick(self,textFieldElem=None):
		if(textFieldElem!=None):
			for unitType in gameState.theUnitTypes.values():
				if(unitType.name == textFieldElem.text):
					cityEditor.theCityEditor.addUnitType(unitType)
			self.destroy()

class gameTypeButton(clickableElement):
	buttons = []
	def __init__(self,xPos,yPos,textureStr,teamSize,selected,offColor="88 88 88"):
		self.offColor = offColor
		self.onColor = "FF FF FF"
		if(selected):
			color = self.onColor
		else:
			color = self.offColor
		clickableElement.__init__(self,xPos,yPos,width=texWidth(textureStr),height=texHeight(textureStr),textureIndex=texIndex(textureStr),color=color)
		self.teamSize = teamSize
		gameTypeButton.buttons.append(self)
		self.selected = selected
	def onClick(self):
		for button in gameTypeButton.buttons:
			button.color = self.offColor
			button.selected = False
		self.color = self.onColor
		self.selected = True
		gameState.setTeamSize(self.teamSize)
		if(hasattr(gameState.getGameMode(),"hostGameMode")):
			gameState.getGameMode().setMap(gameState.getMapDatas()[self.teamSize-1][0].name)
		gameState.getGameMode().soundIndeces.append(cDefines.defines["FINGER_CYMBALS_HIT_INDEX"])

class da1v1Button(gameTypeButton):
	def __init__(self,xPos,yPos,offColor="88 88 88"):
		gameTypeButton.__init__(self,xPos,yPos,"DA_1V1_BUTTON",1,True,offColor=offColor)

class da2v2Button(gameTypeButton):
	def __init__(self,xPos,yPos,offColor="88 88 88"):
		gameTypeButton.__init__(self,xPos,yPos,"DA_2V2_BUTTON",2,False,offColor=offColor)

class da3v3Button(gameTypeButton):
	def __init__(self,xPos,yPos,offColor="88 88 88"):
		gameTypeButton.__init__(self,xPos,yPos,"DA_3V3_BUTTON",3,False,offColor=offColor)

class da4v4Button(gameTypeButton):
	def __init__(self,xPos,yPos,offColor="88 88 88"):
		gameTypeButton.__init__(self,xPos,yPos,"DA_4V4_BUTTON",4,False,offColor=offColor)

class createRoomButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,width=texWidth("CREATE_GAME_BUTTON"),height=texHeight("CREATE_GAME_BUTTON"),textureIndex=texIndex("CREATE_GAME_BUTTON"))
	def onClick(self):
		try:
			server.startServer('')
		except socket.error, msg:
			socketErrorModal()
			print 'server start error'
			print socket.error
			print msg
			return
#		try:
#			client.startClient('127.0.0.1')
#		except socket.error, msg:
#			socketErrorModal()
#			print 'client start error'
#			print socket.error
#			print msg
#			return
		teamSize = 0
		for button in gameTypeButton.buttons:
			if(button.selected):
				teamSize = button.teamSize
				break
		gameState.getGameFindClient().sendCommand("testServer",gameState.getConfig()["serverPort"])
		gameState.setGameMode(gameModes.createGameMode)
		smallModal("testing connection...",dismissable=False)
		gameState.setTeamSize(teamSize)
		gameState.getGameMode().setMap(gameState.getMapDatas()[teamSize-1][0].name)

class chatBox(textInputElement):
	def __init__(self,xPos,yPos,klient,textureName="CHAT_BOX"):
		textInputElement.__init__(self,xPos,yPos,text="",textSize=0.0005,textureIndex=texIndex(textureName),width=texWidth(textureName),textColor="FF FF FF",textXPos=0.02,textYPos=-0.045)
		self.klient = klient
	def sendChat(self):
		if(len(self.realText) > 0):
			self.klient.sendCommand("chat",gameState.getOwnUserName()+": "+self.realText)
			self.realText = ""
			self.text = ""
			self.cursorPosition = 0
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			self.sendChat()
			return
		elif(keycode == "tab"):
			return
		else:
			textInputElement.onKeyDown(self,keycode)

class sendChatButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,width=texWidth("SEND_BUTTON"),height=texHeight("SEND_BUTTON"),textureIndex=texIndex("SEND_BUTTON"))
	def onClick(self):
		gameState.getGameMode().chatBox.sendChat()

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
		unitTypeSelector(self.xPosition,self.yPosition-0.06,gameState.theUnitTypes.values(),text="select unit",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class removeUnitTypeButton(clickableElement):
	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)

		self.unitType = unitType
	def onClick(self):
		cityEditor.theCityEditor.city.unitTypes.remove(self.unitType)
		cityEditor.reset()


class unitCostField(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		unitCostSelector(self.xPosition,self.yPosition-0.06,unitCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class startingManaField(clickableElement):
       	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
	def onClick(self):
		startingManaSelector(self.xPosition,self.yPosition-0.06,startingManas,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))


#class unitBuildTimeField(clickableElement):
#       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
#		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
#		self.unitType = unitType
#	def onClick(self):
#		unitBuildTimeSelector(self.xPosition,self.yPosition-0.06,unitBuildTimes,self,text="select build timeGET RID OF THIS",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

	

class openMenuButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("MENU_BUTTON"),height=texHeight("MENU_BUTTON"),width=texWidth("MENU_BUTTON"))
	def onClick(self):
		menuModal()

class menuButton(clickableElement):
	index = 0
	buttonsList = []
	selectedIndex = 0
	selectedTextColor = "aa aa aa"
	normalTextColor = "1f 10 10"
	currentGameMode = None
	def __init__(self,xPos,yPos,text="",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=2.0,text=text,textColor=menuButton.normalTextColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],mouseOverColor=menuButton.selectedTextColor,textSize=0.0013,fontIndex=1)
		if(menuButton.currentGameMode != gameState.getGameMode()):
			menuButton.index = 0
			menuButton.buttonsList = []
			menuButton.selectedIndex = 0
		self.selected = selected
		self.index = menuButton.index
		menuButton.currentGameMode = gameState.getGameMode()
		menuButton.buttonsList.append(self)
		menuButton.index = menuButton.index + 1
		if(self.index == menuButton.selectedIndex):
			self.textColor = menuButton.selectedTextColor
	def onClick(self):
		print 'override me'

class menuButtonGameModeSelector(menuButton):
	def __init__(self,xPos,yPos,gameMode,text=""):
		menuButton.__init__(self,xPos,yPos,text=text)
		self.gameMode = gameMode
	def onClick(self):
		gameState.setGameMode(self.gameMode)
		gameState.getGameMode().soundIndeces.append(cDefines.defines["DARBUKA_HIT_INDEX"])

class mapEditSelectButton(menuButtonGameModeSelector):
	def onClick(self):
		if(self.text == "create new map"):#TODO: someone naming a map "create new map" would fuck this up, break this into separate classes
			gameState.setGameMode(self.gameMode)
		else:
			gameState.setMapName(self.text)
			gameState.setGameMode(self.gameMode)

class mapPlaySelectButton(menuButtonGameModeSelector):
	def onClick(self):
		gameState.setMapName(self.text)
		gameState.setTeamSize(1)
		gameState.setGameMode(self.gameMode)

class exitButton(menuButton):
	def __init__(self,xPos,yPos,text="Exit"):
		menuButton.__init__(self,xPos,yPos,text=text)
	def onClick(self):
		gameState.rendererUpdateQueue.put(rendererUpdates.exit())
#		gameState.getGameMode().exit = True

class savedGameSelector(scrollableTextFieldsElement):
	def __init__(self):
		dirList=os.listdir("saves")
		textFields = []
		for fileName in dirList:
			if((not fileName.startswith(".")) and (fileName.endswith("sav"))):
				textFields.append(fileName[:-4])
		scrollableTextFieldsElement.__init__(self,-0.5*texWidth("MAP_SELECTOR"),0.76,textFields,width=texWidth("MAP_SELECTOR"),height=texHeight("MAP_SELECTOR"),textureIndex=texIndex("MAP_SELECTOR"),numFields=38,lineHeight=0.036,xPositionOffset=0.015,yPositionOffset=0.045,scrollSpeed=10)
	def onClick(self,textFieldElem=None):
		if(textFieldElem != None):
			gameLogic.loadGame(textFieldElem.text)

class mapSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,mapField):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=texWidth("MAP_SELECTOR"),height=texHeight("MAP_SELECTOR"),textureIndex=texIndex("MAP_SELECTOR"),numFields=38,lineHeight=0.036,xPositionOffset=0.015,yPositionOffset=0.045,scrollSpeed=10)
		self.mapField = mapField
		for mapData in gameState.getMapDatas()[gameState.getTeamSize()-1]:
			self.textFields.append(mapSelect(-0.93,0.0,self,mapData.name))
		self.redraw()

#	def onClick(self,textFieldElem):
#		server.setMap(textFieldElem.text)
#		self.mapField.text = textFieldElem.text
#		self.destroy()

class mapSelect(scrollingTextElement):
	def __init__(self,xPos,yPos,scrollableElement,text):
		scrollingTextElement.__init__(self,xPos,yPos,scrollableElement,text=text,textSize=0.0005,width=texWidth("MAP_SELECTOR"))
	def onClick(self):
		gameState.getGameMode().setMap(self.text)

class onlineMapSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,mapField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=0.04,lineHeight=0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.mapField = mapField
#	def onClick(self,fieldElem):
#		self.mapField.text = fieldElem.text
#		self.mapField.mapName = fieldElem.text
#		self.destroy()

#class mapSelector(scrollableTextFieldsElement):
#	def __init__(self,xPos,yPos,textFields,mapField):
#		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=texWidth("MAP_SELECTOR"),height=texHeight("MAP_SELECTOR"),textureIndex=texIndex("MAP_SELECTOR"))
#		self.mapField = mapField
#	def onClick(self,fieldElem):
#		print fieldElem.text
		

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
		self.selector(self.xPosition,self.yPosition-0.06,mapNames,self,text="select build time",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

#I think all this maxPlayers crap is deprecated, but want to test map editor before deleting
#class maxPlayersSelector(scrollableTextFieldsElement):
#	def onClick(self,fieldElem):
#		gameState.getGameMode().maxPlayersField.text = fieldElem.text + " players"
#		self.destroy()
#class maxPlayersField(clickableElement):
#	def onClick(self):
#		maxPlayersSelector(self.xPosition,self.yPosition-0.06,["1","2","4","8"],textSize=0.0006)

#class createButton(menuButton):
#	def onClick(self):
#		if(gameState.getGameMode().mapField.mapName != None):
#			gameState.getGameFindClient().sendCommand("createGameRoom",gameState.getGameMode().titleField.text + "|" + gameState.getGameMode().maxPlayersField.text.split(" ")[0] + "|" + gameState.getGameMode().mapField.mapName)
#		else:
#			smallModal("Choose a map!")

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

class startButton(menuButtonGameModeSelector):
	def onClick(self):
		server.startGame()


class loginInputElement(textInputElement):
	usernameElem = None
	passwordElem = None
	def __init__(self,xPos,yPos,text,isPassword=False):
		textInputElement.__init__(self,xPos,yPos,text=text,isPassword=isPassword)
	@staticmethod
	def doLogin():
		gameState.getGameFindClient().sendCommand("login",loginInputElement.usernameElem.realText + " " + loginInputElement.passwordElem.realText)
		gameState.setOwnUserName(loginInputElement.usernameElem.realText)
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			loginInputElement.doLogin()
		elif(keycode == "tab"):
			for index,elem in enumerate(textInputElement.elements):
				if(elem.focused):
					if(index >= len(textInputElement.elements)-1):
						gameState.getGameMode().setFocusedElem(textInputElement.elements[0])
					else:
						gameState.getGameMode().setFocusedElem(textInputElement.elements[index+1])
					break
		elif(keycode == "space"):
			return
		else:
			textInputElement.onKeyDown(self,keycode)

class loginUserName(loginInputElement):
	def __init__(self,xPos,yPos,text="clayrab"):
		loginInputElement.__init__(self,xPos,yPos,text=text)
		loginInputElement.usernameElem = self

class loginPassword(loginInputElement):
	def __init__(self,xPos,yPos,text="maskmask"):
		loginInputElement.__init__(self,xPos,yPos,text=text,isPassword=True)
		loginInputElement.passwordElem = self

class loginButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("LOGIN_BUTTON"),height=texHeight("LOGIN_BUTTON"),width=texWidth("LOGIN_BUTTON"))
	def onClick(self):
		loginInputElement.doLogin()
		
class modalButton(clickableElement):
	def __init__(self,modal,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0,fontIndex=0):
		self.modal = modal
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos,fontIndex=fontIndex)

class modalTextInput(textInputElement):
	def __init__(self,modal,xPos,yPos,width=0.0,height=0.0,text="",textColor="FF FF FF"):
		self.modal = modal
		textInputElement.__init__(self,xPos,yPos,width=texWidth("UI_TEXT_INPUT"),height=texHeight("UI_TEXT_INPUT"),textureIndex=texIndex("UI_TEXT_INPUT"),text=text,textColor=textColor)


class modalOkButton(modalButton):
	def __init__(self,modal,yPos=-0.05,text="",textureIndex=cDefines.defines["OK_BUTTON_INDEX"]):
		modalButton.__init__(self,modal,texWidth("OK_BUTTON")/-2.0,yPos,text=text,width=texWidth("OK_BUTTON"),height=texHeight("OK_BUTTON"),textureIndex=textureIndex,textXPos=0.1,textYPos=-0.1)
	def onClick(self):
		self.modal.destroy()

class inGameMenuButton(modalButton):
	def __init__(self,modal,xPos,yPos,text=""):
		modalButton.__init__(self,modal,xPos,yPos,width=2.0,text=text,textColor="bb bb bb",cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],mouseOverColor="88 88 88",textSize=0.0013,fontIndex=1)

class resumeButton(inGameMenuButton):
	def __init__(self,modal,xPos,yPos,text="Resume"):
		inGameMenuButton.__init__(self,modal,xPos,yPos,text=text)
	def onClick(self):
		self.modal.destroy()

class saveGameButton(inGameMenuButton):
	def __init__(self,modal,xPos,yPos,text="Save"):
		inGameMenuButton.__init__(self,modal,xPos,yPos,text=text)
	def onClick(self):
		self.modal.destroy()
		saveGameModal()

class doSaveGameButton(inGameMenuButton):
	def __init__(self,modal,xPos,yPos,text="OK"):
		inGameMenuButton.__init__(self,modal,xPos,yPos,text=text)
	def onClick(self):
		gameLogic.saveGame(self.modal.saveNameInput.realText)
		self.modal.destroy()

class saveNameInput(modalTextInput):
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			gameLogic.saveGame(self.modal.saveNameInput.realText)
		else:
			textInputElement.onKeyDown(self,str(keycode))

def exitGame():
	gameState.setGameMode(gameModes.newGameScreenMode)
	client.stopClient()
	server.shutdownServer()

class exiitButton(inGameMenuButton):
	def __init__(self,modal,xPos,yPos,text="Exit"):
		inGameMenuButton.__init__(self,modal,xPos,yPos,text=text)
	def onClick(self):
		exitGame()

class cancelSaveButton(inGameMenuButton):
	def __init__(self,modal,xPos,yPos,text="Cancel"):
		inGameMenuButton.__init__(self,modal,xPos,yPos,text=text)
	def onClick(self):
		gameState.getGameMode().modal.destroy()

class modal(uiElement):
	def destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		if(hasattr(self,"textElem")):
			   del gameState.getGameMode().elementsDict[self.textElem.name]
		if(hasattr(self,"backgroundElem")):
			del gameState.getGameMode().elementsDict[self.backgroundElem.name]
		if(hasattr(self,"buttonElem")):
			del gameState.getGameMode().elementsDict[self.buttonElem.name]
		gameState.getGameMode().resortElems = True
		gameState.getGameMode().modal = None
		gameState.getGameMode().elementWithFocus = None

class chatModalTextInput(modalTextInput):
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			if(len(self.realText) > 0):
				gameState.getClient().sendCommand("chat",gameState.getOwnUserName()+": "+self.realText)	
			self.modal.destroy()
		else:
			textInputElement.onKeyDown(self,str(keycode))
		
class chatModal(modal):
	def __init__(self,dismissable=True):
		uiElement.__init__(self,0.0,0.0)
		self.names = []
		self.chatTextInput = chatModalTextInput(self,-0.25,0.14)
		self.names.append(self.chatTextInput.name)
		self.dismissable = dismissable
		gameState.getGameMode().modal = self
		gameState.getGameMode().elementWithFocus = self.chatTextInput

class menuModal(modal):
	def __init__(self,dismissable=True):
		uiElement.__init__(self,-1.0,1.0,width=texWidth("MENU_MODAL"),height=texHeight("MENU_MODAL"),textureIndex=texIndex("MENU_MODAL"))
		self.names = []
		self.dismissable = dismissable
		self.names.append(resumeButton(self,-0.12,0.2).name)
		self.names.append(saveGameButton(self,-0.07,0.0).name)
		self.exitButton = exiitButton(self,-0.06,-0.2)
		self.names.append(self.exitButton.name)
		gameState.getGameMode().modal = self

class saveGameModal(modal):
	def __init__(self,dismissable=True):
		uiElement.__init__(self,-1.0,1.0,width=texWidth("MENU_MODAL"),height=texHeight("MENU_MODAL"),textureIndex=texIndex("MENU_MODAL"))
		self.names = []
		self.dismissable = dismissable
#		self.names.append(uiElement(-0.12,0.26,text="save name:",textColor="bb bb bb",textSize=0.0008,fontIndex=1).name)
		
		self.saveNameInput = saveNameInput(self,-0.25,0.14,text="MySave")
		self.names.append(self.saveNameInput.name)
		self.names.append(doSaveGameButton(self,0.160,0.080).name)
		self.exitButton = cancelSaveButton(self,0.062,-0.080)
		self.names.append(self.exitButton.name)
		gameState.getGameMode().modal = self

class smallModal(modal):
	def __init__(self,text,dismissable=True):
		uiElement.__init__(self,texWidth("MODAL_SMALL")/-2.0,texHeight("MODAL_SMALL")/2.0,width=texWidth("MODAL_SMALL"),height=texHeight("MODAL_SMALL"),textureIndex=cDefines.defines["MODAL_SMALL_INDEX"])
		self.dismissable = dismissable
		self.backgroundElem = uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines.defines["MODAL_BACKGROUND_INDEX"])
		self.textElem = uiElement((texWidth("MODAL_SMALL")/-2.0)+0.03,0.1,width=texWidth("MODAL_SMALL")-0.06,text=text,textSize=0.0007,textColor="ee ed 9b")
		if(self.dismissable):
			self.buttonElem = modalOkButton(self,self.yPosition-0.4)
		gameState.getGameMode().modal = self

class disconnectOkButton(modalButton):
	def __init__(self,modal,yPos=-0.05,text="",textureIndex=cDefines.defines["OK_BUTTON_INDEX"]):
		modalButton.__init__(self,modal,texWidth("OK_BUTTON")/-2.0,yPos,text=text,width=texWidth("OK_BUTTON"),height=texHeight("OK_BUTTON"),textureIndex=textureIndex,textXPos=0.1,textYPos=-0.1)
	def onClick(self):
		exitGame()

class playerDisconnectedModal(smallModal):
        def __init__(self):
		print 'disconnected modal'
		smallModal.__init__(self,"",dismissable=True)
		yPos = 0.23
		for player in gameState.getPlayers():
			if(player != None):
				yPos = yPos - 0.05
				if(player.playerNumber in gameState.getGameMode().missingPlayers):
					self.names.append(uiElement(self.xPosition+0.05,yPos,text="Player " + str(player.playerNumber) + " disconnected",textSize=0.0005).name)
				else:
					self.names.append(uiElement(self.xPosition+0.05,yPos,text="Player " + str(player.playerNumber) + " ok",textSize=0.0005).name)
		disconnectOkButton(self,self.yPosition-0.4)


class winLoseModalButton(clickableElement):
	def __init__(self,modal):
		clickableElement.__init__(self,texWidth("OK_BUTTON")/-2.0,0.0,textXPos=0.08,textYPos=-0.08,textureIndex=texIndex("OK_BUTTON"),width=texWidth("OK_BUTTON"),height=texHeight("OK_BUTTON"))
		self.modal = modal
	def onClick(self):
		gameState.setGameMode(gameModes.newGameScreenMode)

class winModal(smallModal):
	def __init__(self):
		smallModal.__init__(self,"You win",dismissable=False)
		winLoseModalButton(self)

class loseModal(smallModal):
	def __init__(self):
		smallModal.__init__(self,"You lose",dismissable=False)
		winLoseModalButton(self)

class socketErrorModalButton(clickableElement,modal):
	def __init__(self,modal):
		clickableElement.__init__(self,texWidth("OK_BUTTON")/-2.0,0.0,textXPos=0.08,textYPos=-0.08,textureIndex=texIndex("OK_BUTTON"),width=texWidth("OK_BUTTON"),height=texHeight("OK_BUTTON"))
		self.modal = modal
	def onClick(self):
		gameState.getGameFindClient().sendCommand("subscribe","lobby")

class socketErrorModal(smallModal):
	def __init__(self):
		smallModal.__init__(self,"Cannot create server. The socket may be in use. Try again in 30 seconds.",dismissable=False)
		socketErrorModalButton(self)

class lanConnectErrorModalButton(clickableElement,modal):
	def __init__(self,modal):
		clickableElement.__init__(self,texWidth("OK_BUTTON")/-2.0,0.0,textXPos=0.08,textYPos=-0.08,textureIndex=texIndex("OK_BUTTON"),width=texWidth("OK_BUTTON"),height=texHeight("OK_BUTTON"))
		self.modal = modal
	def onClick(self):
		gameState.setGameMode(gameModes.newGameScreenMode)

class lanConnectErrorModal(smallModal):
	def __init__(self):
		smallModal.__init__(self,"Cannot connect.",dismissable=False)
		lanConnectErrorModalButton(self)

class createMapButton(clickableElement):
	def __init__(self,xPos,yPos,gameMode,text=""):
		clickableElement.__init__(self,xPos,yPos,width=1.0,height=1.0,text=text,textColor=menuButton.normalTextColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],mouseOverColor="66 66 66",textSize=0.0013,fontIndex=1)
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
				shutil.copyfile("maps/defaultMap"+str(numPlayers),"maps/" + mapName + ".map")
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
			gameState.getGameMode().setFocusedElem(gameState.getGameMode().mapPlayerCountInputElement)
		else:
			if(keycode != "return"):
				textInputElement.onKeyDown(self,keycode)

class newMapPlayerCountInputElement(textInputElement):
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,text="",textSize=0.001,textureIndex=-1,textColor='FF FF FF',textXPos=0.0,textYPos=0.0):
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
		self.gameMode = gameMode
	def onKeyDown(self,keycode):
		if(keycode == "tab"):
			gameState.getGameMode().setFocusedElem(gameState.getGameMode().mapNameInputElement)
		else:
			if(keycode == "0" or keycode == "1" or keycode == "2" or keycode == "3" or keycode == "4" or keycode == "5" or keycode == "6" or keycode == "7" or keycode == "8" or keycode == "9" or keycode == "backspace"):
				textInputElement.onKeyDown(self,keycode)

#class roomNameInputElement(textInputElement):
#	def __init__(self,xPos,yPos):
#		textInputElement.__init__(self,xPos,yPos)

#
class createGameButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("CREATE_GAME_BUTTON_LARGE"),width=texWidth("CREATE_GAME_BUTTON_LARGE"),height=texHeight("CREATE_GAME_BUTTON_LARGE"))
	def onClick(self):
		gameState.getGameFindClient().sendCommand("createGameRoom",gameState.getGameMode().roomNameField.realText + "|" + str(gameState.getTeamSize()) + "|" + gameState.getGameMode().mapNameField.text)
		gameState.getGameMode().soundIndeces.append(cDefines.defines["DARBUKA_HIT_INDEX"])

class createGameButtun(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("CREATE_GAME_BUTTON_LARGE"),width=texWidth("CREATE_GAME_BUTTON_LARGE"),height=texHeight("CREATE_GAME_BUTTON_LARGE"))
	def onClick(self):
		try:
			server.startServer('',6666)
		except socket.error:
			gameState.setGameMode(gameModes.newGameScreenMode)
			smallModal("Cannot create server. The socket may be in use, try again in 30 seconds.")
			print "socket.error:"
			print socket.error
		gameState.setGameMode(gameModes.lanGameRoomMode,["127.0.0.1"])
		gameState.getGameMode().soundIndeces.append(cDefines.defines["DARBUKA_HIT_INDEX"])
#		try:
#			client.startClient('127.0.0.1',6666)
#		except socket.error:
#			gameState.setGameMode(gameModes.newGameScreenMode)
#			smallModal("Cannot connect to server... Try again in 30 seconds.")


class onlineBackButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BACK_BUTTON"),width=texWidth("BACK_BUTTON"),height=texHeight("BACK_BUTTON"))
	def onClick(self):
		gameState.getGameFindClient().sendCommand("subscribe","lobby")
		gameState.getGameMode().soundIndeces.append(cDefines.defines["DARBUKA_HIT_INDEX"])


class lanBackButton(clickableElement):
	def __init__(self,xPos,yPos,gameMode):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BACK_BUTTON"),width=texWidth("BACK_BUTTON"),height=texHeight("BACK_BUTTON"))
		self.gameMode = gameMode
	def onClick(self):
#		gameState.getClient().sendCommand("removePlayer",str(gameState.getPlayerNumber()))
#		gameState.setGameMode(self.gameMode)
		gameState.getGameMode().soundIndeces.append(cDefines.defines["DARBUKA_HIT_INDEX"])
		exitGame()

class backButton(clickableElement):
	def __init__(self,xPos,yPos,gameMode):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BACK_BUTTON"),width=texWidth("BACK_BUTTON"),height=texHeight("BACK_BUTTON"))
		self.gameMode = gameMode
	def onClick(self):
		gameState.setGameMode(self.gameMode)
		gameState.getGameMode().soundIndeces.append(cDefines.defines["DARBUKA_HIT_INDEX"])

class logoutButton(clickableElement):
	def __init__(self,xPos,yPos,gameMode):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BACK_BUTTON"),width=texWidth("BACK_BUTTON"),height=texHeight("BACK_BUTTON"))
		self.gameMode = gameMode
	def onClick(self):
		gameFindClient.stopClient()
		gameState.setGameMode(self.gameMode)
	

class startGameButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("START_BUTTON"),width=texWidth("START_BUTTON"),height=texHeight("START_BUTTON"))
	def onClick(self):
		server.startGame()

class addAIButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("ADD_AI_BUTTON"),width=texWidth("ADD_AI_BUTTON"),height=texHeight("ADD_AI_BUTTON"))
	def onClick(self):
		server.addAIPlayer()
		gameState.getGameMode().soundIndeces.append(cDefines.defines["FINGER_CYMBALS_HIT_INDEX"])

#class autoSelectCheckBox(clickableElement):
#	def __init__(self,xPos,yPos):
#		self.textureName = "CHECK_MARK"
#		if(gameState.getGameMode().autoSelect):
#			self.textureName = "CHECK_MARK_CHECKED"
#		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex(self.textureName),width=texWidth(self.textureName),height=texHeight(self.textureName))
#		uiElement(self.xPosition+0.03,self.yPosition-0.034,text="auto-select units",textSize=0.00045)
#	def onClick(self):
#		gameState.getGameMode().autoSelect = not gameState.getGameMode().autoSelect
#		if(gameState.getGameMode().autoSelect):
#			self.textureName = "CHECK_MARK_CHECKED"
#		else:
#			self.textureName = "CHECK_MARK"
#		self.textureIndex = texIndex(self.textureName)

#class watchFriendlyMovesCheckBox(clickableElement):
#	def __init__(self,xPos,yPos):
#		self.textureName = "CHECK_MARK"
#		if(gameState.getGameMode().watchFriendlyMoves):
#			self.textureName = "CHECK_MARK_CHECKED"
#		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex(self.textureName),width=texWidth(self.textureName),height=texHeight(self.textureName))
#		uiElement(self.xPosition+0.03,self.yPosition-0.034,text="show moves",textSize=0.00045)
#	def onClick(self):
#		gameState.getGameMode().watchFriendlyMoves = not gameState.getGameMode().watchFriendlyMoves
#		if(gameState.getGameMode().watchFriendlyMoves):
#			self.textureName = "CHECK_MARK_CHECKED"
#		else:
#			self.textureName = "CHECK_MARK"
#		self.textureIndex = texIndex(self.textureName)

#class watchEnemyMovesCheckBox(clickableElement):
#	def __init__(self,xPos,yPos):
#		self.textureName = "CHECK_MARK"
#		if(gameState.getGameMode().watchEnemyMoves):
#			self.textureName = "CHECK_MARK_CHECKED"
#		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex(self.textureName),width=texWidth(self.textureName),height=texHeight(self.textureName))
#		uiElement(self.xPosition+0.03,self.yPosition-0.034,text="show enemy moves",textSize=0.00045)
#	def onClick(self):
#		gameState.getGameMode().watchEnemyMoves = not gameState.getGameMode().watchEnemyMoves
#		if(gameState.getGameMode().watchEnemyMoves):
#			self.textureName = "CHECK_MARK_CHECKED"
#		else:
#			self.textureName = "CHECK_MARK"
#		self.textureIndex = texIndex(self.textureName)

