import cDefines
def texIndex(textureName):
	return cDefines.defines[textureName+"_INDEX"]
def texWidth(textureName):
#	return (2.0*cDefines.defines[textureName+'_WIDTH']/cDefines.defines['SCREEN_WIDTH'])
	return (2.0*cDefines.defines[textureName+'_WIDTH']/1600.0)
def texHeight(textureName):
#	return (2.0*cDefines.defines[textureName+'_HEIGHT']/cDefines.defines['SCREEN_HEIGHT'])
	return (2.0*cDefines.defines[textureName+'_HEIGHT']/1200.0)
