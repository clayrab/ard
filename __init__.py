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
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False):
		self.name = nameGenerator.getNextName()
		self.xPosition = xPos
		self.yPosition = yPos
		self.width = width
		self.height = height
		self.textureIndex = textureIndex
		self.hidden=hidden
		theMapEditor.uiElements.append(self)

class mapEditorTileSelectUIElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,textureIndex=-1,hidden=False,tileType=0):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex)
		self.tileType = tileType
		theMapEditor.clickableObjsDict[self.name] = self
	def onClick(self):
		theMapEditor.selectedTileType = self.tileType
		

class textUIElement(uiElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,text="",textSize=1.0,textureIndex=-1):
		uiElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex)
		self.text = text
		self.textSize = textSize

class textInputUIElement(textUIElement):
	def __init__(self,xPos,yPos,width=1.0,height=1.0,text="",textSize=1.0,textureIndex=-1):
		textUIElement.__init__(self,xPos,yPos,width=width,height=height,textureIndex=textureIndex,text=text)
		theMapEditor.clickableObjsDict[self.name] = self

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

	def getUIElementsIterator(self):
		return self.uiElements.__iter__()
	def isNameClickable(self,name):
		return self.clickableObjsDict.has_key(name)
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
		else:
			try:
				int(keycode)
			except:
				return
	def addUIElements(self):
		uiElement(xPos=-1.0,yPos=1.0,width=2.0,height=(2.0*cDefines['UI_TOP_IMAGE_HEIGHT']/cDefines['UI_TOP_IMAGE_WIDTH']),textureIndex=cDefines['UI_TOP_INDEX'])
		mapEditorTileSelectUIElement(-0.93,0.92,tileType=0)
		textUIElement(0.0,0.92,width=1.0,height=1.0,text="asdf",textSize=0.5,textureIndex=-1)
		mapEditorTileSelectUIElement(-0.85,0.92,tileType=1)
		mapEditorTileSelectUIElement(-0.77,0.92,tileType=2)
		mapEditorTileSelectUIElement(-0.69,0.92,tileType=3)
		mapEditorTileSelectUIElement(-0.61,0.92,tileType=4)
		textInputUIElement(-0.2,0.92,text="input")
		
theMapEditor = mapEditor()
theMapEditor.addUIElements()
