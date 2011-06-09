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
class intNameGenerator:
	def __init__(self):
		self.nextName = -1
	def getNextName(self):
		self.nextName = self.nextName + 1
		return self.nextName

nameGenerator = intNameGenerator()

class uiElement:
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False,cursorIndex=-1,text=""):
		self.name = nameGenerator.getNextName()
		self.xPosition = xPos
		self.yPosition = yPos
		self.width = width
		self.height = height
		self.textureIndex = textureIndex
		self.hidden=hidden
		self.cursorIndex=cursorIndex
		self.text = text
		theGameMode.uiElements.append(self)

class clickableElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False,cursorIndex=-1,text=""):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text,cursorIndex=cDefines['CURSOR_HAND_INDEX'])
		theGameMode.clickableObjsDict[self.name] = self
class saveButton(clickableElement):		
	def onClick(self):
		theGameMode.map.save()
#TODO: MAKE SURE YOU CAN'T REMOVE THE LAST ROW OR COLUMN!!
class addColumnButton(clickableElement):
	def onClick(self):
		for row in theGameMode.map.nodes:
			row.append(node(0,0,0))
class removeColumnButton(clickableElement):
	def onClick(self):
		for row in theGameMode.map.nodes:
			row.pop()
class addFirstColumnButton(clickableElement):
	def onClick(self):
		for count in range(0,len(theGameMode.map.nodes)):
			rowCopy = theGameMode.map.nodes[count][:]
			rowCopy.reverse()
			rowCopy.append(node(0,0,0))
			rowCopy.reverse()
			theGameMode.map.nodes[count] = rowCopy
class removeFirstColumnButton(clickableElement):
	def onClick(self):
		for count in range(0,len(theGameMode.map.nodes)):
			rowCopy = theGameMode.map.nodes[count][:]
			rowCopy.reverse()
			rowCopy.pop()
			rowCopy.reverse()
			theGameMode.map.nodes[count] = rowCopy

class addRowButton(clickableElement):
	def onClick(self):
		newRow = []
		for count in range(0,len(theGameMode.map.nodes[0])):
			newRow.append(node(0,0,0))
		theGameMode.map.nodes.append(newRow)
class removeRowButton(clickableElement):
	def onClick(self):
		theGameMode.map.nodes.pop()
class addFirstRowButton(clickableElement):
	def onClick(self):
		nodesCopy = theGameMode.map.nodes[:]
		newRow = []
		for count in range(0,len(theGameMode.map.nodes[0])):
			newRow.append(node(0,0,0))
		nodesCopy.reverse()
		nodesCopy.append(newRow)
		nodesCopy.reverse()
		theGameMode.map.polarity = (~theGameMode.map.polarity)&1
		theGameMode.map.nodes = nodesCopy

class removeFirstRowButton(clickableElement):
	def onClick(self):
		nodesCopy = theGameMode.map.nodes[:]
		nodesCopy.reverse()
		nodesCopy.pop()
		nodesCopy.reverse()
		theGameMode.map.polarity = (~theGameMode.map.polarity)&1
		theGameMode.map.nodes = nodesCopy


class mapEditorTileSelectUIElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False,tileType=0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,cursorIndex=cDefines['CURSOR_HAND_INDEX'])
		self.tileType = tileType
		self.selected = False
		theGameMode.clickableObjsDict[self.name] = self
	def onClick(self):
		if(theGameMode.selectedTile != None):
			theGameMode.selectedTile.selected = False
		self.selected = True
		theGameMode.selectedTile = self

class textInputUIElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,text="",textSize=1.0,textureIndex=-1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text)
		theGameMode.clickableObjsDict[self.name] = self

	def onClick(self):
		print "onclick"
	def onKeyDown(self,keycode):
		if(keycode == "backspace"):
			self.text = self.text.rstrip(self.text[len(self.text)-1])
		else:
			self.text = self.text + keycode

class node:
	def __init__(self,tileValue,roadValue,cityValue):
		self.name = nameGenerator.getNextName()
		self.tileValue = tileValue
		self.roadValue = roadValue
		self.cityValue = cityValue
		self.selected = False
		theGameMode.clickableObjsDict[self.name] = self

	def getValue(self):
		return self.tileValue
	def onClick(self):
		if(theGameMode.selectedTile != None):
			if(theGameMode.selectedTile.tileType == cDefines['ROAD_TILE_INDEX']):
				self.roadValue = (~self.roadValue)&1
			elif(theGameMode.selectedTile.tileType == cDefines['CITY_TILE_INDEX']):
				self.cityValue = (~self.cityValue)&1
			else:
				self.tileValue = theGameMode.selectedTile.tileType
	def onRightClick(self):
		if(theGameMode.selectedNode != None):
			theGameMode.selectedNode.selected = False
		self.selected = True
		theGameMode.selectedNode = self


class map:
	def __init__(self,mapEditor):
		self.polarity = 0
		self.load(mapEditor)
	def load(self,mapEditor):
		mapFile = open('map1','r')
		self.nodes = []
		count = 0
		for line in mapFile:
			if(count == 0):
				self.polarity = int(line)
				print self.polarity
			else:
				newRow = []
				for char in line:
					if(char != '\n'):
						intValue = ord(char)
						tileValue = intValue & 15
						roadValue = (intValue & 16)>>4
						cityValue = (intValue & 32)>>5
						newNode = node(tileValue,roadValue,cityValue)
						newRow.append(newNode)
				self.nodes.append(newRow)
			count = count + 1
		mapFile.close()
	def save(self):
		mapFile = open('map1','w')
		lines = []
		lines.append(str(self.polarity) + "\n")
		for row in self.nodes:
			line = ""
			for node in row:
				line = line + chr(node.tileValue + (16*node.roadValue) + (32*node.cityValue))
			lines.append(line + "\n")
		mapFile.writelines(lines)
		mapFile.close()
		print "done"
	def getNodes(self):
		return self.nodes
	def getIterator(self):
		return self.nodes.__iter__()

class mapEditor:
	def __init__(self):
		self.clickableObjsDict = {}
		self.elementWithFocus = None
		self.selectedTile = None
		self.uiElements = []
		self.selectedNode = None
	def loadMap(self):
		self.map = map(self)
	def getUIElementsIterator(self):
		return self.uiElements.__iter__()
	def handleRightClick(self,name):
		rightClickable = False
		if(self.clickableObjsDict.has_key(name)):
			if(hasattr(self.clickableObjsDict[name],"onRightClick")):
				rightClickable = True
				self.clickableObjsDict[name].onRightClick()
		if(not rightClickable):
			self.selectedNode.selected = False
			self.selectedNode = None
	def handleClick(self,name):
		if(self.clickableObjsDict.has_key(name)):
			self.elementWithFocus = self.clickableObjsDict[name]
			self.clickableObjsDict[name].onClick()
		else:
			self.elementWithFocus = None
	def handleKeyDown(self,keycode):
		try:
			self.elementWithFocus.onKeyDown(keycode)
		except:
			try:
				intKeycode = int(keycode)
				for key,value in self.clickableObjsDict.iteritems():
					if(hasattr(value,'tileType')):
						if(value.tileType == intKeycode-1):
							if(self.selectedTile != None):
								self.selectedTile.selected = False
							value.selected = True
							self.selectedTile = value
			except:
				return
	def addUIElements(self):
		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines['UI_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_TOP_INDEX'])
		uiElement(xPos=-1.0,yPos=1.0-(2.0*cDefines['UI_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_LEFT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_LEFT_IMAGE_HEIGHT']/cDefines['UI_LEFT_IMAGE_WIDTH']),textureIndex=cDefines['UI_LEFT_INDEX'])
		uiElement(xPos=1.0-(2.0*cDefines['UI_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),yPos=1.0-(2.0*cDefines['UI_TOP_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=(2.0*cDefines['UI_RIGHT_IMAGE_WIDTH']/cDefines['SCREEN_WIDTH']),height=(2.0*cDefines['UI_RIGHT_IMAGE_HEIGHT']/cDefines['UI_RIGHT_IMAGE_WIDTH']),textureIndex=cDefines['UI_RIGHT_INDEX'])
#-
		uiElement(xPos=-1.0,yPos=-1.0+(2.0*cDefines['UI_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),width=2.0,height=(2.0*cDefines['UI_BOTTOM_IMAGE_HEIGHT']/cDefines['SCREEN_HEIGHT']),textureIndex=cDefines['UI_BOTTOM_INDEX'])

		mapEditorTileSelectUIElement(-0.93,0.92,tileType=cDefines['DESERT_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.85,0.92,tileType=cDefines['GRASS_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.77,0.92,tileType=cDefines['MOUNTAIN_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.69,0.92,tileType=cDefines['JUNGLE_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.61,0.92,tileType=cDefines['WATER_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.53,0.92,tileType=cDefines['ROAD_TILE_INDEX'])
		mapEditorTileSelectUIElement(-0.45,0.92,tileType=cDefines['CITY_TILE_INDEX'])

		addColumnButton(0.98,0.03,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeColumnButton(0.98,-0.03,width=1.0,height=1.0,text="-",textureIndex=-1)

		addFirstColumnButton(-0.63,0.03,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeFirstColumnButton(-0.63,-0.03,width=1.0,height=1.0,text="-",textureIndex=-1)

		addRowButton(0.18,-0.98,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeRowButton(0.21,-0.98,width=1.0,height=1.0,text="-",textureIndex=-1)

		addFirstRowButton(0.18,0.77,width=1.0,height=1.0,text="+",textureIndex=-1)
		removeFirstRowButton(0.21,0.77,width=1.0,height=1.0,text="-",textureIndex=-1)

		textInputUIElement(0.8,0.885,text="input")
		uiElement(0.8,0.925,width=1.0,height=1.0,text="asdf",textureIndex=-1)
		saveButton(0.9,0.925,width=1.0,height=1.0,text="save",textureIndex=-1)
class newGameScreen:
	def __init__(self):
		self.clickableObjsDict = {}
		self.elementWithFocus = None
		self.uiElements = []
		self.map = None
	def getUIElementsIterator(self):
		return self.uiElements.__iter__()
	def handleRightClick(self,name):
		rightClickable = False
		if(self.clickableObjsDict.has_key(name)):
			if(hasattr(self.clickableObjsDict[name],"onRightClick")):
				rightClickable = True
				self.clickableObjsDict[name].onRightClick()
		if(not rightClickable):
			self.selectedNode.selected = False
			self.selectedNode = None
	def handleClick(self,name):
		if(self.clickableObjsDict.has_key(name)):
			self.elementWithFocus = self.clickableObjsDict[name]
			self.clickableObjsDict[name].onClick()
		else:
			self.elementWithFocus = None
	def handleKeyDown(self,keycode):
		try:
			self.elementWithFocus.onKeyDown(keycode)
		except:
			try:
				intKeycode = int(keycode)
				for key,value in self.clickableObjsDict.iteritems():
					if(hasattr(value,'tileType')):
						if(value.tileType == intKeycode-1):
							if(self.selectedTile != None):
								self.selectedTile.selected = False
							value.selected = True
							self.selectedTile = value
			except:
				return
	def addUIElements(self):
		textInputUIElement(0.8,0.885,text="input")
		uiElement(0.8,0.925,width=1.0,height=1.0,text="asdf",textureIndex=-1)
		saveButton(0.9,0.925,width=1.0,height=1.0,text="save",textureIndex=-1)

theGameMode = newGameScreen()
theGameMode.addUIElements()


#theGameMode = mapEditor()
#theGameMode.loadMap()
#theGameMode.addUIElements()
