class intNameGenerator:
	def __init__(self):
		self.nextName = -1
	def getNextName(self):
		self.nextName = self.nextName + 1
		return self.nextName

nameGenerator = intNameGenerator()

class uiElement:
	def __init__(self,xPos,yPos,tile=0):
		self.name = nameGenerator.getNextName()
		self.xPosition = xPos
		self.yPosition = yPos
	def onClick(self):
		print "uiElem: " + str(self.name)

class textUIElement(uiElement):
	def __init__(self,xPos,yPos,tile=0,text=""):
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
		print "onClick: " + str(self.name)

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
		self.uiElements = []
#		  //  glTranslatef(-0.93,0.92,0.0);

		newUIElement = uiElement(-0.93,0.92)
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement
		
		newUIElement = uiElement(-0.85,0.92)
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = textUIElement(-0.77,0.92,text="asdf")
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		newUIElement = textInputUIElement(-0.69,0.92,text="input")
		self.uiElements.append(newUIElement)
		self.clickableObjsDict[newUIElement.name] = newUIElement

		self.elementWithFocus = None
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
