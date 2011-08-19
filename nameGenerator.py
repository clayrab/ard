
#class intNameGenerator:
#	def __init__(self):
#		self.nextName = -1
#	def getNextName(self):
#		self.nextName = self.nextName + 1
#		return self.nextName

nextName = -1
def getNextName():
    global nextName
    nextName = nextName + 1
    return nextName
