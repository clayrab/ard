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
	def __init__(self,xPos,yPos,width=1.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor=None,textSize=0.001,color=None,mouseOverColor=None,textXPos=0.0,textYPos=0.0,cursorPosition=-1,fontIndex=0,frameLength=10,frameCount=1):
		self.name = nameGenerator.getNextName()
		self.xPosition = xPos
		self.yPosition = yPos
		self.width = width
		self.height = height/frameCount
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
		self.frameLength = frameLength
		self.frameCount = frameCount
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
		self.names = []
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
	def __init__(self,xPos,yPos,isPassword=False,width=texWidth('UI_TEXT_INPUT_IMAGE'),height=texHeight('UI_TEXT_INPUT_IMAGE'),text="",textureIndex=texIndex('UI_TEXT_INPUT'),textColor='DD DD DD',textSize=0.0006,textXPos=0.010,textYPos=-0.045,fontIndex=0):
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

class hostIPConnectButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("CONNECT_BUTTON"),width=texWidth("CONNECT_BUTTON"),height=texHeight("CONNECT_BUTTON"))
	def onClick(self):
		if(len(gameState.hostIPInputElem.text) > 0):
			gameState.setGameMode(gameModes.joinLANGameMode,[gameState.hostIPInputElem.text])
			gameState.setHostIP(gameState.hostIPInputElem.text)
		

class hostIPInputElement(textInputElement):
	def __init__(self,xPos,yPos):
		textInputElement.__init__(self,xPos,yPos,width=texWidth("UI_TEXT_INPUT_IMAGE"),height=texHeight("UI_TEXT_INPUT_IMAGE"),textureIndex=texIndex("UI_TEXT_INPUT"),text="192.168.0.102")
#		self.gameMode = gameMode
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			if(len(self.text) > 0):
				gameState.setGameMode(gameModes.joinLANGameMode,[self.text])
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

class cityViewerButton(clickableElement):
	def onClick(self):
		node = viewer.theViewer.node
		viewer.theViewer.destroy()
		viewer.theViewer = cityViewer(node)

class unitViewerButton(clickableElement):
	def onClick(self):
		node = viewer.theViewer.node
		viewer.theViewer.destroy()
		viewer.theViewer = uniitViewer(node)

class cancelButton(clickableElement):
	def __init__(self,xPos,yPos,index):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('CANCEL_BUTTON'),width=texWidth('CANCEL_BUTTON'),textureIndex=texIndex('CANCEL_BUTTON'))	
		self.index = index
	def onClick(self):
		gameState.getClient().sendCommand("cancelQueuedThing",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos) + " " + str(self.index))
		if(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)

class startGatheringButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('START_GATHERING_BUTTON'),width=texWidth('START_GATHERING_BUTTON'),textureIndex=texIndex('START_GATHERING_BUTTON'))
	def onClick(self):
		viewer.theViewer.destroy()
		gameState.getClient().sendCommand("startMeditating",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos))
		if(gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit):
			gameState.getClient().sendCommand("chooseNextUnit")
		elif(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)

class cancelMovementButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('CANCEL_MOVEMENT_BUTTON'),width=texWidth('CANCEL_MOVEMENT_BUTTON'),textureIndex=texIndex('CANCEL_MOVEMENT_BUTTON'))
	def onClick(self):
		for pathNode in gameState.getGameMode().selectedNode.unit.movePath:
			pathNode.onMovePath = False
		gameState.getGameMode().selectedNode.unit.movePath = []
		if(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)

class skipButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('SKIP_BUTTON'),width=texWidth('SKIP_BUTTON'),textureIndex=texIndex('SKIP_BUTTON'))
	def onClick(self):
		gameState.getClient().sendCommand("skip")
#,str(gameState.getGameMode().nextUnit.node.xPos) + " " + str(gameState.getGameMode().nextUnit.node.yPos))
		gameState.getClient().sendCommand("chooseNextUnit")

class startSummoningButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('START_SUMMONING_BUTTON'),width=texWidth('START_SUMMONING_BUTTON'),textureIndex=texIndex('START_SUMMONING_BUTTON'))
	def onClick(self):
		viewer.theViewer.destroy()
		gameState.getClient().sendCommand("startMeditating",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos))
		if(gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit):
			gameState.getClient().sendCommand("chooseNextUnit")
		elif(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)

class summonButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BUILD_BUTTON"),width=texWidth("BUILD_BUTTON"),height=texHeight("BUILD_BUTTON"))
		self.unitType = unitType
	def onClick(self):
		gameState.getClient().sendCommand("startSummoning",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos) + " " + self.unitType.name)
		if(gameState.getGameMode().selectedNode.unit == gameState.getGameMode().nextUnit):
			gameState.getClient().sendCommand("chooseNextUnit")
		elif(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)

class researchButton(clickableElement):
	def __init__(self,xPos,yPos,unitType):
		clickableElement.__init__(self,xPos,yPos,height=texHeight('RESEARCH_BUTTON'),width=texWidth('RESEARCH_BUTTON'),textureIndex=texIndex('RESEARCH_BUTTON'))
		self.unitType = unitType
	def onClick(self):
		gameState.getClient().sendCommand("startResearch",str(gameState.getGameMode().selectedNode.xPos) + " " + str(gameState.getGameMode().selectedNode.yPos) + " " + self.unitType.name)
		if(gameState.getGameMode().nextUnit == gameState.getGameMode().selectedNode.unit):
			gameState.getClient().sendCommand("chooseNextUnit")
		elif(gameState.getGameMode().nextUnit != None and gameState.getGameMode().nextUnit.isControlled()):
			gameLogic.selectNode(gameState.getGameMode().nextUnit.node)

class unitTypeViewer(uiElement):
	theViewer = None
	def __init__(self,unitType):
		if(hasattr(gameState.getGameMode(),"nextUnit")):
			uiElement.__init__(self,-0.500,0.965,width=texWidth("UI_UNITTYPE_BACKGROUND"),height=texHeight("UI_UNITTYPE_BACKGROUND"),textureIndex=texIndex("UI_UNITTYPE_BACKGROUND"))
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
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.412,text="green wood cost",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.412,text=str(self.unitType.costGreen),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.452,text="blue wood cost",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.452,text=str(self.unitType.costBlue),textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.492,text="build time",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.492,text=str(self.unitType.buildTime),textSize=0.0005,textColor="ee ed 9b").name)

		if(self.unitType.researchCostGreen > 0):
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.572,text="green wood level cost",textSize=0.0005,textColor="ee ed 9b").name)
			self.names.append(uiElement(self.xPosition+0.370,self.yPosition-0.572,text=str(self.unitType.researchCostGreen),textSize=0.0005,textColor="ee ed 9b").name)
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.612,text="green wood level cost",textSize=0.0005,textColor="ee ed 9b").name)
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
		uiElement.__init__(self,xPos,yPos,width,height,textureIndex)
		self.node = node
		self.names = []
		if(node.unit != None):
			self.names.append(unitViewerButton(xPos+0.09,yPos-0.046,text="unit",textSize=0.0007,textColor="ee ed 9b",width=1.0,height=1.0,fontIndex=3).name)
		else:
			self.names.append(uiElement(xPos+0.09,yPos-0.046,text="unit",textSize=0.0007,textColor="cc cc cc",width=1.0,height=1.0,fontIndex=3).name)			
		if(node.city != None):
			self.names.append(cityViewerButton(xPos+0.31,yPos-0.046,text="city",textSize=0.0007,textColor="ee ed 9b",width=1.0,height=1.0,fontIndex=3).name)
		else:
			self.names.append(uiElement(xPos+0.31,yPos-0.046,text="city",textSize=0.0007,textColor="cc cc cc",width=1.0,height=1.0,fontIndex=3).name)
	def destroy(self):
		viewer.theViewer = None
		uiElement.destroy(self)


class uniitViewer(viewer):
	def __init__(self,node):
		viewer.__init__(self,-0.965,0.965,node,width=texWidth("UI_UNIT_BACKGROUND"),height=texHeight("UI_UNIT_BACKGROUND"),textureIndex=texIndex("UI_UNIT_BACKGROUND"))

		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.100,textureIndex=texIndex("GREY_PEDESTAL"),width=2.0*texWidth("GREY_PEDESTAL"),height=2.0*texHeight("GREY_PEDESTAL")).name)
		self.names.append(unitTypeViewerButton(self.xPosition+0.040,self.yPosition-0.120,self.node.unit.unitType,textureIndex=self.node.unit.unitType.textureIndex,height=0.14,width=0.14*0.75).name)

		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.125,text="health",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.130,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.130,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(float(self.node.unit.health)/self.node.unit.getMaxHealth()),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)

		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.185,text="move initiative",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.190,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.190,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(float(self.node.unit.health)/self.node.unit.getMaxHealth()),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)

		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.245,text="atk initiative",textSize=0.0005,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.250,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
		self.names.append(uiElement(self.xPosition+0.180,self.yPosition-0.250,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(float(self.node.unit.health)/self.node.unit.getMaxHealth()),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
		
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.32,text=self.node.unit.unitType.name,textSize=0.00055,textColor="ee ed 9b").name)
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.36,text="lvl " + str(self.node.unit.level),textSize=0.00055,textColor="ee ed 9b").name)

		if(self.node.unit.isMeditating):
			self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.450,text="meditating",textSize=0.00055,textColor="ee ed 9b").name)
		else:
			height = self.yPosition-0.450
			if(self.node.city != None and self.node.unit.unitType.name == "summoner" and not self.node.unit.isMeditating):
				self.names.append(startSummoningButton(self.xPosition+0.022,height).name)
				height = height - 0.055

			if(len(self.node.unit.movePath) > 0):
				self.names.append(cancelMovementButton(self.xPosition+0.022,height).name)
				height = height - 0.055
			if(self.node.unit == gameState.getGameMode().nextUnit and (gameState.getPlayerNumber() == self.node.unit.player or gameState.getPlayerNumber() == -2)):
				self.names.append(skipButton(self.xPosition+0.022,height).name)
				height = height - 0.055
			if(self.node.unit == gameState.getGameMode().nextUnit and self.node.unit.unitType.name == "gatherer" and (self.node.tileValue == cDefines.defines['FOREST_TILE_INDEX'] or self.node.tileValue == cDefines.defines['BLUE_FOREST_TILE_INDEX'])):
				self.names.append(startGatheringButton(self.xPosition+0.022,height).name)
				height = height - 0.055		

class cityViewerNoPlay(uiElement):
	def __init__(self,node):
		if(hasattr(gameState.getGameMode(),"createGameMode")):
			uiElement.__init__(self,-0.31,0.79,width=texWidth("UI_CITYVIEW_BACKGROUND"),height=texHeight("UI_CITYVIEW_BACKGROUND"),textureIndex=texIndex("UI_CITYVIEW_BACKGROUND"))
		else:
			uiElement.__init__(self,-0.91,0.79,width=texWidth("UI_CITYVIEW_BACKGROUND"),height=texHeight("UI_CITYVIEW_BACKGROUND"),textureIndex=texIndex("UI_CITYVIEW_BACKGROUND"))
		self.node = node
		height = 0.76
		for unitType in self.node.city.unitTypes:
			self.names.append(uiElement(self.xPosition+0.022,height,textureIndex=texIndex("GREY_PEDESTAL"),width=texWidth("GREY_PEDESTAL"),height=texHeight("GREY_PEDESTAL")).name)
			self.names.append(unitTypeViewerButton(self.xPosition+0.028,height-0.008,unitType,textureIndex=unitType.textureIndex,height=0.07,width=0.07*0.75).name)
			self.names.append(uiElement(self.xPosition+0.1,height-0.030,text=unitType.name,textSize=0.00055,textColor="ee ee ee",fontIndex=2).name)

			self.names.append(uiElement(self.xPosition+0.1,height-0.042,textureIndex=texIndex("GREEN_WOOD_ICON"),width=texWidth("GREEN_WOOD_ICON"),height=texHeight("GREEN_WOOD_ICON")).name)
			self.names.append(uiElement(self.xPosition+0.123,height-0.065,text=str(unitType.costGreen),textSize=0.00040,textColor="ee ee ee",fontIndex=0).name)
			self.names.append(uiElement(self.xPosition+0.175,height-0.042,textureIndex=texIndex("BLUE_WOOD_ICON"),width=texWidth("BLUE_WOOD_ICON"),height=texHeight("BLUE_WOOD_ICON")).name)
			self.names.append(uiElement(self.xPosition+0.198,height-0.065,text=str(unitType.costBlue),textSize=0.00040,textColor="ee ee ee",fontIndex=0).name)
			self.names.append(uiElement(self.xPosition+0.250,height-0.042,textureIndex=texIndex("TIME_ICON"),width=texWidth("TIME_ICON"),height=texHeight("TIME_ICON")).name)
			self.names.append(uiElement(self.xPosition+0.273,height-0.065,text=str(unitType.buildTime),textSize=0.00040,textColor="ee ee ee",fontIndex=0).name)

			height = height - 0.1
	def destroy(self):
		viewer.theViewer = None
		uiElement.destroy(self)
	

class cityViewer(viewer):
	def __init__(self,node):
		viewer.__init__(self,-0.965,0.965,node,width=texWidth("UI_CITY_BACKGROUND"),height=texHeight("UI_CITY_BACKGROUND"),textureIndex=texIndex("UI_CITY_BACKGROUND"))
		self.isCityViewer = True
		self.names.append(uiElement(self.xPosition+0.022,self.yPosition-0.125,text=self.node.city.name,textSize=0.0008,fontIndex=3,textColor="dd dd dd").name)
		buildableUnitTypes = []
		for unitType in self.node.city.researchProgress:
			if(self.node.city.researchProgress[unitType][0] > 0):
				buildableUnitTypes.append(unitType)
		self.names.append(cityUnitDisplay(self.xPosition+0.012,self.yPosition-0.174,buildableUnitTypes,buildUnitElem,"BUILD_BORDER").name)
		
		researchableUnitTypes = []
		for unitType in self.node.city.unitTypes:
			if(unitType.name != "summoner" and unitType.name != "gatherer"): 
				researchableUnitTypes.append(unitType)
		self.names.append(cityUnitDisplay(self.xPosition+0.012,self.yPosition-0.766,researchableUnitTypes,researchUnitElem,"RESEARCH_BORDER").name)
		queuedThings = []
		if(self.node.city.researching):
			queuedThings.append(self.node.city.researchUnitType)
		elif(self.node.city.unitBeingBuilt != None):
			queuedThings.append(self.node.city.unitBeingBuilt)
		for thing in self.node.city.unitBuildQueue:
			queuedThings.append(thing)
		queuedThingElem.firstThing = True
		self.names.append(cityUnitDisplay(self.xPosition+0.012,self.yPosition-1.358,queuedThings,queuedThingElem,"QUEUE_BORDER").name)
		
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
				
			self.scrollableElement.scrollPosition = int((self.numScrollableElements)*(self.scrollableElement.yPosition-self.topOffset-self.yPosition)/self.totalScrollableHeight)
			self.scrollableElement.hideAndShowTextFields()
	def setScrollPosition(self,scrollPos):
		self.yPosition = 0.0-((self.totalScrollableHeight*scrollPos/(self.numScrollableElements))+self.topOffset-self.scrollableElement.yPosition)

class scrollableElement(uiElement):
	def setYPosition(self,yPos):
		if(hasattr(self,"names")):
			for name in self.names:
				gameState.getGameMode().elementsDict[name].yPosition = gameState.getGameMode().elementsDict[name].yPosition + yPos - self.yPosition
		self.yPosition = yPos

class buildUnitElem(scrollableElement):
	def __init__(self,xPos,yPos,unitType,index):
		scrollableElement.__init__(self,xPos,yPos)
		self.unitType = unitType
		self.names.append(uiElement(self.xPosition,self.yPosition,textureIndex=texIndex("UNIT_UI_BACK"),height=texHeight("UNIT_UI_BACK"),width=texWidth("UNIT_UI_BACK")).name)
		self.names.append(unitTypeViewerButton(self.xPosition+0.009,self.yPosition-0.026,self.unitType,textureIndex=self.unitType.textureIndex,height=0.07,width=0.07).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name,textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.071,textureIndex=texIndex("GREEN_WOOD_ICON"),width=texWidth("GREEN_WOOD_ICON"),height=texHeight("GREEN_WOOD_ICON")).name)
		self.names.append(uiElement(self.xPosition+0.108,self.yPosition-0.094,text=str(self.unitType.costGreen),textSize=0.00034,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.151,self.yPosition-0.071,textureIndex=texIndex("BLUE_WOOD_ICON"),width=texWidth("BLUE_WOOD_ICON"),height=texHeight("BLUE_WOOD_ICON")).name)
		self.names.append(uiElement(self.xPosition+0.174,self.yPosition-0.094,text=str(self.unitType.costBlue),textSize=0.00034,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.221,self.yPosition-0.071,textureIndex=texIndex("TIME_ICON"),width=texWidth("TIME_ICON"),height=texHeight("TIME_ICON")).name)
		self.names.append(uiElement(self.xPosition+0.244,self.yPosition-0.094,text=str(self.unitType.buildTime),textSize=0.00034,textColor="ee ee ee",fontIndex=0).name)
		if(gameState.getGameMode().selectedNode.unit != None and gameState.getGameMode().selectedNode.unit.isMeditating and gameState.getGameMode().selectedNode.unit.isControlled() and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()-1].greenWood >= self.unitType.costGreen and gameState.getGameMode().players[gameState.getGameMode().getPlayerNumber()-1].blueWood >= self.unitType.costBlue):
			self.names.append(summonButton(self.xPosition+0.293,self.yPosition-0.068,self.unitType).name)

class researchUnitElem(scrollableElement):
	def __init__(self,xPos,yPos,unitType,index):
		scrollableElement.__init__(self,xPos,yPos)
		self.unitType = unitType
		self.names.append(uiElement(self.xPosition,self.yPosition,textureIndex=texIndex("UNIT_UI_BACK"),height=texHeight("UNIT_UI_BACK"),width=texWidth("UNIT_UI_BACK")).name)
		self.names.append(unitTypeViewerButton(self.xPosition+23.0/cDefines.defines["SCREEN_WIDTH"],self.yPosition-23.0/cDefines.defines["SCREEN_HEIGHT"],self.unitType,textureIndex=self.unitType.textureIndex,height=70.0/cDefines.defines["SCREEN_HEIGHT"],width=70.0/cDefines.defines["SCREEN_WIDTH"]).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name,textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
		self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.071,textureIndex=texIndex("GREEN_WOOD_ICON"),width=texWidth("GREEN_WOOD_ICON"),height=texHeight("GREEN_WOOD_ICON")).name)
		self.names.append(uiElement(self.xPosition+0.108,self.yPosition-0.094,text=str(self.unitType.costGreen),textSize=0.00034,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.151,self.yPosition-0.071,textureIndex=texIndex("BLUE_WOOD_ICON"),width=texWidth("BLUE_WOOD_ICON"),height=texHeight("BLUE_WOOD_ICON")).name)
		self.names.append(uiElement(self.xPosition+0.174,self.yPosition-0.094,text=str(self.unitType.costBlue),textSize=0.00034,textColor="ee ee ee",fontIndex=0).name)
		self.names.append(uiElement(self.xPosition+0.221,self.yPosition-0.071,textureIndex=texIndex("TIME_ICON"),width=texWidth("TIME_ICON"),height=texHeight("TIME_ICON")).name)
		self.names.append(uiElement(self.xPosition+0.244,self.yPosition-0.094,text=str(self.unitType.buildTime),textSize=0.00034,textColor="ee ee ee",fontIndex=0).name)
		if(gameState.getGameMode().selectedNode.unit != None and gameState.getGameMode().selectedNode.unit.isMeditating and gameState.getGameMode().selectedNode.unit.isControlled() and gameState.getGameMode().players[gameState.getGameMode().selectedNode.unit.player-1].greenWood >= self.unitType.researchCostGreen and gameState.getGameMode().players[gameState.getGameMode().selectedNode.unit.player-1].blueWood >= self.unitType.researchCostBlue):
			self.names.append(researchButton(self.xPosition+0.293,self.yPosition-0.068,self.unitType).name)

class queuedThingElem(scrollableElement):
	firstThing = True
	def __init__(self,xPos,yPos,unitThing,index):
		scrollableElement.__init__(self,xPos,yPos)
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
			self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text=self.unitType.name,textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
			if(self.unit != None):
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(gameState.getGameMode().selectedNode.city.unitBeingBuilt.unitType.buildTime-gameState.getGameMode().selectedNode.city.unitBeingBuilt.buildPoints)/gameState.getGameMode().selectedNode.city.unitBeingBuilt.unitType.buildTime,textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)
			else:
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE'),textureIndex=texIndex('UNIT_BUILD_BAR')).name)
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.08,height=texHeight('UNIT_BUILD_BAR_IMAGE'),width=texWidth('UNIT_BUILD_BAR_IMAGE')*(float(gameState.getGameMode().selectedNode.city.researchProgress[gameState.getGameMode().selectedNode.city.researchUnitType][1])/gameState.getGameMode().selectedNode.city.researchUnitType.researchTime),textureIndex=texIndex('UNIT_BUILD_BAR'),color="FF 00 00").name)

		else:
			if(self.unit != None):
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text="summon",textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
			else:
				self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.05,text="research",textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
			self.names.append(uiElement(self.xPosition+0.085,self.yPosition-0.095,text=self.unitType.name,textSize=0.0005,textColor="ee ee ee",fontIndex=2).name)
			self.names.append(cancelButton(self.xPosition+0.293,self.yPosition-0.068,index).name)

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
		self.roomNameElem = scrollableRoomNameElement(xPos+0.008,yPos,text=roomName,textSize=textSize)
		self.names.append(self.roomNameElem.name)
		self.mapNameElem = scrollableMapNameElement(xPos+0.9,yPos,text=mapName,textSize=textSize)
		self.names.append(self.mapNameElem.name)
		self.roomCountElem = uiElement(xPos+1.36,yPos,text=str(playerCount) + "/" + str(maxPlayerCount),textSize=textSize)
		self.names.append(self.roomCountElem.name)

class scrollableTextFieldsElement(uiElement):
	def __init__(self,xPos,yPos,textFields,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,xPositionOffset=0.0,yPositionOffset=0.04,lineHeight=0.041,numFields=25,scrollSpeed=1,scrollPadTex="UI_SCROLL_PAD"):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.xPositionOffset = xPositionOffset
		self.yPositionOffset = yPositionOffset
		self.lineHeight = lineHeight
		self.numFields = numFields
		self.scrollSpeed = scrollSpeed
		self.scrollPosition = 0
		self.textFields = textFields
		self.scrollPadTex = scrollPadTex
		self.names = []
		self.redraw()
	def redraw(self):
		self.reset()
		for field in self.textFields:
			textFieldElem = None
			if(hasattr(field,"xPosition")):
				textFieldElem = field
				textFieldElem.scrollableElement = self
				textFieldElem.xPosition = self.xPosition+self.xPositionOffset
				gameState.getGameMode().elementsDict[textFieldElem.name] = textFieldElem
			else:
				text = ""
				if(hasattr(field,"name")):
					text = field.name
				else:
					text=field
				textFieldElem = scrollingTextElement(self.xPosition+self.xPositionOffset,0.0,self,width=2.0,height=0.1,text=text,textureIndex=-1,textSize=self.textSize,hidden=True)
			textFieldElem.onScrollUp = self.onScrollUp
			textFieldElem.onScrollDown = self.onScrollDown
			for name in textFieldElem.names:
				gameState.getGameMode().elementsDict[name].onScrollUp = self.onScrollUp
				gameState.getGameMode().elementsDict[name].onScrollDown = self.onScrollDown
			self.names.append(textFieldElem.name)
			self.textFieldElements.append(textFieldElem)
		self.hideAndShowTextFields()
		if(len(self.textFields) <= self.numFields):
			self.scrollPadElem = None
		else:
			self.scrollPadElem = scrollPadElement(self.xPosition + self.width - texWidth(self.scrollPadTex),self.yPosition,scrollableElement=self,width=texWidth(self.scrollPadTex),height=texHeight(self.scrollPadTex),textureIndex=texIndex(self.scrollPadTex),hidden=True)
			self.scrollPadElem.onScrollUp = self.onScrollUp
			self.scrollPadElem.onScrollDown = self.onScrollDown
			self.names.append(self.scrollPadElem.name)
			self.scrollPadElem.setScrollPosition(self.scrollPosition)
	def hideAndShowTextFields(self):
		count = 0
		yPosOffset = 0-self.yPositionOffset
		for textFieldElement in self.textFieldElements:
			count = count + 1
			textFieldElement.setYPosition(self.yPosition+yPosOffset)
			if(count < self.numFields + self.scrollPosition + 1 and count > self.scrollPosition):
				yPosOffset = yPosOffset - self.lineHeight
				textFieldElement.hidden = False
				for name in textFieldElement.names:
					gameState.getGameMode().elementsDict[name].hidden = False
			else:
				textFieldElement.hidden = True
				for name in textFieldElement.names:
					gameState.getGameMode().elementsDict[name].hidden = True
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
		for name in self.names:
			#gameState.getGameMode().elementsDict[name].destroy()
			#it appears this line is no longer needed because uiElement.destroy dels the elem from elementsDict
			del gameState.getGameMode().elementsDict[name]
		self.names = []
#		self.textFields = []
		self.textFieldElements = []

class cityUnitDisplay(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,unitTypes,unitElemClass,textureName):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,[],textureIndex=texIndex(textureName),width=texWidth(textureName),height=texHeight(textureName),xPositionOffset=0.01,yPositionOffset=0.035,lineHeight=0.127,numFields=4,scrollPadTex="SCROLL_BAR")
		self.unitTypes = unitTypes
		index = 0
		for unitType in self.unitTypes:
			elem = unitElemClass(self.xPosition+self.xPositionOffset,0.0,unitType,index)
			self.textFields.append(elem)
			self.names.append(elem.name)
			index = index + 1
		self.redraw()

class chatDisplay(scrollableTextFieldsElement):
	#The goal here is to hold lines of text that are too long in textQueue and run them thru a function in fonts.h which will tell us how many words will constitute one line. This way we can add the text as a textFieldElement in order to reuse all the scrollableTextFields code.
	def __init__(self,xPos,yPos,textureName="CHAT_DISPLAY"):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,[],textSize=0.0005,textureIndex=texIndex(textureName),width=texWidth(textureName),height=texHeight(textureName),numFields=40)
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
	def handleClick(self,textFieldElem):
		for unitType in gameState.theUnitTypes.values():
			if(unitType.name == textFieldElem.text):
				cityEditor.theCityEditor.addUnitType(unitType)
		self.destroy()

class cityCostSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,cityCostField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=0.04,lineHeight=0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.cityCostField = cityCostField
	def handleClick(self,textFieldElem):
		self.cityCostField.text = textFieldElem.text
		cityEditor.theCityEditor.city.costOfOwnership = int(textFieldElem.text)
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
		if(hasattr(gameState.getGameMode(),"hostGameMode")):
			gameState.getGameMode().teamSize = self.teamSize
			gameState.getGameMode().setMap(gameState.getMapDatas()[self.teamSize-1][0].name)

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
		server.startServer('')
		client.startClient('127.0.0.1')
		teamSize = 0
		for button in gameTypeButton.buttons:
			if(button.selected):
				teamSize = button.teamSize
		gameState.getGameFindClient().sendCommand("testServer",gameState.getConfig()["serverPort"])
		gameState.setGameMode(gameModes.createGameMode)
		smallModal("testing connection...",dismissable=False)
		gameState.getGameMode().teamSize = teamSize
		gameState.getGameMode().setMap(gameState.getMapDatas()[teamSize-1][0].name)

class chatBox(textInputElement):
	def __init__(self,xPos,yPos,klient,textureName="CHAT_BOX"):
		textInputElement.__init__(self,xPos,yPos,text="",textSize=0.0005,textureIndex=texIndex(textureName),width=texWidth(textureName),textColor="FF FF FF",textXPos=0.02,textYPos=-0.045)
		self.klient = klient
	def sendChat(self):
		if(len(self.realText) > 0):
			self.klient.sendCommand("chat",gameState.getUserName()+": "+self.realText)
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
	selectedTextColor = "aa aa aa"
	normalTextColor = "1f 10 10"
	gameMode = None
	def __init__(self,xPos,yPos,gameMode,width=1.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=menuButton.normalTextColor,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],mouseOverColor="88 88 88",textSize=0.0013,fontIndex=1)
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
	def __init__(self,xPos,yPos,textFields,mapField):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=texWidth("MAP_SELECTOR"),height=texHeight("MAP_SELECTOR"),textureIndex=texIndex("MAP_SELECTOR"),numFields=4,lineHeight=0.036,xPositionOffset=0.02,yPositionOffset=0.05)
		self.mapField = mapField
#	def handleClick(self,textFieldElem):
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
	def handleClick(self,fieldElem):
		self.mapField.text = fieldElem.text
		self.mapField.mapName = fieldElem.text
		self.destroy()

#class mapSelector(scrollableTextFieldsElement):
#	def __init__(self,xPos,yPos,textFields,mapField):
#		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=texWidth("MAP_SELECTOR"),height=texHeight("MAP_SELECTOR"),textureIndex=texIndex("MAP_SELECTOR"))
#		self.mapField = mapField
#	def handleClick(self,fieldElem):
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
		self.selector(self.xPosition,self.yPosition-0.06,mapNames,self,text="select build time",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class maxPlayersSelector(scrollableTextFieldsElement):
	def handleClick(self,fieldElem):
		gameState.getGameMode().maxPlayersField.text = fieldElem.text + " players"
		self.destroy()

class maxPlayersField(clickableElement):
	def onClick(self):
		maxPlayersSelector(self.xPosition,self.yPosition-0.06,["1","2","4","8"],textSize=0.0006)

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

class startButton(menuButton):
	def onClick(self):
		if(gameState.getMapName() != None):
			server.stopAcceptingConnections()
			for player in gameState.getNetworkPlayers():
				player.dispatchCommand("startGame -1")
		else:
			uiElements.smallModal("Choose a map.")

class loginInputElement(textInputElement):
	usernameElem = None
	passwordElem = None
	def __init__(self,xPos,yPos,text,isPassword=False):
		textInputElement.__init__(self,xPos,yPos,text=text,isPassword=isPassword)
	@staticmethod
	def doLogin():
		gameState.getGameFindClient().sendCommand("login",loginInputElement.usernameElem.realText + " " + loginInputElement.passwordElem.realText)
		gameState.setUserName(loginInputElement.usernameElem.realText)
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			loginInputElement.doLogin()
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
	def __init__(self,modal,yPos=-0.05,text="",textureIndex=cDefines.defines["OK_BUTTON_INDEX"]):
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
		self.textElem = uiElement((texWidth("MODAL_SMALL")/-2.0)+0.03,0.1,width=texWidth("MODAL_SMALL")-0.06,text=text,textSize=0.0007,textColor="ee ed 9b")
		if(self.dismissable):
			self.buttonElem = modalButton(self,self.yPosition-0.4)
		gameState.getGameMode().modal = self

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
				gameState.getGameMode().map.numPlayers = numPlayers
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

#class roomNameInputElement(textInputElement):
#	def __init__(self,xPos,yPos):
#		textInputElement.__init__(self,xPos,yPos)

class createGameButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("CREATE_GAME_BUTTON_LARGE"),width=texWidth("CREATE_GAME_BUTTON_LARGE"),height=texHeight("CREATE_GAME_BUTTON_LARGE"))
	def onClick(self):
		gameState.getGameFindClient().sendCommand("createGameRoom",gameState.getGameMode().roomNameField.realText + "|" + str(gameState.getGameMode().teamSize) + "|" + gameState.getGameMode().mapNameField.text)

class createGameButtun(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("CREATE_GAME_BUTTON_LARGE"),width=texWidth("CREATE_GAME_BUTTON_LARGE"),height=texHeight("CREATE_GAME_BUTTON_LARGE"))
	def onClick(self):
		server.startServer('',6666)
		client.startClient('127.0.0.1',6666)
		gameState.setGameMode(gameModes.joinLANGameMode)
		gameState.getGameMode().setMap(gameState.getMapName())

class backButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BACK_BUTTON"),width=texWidth("BACK_BUTTON"),height=texHeight("BACK_BUTTON"))
	def onClick(self):
		gameState.getGameFindClient().sendCommand("subscribe","lobby")

class backButtun(clickableElement):
	def __init__(self,xPos,yPos,gameMode):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("BACK_BUTTON"),width=texWidth("BACK_BUTTON"),height=texHeight("BACK_BUTTON"))
		self.gameMode = gameMode
	def onClick(self):
		gameState.setGameMode(self.gameMode)

class startGameButton(clickableElement):
	def __init__(self,xPos,yPos):
		clickableElement.__init__(self,xPos,yPos,textureIndex=texIndex("START_BUTTON"),width=texWidth("START_BUTTON"),height=texHeight("START_BUTTON"))
	def onClick(self):
		for player in gameState.getNetworkPlayers():
			player.dispatchCommand("startGame -1")
