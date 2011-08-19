#multiple maps
#campaign
#city viewer in playMode
#unit viewer in playMode
#fog of war
#multiplayer
#AI

import random
import copy
import gameState

zoomSpeed = 0.3
currentMap = ""

def isFloat(str):
	try:
		float(str)
		return True
	except ValueError:
		return False
def isInt(str):
	try:
		int(str)
		return True
	except ValueError:
		return False

cDefines = {}
cFile =  open('main.c','r')
for line in cFile:
	if(line.strip().startswith("#define")):
		tokens = line.split()
		if(isInt(tokens[2])):
			cDefines[tokens[1]] = int(tokens[2])
		elif(isFloat(tokens[2])):
			cDefines[tokens[1]] = float(tokens[2])
		else:
			cDefines[tokens[1]] = tokens[2]
cFile.close()

class city:
	def __init__(self,name,unitTypes=[],costOfOwnership=10):
		self.name = name
		self.costOfOwnership = costOfOwnership
		self.unitTypes = unitTypes

class unitType:
	def __init__(self,name,textureIndex,movementInitiative,attackInitiative,health,canFly=False,canSwim=False,defaultCost=10):
		self.name = name
		self.textureIndex = textureIndex
		self.movementInitiative = movementInitiative
		self.attackInitiative = attackInitiative
		self.health = health
		self.canFly = canFly
		self.canSwim = canSwim
		self.cost = defaultCost

class unit:
	def __init__(self,unitType,player,xPos,yPos,node):
		self.unitType = unitType
		self.player = player
		self.xPos = xPos
		self.yPos = yPos
		self.node = node
		self.movementPoints = 0.0
		self.attackPoints = 0.0
		self.health = self.unitType.health

unitTypesList = []
unitTypesList.append(unitType("summoner",cDefines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("beaver",cDefines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("catapult",cDefines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("fire elemental",cDefines["MEEPLE_INDEX"],1.0,1.0,100))
unitTypesList.append(unitType("dragon",cDefines["MEEPLE_INDEX"],1.0,1.0,100))

theUnitTypes = {}
for unitType in unitTypesList:
	theUnitTypes[unitType.name] = unitType

cityCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
unitCosts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]

cityNames = ["Eshnunna","Tutub","Der","Sippar","Sippar-Amnanum","Kutha","Jemde Nasr","Kish","Babilim","Borsippa","Mashkan-shapir","Dilbat","Nippur","Marad","Adab","Isin","Kisurra","Shuruppak","Bad-tibira","Zabalam","Umma","Girsu","Lagash","Urum","Uruk","Larsa","Ur","Kuara","Eridu","Akshak","Akkad","Urfa","Shanidar cave","Urkesh","Shekhna","Arbid","Harran","Chagar Bazar","Kahat","el Fakhariya (Washukanni?)","Arslan Tash","Carchemish","Til Barsip","Nabada","Nagar","Telul eth-Thalathat","Tepe Gawra","Tell Arpachiyah","Shibaniba","Tarbisu","Ninua","Qatara","Dur Sharrukin","Tell Shemshara","Arbil","Imgur-Enlil","Nimrud","Emar","Arrapha","Kar-Tukulti-Ninurta","Ashur","Nuzi","al-Fakhar","Terqa","Mari","Haradum","Nerebtum","Agrab","Dur-Kurigalzu","Shaduppum","Seleucia","Ctesiphon","Zenobia","Zalabiye","Hasanlu","Takht-i-Suleiman","Behistun","Godin Tepe","Chogha Mish","Tepe Sialk","Susa","Kabnak","Dur Untash","Pasargadai","Naqsh-e Rustam","Parsa","Anshan","Konar Sandal","Tepe Yahya","Miletus","Sfard","Nicaea","Sapinuwa","Yazilikaya","Alaca Hoyuk","Masat Hoyuk","Hattusa","Ilios","Kanesh","Arslantepe","Sam'al","Beycesultan","Adana","Karatepe","Tarsus","Sultantepe","Attalia","Acre","Adoraim","Alalah","Aleppo","Al-Sinnabra","Aphek","Arad Rabbah","Ashdod","Ashkelon","Baalbek","Batroun","Beersheba","Beth Shean","Bet Shemesh","Bethany","Bet-el","Bezer","Byblos","Capernaum","Dan","Dimashq","Deir Alla","Dhiban","Dor","Ebla","En Gedi","Enfeh","Ekron","Et-Tell","Gath","Gezer","Gibeah","Gilgal Refaim","Gubla","Hamath","Hazor","Hebron","Herodion","Jezreel","Kadesh Barnea","Kedesh","Kumidi","Lachish","Megiddo","Qatna","Qumran","Rabat Amon","Samaria","Sarepta","Sharuhen","Shiloh","Sidon","Tadmor","Tirzah","Tyros","Ugarit","Umm el-Marra"]

class intNameGenerator:
	def __init__(self):
		self.nextName = -1
	def getNextName(self):
		self.nextName = self.nextName + 1
		return self.nextName

nameGenerator = intNameGenerator()

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
		print "arg"
		gameState.getGameMode().elementsDict[self.name] = self
		print "arggg"
	def onScrollDown(self):
		return None
	def onScrollUp(self):
		return None

class clickableElement(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)

class mapSelectButton(clickableElement):
	def onClick(self):
		gameState.setMapName(self.text)

class newGameScreenButton(clickableElement):
	index = 0
	buttonsList = []
	selectedIndex = 0
	selectedTextColor = "55 55 55"
	normalTextColor = "33 33 33"
	def __init__(self,xPos,yPos,gameMode,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",selected=False):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=newGameScreenButton.normalTextColor,cursorIndex=cDefines['CURSOR_HAND_INDEX'],mouseOverColor="66 66 66")
		self.gameMode = gameMode
		self.selected = selected
		self.index = newGameScreenButton.index
		newGameScreenButton.buttonsList.append(self)
		newGameScreenButton.index = newGameScreenButton.index + 1
		if(self.index == newGameScreenButton.selectedIndex):
			self.textColor = newGameScreenButton.selectedTextColor
	def onClick(self):


		gameState.setGameMode(self.gameMode)
		if(hasattr(gameState.getGameMode(),"loadMap")):
			gameState.getGameMode().loadMap()
		print "0"
		gameState.getGameMode().addUIElements()
		print "1"
		global theGameMode
		theGameMode = gameState.getGameMode()
		print "2"

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

class cityEditor(uiElement):
	def __init__(self,xPos,yPos,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor)
		self.city = None
		self.names = []
	def show(self,city):
		gameState.getGameMode().mapEditor.hide()
		self.hide()
		self.city = city
		self.names.append(cityNameInputElement(-0.972,0.746,width=(2.0*cDefines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),text=self.city.name,textSize=0.0005,textColor='00 00 00',textureIndex=cDefines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01).name)
		self.names.append(cityCostField(-0.972,0.66,width=(2.0*cDefines['UI_TEXT_INPUT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_TEXT_INPUT_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),text=str(city.costOfOwnership),textSize=0.0005,textColor='00 00 00',mouseOverColor='00 00 00',textureIndex=cDefines['UI_TEXT_INPUT_INDEX'],textYPos=-0.035,textXPos=0.01).name)

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
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,cursorIndex=cDefines['CURSOR_HAND_INDEX'])
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
		uiElement.__init__(self,xPos-rightOffset,yPos-topOffset,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor)
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
			self.yPosition = self.initYPos-(2.0*(gameState.getGameMode().mouseY-self.initMouseYPos)/cDefines['SCREEN_HEIGHT'])
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
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,color=color,mouseOverColor=mouseOverColor,cursorIndex=cDefines['CURSOR_HAND_INDEX'])
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
			self.scrollPadElem = scrollPadElement(self.xPosition + self.width - (2.0*cDefines['UI_SCROLL_PAD_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),self.yPosition,scrollableElement=self,width=(2.0*cDefines['UI_SCROLL_PAD_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_SCROLL_PAD_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_SCROLL_PAD_INDEX'])
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
		unitTypeSelector(self.xPosition,self.yPosition-0.06,unitTypes.values(),text="select unit",textSize=0.0005,textureIndex=cDefines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']))

class cityCostField(clickableElement):
	def onClick(self):
		cityCostSelector(self.xPosition,self.yPosition-0.06,cityCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']))

class unitCostField(clickableElement):
       	def __init__(self,xPos,yPos,unitType,width=0.0,height=0.0,textureIndex=-1,hidden=False,cursorIndex=-1,text="",textColor="FF FF FF",textSize=0.001,color="FF FF FF",mouseOverColor=None,textXPos=0.0,textYPos=0.0):
		clickableElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,textColor=textColor,textSize=textSize,cursorIndex=cDefines['CURSOR_HAND_INDEX'],color=color,mouseOverColor=mouseOverColor,textXPos=textXPos,textYPos=textYPos)
		self.unitType = unitType

	def onClick(self):
		unitCostSelector(self.xPosition,self.yPosition-0.06,unitCosts,self,text="select cost",textSize=0.0005,textureIndex=cDefines['UI_SCROLLABLE_INDEX'],width=(2.0*cDefines['UI_SCROLLABLE_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_SCROLLABLE_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']))

class node:
	def __init__(self,xPos,yPos,tileValue=cDefines['GRASS_TILE_INDEX'],roadValue=0,city=None,playerStartValue=0):
		self.xPos = xPos
		self.yPos = yPos
		self.name = nameGenerator.getNextName()
		self.tileValue = tileValue
		self.roadValue = roadValue
		self.city = city
		self.playerStartValue = playerStartValue
		self.selected = False
		gameState.getGameMode().elementsDict[self.name] = self
		self.unit = None
		self.neighbors = []
	def getValue(self):
		return self.tileValue

class playModeNode(node):
	def onLeftClickDown(self):
		if(gameState.getGameMode().nextUnit.node.selected == True and gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):
			if(self.unit != None):
				print "attack!!!!..?"
			else:
				gameState.getGameMode().nextUnit.node.selected = False
				gameState.getGameMode().nextUnit.node.unit = None
				gameState.getGameMode().nextUnit.node = self
				self.unit = gameState.getGameMode().nextUnit
				gameState.getGameMode().nextUnit.movementPoints = gameState.getGameMode().nextUnit.movementPoints - 1000.0
				gameState.getGameMode().chooseNextUnit()
		else:
			gameState.getGameMode().selectedNode.selected = False
			gameState.getGameMode().selectedNode = self
			self.selected = True
	def onMouseOver(self):
		if(gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):
			print "display 'move' cursor here"
	def onMouseOut(self):
		if(gameState.getGameMode().nextUnit.node.neighbors.count(self) > 0):
			print "remove 'move' cursor here"
		

class mapEditorNode(node):
	def onLeftClickUp(self):
		if(gameState.getGameMode().selectedCityNode != None):
			if(gameState.getGameMode().selectedCityNode != self):
				if(gameState.getGameMode().selectedCityNode.city != None):
					self.city = gameState.getGameMode().selectedCityNode.city
					gameState.getGameMode().selectedCityNode.city = None
					gameState.getGameMode().selectedCityNode.selected = False
					self.selected = True
					gameState.getGameMode().selectedCityNode = self
	def onLeftClickDown(self):
		if(gameState.getGameMode().selectedButton != None):
			if(hasattr(gameState.getGameMode().selectedButton,"tileType")):
				if(gameState.getGameMode().selectedButton.tileType == cDefines['ROAD_TILE_INDEX']):#new road
					self.roadValue = (~self.roadValue)&1
				elif(gameState.getGameMode().selectedButton.tileType == cDefines['CITY_TILE_INDEX']):#new city
					if(self.city == None):
						self.city = city(random.choice(cityNames))
						gameState.getGameMode().cityEditor.show(self.city)
					else:
						gameState.getGameMode().cityEditor.show(self.city)
					if(gameState.getGameMode().selectedCityNode != None):
						gameState.getGameMode().selectedCityNode.selected = False
					self.selected = True
					gameState.getGameMode().selectedCityNode = self
				else:
					self.tileValue = gameState.getGameMode().selectedButton.tileType
			else:
				if(self.playerStartValue == gameState.getGameMode().selectedButton.playerNumber):
					self.playerStartValue = 0
					if(gameState.getGameMode().map.numPlayers == gameState.getGameMode().selectedButton.playerNumber and gameState.getGameMode().map.numPlayers != 1):
						for button in playerStartLocationButton.playerStartLocationButtons:
							if(button.playerNumber == gameState.getGameMode().map.numPlayers + 1):
								button.color = "55 55 55"
						gameState.getGameMode().map.numPlayers = gameState.getGameMode().map.numPlayers - 1
				else:
					for row in gameState.getGameMode().map.nodes:
						for node in row:
							if(node.playerStartValue == gameState.getGameMode().selectedButton.playerNumber):
								node.playerStartValue = 0
					self.playerStartValue = gameState.getGameMode().selectedButton.playerNumber
class map:
	def __init__(self,nodeType):
		self.polarity = 0
		self.nodeType = nodeType
		self.translateZ = 0-cDefines['initZoom']
		self.load()
		print "wtf2"
	def load(self):
		mapFile = open('map1','r')
		self.nodes = []
		count = 0
		yPos = -1
		xPos = -1
		for line in mapFile:
			if(count == 0):#header
				#TODO add players and starting positions to map data
				self.polarity = int(line)
				self.numPlayers = 2
			else:
				yPos = yPos + 1
				xPos = -1
				if(line.startswith("#")):#node
					newRow = []
					line = line.strip("#")
					for char in line:
						xPos = xPos + 1
						if(char != '\n'):
							intValue = ord(char)
							tileValue = intValue & 15
							roadValue = (intValue & 16)>>4
							playerStartValue = (intValue & (32+64+128))>>5
							newNode = self.nodeType(xPos,yPos,tileValue,roadValue,None,playerStartValue=playerStartValue)
							if(xPos > 0):#add neighbor to the left
								newNode.neighbors.append(newRow[len(newRow)-1])
								newRow[len(newRow)-1].neighbors.append(newNode)
							if(yPos > 0):#add neighbors above
								if(not (xPos == 0 and (self.polarity+yPos)%2 == 0)):#has top left neighbor
									if((self.polarity+yPos)%2 == 0):
										newNode.neighbors.append(self.nodes[yPos-1][xPos-1])
										self.nodes[yPos-1][xPos-1].neighbors.append(newNode)
									else:
										newNode.neighbors.append(self.nodes[yPos-1][xPos])
										self.nodes[yPos-1][xPos].neighbors.append(newNode)
								
								if(not (xPos == len(self.nodes[0])-1 and (self.polarity+yPos)%2 == 1)):#has top right neighbor
									if((self.polarity+yPos)%2 == 0):
										newNode.neighbors.append(self.nodes[yPos-1][xPos])
										self.nodes[yPos-1][xPos].neighbors.append(newNode)
									else:
										newNode.neighbors.append(self.nodes[yPos-1][xPos+1])
										self.nodes[yPos-1][xPos+1].neighbors.append(newNode)
							newRow.append(newNode)
					self.nodes.append(newRow)
		                elif(line.startswith("*")):#city
					tokens = line.split(":")
					coords = tokens[0].strip("*").split(",")
					cityName = tokens[1]
					unitTypes = []
					if(len(tokens[2].strip()) != 0):
						unitTypeStrings = tokens[2].strip().split(",")
						for unitTypeString in unitTypeStrings:
							unitTypeTokens = unitTypeString.split("|")
							theUnitType = copy.copy(theUnitTypes[unitTypeTokens[0]])
							theUnitType.cost = unitTypeTokens[1]
							unitTypes.append(theUnitType)
					costOfOwnership = tokens[3]
					self.nodes[int(coords[1])][int(coords[0])].city = city(cityName,unitTypes,costOfOwnership)
			count = count + 1
		mapFile.close()
	def save(self):
		mapFile = open('map1','w')
		yPos = 0
		xPos = 0
		cityLines = []
		nodeLines = []
		nodeLines.append(str(self.polarity) + "\n")
		for row in self.nodes:
			xPos = 0
			yPos = yPos + 1
			line = "#"
			for node in row:
				xPos = xPos + 1
				line = line + chr(node.tileValue + (16*node.roadValue)+ (32*node.playerStartValue) + (512*0))#USE 512 NEXT BECAUSE 8 PLAYERS NEEDS 3 BITS
				if(node.city != None):
					unitTypes = ""
					for unitType in node.city.unitTypes:
						unitTypes = unitTypes + "," + unitType.name + "|" + str(unitType.cost)
					unitTypes = unitTypes[1:]
					cityLines.append("*" + str(xPos-1) + "," + str(yPos-1) + ":" + node.city.name + ":" + unitTypes + ":" + str(node.city.costOfOwnership) + "\n")
			nodeLines.append(line + "\n")
		mapFile.writelines(nodeLines)
		mapFile.writelines(cityLines)
		mapFile.close()
		print "saved"
	def getNodes(self):
		return self.nodes
	def getIterator(self):
		return self.nodes.__iter__()
	def setNumPlayers(self,numPlayers):
		print numPlayers
		self.numPlayers = numPlayers

class gameMode:
	def getUIElementsIterator(self):
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

class tiledGameMode(gameMode):
	def __init__(self):
		self.elementsDict = {}
		self.elementWithFocus = None
		self.mousedOverObject = None
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
	def handleRightClick(self,name):
		rightClickable = False
		if(self.elementsDict.has_key(name)):
			if(hasattr(self.elementsDict[name],"onRightClick")):
				rightClickable = True
				self.elementsDict[name].onRightClick()
		if(not rightClickable):
			self.selectedCityNode.selected = False
			self.selectedCityNode = None
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
	def handleScrollUp(self,name,deltaTicks):
		if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollUp")):
			self.elementsDict[name].onScrollUp()
		else:
			self.map.translateZ = self.map.translateZ + zoomSpeed*deltaTicks;
			if(self.map.translateZ > (-10.0-cDefines['minZoom'])):
				self.map.translateZ = -10.0-cDefines['minZoom']
	def handleScrollDown(self,name,deltaTicks):
		if(name in self.elementsDict and hasattr(self.elementsDict[name],"onScrollDown")):
			self.elementsDict[name].onScrollDown()
		else:
			self.map.translateZ = self.map.translateZ - zoomSpeed*deltaTicks;
			if(self.map.translateZ < (10.0-cDefines['maxZoom'])):
				self.map.translateZ = 10.0-cDefines['maxZoom']
	def handleMouseOver(self,name,isLeftMouseDown):
		#TODO: keeping track of mousedOverObject might not be necessary any more since I added previousMousedoverName to the C code
		if(isLeftMouseDown > 0):#allows onLeftClickDown to be called for tiles when the mouse is dragged over them
			if(gameState.getGameMode().selectedButton != None):
				if(gameState.getGameMode().selectedButton.tileType != cDefines['CITY_TILE_INDEX']):
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
		tiledGameMode.__init__(self)
		self.units = []
		self.cites = []
		self.nextUnit = None
		self.focusNextUnit = 0
		self.focusNextUnitTemp = 0
		self.selectedNode = None
	def loadMap(self):
		self.map = map(playModeNode)
		self.loadSummoners()
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
				elif(unit.node.tileValue == cDefines['MOUNTAIN_TILE_INDEX']):
					unit.movementPoints = unit.movementPoints + 0.1
				elif(unit.node.tileValue == cDefines['WATER_TILE_INDEX'] and unit.canSwim == False):
					unit.movementPoints = unit.movementPoints + 0.5
				elif(unit.node.tileValue == cDefines['DESERT_TILE_INDEX']):
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
		self.orderUnits()
		self.chooseNextUnit()
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
		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElement(xPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_RIGHT_INDEX'])
		uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_BOTTOM_INDEX'])

class mapEditorMode(tiledGameMode):	
	def __init__(self):
		tiledGameMode.__init__(self)
		self.selectedButton = None
		self.selectedCityNode = None
		self.cityEditor = None
		self.mapEditor = None
	def loadMap(self):
		self.map = map(mapEditorNode)
	def handleKeyDown(self,keycode):
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

		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_TOP_INDEX'])
		uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_LEFT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_LEFT_INDEX'])
		uiElement(xPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines['UI_MAP_EDITOR_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT']/cDefines['UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines['UI_MAP_EDITOR_RIGHT_INDEX'])

		uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines['UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_MAP_EDITOR_BOTTOM_INDEX'])
		self.cityEditor = cityEditor(0.0,0.0)

		mapEditorTileSelectUIElement(-0.93,0.92,tileType=cDefines['DESERT_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.85,0.92,tileType=cDefines['GRASS_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.77,0.92,tileType=cDefines['MOUNTAIN_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.69,0.92,tileType=cDefines['FOREST_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.61,0.92,tileType=cDefines['WATER_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.53,0.92,tileType=cDefines['ROAD_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines['CITY_TILE_INDEX'])
		for col in range(0,2):
			for row in range(0,4):

				playerStartLocationButton(-0.39+(0.05*col),0.972-(0.038*row),playerNumber=col*4+row+1,width=2.0*cDefines['PLAYER_START_BUTTON_WIDTH']/cDefines['SCREEN_WIDTH'],height=2.0*cDefines['PLAYER_START_BUTTON_HEIGHT']/cDefines['SCREEN_HEIGHT'],textureIndex=cDefines['PLAYER_START_BUTTON_INDEX'])
				uiElement(-0.370+(0.05*col),0.948-(0.04*row),text=str((col*4)+row+1),textSize=0.0004)
				
		mapEditorMapOptionsButton(-0.25,0.95,width=(2.0*cDefines['MAP_ICON_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['MAP_ICON_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['MAP_ICON_INDEX'],cursorIndex=cDefines['CURSOR_HAND_INDEX'])

		self.mapEditor = mapOptionsEditor(-0.91,0.75,text="map options",textSize=0.0005)

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
		self.elementsDict = {}
		self.map = None
	def handleKeyDown(self,keycode):
		if(keycode == "up"):
			if(newGameScreenButton.selectedIndex == 0):
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = newGameScreenButton.index - 1
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
			else:
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = newGameScreenButton.selectedIndex - 1
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
		elif(keycode == "down"):
			if(newGameScreenButton.selectedIndex == newGameScreenButton.index - 1):
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = 0
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
			else:
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  = newGameScreenButton.normalTextColor
				newGameScreenButton.selectedIndex = newGameScreenButton.selectedIndex + 1
				newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].textColor  =newGameScreenButton.selectedTextColor
		elif(keycode == "return"):
			newGameScreenButton.buttonsList[newGameScreenButton.selectedIndex].onClick()
					
class newGameScreenMode(textBasedMenuMode):
	def addUIElements(self):
		uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines['UI_NEW_GAME_SCREEN_INDEX'])
		newGameScreenButton(-0.16,0.2,text="new game",gameMode=playMode)
		newGameScreenButton(-0.165,0.1,text="map editor",gameMode=mapEditorSelectMode)
#		newGameScreenButton(-0.165,0.1,text="map editor",gameMode=mapEditorMode)

#		newGameScreenButton(-0.16,0.0,text="test test te",gameMode=gameMode)
#		newGameScreenButton(-0.17,-0.1,text="test test tes",gameMode=mapEditorMode)

class mapEditorSelectMode(textBasedMenuMode):
	def addUIElements(self):
		uiElement(-1.0,1.0,width=2.0,height=2.0,textureIndex=cDefines['UI_NEW_GAME_SCREEN_INDEX'])
		mapSelectButton(-0.16,0.2,text="map1")

gameState.setGameMode(newGameScreenMode)
gameState.getGameMode().addUIElements()
theGameMode = gameState.getGameMode()
