import random
import copy
import gameState
import nameGenerator
import cDefines
import shutil

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
	def onScrollDown(self):
		return None
	def onScrollUp(self):
		return None


class clickableElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)

class saveButton(clickableElement):	
	def onClick(self):
		gameState.getGameMode().map.save()

#TODO: MAKE SURE YOU CAN'T REMOVE THE LAST ROW OR COLUMN!!
class addColumnButton(clickableElement):
	def onClick(self):
		for row in gameState.getGameMode().map.nodes:
			row.append(mapEditorNode())

class removeColumnButton(clickableElement):
	def onClick(self):
		for row in gameState.getGameMode().map.nodes:
			row.pop()

class addFirstColumnButton(clickableElement):
	def onClick(self):
		for count in range(0,len(gameState.getGameMode().map.nodes)):
			rowCopy = gameState.getGameMode().map.nodes[count][:]
			rowCopy.reverse()
			rowCopy.append(mapEditorNode())
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
			newRow.append(mapEditorNode())
		gameState.getGameMode().map.nodes.append(newRow)
class removeRowButton(clickableElement):
	def onClick(self):
		gameState.getGameMode().map.nodes.pop()

class addFirstRowButton(clickableElement):
	def onClick(self):
		nodesCopy = gameState.getGameMode().map.nodes[:]
		newRow = []
		for count in range(0,len(gameState.getGameMode().map.nodes[0])):
			newRow.append(mapEditorNode())
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
		print xPos
		print yPos
		print textureIndex
		textInputElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textSize=textSize,textColor=textColor,textXPos=textXPos,textYPos=textYPos)
		self.gameMode = gameMode
		print "wtf"
	def onKeyDown(self,keycode):
		if(keycode == "return"):
			if(len(self.text) > 0):
				shutil.copyfile("maps/defaultMap","maps/" + self.text + ".map")
				gameState.setMapName(self.text)
				gameState.setGameMode(self.gameMode)
			print "enter"
		else:
			textInputElement.onKeyDown(self,keycode)

class cityEditor(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.city = None
		self.names = []
	def show(self,city):
		gameState.getGameMode().mapEditor.hide()
		self.hide()
		self.city = city
		self.names.append(cityNameInputElement(-0.972,0.746,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text=self.city.name,textSize=0.0005,textColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01).name)
		self.names.append(cityCostField(-0.972,0.66,width=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']),text=str(city.costOfOwnership),textSize=0.0005,textColor='00 00 00',mouseOverColor='00 00 00',textureIndex=cDefines.defines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01).name)

		height = 0.56
		for unitType in self.city.unitTypes:
			self.names.append(uiElement(-0.972,height,text=unitType.name,textSize=0.0005).name)
			self.names.append(unitCostField(-0.7,height,unitType,text=str(unitType.cost),textSize=0.0005).name)
			height = height - 0.035
		self.names.append(addUnitTypeButton(-0.972,height,width=0.0,height=0.0,text="+unit",textSize=0.0005).name)
		self.names.append(deleteCityButton(-0.972,-0.9,width=0.0,height=0.0,text="delete city",textSize=0.0005).name)

	def hide(self):
		for name in self.names:
			del gameState.getGameMode().elementsDict[name]
		self.names = []

class mapEditorTileSelectUIElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,tileType=0,playerNumber=-1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'])
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
		gameState.getGameMode().cityEditor.hide()
		gameState.getGameMode().mapEditor.show()


class mapOptionsEditor(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cursorIndex,color=color,mouseOverColor=mouseOverColor,hidden=True)
		self.names = []
	def show(self):
		self.hidden = False
	def hide(self):
		self.hidden = True
		

class scrollPadElement(uiElement):
	def __init__(self,xPos,yPos,scrollableElement,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,topOffset=0.016,bottomOffset=0.020,rightOffset=0.012):
		uiElement.__init__(self,xPos-rightOffset,yPos-topOffset,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor)
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
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor,cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'])
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

class unitTypeSelector(scrollableTextFieldsElement):
	def handleClick(self,textFieldElem):
		for unitType in theUnitTypes.values():
			if(unitType.name == textFieldElem.text):
				gameState.getGameMode().cityEditor.city.unitTypes.append(copy.copy(unitType))
		self.destroy()
		gameState.getGameMode().cityEditor.show(gameState.getGameMode().cityEditor.city)

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
		gameState.getGameMode().cityEditor.hide()
		gameState.getGameMode().selectedCityNode.city = None
		gameState.getGameMode().selectedCityNode.selected = False
		gameState.getGameMode().selectedCityNode = None

class addUnitTypeButton(clickableElement):	
	def onClick(self):
		unitTypes = theUnitTypes.copy()
		for unitType in gameState.getGameMode().cityEditor.city.unitTypes:
			del unitTypes[unitType.name]
		unitTypeSelector(self.xPosition,self.yPosition-0.06,unitTypes.values(),text="select unit",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class cityCostField(clickableElement):
	def onClick(self):
		cityCostSelector(self.xPosition,self.yPosition-0.06,cityCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))

class unitCostField(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType

	def onClick(self):
		unitCostSelector(self.xPosition,self.yPosition-0.06,unitCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines.defines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines.defines['SCREEN_WIDTH']),height=(2.0*cDefines.defines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines.defines['SCREEN_HEIGHT']))


class menuButton(clickableElement):
	index = 0
	buttonsList = []
	selectedIndex = 0
	selectedTextColor = "55 55 55"
	normalTextColor = "33 33 33"
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=menuButton.normalTextColor,cursorIndex=cDefines.defines['CURSOR_HAND_INDEX'],mouseOverColor="66 66 66")
		if(len(menuButton.buttonsList) > 0):
			if(menuButton.buttonsList[0].__class__ != self.__class__):
				menuButton.index = 0
				menuButton.buttonsList = []
				menuButton.selectedIndex = 0
		self.gameMode = gameMode
		self.selected = selected
		self.index = menuButton.index
		menuButton.buttonsList.append(self)
		menuButton.index = menuButton.index + 1
		if(self.index == menuButton.selectedIndex):
			self.textColor = menuButton.selectedTextColor

class newGameScreenButton(menuButton):
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
