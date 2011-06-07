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
cFile =  open('main.c','r')#TODO: close this file
for line in cFile:
	if(line.strip().startswith("#define")):
		tokens = line.split()
		if(isInt(tokens[2])):
			cDefines[tokens[1]] = int(tokens[2])
		elif(isFloat(tokens[2])):
			cDefines[tokens[1]] = float(tokens[2])
		else:
			cDefines[tokens[1]] = tokens[2]

#print cDefines['TILE_GRASS']
#print cDefines['SIN60']
#print cDefines['tilesImage']


class intNameGenerator:
	def __init__(self):
		self.nextName = -1
	def getNextName(self):
		self.nextName = self.nextName + 1
		return self.nextName

nameGenerator = intNameGenerator()

class uiElement:
	def __init__(self,xPos,yPos,width=0,height=0,textureIndex=0):
		self.name = nameGenerator.getNextName()
		self.xPosition = xPos
		self.yPosition = yPos
		self.width = width
		self.height = height
		self.textureIndex = textureIndex

class mapEditorTileSelectUIElement(uiElement):
	def __init__(self,xPos,yPos,tileType=0):
		uiElement.__init__(self,xPos,yPos)
		self.tileType = tileType
	def onClick(self):
		theMapEditor.selectedTileType = self.tileType
		

class textUIElement(uiElement):
	def __init__(self,xPos,yPos,text=""):
		uiElement.__init__(self,xPos,yPos)
		self.text = text

class textInputUIElement(textUIElement):
	def onClick(self):
		print "onclick"
	def onKeyDown(self,keycode):
		if(keycode == "backspace"):
			self.text = self.text.rstrip(self.text[len(self.text)-1])
		else:
			self.text = self.text + keycode

class node:
	def __init__(self,tileValue):
		self.name = nameGenerator.getNextName()
		self.tileValue = tileValue
	def getValue(self):
		return self.tileValue
	def onClick(self):
		if(theMapEditor.selectedTileType != -1):
			self.tileValue = theMapEditor.selectedTileType

class map:
	def __init__(self,mapEditor):
		self.mapFile =  open('map1','rw')#TODO: close this file
		self.nodes = []
		for line in self.mapFile:
			newRow = []
			for char in line:
				if(char != '\n'):
					newNode = node(int(char))
					newRow.append(newNode)
					mapEditor.clickableObjsDict[newNode.name] = newNode
			self.nodes.append(newRow)
	def getNodes(self):
		return self.nodes
	def getIterator(self):
		return self.nodes.__iter__()

class mapEditor:
	def __init__(self):
		self.clickableObjsDict = {}
		self.map = map(self)
		self.elementWithFocus = None
		self.selectedTileType = -1
		self.uiElements = []

		newUIElement = uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines['UI_TOP_IMAGE_HEIGHT']/cDefines['UI_TOP_IMAGE_WIDTH']),textureIndex=cDefines['UI_TOP_INDEX'])
		self.uiElements.append(newUIElement)

		newUIElement = mapEditorTileSelectUIElement(-0.93,0.92,tileType=0)
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = textUIElement(-0.963,0.88,text="asdf")
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = mapEditorTileSelectUIElement(-0.85,0.92,tileType=1)
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = mapEditorTileSelectUIElement(-0.77,0.92,tileType=2)
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = mapEditorTileSelectUIElement(-0.69,0.92,tileType=3)
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = mapEditorTileSelectUIElement(-0.61,0.92,tileType=4)
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = textInputUIElement(-0.69,0.92,text="input")
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

	def getUIElementsIterator(self):
		return self.uiElements.__iter__()
	def handleClick(self,name):
		if(self.clickableObjsDict.has_key(name)):
			self.elementWithFocus = self.clickableObjsDict[name]
			self.clickableObjsDict[name].onClick()
		else:
			self.elementWithFocus = None
	def handleKeyDown(self,keycode):
		if(self.elementWithFocus != None):
			if(hasattr(self.elementWithFocus,'onKeyDown')):
				self.elementWithFocus.onKeyDown(keycode)
		
theMapEditor = mapEditor()
