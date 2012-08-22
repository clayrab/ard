#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <SDL.h>
#include <SDL_opengl.h>
#include <SDL_mixer.h>

#include <libpng12/png.h>
#include <Python/Python.h>

#include <ft2build.h>
#include <freetype/freetype.h>
#include <freetype/ftglyph.h>
#include <freetype/ftoutln.h>
#include <freetype/fttrigon.h>
#include "pystacktrace.c"

#include "fonts.c"
#include "defines.c"
#include "structs.c"
#include "animQueue.c"

float focusSpeed = 0.0;
float focusSpeedX = 0.0;
float focusSpeedY = 0.0;

float screenRatio;
static SDL_Surface *gScreen;

int clickScroll = 0;
long doFocus = 0;
double focusXPos, focusYPos, focusTilesXPos, focusTilesYPos;
PyObject * pyFocusXPos;
PyObject * pyFocusYPos;
int isFocusing = 0;
int isSliding = 0;
int isAnimating = 0;
int doneAnimatingFired = 0;
int considerDoneFocusing = 0;
int leftButtonDown = 0;

int done = 0;    
int moveUp = 0;
int moveRight = 0;
int currentTick = 0;
int deltaTicks = 0;
int testTicks1 = 0;
int testTicks2 = 0;
int testTicks3 = 0;
int testTicks4 = 0;
int testTicks5 = 0;
int avgDeltaTicks = 0;
int totalDeltaTicksDataPoints = 0;

int keyHeld;
int repeatKey;
Uint32 keyHeldTime;

GLfloat mapDepth,mapDepthTest1,mapDepthTest2,mapDepthTest3;
float translateX = 0.0;
float translateY = 0.0;
float translateZ = 0.0-initZoom;
float translateXPrev = 0.0;
float translateYPrev = 0.0;
float translateZPrev = 0.0-initZoom;
float translateZPrev2 = 0.0;
float scrollSpeed = 0.10;

PyObject * pyPolarity;
long mapPolarity;
PyObject * pyLoaded;
long mapLoaded;

GLdouble convertedBottomLeftX,convertedBottomLeftY,convertedBottomLeftZ;
GLdouble convertedTopRightX,convertedTopRightY,convertedTopRightZ;
GLdouble convertedCenterX,convertedCenterY,convertedCenterZ;

PyObject * pyUnitType;
PyObject * pyUnitTextureIndex;
PyObject * pyName;
PyObject * pyHealth;
PyObject * pyMaxHealth;
PyObject * pyLevel;
PyObject * pyPlayerNumber;
PyObject * pyRecentDamage;
PyObject * pyRecentDamageIter;
PyObject * pyDamageTime;
int damageTime;
PyObject * pyDamage;
char * damageStr;
char lvlStr[3];
char * unitName;
long playerNumber;
long unitTextureIndex;
int level;
int flagBits;
double healthBarLength;
PyObject * uiElement;
//PyObject * gameModule;
PyObject * gameState;
PyObject * gameMode;
PyObject * theMap;
PyObject * mapName;
PyObject * mapIterator;
PyObject * UIElementsIterator;
PyObject * rowIterator;
PyObject * pyMapWidth;
PyObject * pyMapHeight;
//PyObject * pyObj;
//PyObject * playableMode;
long mapWidth;
long mapHeight;

GLuint tilesTexture;
GLdouble mouseMapPosX, mouseMapPosY, mouseMapPosZ;
GLdouble mouseMapPosXPrevious, mouseMapPosYPrevious, mouseMapPosZPrevious = -initZoom;
GLint bufRenderMode;
float *textureVertices;
GLuint texturesArray[300];
Mix_Chunk * soundArray[50];
Mix_Music * musicArray[50];
GLuint tilesLists;
GLuint selectionBoxList;
GLuint unitList;
GLuint healthBarList;
GLuint flagList;

int mouseX = 0;
int mouseY = 0;
GLuint selectBuf[BUFSIZE];

int selectedName = -1;//the mousedover object's 'name'
int selectedNodeName = -1;//the mousedover object's 'name'
int previousClickedName = -2;
int previousMousedoverName = -2;
int theCursorIndex = -1;
float * vertexArrays[9];

float forestVertices[6][2] = {
  {(643.0/1280),1.0-(360.0/1280)},
  {(643.0/1280),1.0-(328.0/1280)},
  {(670.0/1280),1.0-(312.0/1280)},
  {(696.0/1280),1.0-(328.0/1280)},
  {(696.0/1280),1.0-(360.0/1280)},
  {(670.0/1280),1.0-(376.0/1280)}
};
float blueForestVertices[6][2] = {
  {(643.0/1280),1.0-(458.0/1280)},
  {(643.0/1280),1.0-(426.0/1280)},
  {(670.0/1280),1.0-(410.0/1280)},
  {(696.0/1280),1.0-(426.0/1280)},
  {(696.0/1280),1.0-(458.0/1280)},
  {(670.0/1280),1.0-(474.0/1280)}
};
float grassVertices[6][2] = {
  {(699.0/1280),1.0-(360.0/1280)},
  {(699.0/1280),1.0-(328.0/1280)},
  {(726.0/1280),1.0-(312.0/1280)},
  {(754.0/1280),1.0-(328.0/1280)},
  {(754.0/1280),1.0-(360.0/1280)},
  {(726.0/1280),1.0-(376.0/1280)}
};
float mountainVertices[6][2] = {
  {(699.0/1280),1.0-(556.0/1280)},
  {(699.0/1280),1.0-(524.0/1280)},
  {(726.0/1280),1.0-(508.0/1280)},
  {(754.0/1280),1.0-(524.0/1280)},
  {(754.0/1280),1.0-(556.0/1280)},
  {(726.0/1280),1.0-(572.0/1280)}
};
float waterVertices[6][2] = {
  {(874.0/1280),1.0-(850.0/1280)},
  {(874.0/1280),1.0-(818.0/1280)},
  {(901.0/1280),1.0-(802.0/1280)},
  {(928.0/1280),1.0-(818.0/1280)},
  {(928.0/1280),1.0-(850.0/1280)},
  {(901.0/1280),1.0-(866.0/1280)}
};
float roadVertices[6][2] = {
  {(467.0/1280),1.0-(66.0/1280)},
  {(467.0/1280),1.0-(34.0/1280)},
  {(494.0/1280),1.0-(18.0/1280)},
  {(522.0/1280),1.0-(34.0/1280)},
  {(522.0/1280),1.0-(66.0/1280)},
  {(494.0/1280),1.0-(82.0/1280)}
};
float cityVertices[6][2] = {
  {(641.0/1280),1.0-(66.0/1280)},
  {(641.0/1280),1.0-(34.0/1280)},
  {(668.0/1280),1.0-(18.0/1280)},
  {(696.0/1280),1.0-(34.0/1280)},
  {(696.0/1280),1.0-(66.0/1280)},
  {(668.0/1280),1.0-(82.0/1280)}
};
float playerStartVertices[6][2] = {
  {(593.0/1280),1.0-(556.0/1280)},
  {(593.0/1280),1.0-(524.0/1280)},
  {(610.0/1280),1.0-(508.0/1280)},
  {(638.0/1280),1.0-(524.0/1280)},
  {(638.0/1280),1.0-(556.0/1280)},
  {(610.0/1280),1.0-(572.0/1280)}
};

/*float hexagonVertices[6][2] = {
  //cheated these all out by 0.01 so the black background doesn't bleed through
  {-SIN60-0.01, -COS60-0.01},
  {-SIN60-0.01, COS60+0.01},
  {0.01, 1.01},
  {SIN60+0.01, COS60+0.01},
  {SIN60+0.01, -COS60-0.01},
  {0.01, -1.01}
  };*/
float hexagonVertices[6][2] = {
  //cheated these all out by 0.03 so the black background doesn't bleed through
  {-SIN60-0.02, -COS60-0.00},
  {-SIN60-0.02, COS60+0.00},
  {0.00, 1.00},
  {SIN60+0.02, COS60+0.00},
  {SIN60+0.02, -COS60-0.00},
  {0.00, -1.00}
};
float textureHexVertices[6][2] = {
  {0.0,0.25},
  {0.0,0.75},
  {0.5,1.0},
  {1.0,0.75},
  {1.0,0.25},
  {0.5,0.0}
};


float returnVal;
float translateTilesXToPositionX(int tileX,int tileY){
  //return (float)tilesX*-(1.9*SIN60);
  returnVal = (float)tileX*-(2.0*SIN60);
  if(abs(tileY)%2 == mapPolarity){
    returnVal += SIN60;
  }
  return returnVal;
}
float translateTilesYToPositionY(int tileY){
  return (float)(tileY*1.5);
}

int rowNumber;
PyObject * pyNode;
PyObject * row;
PyObject * pyXPosition;
PyObject * pyYPosition;
double xPosition;
double yPosition;
int colNumber;
PyObject * nodeIterator;
PyObject * pyNodeName;
PyObject * pyNodeValue;
//PyObject * pyRoadValue;
PyObject * pyCursorIndex;
PyObject * pyPlayerStartValue;
PyObject * pyIsOnMovePath;
PyObject * pyIsVisible;
long isVisible;
PyObject * pySelectionBoxScale;
double selectionBoxScale;
long longName;
long longValue;
//long longRoadValue;
char * cityName;
PyObject * nextUnit;
PyObject * pyUnitPlayer;
long unitPlayer;
long playerStartValue;
long isOnMovePath;
PyObject * pyUnits;
PyObject *pyUnitsIter;
PyObject * pyCities;
PyObject *pyCitiesIter;
PyObject * city;

MAP theMapp;
NODE * theNode;

void loadMap(){
  //theMapp = &(MAP);
  mapIterator = PyObject_CallMethod(theMap,"getIterator",NULL);  
  pyPolarity = PyObject_GetAttrString(theMap,"polarity");
  mapPolarity = PyLong_AsLong(pyPolarity);
  Py_DECREF(pyPolarity);
  rowIterator = PyObject_GetIter(mapIterator);
  pyMapWidth = PyObject_CallMethod(theMap,"getWidth",NULL);//New reference
  theMapp.width = PyLong_AsLong(pyMapWidth);
  Py_DECREF(pyMapWidth);
  pyMapHeight = PyObject_CallMethod(theMap,"getHeight",NULL);//New reference
  theMapp.height = PyLong_AsLong(pyMapHeight);
  Py_DECREF(pyMapHeight);
  theMapp.size = theMapp.width*theMapp.height;
  theMapp.nodes = malloc(theMapp.size*sizeof(NODE));
  int nodesIndex = 0;
  while (row = PyIter_Next(rowIterator)) {
    colNumber = 0;
    rowNumber = rowNumber + 1;
    nodeIterator = PyObject_GetIter(row);
    while(pyNode = PyIter_Next(nodeIterator)) {
      theNode = (&(theMapp.nodes[nodesIndex]));
      theNode->xIndex = colNumber;
      theNode->yIndex = rowNumber;
      xPosition = translateTilesXToPositionX(colNumber,rowNumber);
      yPosition = translateTilesYToPositionY(rowNumber);
      theNode->xPos = xPosition;
      theNode->yPos = yPosition;
      pyNodeName = PyObject_GetAttrString(pyNode,"name");
      theNode->name = PyLong_AsLong(pyNodeName);
      Py_DECREF(pyNodeName);
      pyNodeValue = PyObject_GetAttrString(pyNode,"tileValue");
      theNode->tileValue = PyLong_AsLong(pyNodeValue);      
      Py_DECREF(pyNodeValue);
      pyPlayerStartValue = PyObject_GetAttrString(pyNode,"playerStartValue");
      theNode->playerStartValue = PyLong_AsLong(pyPlayerStartValue);
      Py_DECREF(pyPlayerStartValue);
      pyIsVisible = PyObject_GetAttrString(pyNode,"visible");//New reference
      theNode->visible = PyLong_AsLong(pyIsVisible);
      Py_DECREF(pyIsVisible);
      pyIsOnMovePath = PyObject_GetAttrString(pyNode,"onMovePath");//New reference
      theNode->onMovePath = PyLong_AsLong(pyIsOnMovePath);
      Py_DECREF(pyIsOnMovePath);
      nodesIndex++;
      colNumber = colNumber - 1;
    }
    Py_DECREF(row);
    Py_DECREF(nodeIterator);
  }
  Py_DECREF(rowIterator); 
  Py_DECREF(mapIterator);
}


/**************************** mouse hover object selection ********************************/
void testTicks(char * label, long ticksCounter){
  printf("%s:\t%ld\n",label,SDL_GetTicks() - ticksCounter); ticksCounter = SDL_GetTicks(); 
//  printf("****** a:    \t%d\n",SDL_GetTicks() - testTicks5); testTicks5 = SDL_GetTicks(); 

}
GLuint *bufferPtr,*ptrNames, numberOfNames;
int count;
int nameValue;
int namesCount;
int mouseTextPositionSet;
void processTheHits(GLint hitsCount, GLuint buffer[]){
  glFlush();
  selectedName = -1;
  count = 0;
  nameValue = 0;
  bufferPtr = (GLuint *) buffer;
  mouseTextPositionSet = 0;
  while(count < hitsCount){
    namesCount = 0;
    numberOfNames = *bufferPtr;
    //    nameValue = *(bufferPtr + 3);//the value of the name is stored +3 over in mem
    if(numberOfNames >= 1){
      //elements are created from back to front, the names should be in this order so we return the largest name
      while(namesCount < numberOfNames){
	nameValue = *(bufferPtr + 3 + namesCount);//the value of the name is stored +3 over in mem
	namesCount = namesCount + 1;
	if(nameValue > selectedName){
	  selectedName = nameValue;
	}
      }
      if(nameValue < 5000){//first 5000 names are reserved for text
	pyObj = PyObject_CallMethod(gameMode,"setMouseTextPosition","i",nameValue);
	Py_DECREF(pyObj);
	mouseTextPositionSet = 1;
      }
    }
    bufferPtr = bufferPtr + 3 + numberOfNames;
    count = count + 1;
  }  
  if(!mouseTextPositionSet){
    pyObj = PyObject_CallMethod(gameMode,"setMouseTextPosition","i",-1);
    if(pyObj != NULL){
      Py_DECREF(pyObj);
    }
  }
}

//float glMouseCoords[3];
//void convertWindowCoordsToViewportCoords(int x, int y){
GLint viewport[4];
GLdouble modelview[16];
GLdouble projection[16];
GLfloat winX, winY, winZ, winZOld;
void convertWindowCoordsToViewportCoords(int x, int y, float z, GLdouble* posX, GLdouble* posY, GLdouble* posZ){
  //strange things happen with this when zoom/maxZoom is greater than 45...
  glGetDoublev(GL_MODELVIEW_MATRIX,modelview);
  glGetDoublev(GL_PROJECTION_MATRIX,projection);
  glGetIntegerv(GL_VIEWPORT,viewport);//returns four values: the x and y window coordinates of the viewport, followed by its width and height.
  winX = (float)x;
  winY = SCREEN_HEIGHT - (float)y;
  gluUnProject( winX, winY, mapDepth, modelview, projection, viewport, posX, posY, posZ);
}
/**************************** /mouse hover object selection ********************************/

/************************************* drawing subroutines ***************************************/


int isNextUnit;
PyObject * pyFire;
PyObject * pyIce;
void drawIce(){
  glBindTexture(GL_TEXTURE_2D, texturesArray[ICE_INDEX]);
  glCallList(unitList);
}
void drawFire(){
  glBindTexture(GL_TEXTURE_2D, texturesArray[FIRE_INDEX]);
  glCallList(unitList);
  double fireVitality;
  char fireVit[20];
  PyObject * pyFireVitality = PyObject_GetAttrString(pyFire,"vitality");
  fireVitality = PyFloat_AsDouble(pyFireVitality);
  glColor3f(1.0,1.0,1.0);
  glPushMatrix();
  glTranslatef(-0.8,0.0,0.0);
  glScalef(0.01,0.01,0.0);
  sprintf(fireVit,"%f",fireVitality);
  drawText(fireVit,0,-1,-9999.9,NULL);
  glPopMatrix();
  
}
PyObject * pyXPositionUnit;
PyObject * pyYPositionUnit;
//PyObject * pyIsSelected;
double xPositionUnit;
double yPositionUnit;
//long isSelected;
PyObject * pyUnit;
void drawUnit(){
  pyUnitType = PyObject_GetAttrString(pyUnit,"unitType");
  //  Py_DECREF(pyUnitType);
  pyXPositionUnit = PyObject_GetAttrString(pyUnit,"xPosDraw");
  pyYPositionUnit = PyObject_GetAttrString(pyUnit,"yPosDraw");
  xPositionUnit = PyFloat_AsDouble(pyXPositionUnit);
  yPositionUnit = PyFloat_AsDouble(pyYPositionUnit);
  //  glTranslatef(xPositionUnit,yPositionUnit,0.0);
  glTranslatef(xPositionUnit,yPositionUnit,0.1);
  //  updatePosition();

  pyUnitTextureIndex = PyObject_GetAttrString(pyUnitType,"textureIndex");
  pyName = PyObject_GetAttrString(pyUnitType,"name");
  unitName = PyString_AsString(pyName);
  pyHealth = PyObject_GetAttrString(pyUnit,"health");
  pyMaxHealth = PyObject_CallMethod(pyUnit,"getMaxHealth",NULL);
  pyLevel = PyObject_GetAttrString(pyUnit,"level");
  level = PyLong_AsLong(pyLevel);  
  pyPlayerNumber = PyObject_GetAttrString(pyUnit,"player");
  playerNumber = PyLong_AsLong(pyPlayerNumber);
  unitTextureIndex = PyLong_AsLong(pyUnitTextureIndex);
  pyRecentDamage = PyObject_GetAttrString(pyUnit,"recentDamage");
  pyRecentDamageIter = PyObject_GetIter(pyRecentDamage);

  healthBarLength = 0.7*PyFloat_AsDouble(pyHealth)/PyFloat_AsDouble(pyMaxHealth);
  glColor3f(1.0, 0.0, 0.0);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-.35, 0.9, -0.001);
  glTexCoord2f(1.0,0.0);
  glVertex3f(-.35+healthBarLength, 0.9, -0.001);
  glTexCoord2f(1.0,1.0);
  glVertex3f(-.35+healthBarLength, 0.8, -0.001);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-.35, 0.8, -0.001);
  glEnd();
  glBindTexture(GL_TEXTURE_2D, texturesArray[HEALTH_BAR_INDEX]);
  glCallList(healthBarList);

  //  glPushMatrix();
  //  glTranslatef(-0.1,-0.78,0.0);
  glPushMatrix();
  if(isNextUnit){
    glTranslatef(-0.60,0.90,0.0);
    glScalef(2.0,2.0,0.0);
  }else{
    glScalef(1.2,1.2,0.0);
    glTranslatef(-0.18,0.20,0.0);
  }

  glBindTexture(GL_TEXTURE_2D, texturesArray[FLAG_POLE_INDEX]);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0); glVertex3f(0.5, -0.75, 0.0);
  glTexCoord2f(1.0,0.0); glVertex3f(0.95, -0.75, 0.0);
  glTexCoord2f(1.0,1.0); glVertex3f(0.95, .25, 0.0);
  glTexCoord2f(0.0,1.0); glVertex3f(0.5, .25, 0.0);
  glEnd();

  if(playerNumber == 0){
    glColor3f(1.0,0.0,0.0);//red
  }else if(playerNumber == 1){
    glColor3f(0.0,0.0,1.0);//blue
  }else if(playerNumber == 2){
    glColor3f(1.0,1.0,0.0);//yellow
  }else if(playerNumber == 3){
    glColor3f(0.0,1.0,0.0);//green
  }else if(playerNumber == 4){
    glColor3f(1.0,0.5,0.0);//orange
  }else if(playerNumber == 5){
    glColor3f(0.5,0.0,1.0);//purple/pink
  }else if(playerNumber == 6){
    glColor3f(0.0,1.0,1.0);//teal
  }else if(playerNumber == 7){
    glColor3f(0.23,0.133,0.055);//brown
  }

  flagBits = level;
  while(flagBits != 0){
    glBindTexture(GL_TEXTURE_2D, texturesArray[FLAG_INDEX0+(flagBits&3)]);
    flagBits = flagBits >> 2;
    glTranslatef(0.0,0.16,0.0);
    glCallList(flagList);
  }
  glColor3f(1.0, 1.0, 1.0);
  glPopMatrix();

  glColor3f(1.0,1.0,1.0);
  glBindTexture(GL_TEXTURE_2D, texturesArray[unitTextureIndex]);
  //  glTranslatef(0.0,0.0,0.0);
  glCallList(unitList);
  
  while (pyDamageTime = PyIter_Next(pyRecentDamageIter)) {
    damageTime = PyLong_AsLong(pyDamageTime);
    if(currentTick-damageTime<200){
      glPushMatrix();
      glBindTexture(GL_TEXTURE_2D, texturesArray[SLASH_ANIMATION_INDEX]);
      glColor3f(1.0, 1.0, 1.0);
      float frameNumber = (((currentTick-damageTime)*SLASH_ANIMATION_FRAME_COUNT)/200)%SLASH_ANIMATION_FRAME_COUNT;
      glBegin(GL_QUADS);	
      glTexCoord2f(1.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber-1)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(0.5,-0.5,0.0);
      glTexCoord2f(0.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber-1)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(-0.5,-0.5,0.0);
      glTexCoord2f(0.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(-0.5,0.5,0.0);
      glTexCoord2f(1.0,(SLASH_ANIMATION_FRAME_COUNT-frameNumber)/SLASH_ANIMATION_FRAME_COUNT); glVertex3f(0.5,0.5,0.0);
      glEnd();
      glPopMatrix();
    }
    if(currentTick-damageTime<5000){
      glPushMatrix();
      pyDamage = PyObject_GetItem(pyRecentDamage,pyDamageTime);
      damageStr = PyString_AsString(pyDamage);
      int c = 0;
      while(damageStr[c] != 0){
	glTranslatef(-0.18,0.0,0.0);
	c++;
      }
      glColor4f(1.0, 0.0, 0.0, (5000.0-(currentTick-damageTime))/1000);
      glTranslatef(0.0,((currentTick-damageTime)*0.0002)-0.7,-0.0001);
      glScalef(0.01,0.01,0.0);
      drawText(damageStr,0,-1,-9999.9,NULL);
      glPopMatrix();
    }
  }

  Py_DECREF(pyUnitType);
  Py_DECREF(pyUnitTextureIndex);
  Py_DECREF(pyName);
  Py_DECREF(pyLevel);
  Py_DECREF(pyHealth);
  Py_DECREF(pyMaxHealth);
  Py_DECREF(pyPlayerNumber);
  Py_DECREF(pyXPositionUnit);
  Py_DECREF(pyYPositionUnit);
}
float shading;
char playerStartVal[2];
void drawTile(uint tilesXIndex, uint tilesYIndex, long name, long tileValue, long isOnMovePath,long playerStartValue){
  textureVertices = vertexArrays[tileValue];
  shading = 1.0;
  if(!isVisible){
    shading = shading - 0.3;
  }
  if(name == selectedName){// && !clickScroll){
    shading = shading - 0.3;
    //    if(cursorIndex >= 0){
    //      theCursorIndex = (int)cursorIndex;
    //    }
  }
  glColor3f(shading,shading,shading);
  glPushName(name);
  uint tileHash=0;
  tileHash += (((4294967296*(2654435761)*tilesXIndex)+81)%43261);
  tileHash += (((4294967296*(2654435761)*tilesYIndex)+30)%131071);
  tileHash = tileHash%4;
  glCallList(tilesLists+(4*tileValue)+tileHash);
  glPopName();

  //  glColor3f(0.0,1.0,0.0);
  //  if(roadValue == 1){
  //    glCallList(tilesLists+(4*ROAD_TILE_INDEX));
  //  }

  if(playerStartValue >= 1 && !PyObject_HasAttrString(gameMode,"units")){
    textureVertices = vertexArrays[PLAYER_START_TILE_INDEX];
    glCallList(tilesLists+(4*PLAYER_START_TILE_INDEX));
    sprintf(playerStartVal,"%ld",playerStartValue);

    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(-0.4,0.3,0.0);
    glScalef(0.01,0.01,0.0);
    drawText(playerStartVal,0,-1,-9999.9,NULL);
    glPopMatrix();
  }


}
void drawTilesText(){
  /*  int i,j,cityNameLength,unitNameLength = 0;
  for(i=0; i<cityNamesCount; i++){
    for(j=0; j<MAX_CITY_NAME_LENGTH; j++){
      if(cityNames[i][j] == 0){
	cityNameLength = j;
	break;
      }
    }
    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(cityNamesXs[i]-(0.18*cityNameLength),cityNamesYs[i]+0.5,0.0);
    glScalef(0.010,0.010,0.0);
    drawText(cityNames[i],0,-9999.9,NULL);
    glPopMatrix();
  }
  cityNamesCount = 0;*/
  /*  for(i=0; i<unitNamesCount; i++){
    for(j=0; j<MAX_UNIT_NAME_LENGTH; j++){
      if(unitNames[i][j] == 0){
	unitNameLength = j;
	break;
      }
    }
    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(unitNamesXs[i]-(0.3*j),unitNamesYs[i]+0.5,0.0);
    glScalef(0.009,0.009,0.0);
    drawText(unitNames[i],0,-9999.9,NULL);
    glPopMatrix();
  }
  unitNamesCount = 0;*/
}

PyObject * pyMovePath;
void drawMovePath(){
  pyMovePath = PyObject_GetAttrString(gameState,"movePath");
  nodeIterator = PyObject_CallMethod(pyMovePath,"__iter__",NULL);
  while(pyNode = PyIter_Next(nodeIterator)){
    pyXPosition = PyObject_GetAttrString(pyNode,"xPos");
    colNumber = 0-PyLong_AsLong(pyXPosition);
    pyYPosition = PyObject_GetAttrString(pyNode,"yPos");
    rowNumber = PyLong_AsLong(pyYPosition);
    xPosition = translateTilesXToPositionX(colNumber,rowNumber);
    yPosition = translateTilesYToPositionY(rowNumber);
    glPushMatrix();
    glTranslatef(xPosition,yPosition,0.0);
    glBindTexture(GL_TEXTURE_2D, texturesArray[WALK_ICON_INDEX]);
    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(0.5,-0.5,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(-0.5,-0.5,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(-0.5,0.5,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(0.5,0.5,0.0);
    glEnd();
    glPopMatrix();
  }
  Py_DECREF(pyMovePath);
}
void drawSelectionBox(){
  pyNode = PyObject_GetAttrString(gameMode,"selectedNode");
  if(pyNode != NULL && pyNode != Py_None){
    pyXPosition = PyObject_GetAttrString(pyNode,"xPos");
    colNumber = 0-PyLong_AsLong(pyXPosition);
    pyYPosition = PyObject_GetAttrString(pyNode,"yPos");
    rowNumber = PyLong_AsLong(pyYPosition);
    xPosition = translateTilesXToPositionX(colNumber,rowNumber);
    yPosition = translateTilesYToPositionY(rowNumber);
    pySelectionBoxScale = PyObject_GetAttrString(gameMode,"selectionBoxScale");
    selectionBoxScale = PyFloat_AsDouble(pySelectionBoxScale);
    Py_DECREF(pySelectionBoxScale);

    glColor3f(1.0,1.0,1.0);
    glBindTexture(GL_TEXTURE_2D, texturesArray[SELECTION_BOX_INDEX]);
    glPushMatrix();
    glTranslatef(xPosition,yPosition,0.0);
    glScalef(selectionBoxScale+1.0,selectionBoxScale+1.0,0.0);
    glCallList(selectionBoxList);
    glPopMatrix();
  }
}
void drawCities(){
  pyCities = PyObject_GetAttrString(gameMode,"cities");
  pyCitiesIter = PyObject_CallMethod(pyCities,"__iter__",NULL);
  if(pyCitiesIter != NULL && pyCitiesIter != Py_None){
    while(city = PyIter_Next(pyCitiesIter)){
      pyNode = PyObject_GetAttrString(city,"node");
      pyXPosition = PyObject_GetAttrString(pyNode,"xPos");
      colNumber = 0-PyLong_AsLong(pyXPosition);
      pyYPosition = PyObject_GetAttrString(pyNode,"yPos");
      rowNumber = PyLong_AsLong(pyYPosition);
      xPosition = translateTilesXToPositionX(colNumber,rowNumber);
      yPosition = translateTilesYToPositionY(rowNumber);

      glPushMatrix();
      glTranslatef(xPosition,yPosition,0.1);

      glBindTexture(GL_TEXTURE_2D, texturesArray[CITY_INDEX]);
      glCallList(unitList);
      glPopMatrix();
      Py_DECREF(city);
      Py_DECREF(pyNode);
    }
  }
}
void drawUnits(){
  glDepthFunc(GL_LEQUAL);
  pyUnits = PyObject_GetAttrString(gameMode,"units");
  pyUnitsIter = PyObject_CallMethod(pyUnits,"__iter__",NULL);
  if(pyUnitsIter != NULL && pyUnitsIter != Py_None){
    while(pyUnit = PyIter_Next(pyUnitsIter)){
      pyNode = PyObject_GetAttrString(pyUnit,"node");
      pyXPosition = PyObject_GetAttrString(pyNode,"xPos");
      colNumber = 0-PyLong_AsLong(pyXPosition);
      pyYPosition = PyObject_GetAttrString(pyNode,"yPos");
      rowNumber = PyLong_AsLong(pyYPosition);
      xPosition = translateTilesXToPositionX(colNumber,rowNumber);
      yPosition = translateTilesYToPositionY(rowNumber);
      isNextUnit = 0;
      nextUnit = PyObject_GetAttrString(gameMode,"nextUnit");
      if(pyUnit == nextUnit){
	isNextUnit = 1;
      }
      if(nextUnit != NULL){
      	Py_DECREF(nextUnit);
      }
      pyFire = PyObject_GetAttrString(pyNode,"fire");
      pyIce = PyObject_GetAttrString(pyNode,"ice");
      pyIsVisible = PyObject_GetAttrString(pyNode,"visible");//New reference
      isVisible = PyLong_AsLong(pyIsVisible);
      Py_DECREF(pyIsVisible);

      glPushMatrix();
      if(isVisible){
	glPushMatrix();
	drawUnit();
	glPopMatrix();
      }//else{
	//	updatePosition();
      //      }
      glPopMatrix();
      if(pyFire != NULL && pyFire != Py_None && isVisible){
	drawFire();
      }  
      Py_DECREF(pyNode);
      Py_DECREF(pyUnit);      
    }
    Py_DECREF(pyUnitsIter);
  }
  if(pyUnits != NULL && pyUnits != Py_None){
    Py_DECREF(pyUnits);
  }
}						
void drawTiles(){
  rowNumber = -1;
  /*  if(PyObject_HasAttrString(gameMode,"focusXPos")){
    pyFocusXPos = PyObject_GetAttrString(gameMode,"focusXPos");
    pyFocusYPos = PyObject_GetAttrString(gameMode,"focusYPos");
    focusTilesXPos = PyLong_AsLong(pyFocusXPos);
    focusTilesYPos = PyLong_AsLong(pyFocusYPos);
    focusXPos = translateTilesXToPositionX(0.0-focusTilesXPos,focusTilesYPos);
    focusYPos = translateTilesYToPositionY(focusTilesYPos);
    Py_DECREF(pyFocusXPos);
    Py_DECREF(pyFocusYPos);
    }*/
  pyLoaded = PyObject_CallMethod(theMap,"getLoaded",NULL);
  mapLoaded = PyLong_AsLong(pyLoaded);
  if(mapLoaded){
    loadMap();
  }
  int index;
  for(index = 0;index < theMapp.size;index++){
    theNode = &(theMapp.nodes[index]);
      glPushMatrix();
      glTranslatef(theNode->xPos,theNode->yPos,0.0);
      //      glTranslatef(0.0,0.0,0.03);
      drawTile(theNode->yIndex,theNode->xIndex,theNode->name,theNode->tileValue,theNode->onMovePath,theNode->playerStartValue);
      glPopMatrix();
    //printf("xIndex: %d\n",theNode.xIndex);
  }
  Py_DECREF(pyLoaded);

}

void doViewport(){
  if(PyObject_HasAttrString(gameMode,"gameRoomMode")){
    glViewport(60.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,258.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT,991.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,824.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT);
  }else if(PyObject_HasAttrString(gameMode,"createGameMode")){
    glViewport(544.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,258.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT,991.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,824.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT);
  }else{
    glViewport(0,0,SCREEN_WIDTH,SCREEN_HEIGHT);
  }
}
PyObject * pyTranslateZ;
float mapRightOffset;
float mapTopOffset;
int frameNumber = 0;
void calculateTranslation(){

  pyMapWidth = PyObject_CallMethod(theMap,"getWidth",NULL);//New reference
  pyMapHeight = PyObject_CallMethod(theMap,"getHeight",NULL);//New reference
  mapWidth = PyLong_AsLong(pyMapWidth);
  mapHeight = PyLong_AsLong(pyMapHeight);
  frameNumber++;
  glPushMatrix();
  if(theMap != Py_None && theMap != NULL){
    Py_DECREF(pyMapWidth);
    Py_DECREF(pyMapHeight);
    pyTranslateZ = PyObject_GetAttrString(theMap,"translateZ");
    translateZ = PyFloat_AsDouble(pyTranslateZ);
    Py_DECREF(pyTranslateZ);
    if(translateX - mapRightOffset < convertedTopRightX
       && translateX - (2.0*SIN60) > convertedBottomLeftX
       && translateY < convertedTopRightY - mapTopOffset
       && translateY > convertedBottomLeftY+2.0
       && (translateZ < translateZPrev)){
      translateZ = translateZPrev;
      pyObj = PyObject_CallMethod(gameMode,"setMaxTranslateZ","f",translateZ);//New reference
      Py_DECREF(pyObj);
    }
  }
  glTranslatef(translateX,translateY,translateZ);
  //glTranslatef(0.0,0.0,translateZ);
  glBindTexture(GL_TEXTURE_2D, texturesArray[OK_BUTTON_INDEX]);//draw a big texture for sampling map depth
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0); glVertex3f(-1000.0,-1000.0,0.0);
  glTexCoord2f(1.0,0.0); glVertex3f(1000.0,-1000.0,0.0);
  glTexCoord2f(1.0,1.0); glVertex3f(1000.0,1000.0,0.0);
  glTexCoord2f(0.0,1.0); glVertex3f(-1000.0,1000.0,0.0);
  glEnd();
  glPopMatrix();
  if(translateZ != translateZPrev2){
  if(PyObject_HasAttrString(gameMode,"gameRoomMode")){
    glReadPixels( 7*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1 );
    glReadPixels( 8*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2 );
    glReadPixels( 9*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3 );
  }else if(PyObject_HasAttrString(gameMode,"createGameMode")){
    glReadPixels( 13*SCREEN_WIDTH/16, 7*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1 );
    glReadPixels( 13*SCREEN_WIDTH/16, 8*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2 );
    glReadPixels( 13*SCREEN_WIDTH/16, 9*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3 );
  }else{
    glReadPixels( 7*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1 );
    glReadPixels( 8*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2 );
    glReadPixels( 9*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3 );    
  }
  translateZPrev2 = translateZ;
  }
//  printf("****** c1:    \t%d\n",SDL_GetTicks() - testTicks5); testTicks5 = SDL_GetTicks(); 
  if(mapDepthTest1 == mapDepthTest2 || mapDepthTest1 == mapDepthTest3){
    mapDepth = mapDepthTest1;
  }else if(mapDepthTest2 == mapDepthTest3){
    mapDepth = mapDepthTest2;
  }else{
    printf("mapdepth not found%d\n",1);
  }
//  printf("****** c:    \t%d\n",SDL_GetTicks() - testTicks5); testTicks5 = SDL_GetTicks(); 

  if(PyObject_HasAttrString(gameMode,"gameRoomMode")){
    convertWindowCoordsToViewportCoords(60.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(1551.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }else if(PyObject_HasAttrString(gameMode,"createGameMode")){
    convertWindowCoordsToViewportCoords(100.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(1535.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }else{
    convertWindowCoordsToViewportCoords(390.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(SCREEN_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }
  mouseMapPosXPrevious = mouseMapPosX;
  mouseMapPosYPrevious = mouseMapPosY;
  convertWindowCoordsToViewportCoords(mouseX,mouseY,translateZ,&mouseMapPosX,&mouseMapPosY,&mouseMapPosZ);  
//  printf("****** d:    \t%d\n",SDL_GetTicks() - testTicks5); testTicks5 = SDL_GetTicks(); 
  if(translateZ > translateZPrev){
    translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
    translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
  }
  translateZPrev = translateZ;
  //  convertWindowCoordsToViewportCoords(mouseX,mouseY,translateZ,&mouseMapPosXNew,&mouseMapPosYNew,&mouseMapPosZNew);
  mapRightOffset = translateTilesXToPositionX(mapWidth+1,0);
  mapTopOffset = translateTilesYToPositionY(mapHeight);
  //printf("screen topright %f,%f\n",convertedTopRightX,convertedTopRightY);
  //printf("screen bottomleft %f,%f\n",convertedBottomLeftX,convertedBottomLeftY);
  //printf("translate %f,%f,%f\n",translateX,translateY,translateZ);
  //printf("offsets: %f %f\n",mapRightOffset,mapTopOffset);
  //printf("%f\n",translateTilesYToPositionY(mapHeight));//setting translateY to this number will focus on it
  //printf("mouse %d:%f\t%d:%f\n",mouseX,mouseMapPosX,mouseY,mouseMapPosY);
  
  if(clickScroll > 0 && !isFocusing){
    translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
    translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
  }else if(!isFocusing){
    if(moveRight > 0){// && translateX > -10.0){
      translateX -= scrollSpeed*deltaTicks;
    }
    if(moveRight < 0){// && translateX < 10.0){
      translateX += scrollSpeed*deltaTicks;
    }
    if(moveUp > 0){// && translateY > -10.0){
      translateY -= scrollSpeed*deltaTicks;
    }
    if(moveUp < 0){// && translateY < 10.0){
      translateY += scrollSpeed*deltaTicks;
    }
  }
//  printf("****** e:    \t%d\n",SDL_GetTicks() - testTicks5); testTicks5 = SDL_GetTicks(); 
/*  if(!isAnimating && !doneAnimatingFired){
    doneAnimatingFired = 1;
    if(PyObject_HasAttrString(gameMode,"onDoneAnimating")){
      pyObj = PyObject_CallMethod(gameMode,"onDoneAnimating",NULL);//New reference
      printPyStackTrace();
      Py_DECREF(pyObj);
    }
    }*/
  if(isFocusing){
    //printf("%f %f %f %f\n",translateXPrev,translateX,translateYPrev,translateY);
    if((considerDoneFocusing > 2) && abs(50.0*(translateXPrev - translateX)) == 0.0 && abs(50.0*(translateYPrev - translateY)) == 0.0){//this indicates the auto-scrolling code is not allowing us to move any more
      isFocusing = 0;
      considerDoneFocusing = 0;
    }else if(abs(50.0*(translateXPrev - translateX)) == 0.0 && abs(50.0*(translateYPrev - translateY)) == 0.0){//this indicates the auto-scrolling code is not allowing us to move any more
      considerDoneFocusing = considerDoneFocusing + 1;
      focusSpeed = 0.0;
    }
    translateXPrev = translateX;
    translateYPrev = translateY;
    if(focusSpeed < focusSpeedMax){
      focusSpeed = focusSpeed + 0.00080*deltaTicks;
    }
    //focusSpeed = .0500;
    //this block points the focus toward the focus point
    if(fabs(translateX-(-focusXPos)) > fabs(translateY-(-focusYPos)) && fabs(translateX-(-focusXPos)) != 0.0){
      focusSpeedX = focusSpeed;
      focusSpeedY = focusSpeed*fabs((translateY+focusYPos)/(translateX+focusXPos));
    }else if(fabs(translateY-(-focusYPos)) > fabs(translateX-(-focusXPos)) && fabs(translateY-(-focusYPos)) != 0.0){
      focusSpeedX = focusSpeed*fabs((translateX+focusXPos)/(translateY+focusYPos));
      focusSpeedY = focusSpeed;
    }else{
      focusSpeedX = focusSpeed;
      focusSpeedY = focusSpeed;
    }
    //printf("%f\t%f\t%f\t%f\n",focusSpeedX,focusSpeedY,fabs(translateX-(-focusXPos)),fabs(translateY-(-focusYPos)));
    //these lines roughly make focusspeed consistent rather than faster on diagonals
    if(focusSpeedX > 0.5*focusSpeed || focusSpeedY > 0.5*focusSpeed){
      focusSpeedX = focusSpeedX*focusSpeed/(focusSpeedX + focusSpeedY);
      focusSpeedY = focusSpeedY*focusSpeed/(focusSpeedX + focusSpeedY);
    }
    //    printf("?? %f\t%f\t%f\t%f\n",focusSpeedX,focusSpeedY,fabs(translateX-(-focusXPos)),fabs(translateY-(-focusYPos)));
    
      if(translateX < -focusXPos){
	translateX = translateX + focusSpeedX*deltaTicks;
	if(translateX > -focusXPos){translateX = -focusXPos;}
      }else{
	translateX = translateX - focusSpeedX*deltaTicks;
	if(translateX < -focusXPos){translateX = -focusXPos;}
      }
      if(translateY < -focusYPos){
	translateY = translateY + focusSpeedY*deltaTicks;
	if(translateY > -focusYPos){translateY = -focusYPos;}
      }else{
	translateY = translateY - focusSpeedY*deltaTicks;
	if(translateY < -focusYPos){translateY = -focusYPos;}
      }
    }
//  printf("****** f:    \t%d\n",SDL_GetTicks() - testTicks5); testTicks5 = SDL_GetTicks(); 

  //The following code will adjust translateX/Y so that no off-map area is shown
   //printf("%f\t%f\t%f\n",translateX,mapRightOffset,convertedBottomLeftX);
   if(translateX - mapRightOffset < convertedTopRightX){
    translateX = convertedTopRightX + mapRightOffset;
    if(translateX - (2.0*SIN60) > convertedBottomLeftX){
      //prevents shaking issue that occurs when the map is slightly larger than viewable area
      translateX = (convertedTopRightX + mapRightOffset + convertedBottomLeftX + (2.0*SIN60))/2.0;
    }
  }else if(translateX - (2.0*SIN60) > convertedBottomLeftX){
    translateX = convertedBottomLeftX + (2.0*SIN60);
    if(translateX - mapRightOffset < convertedTopRightX){
      //prevents shaking issue that occurs when the map is slightly larger than viewable area
      translateX = (convertedTopRightX + mapRightOffset + convertedBottomLeftX + (2.0*SIN60))/2.0;
    }
   }
   if(translateY < convertedTopRightY - mapTopOffset){
     translateY = convertedTopRightY - mapTopOffset;
     if(translateY > convertedBottomLeftY+2.0){
       //prevents shaking issue that occurs when the map is slightly larger than viewable area
       translateY = (convertedTopRightY-mapTopOffset+convertedBottomLeftY+2.0)/2.0;
     }
   }else if(translateY > convertedBottomLeftY+2.0){
     translateY = convertedBottomLeftY+2.0;
     if(translateY < convertedTopRightY - mapTopOffset){
       //prevents shaking issue that occurs when the map is slightly larger than viewable area
       translateY = (convertedTopRightY-mapTopOffset+convertedBottomLeftY+2.0)/2.0;
     }
   }
//  printf("****** g:    \t%d\n",SDL_GetTicks() - testTicks5); testTicks5 = SDL_GetTicks(); 
}

void drawBoard(){
  glDepthFunc(GL_LEQUAL);
  glClear(GL_DEPTH_BUFFER_BIT);		 
  if(theMap != Py_None && theMap != NULL){
//    printf("** other:          \t%d\n",SDL_GetTicks() - testTicks3); testTicks3 = SDL_GetTicks(); 
    drawTiles();
    drawMovePath();
//    printf("** drawTiles:      \t%d\n",SDL_GetTicks() - testTicks3); testTicks3 = SDL_GetTicks(); 
    drawSelectionBox();
//    printf("** drawSelectionBox:\t%d\n",SDL_GetTicks() - testTicks3); testTicks3 = SDL_GetTicks(); 
    drawUnits();
//    printf("** drawUnits:      \t%d\n",SDL_GetTicks() - testTicks3); testTicks3 = SDL_GetTicks(); 
    drawCities();
//    printf("** drawCities:      \t%d\n",SDL_GetTicks() - testTicks3); testTicks3 = SDL_GetTicks(); 
  }
}

void drawTileSelect(double xPos, double yPos, int name, long tileType, long selected){
  //THIS REALLY SHOULD HAVE BEEN DONE WITH uiElements...
  glLoadIdentity();
  glColor3f(1.0,1.0,1.0);
  glTranslatef(xPos,yPos,0.0);
  glScalef(0.01,0.01,0.0);
  glBindTexture(GL_TEXTURE_2D, tilesTexture);
  textureVertices = vertexArrays[tileType];
  glPushName(name);
  glBegin(GL_POLYGON);
  glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(3.0*hexagonVertices[0][0], 3.0*hexagonVertices[0][1], 0.0);
  glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(3.0*hexagonVertices[1][0], 3.0*hexagonVertices[1][1], 0.0);
  glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(3.0*hexagonVertices[2][0], 3.0*hexagonVertices[2][1], 0.0);
  glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(3.0*hexagonVertices[3][0], 3.0*hexagonVertices[3][1], 0.0);
  glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(3.0*hexagonVertices[4][0], 3.0*hexagonVertices[4][1], 0.0);
  glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(3.0*hexagonVertices[5][0], 3.0*hexagonVertices[5][1], 0.0);
  glEnd();
  glPopName();
  if(selected){
    glLoadIdentity();
    glTranslatef(xPos-0.04,yPos-0.04,0.0);
    glBindTexture(GL_TEXTURE_2D, texturesArray[TILE_SELECT_BOX_INDEX]);
    glBegin(GL_POLYGON);
    glTexCoord2f(1.0,1.0); glVertex3f(0.08,0.08,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(0.08,0.0,0.0);
    glTexCoord2f(0.0,0.0); glVertex3f(0.0,0.0,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(0.0,0.08,0.0);
    glEnd();
  }
}
int isNode;
unsigned int red[1],green[1],blue[1];
PyObject * pyWidth;
PyObject * pyHeight;
PyObject * pyHidden;
PyObject * pyName;
PyObject * pyTextureIndex;
PyObject * pyCursorIndex;
PyObject * pyText;
PyObject * pyQueuedText;
PyObject * pyRealText;
PyObject * pyLeftmostCharPosition;
PyObject * pyRightmostCharPosition;
PyObject * pyRecalculateText;
PyObject * pyDecrementMe;
PyObject * pyTextColor;
PyObject * pyTextSize;
PyObject * pyColor;
PyObject * pyMouseOverColor;
PyObject * pyTextXPosition;
PyObject * pyTextYPosition;
PyObject * pyCursorPosition;
PyObject * pyFontIndex;
PyObject * pyFrameLength;
PyObject * pyFrameCount;
PyObject * pyIsFocused;
//double xPosition;
//double yPosition;
double width;
double height;
int hidden;
long name;
long textureIndex;
//long cursorIndex;
char * text;
int wordWidth;
char * queuedText;
char * realText;
int leftmostCharPosition;
int rightmostCharPosition;
int recalculateText;
char * textColor;
double textSize;
char * color;
char * mouseOverColor;
double textXPosition;
double textYPosition;
double cursorPosition;
double fontIndex;
int frameLength;
int frameCount;
int isFocused;

void drawUIElement(PyObject * uiElement){
  isNode = PyObject_HasAttrString(uiElement,"tileValue");
  if(!isNode){
    pyXPosition = PyObject_GetAttrString(uiElement,"xPosition");
    pyYPosition = PyObject_GetAttrString(uiElement,"yPosition");
    pyWidth = PyObject_GetAttrString(uiElement,"width");
    pyHeight = PyObject_GetAttrString(uiElement,"height");
    pyHidden = PyObject_GetAttrString(uiElement,"hidden");
    pyName = PyObject_GetAttrString(uiElement,"name");
    pyTextureIndex = PyObject_GetAttrString(uiElement,"textureIndex");
    //    pyCursorIndex = PyObject_GetAttrString(uiElement,"cursorIndex");
    pyText = PyObject_GetAttrString(uiElement,"text");
    pyTextColor = PyObject_GetAttrString(uiElement,"textColor");
    pyTextSize = PyObject_GetAttrString(uiElement,"textSize");
    pyColor = PyObject_GetAttrString(uiElement,"color");
    pyMouseOverColor = PyObject_GetAttrString(uiElement,"mouseOverColor");
    pyTextXPosition = PyObject_GetAttrString(uiElement,"textXPos");
    pyTextYPosition = PyObject_GetAttrString(uiElement,"textYPos");
    pyCursorPosition = PyObject_GetAttrString(uiElement,"cursorPosition");
    pyFontIndex = PyObject_GetAttrString(uiElement,"fontIndex");
    pyFrameLength = PyObject_GetAttrString(uiElement,"frameLength");
    pyFrameCount = PyObject_GetAttrString(uiElement,"frameCount");
    pyIsFocused = PyObject_GetAttrString(uiElement,"focused");

    xPosition = PyFloat_AsDouble(pyXPosition);
    yPosition = PyFloat_AsDouble(pyYPosition);
    width = PyFloat_AsDouble(pyWidth);
    height = PyFloat_AsDouble(pyHeight);
    hidden = pyHidden==Py_True;
    name = PyLong_AsLong(pyName);
    textureIndex = PyLong_AsLong(pyTextureIndex);
    //    cursorIndex = PyLong_AsLong(pyCursorIndex);
    text = PyString_AsString(pyText);
    textColor = PyString_AsString(pyTextColor);
    textSize = PyFloat_AsDouble(pyTextSize);
    color = PyString_AsString(pyColor);
    if(pyMouseOverColor != Py_None){
      mouseOverColor = PyString_AsString(pyMouseOverColor);
    }else{
      mouseOverColor = NULL;
    }
    textXPosition = PyFloat_AsDouble(pyTextXPosition);
    textYPosition = PyFloat_AsDouble(pyTextYPosition);
    cursorPosition = PyFloat_AsDouble(pyCursorPosition);
    fontIndex = PyFloat_AsDouble(pyFontIndex);
    frameLength = PyLong_AsLong(pyFrameLength);
    frameCount = PyLong_AsLong(pyFrameCount);
    isFocused = pyIsFocused==Py_True;
     
    Py_DECREF(pyXPosition);
    Py_DECREF(pyYPosition);
    Py_DECREF(pyWidth);
    Py_DECREF(pyHeight);
    Py_DECREF(pyHidden);
    Py_DECREF(pyName);
    Py_DECREF(pyTextureIndex);
    //    Py_DECREF(pyCursorIndex);
    Py_DECREF(pyText);
    Py_DECREF(pyTextColor);
    Py_DECREF(pyTextSize);
    Py_DECREF(pyColor);
    if(pyMouseOverColor != Py_None){
      Py_DECREF(pyMouseOverColor);
    }
    Py_DECREF(pyTextXPosition);
    Py_DECREF(pyTextYPosition);
    Py_DECREF(pyCursorPosition);
    Py_DECREF(pyFontIndex);
    Py_DECREF(pyFrameLength);
    Py_DECREF(pyFrameCount);
    Py_DECREF(pyIsFocused);

    if(!hidden){
      if(PyObject_HasAttrString(uiElement,"tileType")){//gameModeTileSelectButton
	drawTileSelect(xPosition,yPosition,name,PyLong_AsLong(PyObject_GetAttrString(uiElement,"tileType")),PyLong_AsLong(PyObject_GetAttrString(uiElement,"selected")));
      }else{
	if(textureIndex > -1){
	  glPushMatrix();
	  glLoadIdentity();
	  glBindTexture(GL_TEXTURE_2D, texturesArray[textureIndex]);
	  sscanf(color,"%X %X %X",red,green,blue);
	  //	glColor3f(red1.0f, 1.0f, 1.0f);
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  glPushName(name);
	  glBegin(GL_QUADS);
	  if(frameCount > 1){
	    float frameNumber = frameCount-1-(currentTick/frameLength)%frameCount;
	    glTexCoord2f(0.0,(frameNumber/frameCount)+1.0/frameCount); glVertex3f(xPosition,yPosition,0.0);
	    glTexCoord2f(1.0,(frameNumber/frameCount)+1.0/frameCount); glVertex3f(xPosition+width,yPosition,0.0);
	    glTexCoord2f(1.0,(frameNumber/frameCount)); glVertex3f(xPosition+width,yPosition-height,0.0);
	    glTexCoord2f(0.0,(frameNumber/frameCount)); glVertex3f(xPosition,yPosition-height,0.0);
	  }else{
	    glTexCoord2f(0.0,1.0); glVertex3f(xPosition,yPosition,0.0);
	    glTexCoord2f(1.0,1.0); glVertex3f(xPosition+width,yPosition,0.0);
	    glTexCoord2f(1.0,0.0); glVertex3f(xPosition+width,yPosition-height,0.0);
	    glTexCoord2f(0.0,0.0); glVertex3f(xPosition,yPosition-height,0.0);
	  }
	  glEnd();
	  glPopName();
	  glPopMatrix();
	}
  
	if(PyObject_HasAttrString(uiElement,"realText")){
	  pyRecalculateText = PyObject_GetAttrString(uiElement,"recalculateText");
	  recalculateText = PyLong_AsLong(pyRecalculateText);
	  if(recalculateText){
	    pyRealText = PyObject_GetAttrString(uiElement,"realText");
	    pyLeftmostCharPosition = PyObject_GetAttrString(uiElement,"leftmostCharPosition");
	    pyRightmostCharPosition = PyObject_GetAttrString(uiElement,"rightmostCharPosition");
	    leftmostCharPosition = PyLong_AsLong(pyLeftmostCharPosition);
	    rightmostCharPosition = PyLong_AsLong(pyRightmostCharPosition);
	    realText = PyString_AsString(pyRealText);
	    glPushMatrix();
	    glLoadIdentity();
	    glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	    glScalef(textSize,textSize,0.0);
	    findTextWidth(uiElement,fontIndex,realText,xPosition+width,leftmostCharPosition,rightmostCharPosition,cursorPosition,recalculateText);
	    glPopMatrix();
	    Py_DECREF(pyLeftmostCharPosition);
	    Py_DECREF(pyRightmostCharPosition);
	    Py_DECREF(pyRealText);
	  }
	  Py_DECREF(pyRecalculateText);	  
	}
	if(PyObject_HasAttrString(uiElement,"textQueue")){
	  pyQueuedText = PyObject_CallMethod(uiElement,"getText",NULL);
	  queuedText = PyString_AsString(pyQueuedText);
	  if(queuedText[0] != 0){
	    glPushMatrix();
	    glLoadIdentity();
	    glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	    glScalef(textSize,textSize,0.0);
	    wordWidth = findWordWidth(fontIndex,queuedText,xPosition+width);
	    glPopMatrix();
	    pyObj = PyObject_CallMethod(uiElement,"addLine","i",wordWidth);
	    Py_DECREF(pyObj);
	  }
	  Py_DECREF(pyQueuedText);
	}
	if(PyObject_HasAttrString(uiElement,"text") && text[0] != 0){
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  if(selectedName == name && mouseOverColor != NULL){
	    sscanf(mouseOverColor,"%X %X %X",red,green,blue);
	  }else{
	    sscanf(textColor,"%X %X %X",red,green,blue);
	  }
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  glPushMatrix();
	  glLoadIdentity();
	  glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	  glScalef(textSize,textSize,0.0);
	  //glTranslatef(0.0,0.0,-10.0);
	  glPushName(name);
	  if(isFocused){
	    drawText(text,fontIndex,cursorPosition,xPosition+width,NULL);
	  }else{
	    drawText(text,fontIndex,-1,xPosition+width,NULL);
	  }
	  glPopName();
	  glPopMatrix();
	}
      }
      Py_DECREF(uiElement);
      //      if(name == selectedName && cursorIndex >= 0){
      //	theCursorIndex = cursorIndex;
      //      }
    }
  }
}
float xPos;
float yPos;
float pointerWidth;
float pointerHeight;
char frameRate[20];
void drawUI(){
  glDepthFunc(GL_ALWAYS);
  pyObj = PyObject_CallMethod(gameMode,"getUIElementsIterator",NULL);
  if(pyObj != NULL){
    UIElementsIterator = PyObject_GetIter(pyObj);//New reference
    while (uiElement = PyIter_Next(UIElementsIterator)) {
      drawUIElement(uiElement);
    }
    Py_DECREF(UIElementsIterator);
    Py_DECREF(pyObj);
  }
  glGetIntegerv(GL_RENDER_MODE,&bufRenderMode);
  if(bufRenderMode==GL_RENDER){//need to hide the cursor during GL_SELECT
    /*draw cursor*/
    glPushMatrix();
    glLoadIdentity();
    if(theCursorIndex >= 0){
      glBindTexture(GL_TEXTURE_2D, texturesArray[theCursorIndex]);
    }else{
      glBindTexture(GL_TEXTURE_2D, texturesArray[CURSOR_POINTER_INDEX]);
    }
    glColor3f(1.0,1.0,1.0);
    glBegin(GL_QUADS);
    xPos = (mouseX/(SCREEN_WIDTH/2.0))-1.0;
    yPos = 1.0-(mouseY/(SCREEN_HEIGHT/2.0));
    pointerWidth = 2.0*CURSOR_WIDTH/SCREEN_WIDTH;
    pointerHeight = 2.0*CURSOR_HEIGHT/SCREEN_HEIGHT;
    
    glTexCoord2f(0.0,1.0); glVertex3f(xPos,yPos,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(xPos+pointerWidth,yPos,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(xPos+pointerWidth,yPos-pointerHeight,0.0);
    glTexCoord2f(0.0,0.0); glVertex3f(xPos,yPos-pointerHeight,0.0);
    glEnd();
    glPopMatrix();
  }

  /*frame rate display*/
  if(deltaTicks != 0){
    
    avgDeltaTicks = ((avgDeltaTicks*totalDeltaTicksDataPoints) + deltaTicks)/(totalDeltaTicksDataPoints+1);
    totalDeltaTicksDataPoints = totalDeltaTicksDataPoints + 1;
    sprintf(frameRate,"%ld",(long)(1000.0/avgDeltaTicks));
    glPushMatrix();
    glColor3f(1.0,1.0,1.0);
    glLoadIdentity();
    glTranslatef(-1.0,-1.0,0.0);
    glScalef(0.0005,0.0005,0.0);
    drawText(frameRate,0,-1,-9999.9,NULL);
    glPopMatrix();
    if(totalDeltaTicksDataPoints > 100){
      avgDeltaTicks = 0;
      totalDeltaTicksDataPoints = 0;
    }

  }
}
/************************************* /drawing subroutines ***************************************/

/************************************** opengl init **************************************/
static void initGL (){
  /** needs to be called on screen resize **/
  //unneeded with sdl?

  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);//default values anyway, put it here anyway
  glInitNames(); //init names stack	
  glClearColor(0.0, 0.0, 0.0, 0.0); //sets screen clear color

  //glClearColor(1.0, 1.0, 1.0, 1.0); //sets screen clear color
  //glClearColor(123.0/255.0,126.0/255.0,125.0/255.0,1.0);//grey that matches the UI...
  glEnable(GL_ALPHA_TEST);
  //  glAlphaFunc(GL_GREATER,0.1);
  glClearDepth(1);//default
  glEnable(GL_DEPTH_TEST);
  glDepthRange(0,1);//default
  glDepthFunc(GL_LEQUAL);    
  //  glAlphaFunc(GL_GREATER,0.1);//clear area around the fonts will not write to the z-buffer
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  //glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_DST_ALPHA);

  //  glBlendFunc(GL_SRC_ALPHA, GL_ZERO);
  screenRatio = (GLfloat)SCREEN_WIDTH/(GLfloat)SCREEN_HEIGHT;

  pngLoad(&tilesTexture, TILES);	/******************** /image init ***********************/
  pngLoad(&texturesArray[TILE_SELECT_BOX_INDEX],TILE_SELECT_BOX);
  pngLoad(&texturesArray[UI_MAP_EDITOR_TOP_INDEX],UI_MAP_EDITOR_TOP);
  pngLoad(&texturesArray[UI_MAP_EDITOR_BOTTOM_INDEX],UI_MAP_EDITOR_BOTTOM);
  pngLoad(&texturesArray[UI_MAP_EDITOR_LEFT_INDEX],UI_MAP_EDITOR_LEFT);
  pngLoad(&texturesArray[UI_MAP_EDITOR_RIGHT_INDEX],UI_MAP_EDITOR_RIGHT);
  pngLoad(&texturesArray[UI_NEW_GAME_SCREEN_INDEX],UI_NEW_GAME_SCREEN);
  pngLoad(&texturesArray[CURSOR_POINTER_INDEX],CURSOR_POINTER);
  pngLoad(&texturesArray[CURSOR_POINTER_ON_INDEX],CURSOR_POINTER_ON);
  pngLoad(&texturesArray[CURSOR_MOVE_INDEX],CURSOR_MOVE);
  pngLoad(&texturesArray[PLAYER_START_BUTTON_INDEX],PLAYER_START_BUTTON);
  pngLoad(&texturesArray[UI_SCROLLABLE_INDEX],UI_SCROLLABLE);
  pngLoad(&texturesArray[UI_SCROLL_PAD_INDEX],UI_SCROLL_PAD);
  pngLoad(&texturesArray[UI_TEXT_INPUT_INDEX],UI_TEXT_INPUT);
  pngLoad(&texturesArray[MEEPLE_INDEX],MEEPLE);
  pngLoad(&texturesArray[HEALTH_BAR_INDEX],HEALTH_BAR);
  pngLoad(&texturesArray[UNIT_BUILD_BAR_INDEX],UNIT_BUILD_BAR);
  pngLoad(&texturesArray[CITY_SANS_TREE_INDEX],CITY_SANS_TREE);
  pngLoad(&texturesArray[WALK_ICON_INDEX],WALK_ICON);
  pngLoad(&texturesArray[ADD_BUTTON_INDEX],ADD_BUTTON);
  pngLoad(&texturesArray[REMOVE_BUTTON_INDEX],REMOVE_BUTTON);
  pngLoad(&texturesArray[CITY_VIEWER_BOX_INDEX],CITY_VIEWER_BOX);
  pngLoad(&texturesArray[UNIT_TYPE_VIEWER_BOX_INDEX],UNIT_TYPE_VIEWER_BOX);
  pngLoad(&texturesArray[UNIT_VIEWER_BOX_INDEX],UNIT_VIEWER_BOX);
  pngLoad(&texturesArray[RESEARCH_BOX_INDEX],RESEARCH_BOX);
  pngLoad(&texturesArray[SELECTION_BRACKET_INDEX],SELECTION_BRACKET);
  pngLoad(&texturesArray[ADD_BUTTON_SMALL_INDEX],ADD_BUTTON_SMALL);
  pngLoad(&texturesArray[REMOVE_BUTTON_SMALL_INDEX],REMOVE_BUTTON_SMALL);
  pngLoad(&texturesArray[UNIT_CIRCLE_RED_INDEX],UNIT_CIRCLE_RED);
  pngLoad(&texturesArray[UNIT_CIRCLE_BLUE_INDEX],UNIT_CIRCLE_BLUE);
  pngLoad(&texturesArray[UNIT_CIRCLE_GREEN_INDEX],UNIT_CIRCLE_GREEN);
  pngLoad(&texturesArray[UNIT_CIRCLE_YELLOW_INDEX],UNIT_CIRCLE_YELLOW);
  pngLoad(&texturesArray[UNIT_CIRCLE_PINK_INDEX],UNIT_CIRCLE_PINK);
  pngLoad(&texturesArray[UNIT_CIRCLE_ORANGE_INDEX],UNIT_CIRCLE_ORANGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_PURPLE_INDEX],UNIT_CIRCLE_PURPLE);
  pngLoad(&texturesArray[UNIT_CIRCLE_BROWN_INDEX],UNIT_CIRCLE_BROWN);
  pngLoad(&texturesArray[CURSOR_ATTACK_INDEX],CURSOR_ATTACK);
  pngLoad(&texturesArray[CURSOR_HEAL_INDEX],CURSOR_HEAL);
  pngLoad(&texturesArray[ARCHER_INDEX],ARCHER);
  pngLoad(&texturesArray[SWORDSMAN_INDEX],SWORDSMAN);
  pngLoad(&texturesArray[SELECTION_BOX_INDEX],SELECTION_BOX);
  pngLoad(&texturesArray[SUMMONER_INDEX],SUMMONER);
  pngLoad(&texturesArray[CITY_INDEX],CITY);
  pngLoad(&texturesArray[GATHERER_INDEX],GATHERER);
  pngLoad(&texturesArray[DRAGON_INDEX],DRAGON);
  pngLoad(&texturesArray[WHITE_MAGE_INDEX],WHITE_MAGE);
  pngLoad(&texturesArray[WOLF_INDEX],WOLF);
  pngLoad(&texturesArray[FIRE_INDEX],FIRE);
  pngLoad(&texturesArray[RED_MAGE_INDEX],RED_MAGE);
  pngLoad(&texturesArray[BLUE_MAGE_INDEX],BLUE_MAGE);
  pngLoad(&texturesArray[ICE_INDEX],ICE);
  pngLoad(&texturesArray[GAME_FIND_BACKGROUND_INDEX],GAME_FIND_BACKGROUND);
  pngLoad(&texturesArray[DEPRECATED_INDEX],DEPRECATED);
  pngLoad(&texturesArray[ROOMS_DISPLAY_INDEX],ROOMS_DISPLAY);
  pngLoad(&texturesArray[MODAL_INDEX],MODAL);
  pngLoad(&texturesArray[OK_BUTTON_INDEX],OK_BUTTON);
  pngLoad(&texturesArray[MODAL_BACKGROUND_INDEX],MODAL_BACKGROUND);
  pngLoad(&texturesArray[MODAL_SMALL_INDEX],MODAL_SMALL);
  pngLoad(&texturesArray[SEND_BUTTON_INDEX],SEND_BUTTON);
  pngLoad(&texturesArray[CHAT_BOX_INDEX],CHAT_BOX);
  pngLoad(&texturesArray[CHAT_DISPLAY_INDEX],CHAT_DISPLAY);
  pngLoad(&texturesArray[CREATE_GAME_BUTTON_INDEX],CREATE_GAME_BUTTON);
  pngLoad(&texturesArray[BACK_BUTTON_INDEX],BACK_BUTTON);
  pngLoad(&texturesArray[DA_1V1_BUTTON_INDEX],DA_1V1_BUTTON);
  pngLoad(&texturesArray[DA_2V2_BUTTON_INDEX],DA_2V2_BUTTON);
  pngLoad(&texturesArray[DA_3V3_BUTTON_INDEX],DA_3V3_BUTTON);
  pngLoad(&texturesArray[DA_4V4_BUTTON_INDEX],DA_4V4_BUTTON);
  pngLoad(&texturesArray[CREATE_GAME_BUTTON_LARGE_INDEX],CREATE_GAME_BUTTON_LARGE);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_LEFT_INDEX],CREATE_GAME_BACKGROUND_LEFT);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_RIGHT_INDEX],CREATE_GAME_BACKGROUND_RIGHT);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_TOP_INDEX],CREATE_GAME_BACKGROUND_TOP);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_BOTTOM_INDEX],CREATE_GAME_BACKGROUND_BOTTOM);
  pngLoad(&texturesArray[CREATE_GAME_BACKGROUND_INDEX],CREATE_GAME_BACKGROUND);
  pngLoad(&texturesArray[MAP_SELECTOR_INDEX],MAP_SELECTOR);
  pngLoad(&texturesArray[JOIN_GAME_BACKGROUND_INDEX],JOIN_GAME_BACKGROUND);
  pngLoad(&texturesArray[JOIN_GAME_CHAT_INDEX],JOIN_GAME_CHAT);
  pngLoad(&texturesArray[JOIN_GAME_CHAT_BOX_INDEX],JOIN_GAME_CHAT_BOX);
  pngLoad(&texturesArray[JOIN_GAME_PLAYERS_INDEX],JOIN_GAME_PLAYERS);
  pngLoad(&texturesArray[START_BUTTON_INDEX],START_BUTTON);
  pngLoad(&texturesArray[LOGIN_BUTTON_INDEX],LOGIN_BUTTON);
  pngLoad(&texturesArray[SCROLL_BAR_INDEX],SCROLL_BAR);
  pngLoad(&texturesArray[UNIT_UI_BACK_INDEX],UNIT_UI_BACK);
  pngLoad(&texturesArray[BUILD_BUTTON_INDEX],BUILD_BUTTON);
  pngLoad(&texturesArray[UI_CITY_BACKGROUND_INDEX],UI_CITY_BACKGROUND);
  pngLoad(&texturesArray[UI_UNIT_BACKGROUND_INDEX],UI_UNIT_BACKGROUND);
  pngLoad(&texturesArray[MEDITATE_BUTTON_INDEX],MEDITATE_BUTTON);
  pngLoad(&texturesArray[MOVE_BUTTON_INDEX],MOVE_BUTTON);
  pngLoad(&texturesArray[GREY_PEDESTAL_INDEX],GREY_PEDESTAL);
  pngLoad(&texturesArray[CANCEL_MOVEMENT_BUTTON_INDEX],CANCEL_MOVEMENT_BUTTON);
  pngLoad(&texturesArray[SKIP_BUTTON_INDEX],SKIP_BUTTON);
  pngLoad(&texturesArray[START_GATHERING_BUTTON_INDEX],START_GATHERING_BUTTON);
  pngLoad(&texturesArray[BUILD_BORDER_INDEX],BUILD_BORDER);
  pngLoad(&texturesArray[RED_WOOD_ICON_INDEX],RED_WOOD_ICON);
  pngLoad(&texturesArray[BLUE_WOOD_ICON_INDEX],BLUE_WOOD_ICON);
  pngLoad(&texturesArray[TIME_ICON_INDEX],TIME_ICON);
  pngLoad(&texturesArray[RESEARCH_BUTTON_INDEX],RESEARCH_BUTTON);
  pngLoad(&texturesArray[RESEARCH_BORDER_INDEX],RESEARCH_BORDER);
  pngLoad(&texturesArray[QUEUE_BORDER_INDEX],QUEUE_BORDER);
  pngLoad(&texturesArray[CANCEL_BUTTON_INDEX],CANCEL_BUTTON);
  pngLoad(&texturesArray[UI_UNITTYPE_BACKGROUND_INDEX],UI_UNITTYPE_BACKGROUND);
  pngLoad(&texturesArray[UI_CITYVIEW_BACKGROUND_INDEX],UI_CITYVIEW_BACKGROUND);
  pngLoad(&texturesArray[SLASH_ANIMATION_INDEX],SLASH_ANIMATION);
  pngLoad(&texturesArray[TITLE_INDEX],TITLE);
  pngLoad(&texturesArray[MENU_BUTTON_INDEX],MENU_BUTTON);
  pngLoad(&texturesArray[FLAG_POLE_INDEX],FLAG_POLE);
  pngLoad(&texturesArray[FLAG_TOP_INDEX],FLAG_TOP);
  pngLoad(&texturesArray[ARCHER_OVERLAY_INDEX],ARCHER_OVERLAY);
  pngLoad(&texturesArray[WHITE_MAGE_OVERLAY_INDEX],WHITE_MAGE_OVERLAY);
  pngLoad(&texturesArray[RED_MAGE_OVERLAY_INDEX],RED_MAGE_OVERLAY);
  pngLoad(&texturesArray[BLUE_MAGE_OVERLAY_INDEX],BLUE_MAGE_OVERLAY);
  pngLoad(&texturesArray[WOLF_OVERLAY_INDEX],WOLF_OVERLAY);
  pngLoad(&texturesArray[DRAGON_OVERLAY_INDEX],DRAGON_OVERLAY);
  pngLoad(&texturesArray[GATHERER_OVERLAY_INDEX],GATHERER_OVERLAY);
  pngLoad(&texturesArray[CONNECT_BUTTON_INDEX],CONNECT_BUTTON);
  pngLoad(&texturesArray[CHECK_MARK_INDEX],CHECK_MARK);
  pngLoad(&texturesArray[CHECK_MARK_CHECKED_INDEX],CHECK_MARK_CHECKED);
  pngLoad(&texturesArray[CHECKBOXES_BACKGROUND_INDEX],CHECKBOXES_BACKGROUND);
  pngLoad(&texturesArray[UI_CITY_EDITOR_BACKGROUND_BACKGROUND_INDEX],UI_CITY_EDITOR_BACKGROUND_BACKGROUND);
  pngLoad(&texturesArray[MENU_MODAL_INDEX],MENU_MODAL);
  pngLoad(&texturesArray[FOREST_INDEX0],FOREST0);
  pngLoad(&texturesArray[FOREST_INDEX1],FOREST1);
  pngLoad(&texturesArray[FOREST_INDEX2],FOREST2);
  pngLoad(&texturesArray[FOREST_INDEX3],FOREST3);
  pngLoad(&texturesArray[GRASS_INDEX0],GRASS0);
  pngLoad(&texturesArray[GRASS_INDEX1],GRASS1);
  pngLoad(&texturesArray[GRASS_INDEX2],GRASS2);
  pngLoad(&texturesArray[GRASS_INDEX3],GRASS3);
  pngLoad(&texturesArray[MOUNTAIN_INDEX0],MOUNTAIN0);
  pngLoad(&texturesArray[MOUNTAIN_INDEX1],MOUNTAIN1);
  pngLoad(&texturesArray[MOUNTAIN_INDEX2],MOUNTAIN2);
  pngLoad(&texturesArray[MOUNTAIN_INDEX3],MOUNTAIN3);
  pngLoad(&texturesArray[REDFOREST_INDEX0],REDFOREST0);
  pngLoad(&texturesArray[REDFOREST_INDEX1],REDFOREST1);
  pngLoad(&texturesArray[REDFOREST_INDEX2],REDFOREST2);
  pngLoad(&texturesArray[REDFOREST_INDEX3],REDFOREST3);
  pngLoad(&texturesArray[BLUEFOREST_INDEX0],BLUEFOREST0);
  pngLoad(&texturesArray[BLUEFOREST_INDEX1],BLUEFOREST1);
  pngLoad(&texturesArray[BLUEFOREST_INDEX2],BLUEFOREST2);
  pngLoad(&texturesArray[BLUEFOREST_INDEX3],BLUEFOREST3);
  pngLoad(&texturesArray[WATER_INDEX0],WATER0);
  pngLoad(&texturesArray[WATER_INDEX1],WATER1);
  pngLoad(&texturesArray[WATER_INDEX2],WATER2);
  pngLoad(&texturesArray[WATER_INDEX3],WATER3);
  pngLoad(&texturesArray[FLAG_INDEX0],FLAG0);
  pngLoad(&texturesArray[FLAG_INDEX1],FLAG1);
  pngLoad(&texturesArray[FLAG_INDEX2],FLAG2);
  pngLoad(&texturesArray[FLAG_INDEX3],FLAG3);
  pngLoad(&texturesArray[ADD_AI_BUTTON_INDEX],ADD_AI_BUTTON);
  pngLoad(&texturesArray[UNIT_VIEWER_BACKGROUND_INDEX],UNIT_VIEWER_BACKGROUND);
  pngLoad(&texturesArray[SUMMON_VIEWER_BACKGROUND_INDEX],SUMMON_VIEWER_BACKGROUND);
  pngLoad(&texturesArray[STONE_VIEWER_BACKGROUND_INDEX],STONE_VIEWER_BACKGROUND);
  pngLoad(&texturesArray[BUILD_INDEX],BUILD);
  pngLoad(&texturesArray[SUMMON_INDEX],SUMMON);
  pngLoad(&texturesArray[QUEUE_INDEX],QUEUE);
  
  soundArray[WOOD_HIT_INDEX] = Mix_LoadWAV(WOOD_HIT);
  soundArray[TUBE_HIT_INDEX] = Mix_LoadWAV(TUBE_HIT);
  soundArray[DARBUKA_HIT_INDEX] = Mix_LoadWAV(DARBUKA_HIT);
  soundArray[DARBUKA2_HIT_INDEX] = Mix_LoadWAV(DARBUKA2_HIT);
  soundArray[FINGER_CYMBALS_HIT_INDEX] = Mix_LoadWAV(FINGER_CYMBALS_HIT);
  soundArray[SWORD_HIT_INDEX] = Mix_LoadWAV(SWORD_HIT);
  soundArray[DRAGON_FIRE_INDEX] = Mix_LoadWAV(DRAGON_FIRE);
  soundArray[BOW_HIT_INDEX] = Mix_LoadWAV(BOW_HIT);

  musicArray[OMAR_1_INDEX] = Mix_LoadMUS(OMAR_1);
  musicArray[OMAR_7_INDEX] = Mix_LoadMUS(OMAR_7);

  vertexArrays[FOREST_TILE_INDEX] = *forestVertices;
  vertexArrays[GRASS_TILE_INDEX] = *grassVertices;
  vertexArrays[MOUNTAIN_TILE_INDEX] = *mountainVertices;
  vertexArrays[RED_FOREST_TILE_INDEX] = *forestVertices;
  vertexArrays[BLUE_FOREST_TILE_INDEX] = *blueForestVertices;
  vertexArrays[WATER_TILE_INDEX] = *waterVertices;
  vertexArrays[ROAD_TILE_INDEX] = *roadVertices;
  vertexArrays[CITY_TILE_INDEX] = *cityVertices;
  vertexArrays[PLAYER_START_TILE_INDEX] = *playerStartVertices;
  
  tilesLists = glGenLists(100);

  int c;
  int d;
  for(c=0;c<9;c++){
    for(d=0;d<4;d++){
      glNewList(tilesLists+(c*4)+d,GL_COMPILE);
      if(c <= 5){
	glBindTexture(GL_TEXTURE_2D, texturesArray[TILE_INDEX_START+(4*c)+d]);
	glBegin(GL_POLYGON);
	glTexCoord2f(textureHexVertices[0][0],textureHexVertices[0][1]); glVertex3f(hexagonVertices[0][0], hexagonVertices[0][1], 0.0);
	glTexCoord2f(textureHexVertices[1][0],textureHexVertices[1][1]); glVertex3f(hexagonVertices[1][0], hexagonVertices[1][1], 0.0);
	glTexCoord2f(textureHexVertices[2][0],textureHexVertices[2][1]); glVertex3f(hexagonVertices[2][0], hexagonVertices[2][1], 0.0);
	glTexCoord2f(textureHexVertices[3][0],textureHexVertices[3][1]); glVertex3f(hexagonVertices[3][0], hexagonVertices[3][1], 0.0);
	glTexCoord2f(textureHexVertices[4][0],textureHexVertices[4][1]); glVertex3f(hexagonVertices[4][0], hexagonVertices[4][1], 0.0);
	glTexCoord2f(textureHexVertices[5][0],textureHexVertices[5][1]); glVertex3f(hexagonVertices[5][0], hexagonVertices[5][1], 0.0);
	glEnd();
      }else{
	glBindTexture(GL_TEXTURE_2D, tilesTexture);
	glBegin(GL_POLYGON);
	glTexCoord2f(*(vertexArrays[c]+0),*(vertexArrays[c]+1)); glVertex3f(hexagonVertices[0][0], hexagonVertices[0][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+2),*(vertexArrays[c]+3)); glVertex3f(hexagonVertices[1][0], hexagonVertices[1][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+4),*(vertexArrays[c]+5)); glVertex3f(hexagonVertices[2][0], hexagonVertices[2][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+6),*(vertexArrays[c]+7)); glVertex3f(hexagonVertices[3][0], hexagonVertices[3][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+8),*(vertexArrays[c]+9)); glVertex3f(hexagonVertices[4][0], hexagonVertices[4][1], 0.0);
	glTexCoord2f(*(vertexArrays[c]+10),*(vertexArrays[c]+11)); glVertex3f(hexagonVertices[5][0], hexagonVertices[5][1], 0.0);
	glEnd();
      }
      glEndList();
    }
  }
  selectionBoxList = tilesLists+(c*d)+1;
  unitList = selectionBoxList+1;
  healthBarList = unitList+1;
  flagList = healthBarList+1;

  glNewList(selectionBoxList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-0.88,-1.0,0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(0.84,-1.0,0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(0.84,1.0, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-0.88,1.0, 0.0);
  glEnd();
  glEndList();

  glNewList(unitList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-0.75, -0.75, 0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(0.75, -0.75, 0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(0.75, 0.75, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-0.75, 0.75, 0.0);
  glEnd();
  glEndList();

  glNewList(healthBarList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-.35, 0.9, 0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(.35, 0.9, 0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(.35, 0.8, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-.35, 0.8, 0.0);
  glEnd();
  glEndList();

  glNewList(flagList,GL_COMPILE);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0); glVertex3f(0.5, -0.1, 0.0);
  glTexCoord2f(1.0,0.0); glVertex3f(0.95, -0.1, 0.0);
  glTexCoord2f(1.0,1.0); glVertex3f(0.95, 0.1, 0.0);
  glTexCoord2f(0.0,1.0); glVertex3f(0.5, 0.1, 0.0);
  glEnd();
  glEndList();

}

static void initPython(){
  //http://docs.python.org/release/2.6.6/c-api/index.html
  //  char [100] = "-v";
  //	sprintf(path,"%s","hello");
  Py_SetPythonHome(".");
  Py_Initialize();
  char *pyArgv[1];
  pyArgv[0] = "";
  PySys_SetArgv(1, pyArgv);
  if(isWindows){
    PyObject* sys = PyImport_ImportModule("sys");
    PyObject* pystdout = PyFile_FromString("stdout.txt", "wt");
    if (-1 == PyObject_SetAttrString(sys, "stdout", pystdout)) {
      printf("NO STDOUT AVAILABLE");
    }
    PyObject* pystderr = PyFile_FromString("stderr.txt", "wt");
    if (-1 == PyObject_SetAttrString(sys, "stderr", pystderr)) {
      printf("NO STDERR AVAILABLE");
    }
    if(pystdout != NULL){
      Py_DECREF(pystdout);
    }
    if(pystderr != NULL){
      Py_DECREF(pystderr);
    }
    Py_DECREF(sys);
  }
}
SDL_Event event;
PyObject * pyFocusNextUnit;
char keyArray[20];
PyObject * pyClickScroll;
static void handleInput(){
  if(PyObject_HasAttrString(gameMode,"clickScroll")){
      pyClickScroll = PyObject_GetAttrString(gameMode, "clickScroll");//New reference
      clickScroll = pyClickScroll == Py_True;
      Py_DECREF(pyClickScroll);
  }
  /*  if(PyObject_HasAttrString(gameMode,"getFocusNextUnit")){
    pyFocusNextUnit = PyObject_CallMethod(gameMode,"getFocusNextUnit",NULL);
    doFocus = PyLong_AsLong(pyFocusNextUnit);
    if(doFocus){
      isFocusing = 1;
    }
    //    Py_DECREF(pyClickScroll);
    }*/
  if(previousMousedoverName != selectedName){
    if(PyObject_HasAttrString(gameMode,"handleMouseOver")){
      pyObj = PyObject_CallMethod(gameMode,"handleMouseOver","(ii)",selectedName,leftButtonDown);//New reference
      printPyStackTrace();
      Py_DECREF(pyObj);
    }
    previousMousedoverName = selectedName;
  }

  //SDL_Delay(20);//for framerate testing...

  if(keyHeld){
    if(repeatKey){
      if(SDL_GetTicks() - keyHeldTime > 40){
	keyHeldTime = SDL_GetTicks();
	if(PyObject_HasAttrString(gameMode,"handleKeyDown")){
	  //	  pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",keyArray);
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
      }
    }else if(SDL_GetTicks() - keyHeldTime > 500){
      repeatKey = 1;
      keyHeldTime = SDL_GetTicks();
    }
  }
  while(SDL_PollEvent(&event)){
    switch(event.type){
    case SDL_MOUSEMOTION:
      mouseX = event.motion.x;
      mouseY = event.motion.y;
      if(PyObject_HasAttrString(gameMode,"handleMouseMovement")){
	pyObj = PyObject_CallMethod(gameMode,"handleMouseMovement","(iii)",selectedName,mouseX,mouseY);
	Py_DECREF(pyObj);
      }
      printPyStackTrace();
      if(mouseX == 0){
	moveRight = -1;
      }else if(mouseX >= SCREEN_WIDTH-1){
	moveRight = 1;
      }else{
	moveRight = 0;
      }
      if(mouseY == 0){
	moveUp = 1;
      }else if(mouseY >= SCREEN_HEIGHT-1){
	moveUp = -1;
      }else{
	moveUp = 0;
      }
      break;
    case SDL_MOUSEBUTTONDOWN:
      if(event.button.button == SDL_BUTTON_WHEELUP){
	if(PyObject_HasAttrString(gameMode,"handleScrollUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleScrollUp","i",selectedName);//New reference
	  Py_DECREF(pyObj);
	}
      }else if(event.button.button == SDL_BUTTON_WHEELDOWN){
	if(PyObject_HasAttrString(gameMode,"handleScrollDown")){
	  PyObject_CallMethod(gameMode,"handleScrollDown","i",selectedName);//New reference
	  Py_DECREF(pyObj);
	}
      }
      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 1;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	leftButtonDown = 1;
	if(PyObject_HasAttrString(gameMode,"handleLeftClickDown")){
	  pyObj = PyObject_CallMethod(gameMode,"handleLeftClickDown","i",selectedName);//New reference
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
	previousClickedName = selectedName;
      }
      printPyStackTrace();
      if(event.button.button == SDL_BUTTON_RIGHT){
	//	clickScroll = 1;
	pyObj = PyObject_CallMethod(gameMode,"handleRightClick","i",selectedName);//New reference
	  Py_DECREF(pyObj);
      }
      break;
    case SDL_MOUSEBUTTONUP:
      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 0;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	if(PyObject_HasAttrString(gameMode,"handleLeftClickUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleLeftClickUp","i",selectedName);//New reference
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
	leftButtonDown = 0;
      }
      if(event.button.button == SDL_BUTTON_RIGHT){
	if(PyObject_HasAttrString(gameMode,"handleRightClickUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleRightClickUp","i",selectedName);//New reference
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
      }
      break;
    case SDL_KEYDOWN:
      /*      if(event.key.keysym.sym == SDLK_ESCAPE){
	done = 1;	
	
      }else if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 1;
	avgDeltaTicks = 0;
	totalDeltaTicksDataPoints = 0;
      }else */
      if(event.key.keysym.sym == SDLK_NUMLOCK
	       || event.key.keysym.sym ==SDLK_CAPSLOCK
	       || event.key.keysym.sym ==SDLK_SCROLLOCK
	       //	       || event.key.keysym.sym ==SDLK_RSHIFT
	       //	       || event.key.keysym.sym ==SDLK_LSHIFT
	       || event.key.keysym.sym ==SDLK_RCTRL
	       || event.key.keysym.sym ==SDLK_LCTRL
	       || event.key.keysym.sym ==SDLK_RALT
	       || event.key.keysym.sym ==SDLK_LALT
	       || event.key.keysym.sym == SDLK_RMETA
	       || event.key.keysym.sym == SDLK_LMETA
	       || event.key.keysym.sym == SDLK_LSUPER
	       || event.key.keysym.sym == SDLK_RSUPER
	       || event.key.keysym.sym == SDLK_MODE
	       || event.key.keysym.sym == SDLK_COMPOSE
	       || event.key.keysym.sym == SDLK_HELP
	       || event.key.keysym.sym == SDLK_PRINT
	       || event.key.keysym.sym == SDLK_SYSREQ
	       || event.key.keysym.sym == SDLK_BREAK
	       || event.key.keysym.sym == SDLK_MENU
	       || event.key.keysym.sym == SDLK_POWER
	       || event.key.keysym.sym == SDLK_EURO
	       || event.key.keysym.sym == SDLK_UNDO){
	//	printf("rejected: %d\n",event.key.keysym.sym);
      }else{
	if(event.key.keysym.sym != SDLK_RSHIFT && event.key.keysym.sym != SDLK_LSHIFT){
	  keyHeld = 1;
	  repeatKey = 0;
	}
	keyHeldTime = SDL_GetTicks();
	if((event.key.keysym.mod & KMOD_CAPS | event.key.keysym.mod & KMOD_LSHIFT | event.key.keysym.mod & KMOD_RSHIFT) && (event.key.keysym.sym > 0x60 && event.key.keysym.sym <= 0x7A)){
	  keyArray[0] = (*SDL_GetKeyName(event.key.keysym.sym))-32;
	  keyArray[1] = 0;
	}else if(event.key.keysym.mod & KMOD_LSHIFT | event.key.keysym.mod & KMOD_RSHIFT){
	  switch(event.key.keysym.sym){
	  case SDLK_COMMA:
	    keyArray[0] = SDLK_LESS;
	    keyArray[1] = 0;
	    break;
	  case SDLK_MINUS:
	    keyArray[0] = SDLK_UNDERSCORE;
	    keyArray[1] = 0;
	    break;
	  case SDLK_SEMICOLON:
	    keyArray[0] = SDLK_COLON;
	    keyArray[1] = 0;
	    break;
	  case SDLK_EQUALS:
	    keyArray[0] = SDLK_PLUS;
	    keyArray[1] = 0;
	    break;
	  case SDLK_PERIOD:
	    keyArray[0] = SDLK_GREATER;
	    keyArray[1] = 0;
	    break;
	  case SDLK_SLASH:
	    keyArray[0] = SDLK_QUESTION;
	    keyArray[1] = 0;
	    break;
	  case SDLK_LEFTBRACKET:
	    keyArray[0] = 123;
	    keyArray[1] = 0;
	    break;
	  case SDLK_RIGHTBRACKET:
	    keyArray[0] = 125;
	    keyArray[1] = 0;
	    break;
	  case SDLK_BACKSLASH:
	    keyArray[0] = 124;
	    keyArray[1] = 0;
	    break;
	  case SDLK_0:
	    keyArray[0] = SDLK_RIGHTPAREN;
	    keyArray[1] = 0;
	    break;
	  case SDLK_1:
	    keyArray[0] = SDLK_EXCLAIM;
	    keyArray[1] = 0;
	    break;
	  case SDLK_2:
	    keyArray[0] = SDLK_AT;
	    keyArray[1] = 0;
	    break;
	  case SDLK_3:
	    keyArray[0] = SDLK_HASH;
	    keyArray[1] = 0;
	    break;
	  case SDLK_4:
	    keyArray[0] = SDLK_DOLLAR;
	    keyArray[1] = 0;
	    break;
	  case SDLK_5:
	    keyArray[0] = 37;
	    keyArray[1] = 0;
	    break;
	  case SDLK_6:
	    keyArray[0] = SDLK_CARET;
	    keyArray[1] = 0;
	    break;
	  case SDLK_7:
	    keyArray[0] = SDLK_AMPERSAND;
	    keyArray[1] = 0;
	    break;
	  case SDLK_8:
	    keyArray[0] = SDLK_ASTERISK;
	    keyArray[1] = 0;
	    break;
	  case SDLK_9:
	    keyArray[0] = SDLK_LEFTPAREN;
	    keyArray[1] = 0;
	    break;
	  }
	}else{
	  sprintf(keyArray,"%s",SDL_GetKeyName(event.key.keysym.sym));
	}
	if(PyObject_HasAttrString(gameMode,"handleKeyDown")){	
	  pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",keyArray); 
	  printPyStackTrace();
	  Py_DECREF(pyObj);
	}
      }
      break;
    case SDL_KEYUP:
      keyHeld = 0;
      repeatKey = 0;
      /*if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 0;
	}else*/
      if(event.key.keysym.sym == 303//rightshift
	 || event.key.keysym.sym == 304//leftshift
	 || event.key.keysym.sym == SDLK_BACKQUOTE){
	if(PyObject_HasAttrString(gameMode,"handleKeyUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleKeyUp","s",SDL_GetKeyName(event.key.keysym.sym));
	  Py_DECREF(pyObj);
	}
      }
      break;
    case SDL_QUIT:
      done = 1;
      break;
    default:
      break;
    }
  }
}
PyObject * pyBackgroundImageIndex;
int backgroundImageIndex;
void drawBackground(){
  if(PyObject_HasAttrString(gameMode,"backgroundImageIndex")){
    pyBackgroundImageIndex = PyObject_GetAttrString(gameMode, "backgroundImageIndex");//New reference
    backgroundImageIndex = PyLong_AsLong(pyBackgroundImageIndex);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glBindTexture(GL_TEXTURE_2D, texturesArray[backgroundImageIndex]);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(1.0,-1.0,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(1.0,1.0,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(-1.0,1.0,0.0);
    glEnd();
    Py_DECREF(pyBackgroundImageIndex);
  }
}
GLint viewport[4];
GLint hitsCnt;
PyObject * pyChooseNextDelayed;
int chooseNextDelayed;
Uint32 chooseNextTimeStart;
PyObject * pyAnimQueue;
PyObject * pyAnimQueueEmpty;
PyObject * pyAnim;
listelement * animQueue = NULL;
ANIMATION * theAnim;
static void draw(){
  PyObject_SetAttrString(gameMode,"ticks",PyLong_FromLong(SDL_GetTicks()));
  if(PyObject_HasAttrString(gameMode,"onDraw")){
    pyObj = PyObject_CallMethod(gameMode,"onDraw","(ii)",deltaTicks,isAnimating);//New reference
    printPyStackTrace();
    Py_DECREF(pyObj);
  }
  pyAnimQueue = PyObject_GetAttrString(gameState,"animQueue");
  pyAnimQueueEmpty = PyObject_CallMethod(pyAnimQueue,"empty",NULL);
  //  printf("afg%d\n",1);
  while(pyAnimQueueEmpty == Py_False){
    pyAnim = PyObject_CallMethod(pyAnimQueue,"get",NULL);
    ANIMATION temp;
    theAnim = &(temp);
    pyObj = PyObject_GetAttrString(pyAnim,"type");
    theAnim->type = PyLong_AsLong(pyObj);
    Py_DECREF(pyObj);
    pyObj = PyObject_GetAttrString(pyAnim,"xPos");
    theAnim->xPos = PyFloat_AsDouble(pyObj);
    Py_DECREF(pyObj);
    pyObj = PyObject_GetAttrString(pyAnim,"yPos");
    theAnim->yPos = PyFloat_AsDouble(pyObj);
    Py_DECREF(pyObj);
    pyUnit = PyObject_GetAttrString(pyAnim,"unit");
    if(pyUnit != Py_None){
      pyUnitType = PyObject_GetAttrString(pyUnit,"unitType");
      UNIT temp;
      theAnim->unit = &(temp);
      pyObj = PyObject_GetAttrString(pyUnit,"xPos");
      theAnim->unit->xPos = PyLong_AsLong(pyObj);
      Py_DECREF(pyObj);
      pyObj = PyObject_GetAttrString(pyUnit,"yPos");
      theAnim->unit->yPos = PyLong_AsLong(pyObj);
      Py_DECREF(pyObj);
      pyObj = PyObject_GetAttrString(pyUnit,"health");
      theAnim->unit->health = PyLong_AsLong(pyObj);
      Py_DECREF(pyObj);
      pyObj = PyObject_GetAttrString(pyUnitType,"health");
      theAnim->unit->maxHealth = PyLong_AsLong(pyObj);
      Py_DECREF(pyObj);
      Py_DECREF(pyUnit);
    }
    Py_DECREF(pyAnim);
    Py_DECREF(pyAnimQueueEmpty);
    pyAnimQueueEmpty = PyObject_CallMethod(pyAnimQueue,"empty",NULL);
    animQueue = AddItem(animQueue,theAnim);
  }
  Py_DECREF(pyAnimQueue);
  //  Py_DECREF(pyAnimQueueEmpty);
  if(animQueue != NULL && !isAnimating){//> 0 items
    isAnimating = 1;
    listelement * listpointer;
    ANIMATION * animation = animQueue->item; 
    animQueue = RemoveItem(animQueue);
    if(animation->type == ANIMATION_AUTO_FOCUS){
      isFocusing = 1;
      focusXPos = translateTilesXToPositionX(0.0-animation->xPos,animation->yPos);
      focusYPos = translateTilesYToPositionY(animation->yPos);
    }else{
      printf("fs%d\n",1);
      isAnimating = 0; 
    }
  }
  if(!isFocusing && !isSliding){
    //      printf("done%d\n",1);
    isAnimating = 0;
  }

  //  pyCursorIndex = PyObject_GetAttrString(gameState,"cursorIndex");
  theCursorIndex = -1;
  pyCursorIndex = PyObject_GetAttrString(gameState,"cursorIndex");
  theCursorIndex = PyLong_AsLong(pyCursorIndex);
  Py_DECREF(pyCursorIndex);

  if(PyObject_HasAttrString(gameMode,"chooseNextDelayed")){
    pyChooseNextDelayed = PyObject_CallMethod(gameMode,"getChooseNextDelayed",NULL);//New reference
    printPyStackTrace();
    Py_DECREF(pyChooseNextDelayed);
    if(pyChooseNextDelayed == Py_True){
      chooseNextTimeStart = SDL_GetTicks();
      chooseNextDelayed = 1;
    }
  }
  if(chooseNextDelayed && ((SDL_GetTicks() - chooseNextTimeStart) > AUTO_CHOOSE_NEXT_DELAY)){
    chooseNextDelayed = 0;
    pyObj = PyObject_CallMethod(gameMode,"sendChooseNextUnit",NULL);//New reference
    printPyStackTrace();
    Py_DECREF(pyObj);
  }

//  printf("**** other:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		 
  glSelectBuffer(BUFSIZE,selectBuf);//glSelectBuffer must be issued before selection mode is enabled, and it must not be issued while the rendering mode is GL_SELECT.

  doViewport();
  glGetIntegerv(GL_VIEWPORT,viewport);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPickMatrix(mouseX,SCREEN_HEIGHT-mouseY,1,1,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glTranslatef(translateX,translateY,translateZ);
  glRenderMode(GL_SELECT);
//  printf("**** selecta:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 
  drawBoard();
//  printf("**** selectb:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPickMatrix(mouseX,SCREEN_HEIGHT-mouseY,1,1,viewport);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  hitsCnt = glRenderMode(GL_RENDER);
//  printf("**** selectc:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 
  processTheHits(hitsCnt,selectBuf);
//  printf("**** selectd:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 
  selectedNodeName = selectedName;

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		 
  glSelectBuffer(BUFSIZE,selectBuf);//glSelectBuffer must be issued before selection mode is enabled, and it must not be issued while the rendering mode is GL_SELECT.
  glRenderMode(GL_SELECT);

  drawUI();
  hitsCnt = glRenderMode(GL_RENDER);
//  printf("**** selecte:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 
  processTheHits(hitsCnt,selectBuf);
//  printf("**** selectf:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 
  if(selectedName == -1){
    selectedName = selectedNodeName;
  }
//  printf("**** selectg:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 
//  printf("****** other1:    \t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  calculateTranslation();
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		
  drawBackground();
//  printf("****** other1a:    \t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 
  doViewport();
//  printf("****** other1b:    \t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);
//  printf("****** other1c:    \t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glColor3f(0.0,0.0,0.0);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,-1.01);
  glTexCoord2f(1.0,0.0); glVertex3f(1.0,-1.0,-1.01);
  glTexCoord2f(1.0,1.0); glVertex3f(1.0,1.0,-1.01);
  glTexCoord2f(0.0,1.0); glVertex3f(-1.0,1.0,-1.01);
  glEnd();
  glTranslatef(translateX,translateY,translateZ);
//  printf("****** other2:    \t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 
  drawBoard();
//  printf("****** drawBoard:\t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
//  printf("****** other3:    \t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 
  drawUI();
//  printf("****** drawUI:   \t%d\n",SDL_GetTicks() - testTicks4); testTicks4 = SDL_GetTicks(); 
  glFlush();
  SDL_GL_SwapBuffers();
//  printf("**** render:      \t%d\n",SDL_GetTicks() - testTicks2); testTicks2 = SDL_GetTicks(); 
}
PyObject * pyExit;
int musicChannel = -2;
int soundIndex = -1;
int restartMusic = 0;
static void mainLoop (){
  while ( !done ) {
    gameMode = PyObject_CallMethod(gameState,"getGameMode",NULL);
    pyObj = PyObject_CallMethod(gameMode, "getRestartMusic",NULL);//New reference
    restartMusic = PyLong_AsLong(pyObj);
    Py_DECREF(pyObj);
    /*if(!Mix_PlayingMusic() || restartMusic){
      Py_DECREF(pyObj);
      pyObj = PyObject_CallMethod(gameMode,"getMusic",NULL);
      soundIndex = PyLong_AsLong(pyObj);
      Mix_PlayMusic(musicArray[soundIndex], 0);
      }*/
    pyObj = PyObject_CallMethod(gameMode,"getSound",NULL);
    while(pyObj != Py_None && pyObj != NULL){
      soundIndex = PyLong_AsLong(pyObj);
      Py_DECREF(pyObj);
      Mix_PlayChannel(-1, soundArray[soundIndex], 0);
      pyObj = PyObject_CallMethod(gameMode,"getSound",NULL);
      Py_DECREF(pyObj);
    }
    if(PyObject_HasAttrString(gameMode,"map")){
      theMap = PyObject_GetAttrString(gameMode, "map");//New reference
    }
    pyExit = PyObject_GetAttrString(gameMode,"exit");
    done = (pyExit == Py_True);
    deltaTicks = SDL_GetTicks()-currentTick;
    currentTick = SDL_GetTicks();
//    printf("**** other:      \t%d\n",SDL_GetTicks() - testTicks); testTicks = SDL_GetTicks(); 
    handleInput();
//    printf("**** handleInput:\t%d\n",SDL_GetTicks() - testTicks); testTicks = SDL_GetTicks(); 
    draw();
//    printf("**** draw:       \t%d\n",SDL_GetTicks() - testTicks); testTicks = SDL_GetTicks(); 
    
    if(theMap != NULL && theMap != Py_None){
      Py_DECREF(theMap);
    }
    Py_DECREF(gameMode);
  }
  pyObj = PyObject_CallMethod(gameMode,"onQuit",NULL);
  Py_DECREF(pyObj);
}
int nextPowerOf2(unsigned int v){
  const unsigned int b[] = {0x2, 0xC, 0xF0, 0xFF00, 0xFFFF0000};
  const unsigned int S[] = {1, 2, 4, 8, 16};
  int i;
  register unsigned int r = 0; // result of log2(v) will go here
  for (i = 4; i >= 0; i--){ // unroll for speed...
    if (v & b[i]){
      v >>= S[i];
      r |= S[i];
    } 
  }
  return pow(2,r+1);
}

int main(int argc, char **argv){
  if ( SDL_Init (SDL_INIT_VIDEO | SDL_INIT_AUDIO) < 0 ) {
    fprintf(stderr, "Couldn't initialize SDL: %s\n",SDL_GetError());
    exit(1);
  }

  int audio_rate = 44100;//22050;
  Uint16 audio_format = AUDIO_S16SYS;
  int audio_channels = 2;
  int audio_buffers = 4096;

  if(Mix_OpenAudio(audio_rate, audio_format, audio_channels, audio_buffers) != 0) {
    fprintf(stderr, "Unable to initialize audio: %s\n", Mix_GetError());
    exit(1);
  }

  SDL_GL_SetAttribute (SDL_GL_DEPTH_SIZE, 16);
  //  SDL_GL_SetAttribute (SDL_GL_DOUBLEBUFFER, 1);
  Uint32 flags = SDL_OPENGL;
  if(FULL_SCREEN){
    flags |= SDL_FULLSCREEN;
  }
  gScreen = SDL_SetVideoMode (SCREEN_WIDTH, SCREEN_HEIGHT, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Could not set OpenGL video mode: %s\n",
	     SDL_GetError());
    SDL_Quit();
    exit(2);
  }
  int * value;
  //  SDL_GL_GetAttribute(SDL_GL_DEPTH_SIZE,value);
  SDL_ShowCursor(0);
  initGL();
  const GLubyte * glVersion = glGetString(GL_VERSION);
  initPython();
  initFonts();
  //SDL_EnableUNICODE(1);
  gameModule = PyImport_ImportModule("gameModes");//New reference
  gameState = PyImport_ImportModule("gameState");
  mainLoop();
  Py_DECREF(gameModule);
  Py_DECREF(gameState);
  Py_Finalize();
  exit(0);
}
