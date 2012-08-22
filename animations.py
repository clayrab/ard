import cDefines

class animation(object):
    def __init__(self,type,unit=None,xPos=0.0,yPos=-0.0):
        self.type = type
        self.unit = unit
        self.xPos = xPos
        self.yPos = yPos
class unitSlideAnimation(animation):
    def __init__(self,unit):
        animation.__init__(self,cDefines.defines["ANIMATION_UNIT_SLIDE"],unit=unit)

class autoFocusAnimation(animation):
    def __init__(self,xPos,yPos):
        animation.__init__(self,cDefines.defines["ANIMATION_AUTO_FOCUS"],xPos=xPos,yPos=yPos)

class damageAnimation(animation):
    def __init__(self):
        animation.__init__(self,cDefines.defines["ANIMATION_DAMAGE"])
