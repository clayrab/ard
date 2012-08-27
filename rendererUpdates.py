import cDefines
class rendererUpdate(object):
    def __init__(self,type,unit=None,node=None,xPos=0.0,yPos=0.0,health=0.0):
        self.type = type
        self.unit = unit
        self.node = None
        self.xPos = xPos
        self.yPos = yPos

class renderNewUnit(rendererUpdate):
    def __init__(self,unit):
        rendererUpdate.__init__(self,cDefines.defines["RENDERER_CHANGE_UNIT_ADD"],unit=unit)

class renderRemoveUnit(rendererUpdate):
    def __init__(self,unit):
        rendererUpdate.__init__(self,cDefines.defines["RENDERER_CHANGE_UNIT_REMOVE"],unit=unit)

class renderUnitChange(rendererUpdate):
    def __init__(self,unit):
        rendererUpdate.__init__(self,cDefines.defines["RENDERER_CHANGE_UNIT_CHANGE"],unit=unit)

class renderNodeChange(rendererUpdate):
    def __init__(self,node):
        rendererUpdate.__init__(self,cDefines.defines["RENDERER_CHANGE_NODE_CHANGE"],node=node)

class renderTextChange(rendererUpdate):
    def __init__(self,unit):
        rendererUpdate.__init__(self,cDefines.defines["RENDERER_CHANGE_TEXT_INPUT"])

class renderSelectNextUnit(rendererUpdate):
    def __init__(self):
        rendererUpdate.__init__(self,cDefines.defines["RENDERER_SELECT_NEXT_UNIT"])
    
class renderFocus(rendererUpdate):
    def __init__(self,xPos,yPos):
        rendererUpdate.__init__(self,cDefines.defines["RENDERER_FOCUS"],xPos=xPos,yPos=yPos)
    
    
