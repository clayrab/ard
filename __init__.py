class node:
	def __init__(self,neighbor):
		self.neightbors = []
	
class map:
	def __init__(self,name):
		self.name = name
		self.nodes = [[1,0,1],[0,0,1],[1,0,1]]
		for row in self.nodes:
			print row
	def getName(self):
		return self.name
		
map1 = map("map1")