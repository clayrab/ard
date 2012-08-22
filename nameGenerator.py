
#class intNameGenerator:
#	def __init__(self):
#		self.nextName = -1
#	def getNextName(self):
#		self.nextName = self.nextName + 1
#		return self.nextName

nextName = 5000#going to use the first 5000 names for text
def getNextName():
    global nextName
    nextName = nextName + 1
    return nextName
