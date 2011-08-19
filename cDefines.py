import gameState
import sys

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

defines = {}
cFile =  open('main.c','r')
for line in cFile:
    if(line.strip().startswith("#define")):
        tokens = line.split()
        if(isInt(tokens[2])):
            defines[tokens[1]] = int(tokens[2])
        elif(isFloat(tokens[2])):
            defines[tokens[1]] = float(tokens[2])
        else:
            defines[tokens[1]] = tokens[2]
cFile.close()

