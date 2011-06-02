class node:
	def __init__(self,intName,tileValue):
		self.intName = intName
		self.tileValue = tileValue
	def getName(self):
		return self.intName
	def getValue(self):
		return self.tileValue


class map:
	def __init__(self,name):
		self.name = name
		self.mapFile =  open('map1','rw')#TODO: close this file
		self.nodes = []
		self.intGenerator = intGenerator()
		for line in self.mapFile:
			newRow = []
			for char in line:
				if(char != '\n'):
					newRow.append(node(self.intGenerator.getNextInt(),int(char)))
			self.nodes.append(newRow)
#		self.nodes = [[node(self.intGenerator.getNextInt(),0),node(self.intGenerator.getNextInt(),0),node(self.intGenerator.getNextInt(),0)],[node(self.intGenerator.getNextInt(),0),node(self.intGenerator.getNextInt(),0),node(self.intGenerator.getNextInt(),0)]]
	def getName(self):
		self.intGenerator.getNextInt()
		return self.name
	def getNodes(self):
		return self.nodes
	def getIterator(self):
		return self.nodes.__iter__()
class intGenerator:
	def __init__(self):
		self.nextInt = 0
	def getNextInt(self):
		self.nextInt = self.nextInt + 1
		return self.nextInt

map1 = map("map1")
