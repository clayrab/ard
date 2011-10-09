import os
import random
import copy
import gameState
import gameLogic
import nameGenerator
import cDefines
import shutil
import client

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
		gameState.getGameMode().cityEditor.city.name = self.text

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



class cityViewer(uiElement):
	theCityViewer = None
	def __init__(self,node,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.node = node
		self.names = []
		self.names.append(uiElement(-0.972,0.75,text=self.node.city.name,textSize=0.0007).name)
		if(self.node.city.unitBeingBuilt != None):
			self.names.append(uiElement(-0.972,0.67,text=self.node.city.unitBeingBuilt.unitType.name,textSize=0.0005).name)
			self.names.append(uiElement(-0.972,0.65,height=(2.0*cDefines.defines['UNIT_BUILD_BAR_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UNIT_BUILD_BAR_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),textureIndex=cDefines.defines['UNIT_BUILD_BAR_INDEX']).name)
                        self.names.append(uiElement(-0.972,0.65,height=(2.0*cDefines.defines['UNIT_BUILD_BAR_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),width=(2.0*cDefines.defines['UNIT_BUILD_BAR_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH'])*(self.node.city.unitBeingBuilt.unitType.buildTime-self.node.city.unitBeingBuilt.buildPoints)/self.node.city.unitBeingBuilt.unitType.buildTime,textureIndex=cDefines.defines['UNIT_BUILD_BAR_INDEX'],color="FF 00 00").name)
		height = 0.6
		for unit in self.node.city.unitBuildQueue[1:]:
			height = height - 0.035
			self.names.append(uiElement(-0.972,height,text=str(unit.unitType.name),textSize=0.0005).name)

		height = 0.16
		for unitType in self.node.city.unitTypes:
			self.names.append(unitSelectButton(-0.972,height,unitType,self.node,text=unitType.name,textSize=0.0005).name)
			self.names.append(uiElement(-0.7,height,text=str(unitType.cost),textSize=0.0005).name)
			height = height - 0.035
		
	def destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True
	def reset(self):
		self.destroy()
		cityViewer.theCityViewer = cityViewer(self.node)

class unitViewer(uiElement):
	theUnitViewer = None
	def __init__(self,node,xPos=0.0,yPos=0.0,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.node = node
		self.names = []
		self.names.append(uiElement(-0.972,0.0,text=self.node.unit.unitType.name,textSize=0.0005).name)
		
	def destroy(self):
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True

class cityEditor(uiElement):
	def __init__(self,xPos,yPos,city,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		if(gameState.getGameMode().mapOptionsEditor != None):
			gameState.getGameMode().mapOptionsEditor.destroy()
		if(gameState.getGameMode().cityEditor != None):
			gameState.getGameMode().cityEditor.destroy()
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.names = []
		self.city = city
		self.draw()
	def addUnitType(self,unitType):
		self.city.unitTypes.append(unitType)
		self.draw()
	def draw(self):
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		self.names.append(cityNameInputElement(-0.972,0.746,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text=self.city.name,textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01).name)
		self.names.append(cityCostField(-0.972,0.66,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text=str(self.city.costOfOwnership),textSize=0.0005,textColor='00 00 00',mouseOverColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01).name)
		height = 0.56
		for unitType in self.city.unitTypes:
			self.names.append(uiElement(-0.972,height,text=unitType.name,textSize=0.0005).name)
			self.names.append(unitCostField(-0.75,height,unitType,text=str(unitType.cost),textSize=0.0005).name)
			self.names.append(unitBuildTimeField(-0.7,height,unitType,text=str(unitType.buildTime),textSize=0.0005).name)
			height = height - 0.035
		self.names.append(addUnitTypeButton(-0.972,height,width=0.0,height=0.0,text="+unit",textSize=0.0005).name)
		self.names.append(deleteCityButton(-0.972,-0.9,width=0.0,height=0.0,text="delete city",textSize=0.0005).name)
		
	def destroy(self):
		gameState.getGameMode().cityEditor = None
		del gameState.getGameMode().elementsDict[self.name]
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		gameState.getGameMode().resortElems = True


class mapEditorTileSelectUIElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,tileType=0,playerNumber=-1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'])
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
		gameState.getGameMode().mapOptionsEditor = mapOptionsEditor(0.0,0.0)

class mapOptionsEditor(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		if(gameState.getGameMode().mapOptionsEditor != None):
			gameState.getGameMode().mapOptionsEditor.destroy()
		if(gameState.getGameMode().cityEditor != None):
			gameState.getGameMode().cityEditor.destroy()
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cursorIndex,color=color,mouseOverColor=mouseOverColor,hidden=True)
		self.names = []
		self.names.append(uiElement(-0.96,0.73,text="map options",textSize=0.0008).name)
		self.names.append(uiElement(-0.96,0.63,text="starting mana",textSize=0.0005).name)
		self.names.append(startingManaField(-0.96,0.53,text="10",textSize=0.0005).name)
	def destroy(self):
		gameState.getGameMode().mapOptionsEditor = None
		print "destroy"
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []
		del gameState.getGameMode().elementsDict[self.name]
		gameState.getGameMode().resortElems = True

class scrollPadElement(uiElement):
	def __init__(self,xPos,yPos,scrollableElement,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,topOffset=0.016,bottomOffset=0.020,rightOffset=0.012):
		uiElement.__init__(self,xPos-rightOffset,yPos-topOffset,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor)
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
				gameState.getGameMode().cityEditor.addUnitType(copy.copy(unitType))
		self.destroy()

class cityCostSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,cityCostField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.cityCostField = cityCostField
	def handleClick(self,textFieldElem):
		self.cityCostField.text = textFieldElem.text
		gameState.getGameMode().cityEditor.city.costOfOwnership = int(textFieldElem.text)
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
		print 'click'
		self.startingManaField.text = textFieldElem.text
		#TODO: Save this data to the map and update save/load
#		self.unitCostField.unitType.cost = int(textFieldElem.text)
		self.destroy()

class unitBuildTimeSelector(scrollableTextFieldsElement):
	def __init__(self,xPos,yPos,textFields,unitBuildTimeField,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,yPositionOffset=-0.04,yOffset=-0.041,numFields=25,scrollSpeed=1):
		scrollableTextFieldsElement.__init__(self,xPos,yPos,textFields,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor)
		self.unitBuildTimeField = unitBuildTimeField
	def handleClick(self,textFieldElem):
		print 'click'
		self.unitBuildTimeField.text = textFieldElem.text
		self.unitBuildTimeField.unitType.cost = int(textFieldElem.text)
		self.destroy()

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
		gameState.getGameMode().cityEditor.destroy()
		gameState.getGameMode().selectedCityNode.city = None
		gameState.getGameMode().selectedCityNode.selected = False
		gameState.getGameMode().selectedCityNode = None

class addUnitTypeButton(clickableElement):	
	def onClick(self):
		unitTypes = gameState.theUnitTypes.copy()
		for unitType in gameState.getGameMode().cityEditor.city.unitTypes:
			del unitTypes[unitType.name]
		unitTypeSelector(self.xPosition,self.yPosition-0.06,unitTypes.values(),text="select unit",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))


class cityCostField(clickableElement):
	def onClick(self):
		cityCostSelector(self.xPosition,self.yPosition-0.06,cityCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class unitCostField(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
	def onClick(self):
		print unitCosts
		unitCostSelector(self.xPosition,self.yPosition-0.06,unitCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))
		print 'done'

class startingManaField(clickableElement):
       	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
	def onClick(self):
		startingManaSelector(self.xPosition,self.yPosition-0.06,startingManas,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))


class unitBuildTimeField(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType

	def onClick(self):
		unitBuildTimeSelector(self.xPosition,self.yPosition-0.06,unitBuildTimes,self,text="select build time",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))


class unitSelectButton(clickableElement):
       	def __init__(self,xPos,yPos,unitType,node,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_POINTER_ON_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType
		self.node = node
	def onClick(self):
		if(gameState.getGameMode().selectedNode.unit != None and gameState.getGameMode().selectedNode.unit.unitType.name == "summoner"):
			self.node.city.queueUnit(gameLogic.unit(self.unitType,self.node.city.playerOwner,self.node.xPos,self.node.yPos,self.node))
			cityViewer.theCityViewer.reset()

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
		for player in gameState.getNetworkPlayers():
			print player
			player.dispatchCommand("setMap " + textFieldElem.text + "|")
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
			print '1'
			gameState.getServer().acceptingConnections = False
			for player in gameState.getNetworksPlayers():
				player.dispatchCommand("startGame|")
				print '2'
			#gameState.setGameMode(self.gameMode)
			print '3'

