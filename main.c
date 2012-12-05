//#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <SDL.h>
#include <SDL_opengl.h>
#include <SDL_mixer.h>
#include <SDL_thread.h>

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
//#include "animQueue.c"

float focusSpeed = 0.0;
float focusTime = 0.0;
float focusSpeedX = 0.0;
float focusSpeedY = 0.0;

float screenRatio;
static SDL_Surface *gScreen;

int clickScroll = 0;
long doFocus = 0;
long focusTicks;
double focusXPos, focusYPos, focusTilesXPos, focusTilesYPos, focusXPosPrev, focusYPosPrev;
PyObject * pyFocusXPos;
PyObject * pyFocusYPos;
int isFocusing = 0;
int isSliding = 0;
Uint32 slidingTicks;
int isAnimating = 0;
int doneAnimatingFired = 0;
int considerDoneFocusing = 0;
int leftButtonDown = 0;

int doQuit = 0;    
int quit = 0;    
int moveUp = 0;
int moveRight = 0;
int currentTick = 0;
int pythonCurrentTick = 0;
int deltaTicks = 0;
int avgDeltaTicks = 0;
int totalDeltaTicksDataPoints = 0;

int keyHeld;
int repeatKey;
Uint32 keyHeldTime;

GLfloat mapDepth,mapDepthTest1,mapDepthTest2,mapDepthTest3;
float translateX = 0.0;
float translateY = 0.0;
float translateZ = 0.0-initZoom;
float maxTranslateZ = 0.0-maxZoom;
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
PyObject * pyMap;
PyObject * mapName;
PyObject * mapIterator;
PyObject * UIElementsIterator;
PyObject * rowIterator;
PyObject * pyMapWidth;
PyObject * pyMapHeight;
//PyObject * pyObj;
//PyObject * playableMode;
//long mapWidth;
//long mapHeight;

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


/**************************** mouse hover object selection ********************************/
//easing functions shamelessly stolen from:
//http://timotheegroleau.com/Flash/experiments/easing_function_generator.htm
double ticksPercentage;
double ts;
double tc;
double slidingEasingFunction(Uint32 deltaTicks,double startPos,double endPos,int totalTicks){
  ticksPercentage = ((double)deltaTicks)/((double)totalTicks);
  ts = ticksPercentage*ticksPercentage;
  tc = ts*ticksPercentage;
  //  return startPos+((endPos-startPos)*(0.75*tc*ts + -1.7*ts*ts + -0.9*tc + 2.8*ts + 0.05*ticksPercentage));
  //  return startPos+((endPos-startPos)*(10.3525*tc*ts + -30.5025*ts*ts + 27.9*tc + -6.8*ts + 0.05*ticksPercentage));
  //  return startPos+((endPos-startPos)*(10.995*tc*ts + -28.69*ts*ts + 22.395*tc + -3.7*ts));
  //  return startPos+((endPos-startPos)*(-4.8975*tc*ts + 16.1475*ts*ts + -20.6*tc + 11.3*ts + -0.95*ticksPercentage));
  //  return startPos+((endPos-startPos)*(-14.6475*tc*ts + 48.7425*ts*ts + -58.29*tc + 27.895*ts + -2.7*ticksPercentage));
		   //  return startPos+((endPos-startPos)*(-12.0975*tc*ts + 38.5425*ts*ts + -42.99*tc + 17.695*ts + -0.15*ticksPercentage));
  return startPos+((endPos-startPos)*(0.699999999999997*tc*ts + 0.800000000000004*ts*ts + -5.6*tc + 5*ts + 0.1*ticksPercentage));
}
double focusEasingFunction(int deltaTicks,double startPos,double endPos,int totalTicks){
  ticksPercentage = ((double)deltaTicks)/((double)totalTicks);
  ts = ticksPercentage*ticksPercentage;
  tc = ts*ticksPercentage;
  //  return startPos+((endPos-startPos)*(4.795*tc*ts + -11.69*ts*ts + 6.995*tc + 0.9*ts));
  return startPos+((endPos-startPos)*(tc + -3*ts + 3*ticksPercentage));
}
double damageSize1EasingFunction(int deltaTicks,double startPos,double endPos,int totalTicks){
  ticksPercentage = ((double)deltaTicks)/((double)totalTicks);
  ts = ticksPercentage*ticksPercentage;
  tc = ts*ticksPercentage;
  return startPos+((endPos-startPos)*(-1*ts*ts + 4*tc + -6*ts + 4*ticksPercentage));
}
double damagePosEasingFunction(int deltaTicks,double startPos,double endPos,int totalTicks){
  ticksPercentage = ((double)deltaTicks)/((double)totalTicks);
  ts = ticksPercentage*ticksPercentage;
  tc = ts*ticksPercentage;
  //  return startPos+((endPos-startPos)*(4.795*tc*ts + -11.69*ts*ts + 6.995*tc + 0.9*ts));
  return startPos+((endPos-startPos)*(-1*ts*ts + 4*tc + -6*ts + 4*ticksPercentage));
}
double damageAlphaEasingFunction(int deltaTicks,double startPos,double endPos,int totalTicks){
  ticksPercentage = ((double)deltaTicks)/((double)totalTicks);
  ts = ticksPercentage*ticksPercentage;
  tc = ts*ticksPercentage;
  return startPos+((endPos-startPos)*(4.795*tc*ts + -11.69*ts*ts + 6.995*tc + 0.9*ts));
}
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
SDL_mutex * pythonCallbackMutex;
SDL_mutex * unitsMutex;//protects theUnits
SDL_mutex * animationsMutex;//protects animQueue
SDL_mutex * modalAnimationsMutex;//protects modalAnimQueue
SDL_mutex * uiElementsMutex;//protects uiElements
SDL_mutex * movePathMutex;//protects movePath
SDL_mutex * aStarMutex;//protects movePath
SDL_mutex * selectedNodeMutex;//protects selectedNode
SDL_mutex * backgroundImageMutex;//protects backgroundImageIndex
SDL_mutex * mapMutex;//protects theMap
SDL_mutex * exitMutex;//protects doQuit
SDL_mutex * clickScrollMutex;//protects clickScroll
SDL_mutex * viewportModeMutex;//protects viewportMode
SDL_mutex * chooseNextDelayedMutex;//protects chooseNextDelayed and chooseNextStartTime
SDL_mutex * currentTickMutex;//protects pythonCurrentTick

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
PyObject * pyUnits;
PyObject * pyUnitsIter;
PyObject * pyCities;
PyObject *pyCitiesIter;
PyObject * pyCity;
PyObject * pyId;
int nodesIndex = 0;
MAP theMap;
NODE * theNode;
ANIMATION * currentAnim;
ANIMATION * nextAnim;
listelement * nextAnimListElem;
listelement * modalAnimQueue = NULL;
listelement * animQueue = NULL;
struct unit * theUnits = NULL;//linked list of units
int c;
char damageStr[12] = "2222";
float damageSize;
void drawAnimations(){
  glDepthFunc(GL_ALWAYS);
  nextAnimListElem = animQueue;
  while(nextAnimListElem != NULL){
    nextAnim = nextAnimListElem->item;
    if(SDL_GetTicks()-nextAnim->time > animationTimes[nextAnim->type]){
      animQueue = RemoveItem(animQueue);
    }else{
      break;
    }
    nextAnimListElem = nextAnimListElem->link;
  }
  nextAnimListElem = animQueue;
  while(nextAnimListElem != NULL){
    nextAnim = nextAnimListElem->item;
    if(nextAnim->type == ANIMATION_DAMAGE){
      sprintf(damageStr,"%ld",nextAnim->damage);
      glPushMatrix();
      glTranslatef(nextAnim->unit->xPosDraw,nextAnim->unit->yPosDraw,0.0);
      //  glColor4f(1.0, 0.0, 0.0, (5000.0-(currentTick-damageTime))/1000);
      glColor4f(1.0, 0.0, 0.0, 1.0);
      glColor4f(1.0,0.0,0.0,damageAlphaEasingFunction(SDL_GetTicks()-nextAnim->time,1.0,0.0,animationTimes[ANIMATION_DAMAGE]));
      glTranslatef(0.0,damagePosEasingFunction(SDL_GetTicks()-nextAnim->time,0.0,1.5,2.0*animationTimes[ANIMATION_DAMAGE]),0.0);
      if(SDL_GetTicks()-nextAnim->time < (0.2*animationTimes[ANIMATION_DAMAGE])){
	damageSize = damageSize1EasingFunction(SDL_GetTicks()-nextAnim->time,0.0,0.012,(0.2*animationTimes[ANIMATION_DAMAGE]));
      }else{
	damageSize = 0.012;
	//	damageSize = damageSize1EasingFunction(SDL_GetTicks()-nextAnim->time-(0.25*animationTimes[ANIMATION_DAMAGE]),0.008,0.002,(0.75*animationTimes[ANIMATION_DAMAGE]));
      }
      c = 0;
      while(damageStr[c] != 0){
	glTranslatef(-18.0*damageSize,0.0,0.0);
	c++;
      }
      glScalef(damageSize,damageSize,1.0);
      drawText(damageStr,0,-1,-9999.9,NULL);
      glPopMatrix();
    }
    nextAnimListElem = nextAnimListElem->link;
  }
  //  drawText("55",0,-1,-9999.9,NULL);
  /*      damageStr = PyString_AsString(pyDamage);
      int c = 0;
      glScalef(0.01,0.01,0.0);
      drawText(damageStr,0,-1,-9999.9,NULL);
*/
}
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
long name;
UIELEMENT * uiElements = NULL;
UIELEMENT * tempUIElem;
UIELEMENT * nextElement;
void freeUIElem(UIELEMENT * uiElem){
  free(uiElem->text);
  free(uiElem->textColor);
  free(uiElem->color);
  if(uiElem->mouseOverColor != NULL){
    free(uiElem->mouseOverColor);
  }
}
void loadUIElem(PyObject * pyUIElem,UIELEMENT * uiElem){
    pyXPosition = PyObject_GetAttrString(pyUIElem,"xPosition");
    pyYPosition = PyObject_GetAttrString(pyUIElem,"yPosition");
    pyWidth = PyObject_GetAttrString(pyUIElem,"width");
    pyHeight = PyObject_GetAttrString(pyUIElem,"height");
    pyHidden = PyObject_GetAttrString(pyUIElem,"hidden");
    pyName = PyObject_GetAttrString(pyUIElem,"name");
    pyTextureIndex = PyObject_GetAttrString(pyUIElem,"textureIndex");
    pyCursorIndex = PyObject_GetAttrString(pyUIElem,"cursorIndex");
    pyText = PyObject_GetAttrString(pyUIElem,"text");
    pyTextColor = PyObject_GetAttrString(pyUIElem,"textColor");
    pyTextSize = PyObject_GetAttrString(pyUIElem,"textSize");
    pyColor = PyObject_GetAttrString(pyUIElem,"color");
    pyMouseOverColor = PyObject_GetAttrString(pyUIElem,"mouseOverColor");
    pyTextXPosition = PyObject_GetAttrString(pyUIElem,"textXPos");
    pyTextYPosition = PyObject_GetAttrString(pyUIElem,"textYPos");
    pyCursorPosition = PyObject_GetAttrString(pyUIElem,"cursorPosition");
    pyFontIndex = PyObject_GetAttrString(pyUIElem,"fontIndex");
    //    pyFrameLength = PyObject_GetAttrString(pyUIElem,"frameLength");
    // pyFrameCount = PyObject_GetAttrString(pyUIElem,"frameCount");
    pyIsFocused = PyObject_GetAttrString(pyUIElem,"focused");
    uiElem->xPosition = PyFloat_AsDouble(pyXPosition);
    uiElem->yPosition = PyFloat_AsDouble(pyYPosition);
    
    uiElem->width = PyFloat_AsDouble(pyWidth);
    uiElem->height = PyFloat_AsDouble(pyHeight);
    uiElem->hidden = pyHidden==Py_True;
    uiElem->name = PyLong_AsLong(pyName);
    uiElem->textureIndex = PyLong_AsLong(pyTextureIndex);
    uiElem->cursorIndex = PyLong_AsLong(pyCursorIndex);
    uiElem->textSize = PyFloat_AsDouble(pyTextSize);

    uiElem->text = (char*)malloc(strlen(PyString_AsString(pyText)));
    strcpy(uiElem->text,PyString_AsString(pyText));
    uiElem->textColor = (char*)malloc(strlen(PyString_AsString(pyTextColor)));
    strcpy(uiElem->textColor,PyString_AsString(pyTextColor));
    uiElem->color = (char*)malloc(strlen(PyString_AsString(pyColor)));
    strcpy(uiElem->color,PyString_AsString(pyColor));

    //    uiElem->textColor = PyString_AsString(pyTextColor);
    //    uiElem->color = PyString_AsString(pyColor);

    if(pyMouseOverColor != Py_None){
      uiElem->mouseOverColor = (char*)malloc(strlen(PyString_AsString(pyMouseOverColor)));
      strcpy(uiElem->mouseOverColor,PyString_AsString(pyMouseOverColor));
      //      uiElem->mouseOverColor = PyString_AsString(pyMouseOverColor);
    }else{
      uiElem->mouseOverColor = NULL;
    }
    uiElem->textXPosition = PyFloat_AsDouble(pyTextXPosition);
    uiElem->textYPosition = PyFloat_AsDouble(pyTextYPosition);
    uiElem->cursorPosition = PyFloat_AsDouble(pyCursorPosition);
    uiElem->fontIndex = PyFloat_AsDouble(pyFontIndex);
    uiElem->focused = pyIsFocused==Py_True;
    Py_DECREF(pyXPosition);
    Py_DECREF(pyYPosition);
    Py_DECREF(pyWidth);
    Py_DECREF(pyHeight);
    Py_DECREF(pyHidden);
    Py_DECREF(pyName);
    Py_DECREF(pyTextureIndex);
    Py_DECREF(pyCursorIndex);
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
    //    Py_DECREF(pyFrameLength);
    //    Py_DECREF(pyFrameCount);
    Py_DECREF(pyIsFocused);
}
void updateUIElement(PyObject * pyUIElem){
  pyName = PyObject_GetAttrString(pyUIElem,"name");
  name = PyLong_AsLong(pyName);
  Py_DECREF(pyName);
  nextElement = uiElements->nextElement;
  while(nextElement != NULL){
    if(nextElement->name == name){
      break;
    }
    nextElement = nextElement->nextElement;
  }
  freeUIElem(nextElement);
  loadUIElem(pyUIElem,nextElement);
}
void removeUIElement(PyObject * pyUIElem){
  //  printf("removeUIElement%d\n",1);
  pyName = PyObject_GetAttrString(pyUIElem,"name");
  name = PyLong_AsLong(pyName);
  Py_DECREF(pyName);
  nextElement = uiElements;
  tempUIElem = NULL;
  while(nextElement != NULL){
    if(nextElement->name == name){
      break;
    }
    tempUIElem = nextElement;
    nextElement = nextElement->nextElement;
  }
  if(nextElement == NULL){
    printf("ERROR, TRIED TO REMOVE AN ELEMENT WHICH ISN'T BEING DRAWN!%d!!\n",1);
  }
  if(tempUIElem != NULL){
    tempUIElem->nextElement = nextElement->nextElement;
  }else{
    uiElements = nextElement->nextElement;
  }
  freeUIElem(nextElement);
  free(nextElement);    
}
void addUIElement(PyObject * pyUIElem){
  tempUIElem = (UIELEMENT *)malloc(sizeof(UIELEMENT));
  if(uiElements == NULL){
    uiElements = tempUIElem;
  }else{
    nextElement = uiElements;
    while(nextElement->nextElement != NULL){
      nextElement = nextElement->nextElement;
    }
    nextElement->nextElement = tempUIElem;
  }
  loadUIElem(pyUIElem,tempUIElem);
  tempUIElem->nextElement = NULL;
}
void resetUIElements(){
  nextElement = uiElements;
  while(nextElement != NULL){
    tempUIElem = nextElement->nextElement;
    freeUIElem(nextElement);
    free(nextElement);
    nextElement = tempUIElem;
  }
  uiElements = NULL;
}
void freeUnit(struct unit * daUnit){
  free(daUnit->id);
  free(daUnit);
}
void loadUnit(struct unit * daUnit,PyObject * pyUnit){
  pyUnitType = PyObject_GetAttrString(pyUnit,"unitType");
  pyId = PyObject_GetAttrString(pyUnit,"id");
  pyObj = PyObject_GetAttrString(pyId,"hex");
  daUnit->id = malloc(33*sizeof(char));//TODO: WTF IS THIS 33 FOR???
  strcpy(daUnit->id,PyString_AsString(pyObj));
  //  daUnit->id = PyString_AsString(pyObj);
  Py_DECREF(pyObj);
  Py_DECREF(pyId);
  pyXPosition = PyObject_GetAttrString(pyUnit,"xPos");
  daUnit->xPos = PyFloat_AsDouble(pyXPosition);
  Py_DECREF(pyXPosition);
  pyYPosition = PyObject_GetAttrString(pyUnit,"yPos");
  daUnit->yPos = PyFloat_AsDouble(pyYPosition);
  Py_DECREF(pyYPosition);
  pyObj = PyObject_GetAttrString(pyUnit,"health");
  daUnit->health = PyLong_AsLong(pyObj);
  Py_DECREF(pyObj);
  pyObj = PyObject_GetAttrString(pyUnitType,"health");
  daUnit->maxHealth = PyLong_AsLong(pyObj);
  Py_DECREF(pyObj);
  pyObj = PyObject_GetAttrString(pyUnitType,"textureIndex");
  daUnit->textureIndex = PyLong_AsLong(pyObj);
  Py_DECREF(pyObj);
  Py_DECREF(pyUnitType);
}
UNIT * daUnit;
UNIT * temp;
resetUnits(){
  daUnit = theUnits;
  while(daUnit != NULL){
    temp = daUnit;
    freeUnit(daUnit);
    daUnit = temp->nextUnit;
  }
  theUnits = NULL;
}
void addUnit(PyObject * pyUnit){
  UNIT * daUnit = (UNIT *) malloc(sizeof(UNIT));
  daUnit->nextUnit = theUnits;
  theUnits = daUnit;
  loadUnit(daUnit,pyUnit);
  daUnit->xPosDraw = daUnit->xPos;
  daUnit->yPosDraw = daUnit->yPos;
}
char * unitId;
struct unit * daNextUnit;
struct unit * daPrevUnit;
void removeUnit(PyObject * pyUnit){
  pyId = PyObject_GetAttrString(pyUnit,"id");
  pyObj = PyObject_GetAttrString(pyId,"hex");
  unitId = PyString_AsString(pyObj);
  Py_DECREF(pyObj);
  Py_DECREF(pyId);  
  daPrevUnit = NULL;
  daNextUnit = theUnits;
  while(daNextUnit != NULL){
    if(strcmp(daNextUnit->id,unitId) == 0){
      break;
    }
    daPrevUnit = daNextUnit;
    daNextUnit = daNextUnit->nextUnit;
  }
  if(daPrevUnit != NULL){
    daPrevUnit->nextUnit = daNextUnit->nextUnit;
    freeUnit(daNextUnit);
  }else{
    theUnits = daNextUnit->nextUnit;
    freeUnit(daNextUnit);    
  }
}
double unitHealthPrev;
void updateUnit(PyObject * pyUnit){
  pyId = PyObject_GetAttrString(pyUnit,"id");
  pyObj = PyObject_GetAttrString(pyId,"hex");
  unitId = PyString_AsString(pyObj);
  Py_DECREF(pyObj);
  Py_DECREF(pyId);  
  daNextUnit = theUnits;
  while(daNextUnit != NULL){
    if(strcmp(daNextUnit->id,unitId) == 0){
      unitHealthPrev = daNextUnit->health;
      loadUnit(daNextUnit,pyUnit);
      break;
    }
    daNextUnit = daNextUnit->nextUnit;
  }
  if(daNextUnit->xPos != daNextUnit->xPosDraw){//unit moved
    ANIMATION * theAnim = malloc(sizeof(ANIMATION));
    theAnim->type = ANIMATION_UNIT_SLIDE;
    theAnim->unit = daNextUnit;
    theAnim->xPos = daNextUnit->xPosDraw;
    theAnim->yPos = daNextUnit->yPosDraw;
    SDL_mutexP(modalAnimationsMutex);
    modalAnimQueue = AddItem(modalAnimQueue,theAnim);
    SDL_mutexV(modalAnimationsMutex);
  }
  if(unitHealthPrev != daNextUnit->health){
    ANIMATION * theAnim = malloc(sizeof(ANIMATION));
    theAnim->type = ANIMATION_DAMAGE;
    theAnim->time = pythonCurrentTick;
    theAnim->unit = daNextUnit;
    theAnim->damage = unitHealthPrev - daNextUnit->health;
    animQueue = AddItem(animQueue,theAnim);
  }
}
void loadNode(NODE * theNode, PyObject * pyNode){
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
}

long nodeName;
void updateNode(PyObject * pyNode){
  pyNodeName = PyObject_GetAttrString(pyNode,"name");
  nodeName = PyLong_AsLong(pyNodeName);
  Py_DECREF(pyNodeName);
  for(nodesIndex = 0;nodesIndex < theMap.size;nodesIndex++){
    theNode = (&(theMap.nodes[nodesIndex]));
    if(theNode->name == nodeName){
      break;
    }
  }
  loadNode(theNode,pyNode);
}
CITYNODELISTELEM * theCities = NULL;
void addCity(NODE * theNode){
  CITYNODELISTELEM * theCityElem = malloc(sizeof(ANIMATION));
  theCityElem->nextCity = theCities;
  theCityElem->node = theNode;
  theCities = theCityElem;
}
void freeCities(){
  CITYNODELISTELEM * theCityElem = NULL;
  CITYNODELISTELEM * theNextCityElem = theCities;
  while(theNextCityElem != NULL){
    theCityElem = theNextCityElem;
    theNextCityElem = theCityElem->nextCity;
    free(theCityElem);
  }
  theCities = NULL;  
}
void freeMap(){
  freeCities();  
  if(theMap.nodes != NULL){
    free(theMap.nodes);
  }  
}
float mapRightOffset;
float mapTopOffset;
void loadMap(){
  freeMap();
  mapIterator = PyObject_CallMethod(pyMap,"getIterator",NULL);  
  pyPolarity = PyObject_GetAttrString(pyMap,"polarity");
  mapPolarity = PyLong_AsLong(pyPolarity);
  Py_DECREF(pyPolarity);
  rowIterator = PyObject_GetIter(mapIterator);
  pyMapWidth = PyObject_CallMethod(pyMap,"getWidth",NULL);//New reference
  theMap.width = PyLong_AsLong(pyMapWidth);
  Py_DECREF(pyMapWidth);
  pyMapHeight = PyObject_CallMethod(pyMap,"getHeight",NULL);//New reference
  theMap.height = PyLong_AsLong(pyMapHeight);
  Py_DECREF(pyMapHeight);
  theMap.size = theMap.width*theMap.height;
  theMap.nodes = malloc(theMap.size*sizeof(NODE));
  nodesIndex = 0;
  rowNumber = -1;
  while (row = PyIter_Next(rowIterator)) {
    colNumber = 0;
    rowNumber = rowNumber + 1;
    nodeIterator = PyObject_GetIter(row);
    while(pyNode = PyIter_Next(nodeIterator)) {
      theNode = (&(theMap.nodes[nodesIndex]));
      theNode->xIndex = colNumber;
      theNode->yIndex = rowNumber;
      xPosition = translateTilesXToPositionX(colNumber,rowNumber);
      yPosition = translateTilesYToPositionY(rowNumber);
      theNode->xPos = xPosition;
      theNode->yPos = yPosition;
      loadNode(theNode,pyNode);
      theNode->hash = 0;
      theNode->hash += (((4294967296*(2654435761)*theNode->xIndex)+81)%43261);
      theNode->hash += (((4294967296*(2654435761)*theNode->yIndex)+30)%131071);
      theNode->hash = theNode->hash%4;
      pyCity = PyObject_GetAttrString(pyNode,"city");
      if(pyCity != Py_None && pyCity != NULL){
	addCity(theNode);
      }
      nodesIndex++;
      colNumber = colNumber - 1;
    }
    Py_DECREF(row);
    Py_DECREF(nodeIterator);
  }
  Py_DECREF(rowIterator); 
  Py_DECREF(mapIterator);
  mapRightOffset = translateTilesXToPositionX(theMap.width+1,0);
  mapTopOffset = translateTilesYToPositionY(theMap.height);
}
MOVEPATHNODE * movePath = NULL;
MOVEPATHNODE * aStarPath = NULL;
MOVEPATHNODE * tempPathNode;
addMovePathNode(PyObject * pyNode, MOVEPATHNODE ** path){
  pyXPosition = PyObject_GetAttrString(pyNode,"xPos");
  colNumber = 0-PyLong_AsLong(pyXPosition);
  Py_DECREF(pyXPosition);
  pyYPosition = PyObject_GetAttrString(pyNode,"yPos");
  rowNumber = PyLong_AsLong(pyYPosition);
  Py_DECREF(pyYPosition);
  MOVEPATHNODE * movePathNode = (MOVEPATHNODE *)malloc(sizeof(MOVEPATHNODE));
  movePathNode->xPos = translateTilesXToPositionX(colNumber,rowNumber);
  movePathNode->yPos = translateTilesYToPositionY(rowNumber);
  movePathNode->nextNode = *(path);
  *(path) = movePathNode;
}
MOVEPATHNODE * nextMovePathNode;
freeMovePath(MOVEPATHNODE ** path){
  nextMovePathNode = *(path);
  while(nextMovePathNode != NULL){
    tempPathNode = nextMovePathNode;
    nextMovePathNode = nextMovePathNode->nextNode;
    free(tempPathNode);
  }
  *(path) = NULL;
}
PyObject * pyMovePath;
loadMovePath(PyObject * pyPath,MOVEPATHNODE ** path){
  freeMovePath(path);
  nodeIterator = PyObject_CallMethod(pyPath,"__iter__",NULL);
  while(pyNode = PyIter_Next(nodeIterator)){
    addMovePathNode(pyNode,path);
  }
}
SELECTEDNODE * selectedNode = NULL;
setSelectedNode(){
  SDL_mutexP(selectedNodeMutex);
  if(selectedNode != NULL){
    free(selectedNode);
  }
  selectedNode = (SELECTEDNODE *)malloc(sizeof(SELECTEDNODE));
  pyNode = PyObject_GetAttrString(gameMode,"selectedNode");
  if(pyNode != NULL && pyNode != Py_None){
    pyXPosition = PyObject_GetAttrString(pyNode,"xPos");
    colNumber = 0-PyLong_AsLong(pyXPosition);
    pyYPosition = PyObject_GetAttrString(pyNode,"yPos");
    rowNumber = PyLong_AsLong(pyYPosition);
    selectedNode->xPos = translateTilesXToPositionX(colNumber,rowNumber);
    selectedNode->yPos = translateTilesYToPositionY(rowNumber);
  }
  SDL_mutexV(selectedNodeMutex);
}
PyObject * pyBackgroundImageIndex;
int backgroundImageIndex = -1;
setBackgroundImage(){
  SDL_mutexP(backgroundImageMutex);
  if(PyObject_HasAttrString(gameMode,"backgroundImageIndex")){
    pyBackgroundImageIndex = PyObject_GetAttrString(gameMode, "backgroundImageIndex");//New reference
    backgroundImageIndex = PyLong_AsLong(pyBackgroundImageIndex);
    Py_DECREF(pyBackgroundImageIndex);
  }else{
    backgroundImageIndex = -1;    
  }
  SDL_mutexV(backgroundImageMutex);
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
	//	PYTHONCALLBACK * callback = (PYTHONCALLBACK *)malloc(sizeof(PYTHONCALLBACK));
	//	callback->id = 	EVENT_SET_CURSOR_POSITION;
	//	callback->nameValue = nameValue;
	//	queueCallback(callback);
	//	pyObj = PyObject_CallMethod(gameMode,"setMouseTextPosition","i",nameValue);
	//	Py_DECREF(pyObj);
	mouseTextPositionSet = 1;
      }
    }
    bufferPtr = bufferPtr + 3 + numberOfNames;
    count = count + 1;
  }  
  if(!mouseTextPositionSet){
    //  pyObj = PyObject_CallMethod(gameMode,"setMouseTextPosition","i",-1);
    //    if(pyObj != NULL){
    //      Py_DECREF(pyObj);
    //    }
  }
}

//float glMouseCoords[3];
//void convertWindowCoordsToViewportCoords(int x, int y){
GLint viewport[4];
GLdouble modelview[16];
GLdouble projection[16];
GLfloat winX, winY, winZ, winZOld;
void convertWindowCoordsToViewportCoords(int x, int y, float z, GLdouble* posX, GLdouble* posY, GLdouble* posZ){
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
  /*  glBindTexture(GL_TEXTURE_2D, texturesArray[FIRE_INDEX]);
  glCallList(unitList);
  double fireVitality;
  char fireVit[20];
  //  PyObject * pyFireVitality = PyObject_GetAttrString(pyFire,"vitality");
  fireVitality = PyFloat_AsDouble(pyFireVitality);
  glColor3f(1.0,1.0,1.0);
  glPushMatrix();
  glTranslatef(-0.8,0.0,0.0);
  glScalef(0.01,0.01,0.0);
  sprintf(fireVit,"%f",fireVitality);
  drawText(fireVit,0,-1,-9999.9,NULL);
  glPopMatrix();
  */
}
PyObject * pyXPositionUnit;
PyObject * pyYPositionUnit;
//PyObject * pyIsSelected;
double xPositionUnit;
double yPositionUnit;
//long isSelected;
PyObject * pyUnit;
void drawUnit(UNIT * daUnit){
  //  glTranslatef(xPositionUnit,yPositionUnit,0.0);
  glTranslatef(daUnit->xPosDraw,daUnit->yPosDraw,0.0);
  healthBarLength = 0.7*(float)daUnit->health/(float)daUnit->maxHealth;
  glBindTexture(GL_TEXTURE_2D, texturesArray[HEALTH_BAR_INDEX]);
  glColor3f(1.0, 1.0, 1.0);
  glCallList(healthBarList);
  glColor3f(1.0, 0.0, 0.0);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-.35, 0.9, 0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(-.35+healthBarLength, 0.9, 0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(-.35+healthBarLength, 0.8, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-.35, 0.8, 0.0);
  glEnd();

  glPushMatrix();
  //  if(isNextUnit){
  if(0){
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
  glBindTexture(GL_TEXTURE_2D, texturesArray[daUnit->textureIndex]);
  //  glTranslatef(0.0,0.0,0.0);
  glCallList(unitList);
  
}
float shading;
char playerStartVal[2];
void drawTile(NODE * theNode){
  textureVertices = vertexArrays[theNode->tileValue];
  shading = 1.0;
  if(!theNode->visible){
    shading = shading - 0.3;
  }
  if(theNode->name == selectedName){// && !clickScroll){
    shading = shading - 0.3;
    //    if(cursorIndex >= 0){
    //      theCursorIndex = (int)cursorIndex;
    //    }
  }
  glColor3f(shading,shading,shading);
  glPushName(theNode->name);
  glCallList(tilesLists+(4*theNode->tileValue)+theNode->hash);
  glPopName();

  //  glColor3f(0.0,1.0,0.0);
  //  if(roadValue == 1){
  //    glCallList(tilesLists+(4*ROAD_TILE_INDEX));
  //  }

  if(theNode->playerStartValue >= 1){
    textureVertices = vertexArrays[PLAYER_START_TILE_INDEX];
    glCallList(tilesLists+(4*PLAYER_START_TILE_INDEX));
    sprintf(playerStartVal,"%d",theNode->playerStartValue);

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
MOVEPATHNODE * nextMovePathNoed;
void drawMovePath(MOVEPATHNODE ** path){
  nextMovePathNoed = *(path);
  while(nextMovePathNoed != NULL){
    glPushMatrix();
    glTranslatef(nextMovePathNoed->xPos,nextMovePathNoed->yPos,0.0);
    glBindTexture(GL_TEXTURE_2D, texturesArray[WALK_ICON_INDEX]);
    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(0.5,-0.5,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(-0.5,-0.5,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(-0.5,0.5,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(0.5,0.5,0.0);
    glEnd();
    glPopMatrix();
    nextMovePathNoed = nextMovePathNoed->nextNode;
  }
}
void drawSelectionBox(){
  SDL_mutexP(selectedNodeMutex);
  if(selectedNode != NULL){
    glColor3f(1.0,1.0,1.0);
    glBindTexture(GL_TEXTURE_2D, texturesArray[SELECTION_BOX_INDEX]);
    glPushMatrix();
    glTranslatef(selectedNode->xPos,selectedNode->yPos,0.0);
    //  glScalef(selectionBoxScale+1.0,selectionBoxScale+1.0,0.0);
    glCallList(selectionBoxList);
    glPopMatrix();
  }
  SDL_mutexV(selectedNodeMutex);
}
CITYNODELISTELEM * nextCity;
void drawCities(){
  glColor4f(1.0,1.0,1.0,1.0);
  nextCity = theCities;
  while(nextCity != NULL){
    glPushMatrix();
    glTranslatef(nextCity->node->xPos,nextCity->node->yPos,0.0);
    glBindTexture(GL_TEXTURE_2D, texturesArray[CITY_INDEX]);
    glCallList(unitList);
    glPopMatrix();
    nextCity = nextCity->nextCity;
  }
}
void drawUnits(){
  //  glDepthFunc(GL_LEQUAL);
  daNextUnit = theUnits;
  while(daNextUnit != NULL){
    glPushMatrix();
    drawUnit(daNextUnit);
    glPopMatrix();
    
    daNextUnit = daNextUnit->nextUnit;
  }
}						
int nodesIndex;
NODE * daNode;
void drawTiles(){  
  SDL_mutexP(mapMutex);
  if(theMap.nodes != NULL){
    for(nodesIndex = 0;nodesIndex < theMap.size;nodesIndex++){
      daNode = &(theMap.nodes[nodesIndex]);
      glPushMatrix();
      glTranslatef(daNode->xPos,daNode->yPos,0.0);
      drawTile(daNode);
      glPopMatrix();
    }
  }
  SDL_mutexV(mapMutex);
}
char viewportMode = FULL_SCREEN_MODE;
void doViewport(){
  SDL_mutexP(viewportModeMutex);
  if(viewportMode == JOIN_GAME_ROOM_MODE){
    glViewport(60.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,258.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT,991.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,824.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT);
  }else if(viewportMode == CREATE_GAME_ROOM_MODE){
    glViewport(544.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,258.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT,991.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,824.0*SCREEN_HEIGHT/SCREEN_BASE_HEIGHT);
  }else{
    glViewport(0,0,SCREEN_WIDTH,SCREEN_HEIGHT);
  }
  SDL_mutexV(viewportModeMutex);
}
PyObject * pyTranslateZ;
int frameNumber = 0;
void calculateTranslation(){
  frameNumber++;
  glPushMatrix();
  SDL_mutexP(mapMutex);
  if(theMap.nodes != NULL){
    if(translateX - mapRightOffset < convertedTopRightX
       && translateX - (2.0*SIN60) > convertedBottomLeftX
       && translateY < convertedTopRightY - mapTopOffset
       && translateY > convertedBottomLeftY+2.0
       && (translateZ < translateZPrev)){
      translateZ = translateZPrev;
      if(translateZ > maxTranslateZ){
	maxTranslateZ = translateZ;
      }
    }
    if(translateZ < 1.0 - maxZoom){
      translateZ = 1.0 - maxZoom;
    }
    if(translateZ < maxTranslateZ){
      translateZ = maxTranslateZ;
    }
    if(translateZ > - 1.0 - minZoom){
      translateZ = - 1.0 - minZoom;
    }
  }
  SDL_mutexV(mapMutex);
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
    SDL_mutexP(viewportModeMutex);
    if(viewportMode == JOIN_GAME_ROOM_MODE){
      glReadPixels(7*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1);
      glReadPixels(8*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2);
      glReadPixels(9*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3);
    }else if(viewportMode == CREATE_GAME_ROOM_MODE){
      glReadPixels(13*SCREEN_WIDTH/16, 7*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1);
      glReadPixels(13*SCREEN_WIDTH/16, 8*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2);
      glReadPixels(13*SCREEN_WIDTH/16, 9*SCREEN_HEIGHT/16, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3);
    }else{
      glReadPixels( 7*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1);
      glReadPixels( 8*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2);
      glReadPixels( 9*SCREEN_WIDTH/16, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3);
    }
    SDL_mutexV(viewportModeMutex);
    translateZPrev2 = translateZ;
  }
  if(mapDepthTest1 == mapDepthTest2 || mapDepthTest1 == mapDepthTest3){
    mapDepth = mapDepthTest1;
  }else if(mapDepthTest2 == mapDepthTest3){
    mapDepth = mapDepthTest2;
  }else{
    printf("mapdepth not found%d\n",1);
  }
  SDL_mutexP(viewportModeMutex);
  if(viewportMode == JOIN_GAME_ROOM_MODE){
    convertWindowCoordsToViewportCoords(60.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(1551.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }else if(viewportMode == CREATE_GAME_ROOM_MODE){
    convertWindowCoordsToViewportCoords(100.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(1535.5*SCREEN_WIDTH/SCREEN_BASE_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }else{
    convertWindowCoordsToViewportCoords(390.0*SCREEN_WIDTH/SCREEN_BASE_WIDTH,SCREEN_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
    convertWindowCoordsToViewportCoords(SCREEN_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  }
  SDL_mutexV(viewportModeMutex);
  mouseMapPosXPrevious = mouseMapPosX;
  mouseMapPosYPrevious = mouseMapPosY;
  convertWindowCoordsToViewportCoords(mouseX,mouseY,translateZ,&mouseMapPosX,&mouseMapPosY,&mouseMapPosZ);  
  if(translateZ > translateZPrev){
    translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
    translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
  }
  translateZPrev = translateZ;
  //  convertWindowCoordsToViewportCoords(mouseX,mouseY,translateZ,&mouseMapPosXNew,&mouseMapPosYNew,&mouseMapPosZNew);
  //printf("screen topright %f,%f\n",convertedTopRightX,convertedTopRightY);
  //printf("screen bottomleft %f,%f\n",convertedBottomLeftX,convertedBottomLeftY);
  //printf("translate %f,%f,%f\n",translateX,translateY,translateZ);
  //printf("offsets: %f %f\n",mapRightOffset,mapTopOffset);
  //printf("%f\n",translateTilesYToPositionY(mapHeight));//setting translateY to this number will focus on it
  //printf("mouse %d:%f\t%d:%f\n",mouseX,mouseMapPosX,mouseY,mouseMapPosY);
  SDL_mutexP(clickScrollMutex);
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
  SDL_mutexV(clickScrollMutex);
  if(isSliding){
    if(SDL_GetTicks()-slidingTicks < SLIDE_UNIT_TIME){
      currentAnim->unit->xPosDraw = slidingEasingFunction(SDL_GetTicks()-slidingTicks, currentAnim->xPos,currentAnim->unit->xPos,SLIDE_UNIT_TIME);
      currentAnim->unit->yPosDraw = slidingEasingFunction(SDL_GetTicks()-slidingTicks, currentAnim->yPos,currentAnim->unit->yPos,SLIDE_UNIT_TIME);
    }else{
      currentAnim->unit->xPosDraw = currentAnim->unit->xPos;
      currentAnim->unit->yPosDraw = currentAnim->unit->yPos;
      isSliding = 0;
    }
  }
  if(isFocusing){
    if((considerDoneFocusing > 0) && abs(50.0*(translateXPrev - translateX)) == 0.0 && abs(50.0*(translateYPrev - translateY)) == 0.0){//this indicates the auto-scrolling code is not allowing us to move any more
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
    //these lines roughly make focusspeed consistent rather than faster on diagonals
    if(focusSpeedX > 0.5*focusSpeed || focusSpeedY > 0.5*focusSpeed){
      focusSpeedX = focusSpeedX*focusSpeed/(focusSpeedX + focusSpeedY);
      focusSpeedY = focusSpeedY*focusSpeed/(focusSpeedX + focusSpeedY);
    }
    
    /*      if(translateX < -focusXPos){
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
	}*/
    if(SDL_GetTicks()-focusTicks < focusTime){
      translateX = focusEasingFunction(SDL_GetTicks()-focusTicks,focusXPosPrev,-focusXPos,focusTime);
      translateY = focusEasingFunction(SDL_GetTicks()-focusTicks,focusYPosPrev,-focusYPos,focusTime);
    }else{
      translateX = -focusXPos;
      translateY = -focusYPos;
    }
  }


  //The following code will adjust translateX/Y so that no off-map area is shown
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
}

void drawBoard(){
  glDepthFunc(GL_LEQUAL);
  glClear(GL_DEPTH_BUFFER_BIT);		 
  SDL_mutexP(mapMutex);
  if(theMap.nodes != NULL){
    drawTiles();
    SDL_mutexP(movePathMutex);
    drawMovePath(&(movePath));
    SDL_mutexV(movePathMutex);
    SDL_mutexP(aStarMutex);
    drawMovePath(&(aStarPath));
    SDL_mutexV(aStarMutex);
    drawSelectionBox();
    drawUnits();
    drawCities();
    drawAnimations();
  }
  SDL_mutexV(mapMutex);
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
//double xPosition;
//double yPosition;
double width;
double height;
int hidden;
long textureIndex;
long cursorIndex;
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
void drawUIElement(UIELEMENT * uiElement){
  if(!uiElement->hidden){
    if(uiElement->textureIndex > -1){
      glBindTexture(GL_TEXTURE_2D, texturesArray[uiElement->textureIndex]);
      if(selectedName == uiElement->name && uiElement->mouseOverColor != NULL){
	sscanf(uiElement->mouseOverColor,"%X %X %X",red,green,blue);
      }else{
	sscanf(uiElement->color,"%X %X %X",red,green,blue);
      } 
      glColor3f(*red/255.0, *green/255.0, *blue/255.0);
      glPushName(uiElement->name);
      glBegin(GL_QUADS);
      glTexCoord2f(0.0,1.0); glVertex3f(uiElement->xPosition,uiElement->yPosition,0.0);
      glTexCoord2f(1.0,1.0); glVertex3f(uiElement->xPosition+uiElement->width,uiElement->yPosition,0.0);
      glTexCoord2f(1.0,0.0); glVertex3f(uiElement->xPosition+uiElement->width,uiElement->yPosition-uiElement->height,0.0);
      glTexCoord2f(0.0,0.0); glVertex3f(uiElement->xPosition,uiElement->yPosition-uiElement->height,0.0);
      glEnd();
      glPopName();
    }
    if((uiElement->text) != NULL){
      sscanf(uiElement->textColor,"%X %X %X",red,green,blue);
      glColor3f(*red/255.0, *green/255.0, *blue/255.0);
      glPushMatrix();
      glLoadIdentity();
      glTranslatef(uiElement->xPosition+(uiElement->textXPosition),uiElement->yPosition+(uiElement->textYPosition),0.0);
      glScalef(uiElement->textSize,uiElement->textSize,0.0);
      //glTranslatef(0.0,0.0,-10.0);
      glPushName(uiElement->name);
      if(uiElement->focused){
	drawText(uiElement->text,uiElement->fontIndex,uiElement->cursorPosition,uiElement->xPosition+uiElement->width,NULL);
      }else{
	drawText(uiElement->text,uiElement->fontIndex,-1,uiElement->xPosition+uiElement->width,NULL);
      }
      glPopName();
      glPopMatrix();
    }
  }
}
float xPos;
float yPos;
float pointerWidth;
float pointerHeight;
char frameRate[20];
UIELEMENT * nextUIElement;
void drawUI(){
  glDepthFunc(GL_ALWAYS);
  SDL_mutexP(uiElementsMutex);
  nextUIElement = uiElements;
  theCursorIndex = -1;
  while(nextUIElement != NULL){
    drawUIElement(nextUIElement);
    if(nextUIElement->name == selectedName){
      theCursorIndex = nextUIElement->cursorIndex;
    }
    nextUIElement = nextUIElement->nextElement;
  }
  SDL_mutexV(uiElementsMutex);
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
  //glAlphaFunc(GL_GREATER,0.1);//clear area around the fonts will not write to the z-buffer
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

SDL_Event event;
PyObject * pyFocusNextUnit;
char keyArray[20];
//PyObject * pyClickScroll;
PYTHONCALLBACK * firstCallback = NULL;
PYTHONCALLBACK * lastCallback = NULL;//put new callbacks here
void queueCallback(PYTHONCALLBACK * callback){
  SDL_mutexP(pythonCallbackMutex);
  callback->nextCallback = NULL;
  if(lastCallback != NULL){
    lastCallback->nextCallback = callback;
  }
  lastCallback = callback;
  if(firstCallback == NULL){
    firstCallback = callback;
  }
  SDL_mutexV(pythonCallbackMutex);
}
static void dispatch(PYTHONCALLBACK * callback){
  if(callback->id == EVENT_MOUSE_OVER){
    if(PyObject_HasAttrString(gameMode,"handleMouseOver")){
      pyObj = PyObject_CallMethod(gameMode,"handleMouseOver","(ii)",callback->selectedName,callback->leftButtonDown);
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_LEFT_CLICK_DOWN){
    if(PyObject_HasAttrString(gameMode,"handleLeftClickDown")){
      pyObj = PyObject_CallMethod(gameMode,"handleLeftClickDown","i",callback->selectedName);//New reference
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_MOUSE_MOVE){
    if(PyObject_HasAttrString(gameMode,"handleMouseMovement")){
      pyObj = PyObject_CallMethod(gameMode,"handleMouseMovement","(iii)",callback->selectedName,callback->mouseX,callback->mouseY);
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_SCROLL_UP){
    if(PyObject_HasAttrString(gameMode,"handleScrollUp")){
      pyObj = PyObject_CallMethod(gameMode,"handleScrollUp","i",callback->selectedName);//New reference
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_SCROLL_DOWN){
    if(PyObject_HasAttrString(gameMode,"handleScrollDown")){
      pyObj = PyObject_CallMethod(gameMode,"handleScrollDown","i",callback->selectedName);//New reference
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_RIGHT_CLICK_DOWN){
    pyObj = PyObject_CallMethod(gameMode,"handleRightClick","i",callback->selectedName);//New reference
    printPyStackTrace();
    if(pyObj != NULL){
      Py_DECREF(pyObj);
    }
  }else if(callback->id == EVENT_LEFT_CLICK_UP){
    if(PyObject_HasAttrString(gameMode,"handleLeftClickUp")){
      pyObj = PyObject_CallMethod(gameMode,"handleLeftClickUp","i",callback->selectedName);//New reference
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_RIGHT_CLICK_UP){
    if(PyObject_HasAttrString(gameMode,"handleRightClickUp")){
      pyObj = PyObject_CallMethod(gameMode,"handleRightClickUp","i",callback->selectedName);//New reference
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_KEY_DOWN){
    if(PyObject_HasAttrString(gameMode,"handleKeyDown")){	
      pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",callback->keyArray); 
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_KEY_UP){
    if(PyObject_HasAttrString(gameMode,"handleKeyUp")){
      pyObj = PyObject_CallMethod(gameMode,"handleKeyUp","s",callback->keyArray);
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
  }else if(callback->id == EVENT_ON_DRAW){
    if(PyObject_HasAttrString(gameMode,"onDraw")){
      pyObj = PyObject_CallMethod(gameMode,"onDraw","(ii)",callback->deltaTicks,callback->isAnimating);//New reference
      printPyStackTrace();
      if(pyObj != NULL){
	Py_DECREF(pyObj);
      }
    }
    //  }else if(callback->id == EVENT_ON_QUIT){
  }else if(callback->id == EVENT_CHOOSE_NEXT_DELAYED){
    pyObj = PyObject_CallMethod(gameMode,"sendChooseNextUnit",NULL);//New reference
    printPyStackTrace();
    if(pyObj != NULL){
      Py_DECREF(pyObj);
    }
  }
}
PYTHONCALLBACK * dispatchCallback;
static void dispatchPythonCallbacks(){
  SDL_mutexP(pythonCallbackMutex);
  while(firstCallback != NULL){
    dispatchCallback = firstCallback;
    firstCallback = dispatchCallback->nextCallback;
    if(firstCallback == NULL){
      lastCallback = NULL;
    }
    dispatch(dispatchCallback);
    free(dispatchCallback);
    //#define EVENT_LEFT_CLICK_UP
  }
  SDL_mutexV(pythonCallbackMutex);
}
static void queueSimpleCallback(int id){
  PYTHONCALLBACK * callback = (PYTHONCALLBACK *)malloc(sizeof(PYTHONCALLBACK));
  callback->id = id;
  callback->selectedName = selectedName;
  queueCallback(callback);
}

static void handleInput(){
  if(previousMousedoverName != selectedName){
    PYTHONCALLBACK * callback = (PYTHONCALLBACK *)malloc(sizeof(PYTHONCALLBACK));
    callback->id = EVENT_MOUSE_OVER;
    callback->selectedName = selectedName;
    callback->leftButtonDown = leftButtonDown;
    queueCallback(callback);
    previousMousedoverName = selectedName;
  }

  //SDL_Delay(20);//for framerate testing...

  if(keyHeld){
    if(repeatKey){
      if(SDL_GetTicks() - keyHeldTime > 40){
	keyHeldTime = SDL_GetTicks();
	//	if(PyObject_HasAttrString(gameMode,"handleKeyDown")){
	  //	  pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",keyArray);
	//	  Py_DECREF(pyObj);
	//	}
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
      PYTHONCALLBACK * callback = (PYTHONCALLBACK *)malloc(sizeof(PYTHONCALLBACK));
      callback->id = EVENT_MOUSE_MOVE;
      callback->selectedName = selectedName;
      callback->mouseX = mouseX;
      callback->mouseY = mouseY;
      queueCallback(callback);
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
	translateZ = translateZ + ZOOM_SPEED*deltaTicks;
	queueSimpleCallback(EVENT_SCROLL_UP);
      }else if(event.button.button == SDL_BUTTON_WHEELDOWN){
	translateZ = translateZ - ZOOM_SPEED*deltaTicks;
	queueSimpleCallback(EVENT_SCROLL_DOWN);
      }
      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 1;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	leftButtonDown = 1;
	queueSimpleCallback(EVENT_LEFT_CLICK_DOWN);
	previousClickedName = selectedName;
      }
      printPyStackTrace();
      if(event.button.button == SDL_BUTTON_RIGHT){
	//	clickScroll = 1;
	queueSimpleCallback(EVENT_RIGHT_CLICK_DOWN);
      }
      break;
    case SDL_MOUSEBUTTONUP:
      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 0;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	queueSimpleCallback(EVENT_LEFT_CLICK_UP);
	leftButtonDown = 0;
      }
      if(event.button.button == SDL_BUTTON_RIGHT){
	SDL_mutexP(clickScrollMutex);
	clickScroll = 0;
	SDL_mutexV(clickScrollMutex);
	queueSimpleCallback(EVENT_RIGHT_CLICK_UP);
      }
      break;
    case SDL_KEYDOWN:
      /*      if(event.key.keysym.sym == SDLK_ESCAPE){
	doQuit = 1;	
	
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
	PYTHONCALLBACK * callback = (PYTHONCALLBACK *)malloc(sizeof(PYTHONCALLBACK));
	callback->id = EVENT_KEY_DOWN;
	callback->selectedName = selectedName;
	sprintf(callback->keyArray,"%s",keyArray);
	queueCallback(callback);
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
	PYTHONCALLBACK * callback = (PYTHONCALLBACK *)malloc(sizeof(PYTHONCALLBACK));
	callback->id = EVENT_KEY_UP;
	callback->selectedName = selectedName;
	sprintf(callback->keyArray,"%s",SDL_GetKeyName(event.key.keysym.sym));
	queueCallback(callback);	
      }
      break;
    case SDL_QUIT://when user x's the window
      SDL_mutexP(exitMutex);
      doQuit = 1;
      SDL_mutexV(exitMutex);
      break;
    default:
      break;
    }
  }
}
void drawBackground(){
  SDL_mutexP(backgroundImageMutex);
  if(backgroundImageIndex >= 0){
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glBindTexture(GL_TEXTURE_2D, texturesArray[backgroundImageIndex]);
    glColor3f(1.0,1.0,1.0);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(1.0,-1.0,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(1.0,1.0,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(-1.0,1.0,0.0);
    glEnd();
  }
  SDL_mutexV(backgroundImageMutex);
}
GLint viewport[4];
GLint hitsCnt;
PyObject * pyChooseNextDelayed;
int chooseNextDelayed;
Uint32 chooseNextTimeStart;
PyObject * pyAnim;
ANIMATION * theAnim;
PyObject * pyUpdatesQueue;
PyObject * pyUpdatesQueueEmpty;
PyObject * pyUpdate;
PyObject * pyUIElement;
PyObject * pyMode;
long updateType;
int doResetUI = 0;

static void getPythonUpdates(){
  pyUpdatesQueue = PyObject_GetAttrString(gameState,"rendererUpdateQueue");
  pyUpdatesQueueEmpty = PyObject_CallMethod(pyUpdatesQueue,"empty",NULL);
  while(pyUpdatesQueueEmpty == Py_False){
    Py_DECREF(pyUpdatesQueueEmpty);
    pyUpdate = PyObject_CallMethod(pyUpdatesQueue,"get",NULL);
    pyObj = PyObject_GetAttrString(pyUpdate,"type");
    updateType = PyLong_AsLong(pyObj);
    Py_DECREF(pyObj);    
    if(updateType == RENDERER_CHANGE_UNIT_ADD){
      pyUnit = PyObject_GetAttrString(pyUpdate,"unit");
      SDL_mutexP(unitsMutex);
      addUnit(pyUnit);
      SDL_mutexV(unitsMutex);
      Py_DECREF(pyUnit);
    }else if(updateType == RENDERER_CHANGE_UNIT_REMOVE){
      pyUnit = PyObject_GetAttrString(pyUpdate,"unit");
      SDL_mutexP(unitsMutex);
      removeUnit(pyUnit);
      SDL_mutexV(unitsMutex);
      Py_DECREF(pyUnit);
    }else if(updateType == RENDERER_CHANGE_UNIT_CHANGE){
      pyUnit = PyObject_GetAttrString(pyUpdate,"unit");
      SDL_mutexP(unitsMutex);
      updateUnit(pyUnit);
      SDL_mutexV(unitsMutex);
      Py_DECREF(pyUnit);     
    }else if(updateType == RENDERER_RESET_UNITS){
      SDL_mutexP(unitsMutex);
      resetUnits();
      SDL_mutexV(unitsMutex);
    }else if(updateType == RENDERER_CHANGE_NODE_CHANGE){
      pyNode = PyObject_GetAttrString(pyUpdate,"node");
      SDL_mutexP(mapMutex);
      updateNode(pyNode);
      SDL_mutexV(mapMutex);
      Py_DECREF(pyNode);
    }else if(updateType == RENDERER_FOCUS){
      ANIMATION * theAnim = malloc(sizeof(ANIMATION));
      theAnim->type = ANIMATION_AUTO_FOCUS;
      pyXPosition = PyObject_GetAttrString(pyUpdate,"xPos");
      theAnim->xPos = PyFloat_AsDouble(pyXPosition);
      Py_DECREF(pyXPosition);
      pyYPosition = PyObject_GetAttrString(pyUpdate,"yPos");
      theAnim->yPos = PyFloat_AsDouble(pyYPosition);
      Py_DECREF(pyYPosition);      
      SDL_mutexP(modalAnimationsMutex);
      modalAnimQueue = AddItem(modalAnimQueue,theAnim);
      SDL_mutexV(modalAnimationsMutex);
    }else if(updateType == RENDERER_RESET_UI){
      SDL_mutexP(uiElementsMutex);
      resetUIElements();
      SDL_mutexV(uiElementsMutex);
    }else if(updateType == RENDERER_ADD_UIELEM){
      pyUIElement = PyObject_GetAttrString(pyUpdate,"uiElement");
      SDL_mutexP(uiElementsMutex);
      addUIElement(pyUIElement);
      SDL_mutexV(uiElementsMutex);
    }else if(updateType == RENDERER_REMOVE_UIELEM){
      pyUIElement = PyObject_GetAttrString(pyUpdate,"uiElement");
      SDL_mutexP(uiElementsMutex);
      removeUIElement(pyUIElement);
      SDL_mutexV(uiElementsMutex);
    }else if(updateType == RENDERER_UPDATE_UIELEM){
      pyUIElement = PyObject_GetAttrString(pyUpdate,"uiElement");
      SDL_mutexP(uiElementsMutex);
      updateUIElement(pyUIElement);
      SDL_mutexV(uiElementsMutex);
    }else if(updateType == RENDERER_RELOAD_MOVEPATH){
      pyMovePath = PyObject_GetAttrString(gameState,"movePath");
      SDL_mutexP(movePathMutex);
      loadMovePath(pyMovePath,&(movePath));
      SDL_mutexV(movePathMutex);
      Py_DECREF(pyMovePath);
    }else if(updateType == RENDERER_RELOAD_ASTARPATH){
      pyMovePath = PyObject_GetAttrString(gameState,"aStarPath");
      SDL_mutexP(aStarMutex);
      loadMovePath(pyMovePath,&(aStarPath));
      SDL_mutexV(aStarMutex);
      Py_DECREF(pyMovePath);
    }else if(updateType == RENDERER_SET_SELECTEDNODE){
      setSelectedNode();
    }else if(updateType == RENDERER_SET_BACKGROUND){
      setBackgroundImage();
    }else if(updateType == RENDERER_LOAD_MAP){
      pyMap = PyObject_GetAttrString(gameMode, "map");//New reference
      SDL_mutexP(mapMutex);
      loadMap();
      SDL_mutexV(mapMutex);
    }else if(updateType == RENDERER_EXIT){
      SDL_mutexP(exitMutex);
      doQuit = 1;
      SDL_mutexV(exitMutex);
    }else if(updateType == RENDERER_CLICKSCROLL){
      SDL_mutexP(clickScrollMutex);
      clickScroll = 1;
      SDL_mutexV(clickScrollMutex);
    }else if(updateType == RENDERER_SETVIEWPORTMODE){
      pyMode = PyObject_GetAttrString(pyUpdate,"mode");
      SDL_mutexP(viewportModeMutex);
      viewportMode = PyLong_AsLong(pyMode);
      SDL_mutexV(viewportModeMutex);
      Py_DECREF(pyMode);
    }else if(updateType == RENDERER_SETCHOOSENEXTDELAYED){
      SDL_mutexP(chooseNextDelayedMutex);
      chooseNextTimeStart = pythonCurrentTick;
      chooseNextDelayed = 1;
      SDL_mutexV(chooseNextDelayedMutex);
    }
    Py_DECREF(pyUpdate);    
    pyUpdatesQueueEmpty = PyObject_CallMethod(pyUpdatesQueue,"empty",NULL);
  } 
  Py_DECREF(pyUpdatesQueue);
  Py_DECREF(pyUpdatesQueueEmpty);
}
static void draw(){
  SDL_mutexP(modalAnimationsMutex);
  if(modalAnimQueue != NULL && !isFocusing && !isSliding){//> 0 items
    isAnimating = 1;
    listelement * listpointer;
    currentAnim = modalAnimQueue->item; 
    modalAnimQueue = RemoveItem(modalAnimQueue);
    if(currentAnim->type == ANIMATION_AUTO_FOCUS){
      isFocusing = 1;
      focusTicks = SDL_GetTicks();
      focusXPos = translateTilesXToPositionX(0.0-currentAnim->xPos,currentAnim->yPos);
      focusYPos = translateTilesYToPositionY(currentAnim->yPos);
      focusXPosPrev = translateX;
      focusYPosPrev = translateY;
      focusTime = 20.0*(abs(focusXPosPrev-(-focusXPos))+abs(focusYPosPrev-(-focusYPos)));
      if(focusTime > AUTO_FOCUS_TIME_MAX){
	focusTime = AUTO_FOCUS_TIME_MAX;
      }else if(focusTime < AUTO_FOCUS_TIME_MIN){
	focusTime = AUTO_FOCUS_TIME_MIN;
      } 
    }else if(currentAnim->type == ANIMATION_UNIT_SLIDE){
      isSliding = 1;
      slidingTicks = SDL_GetTicks();
    }
  }
  SDL_mutexV(modalAnimationsMutex);
  if(!isFocusing && !isSliding && isAnimating){
    isAnimating = 0;
  }
  PYTHONCALLBACK * callback = (PYTHONCALLBACK *)malloc(sizeof(PYTHONCALLBACK));
  callback->id = EVENT_ON_DRAW;
  callback->deltaTicks = deltaTicks;
  callback->isAnimating = isAnimating;
  queueCallback(callback);

  //  pyCursorIndex = PyObject_GetAttrString(gameState,"cursorIndex");
  //  theCursorIndex = -1;
  //pyCursorIndex = PyObject_GetAttrString(gameState,"cursorIndex");
  //  theCursorIndex = PyLong_AsLong(pyCursorIndex);
  //  Py_DECREF(pyCursorIndex);

  /*  if(PyObject_HasAttrString(gameMode,"chooseNextDelayed")){
    pyChooseNextDelayed = PyObject_CallMethod(gameMode,"getChooseNextDelayed",NULL);//New reference
    printPyStackTrace();
    Py_DECREF(pyChooseNextDelayed);
    if(pyChooseNextDelayed == Py_True){
      chooseNextTimeStart = SDL_GetTicks();
      chooseNextDelayed = 1;
    }
    }*/
  SDL_mutexP(chooseNextDelayedMutex);
  if(chooseNextDelayed && ((SDL_GetTicks() - chooseNextTimeStart) > AUTO_CHOOSE_NEXT_DELAY)){
    chooseNextDelayed = 0;
    queueSimpleCallback(EVENT_CHOOSE_NEXT_DELAYED);
  }
  SDL_mutexV(chooseNextDelayedMutex);

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
  drawBoard();

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPickMatrix(mouseX,SCREEN_HEIGHT-mouseY,1,1,viewport);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  hitsCnt = glRenderMode(GL_RENDER);
  processTheHits(hitsCnt,selectBuf);
  selectedNodeName = selectedName;

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		 
  glSelectBuffer(BUFSIZE,selectBuf);//glSelectBuffer must be issued before selection mode is enabled, and it must not be issued while the rendering mode is GL_SELECT.
  glRenderMode(GL_SELECT);

  drawUI();
  hitsCnt = glRenderMode(GL_RENDER);
  processTheHits(hitsCnt,selectBuf);
  if(selectedName == -1){
    selectedName = selectedNodeName;
  }

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  calculateTranslation();
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		
  drawBackground();
  doViewport();
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  glColor3f(0.0,0.0,0.0);
  //  glBindTexture(GL_TEXTURE_2D, texturesArray[HEALTH_BAR_INDEX]);
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,0.0);//-11.01);
  glTexCoord2f(1.0,0.0); glVertex3f(1.0,-1.0,0.0);//-11.01);
  glTexCoord2f(1.0,1.0); glVertex3f(1.0,1.0,0.0);
  glTexCoord2f(0.0,1.0); glVertex3f(-1.0,1.0,0.0);
  glEnd();

  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPerspective(45.0f,(float)viewport[2]/(float)viewport[3],minZoom,maxZoom);

  glTranslatef(translateX,translateY,translateZ);
  drawBoard();
  
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  drawUI();
  glFlush();
  SDL_GL_SwapBuffers();
}
//PyObject * pyExit;
int musicChannel = -2;
int soundIndex = -1;
int restartMusic = 0;
int counter = 0;
static void fetchPyGameMode(){ 
  gameMode = PyObject_CallMethod(gameState,"getGameMode",NULL);
}

static void mainLoop (){
  while ( !quit ) {
    //    pyObj = PyObject_CallMethod(gameMode, "getRestartMusic",NULL);//New reference
    //    restartMusic = PyLong_AsLong(pyObj);
    //    Py_DECREF(pyObj);
    /*if(!Mix_PlayingMusic() || restartMusic){
      Py_DECREF(pyObj);
      pyObj = PyObject_CallMethod(gameMode,"getMusic",NULL);
      soundIndex = PyLong_AsLong(pyObj);
      Mix_PlayMusic(musicArray[soundIndex], 0);
      }*/
    /*    pyObj = PyObject_CallMethod(gameMode,"getSound",NULL);
    while(pyObj != Py_None && pyObj != NULL){
      soundIndex = PyLong_AsLong(pyObj);
      Py_DECREF(pyObj);
      Mix_PlayChannel(-1, soundArray[soundIndex], 0);
      pyObj = PyObject_CallMethod(gameMode,"getSound",NULL);
      Py_DECREF(pyObj);
      }*/
    //    printf("%d\n",0);
    deltaTicks = SDL_GetTicks()-currentTick;
    currentTick = SDL_GetTicks();
    SDL_mutexP(currentTickMutex);
    pythonCurrentTick = currentTick;
    SDL_mutexV(currentTickMutex);
    
    //    printf("%d\n",-1);
    draw();
    //printf("%d\n",-2);
    handleInput();
    //printf("%d\n",-3);
    SDL_mutexP(exitMutex);
    if(doQuit){
      quit = 1;
    }
    SDL_mutexV(exitMutex);
    //printf("%d\n",-4);
  }
}
int pyQuit = 0;
int pythonThread(void * data){
  while(!pyQuit){
    //    printf("%d\n",1);
    fetchPyGameMode();
    //    printf("%d\n",2);
    getPythonUpdates();
    //    printf("%d\n",3);
    dispatchPythonCallbacks();
    //    printf("%d\n",4);
    PyObject_SetAttrString(gameMode,"ticks",PyLong_FromLong(pythonCurrentTick));
    SDL_mutexP(exitMutex);
    if(doQuit){
      pyQuit = 1;
    }
    SDL_mutexV(exitMutex);
    //    sleep(0.01);
  }  
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
  gameModule = PyImport_ImportModule("gameModes");//New reference
  gameState = PyImport_ImportModule("gameState");
  fetchPyGameMode();
  //  getPythonUpdates();
  //    dispatchPythonCallbacks();
}
int ppid;
SDL_Thread * pyThread = NULL;
int main(int argc, char ** argv){
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
  initPython();
  //SDL_EnableUNICODE(1);

  pythonCallbackMutex = SDL_CreateMutex();
  unitsMutex = SDL_CreateMutex();
  animationsMutex = SDL_CreateMutex();
  modalAnimationsMutex = SDL_CreateMutex();
  uiElementsMutex = SDL_CreateMutex();
  movePathMutex = SDL_CreateMutex();
  aStarMutex = SDL_CreateMutex();
  selectedNodeMutex = SDL_CreateMutex();
  backgroundImageMutex = SDL_CreateMutex();
  mapMutex = SDL_CreateMutex();
  exitMutex = SDL_CreateMutex();
  clickScrollMutex = SDL_CreateMutex();
  viewportModeMutex = SDL_CreateMutex();
  chooseNextDelayedMutex = SDL_CreateMutex();
  currentTickMutex = SDL_CreateMutex();
  SDL_mutexP(mapMutex);//don't really need this yet, but putting it here for consistency's sake
  theMap.nodes = NULL;
  SDL_mutexV(mapMutex);
  initFonts();
  pyThread = SDL_CreateThread(pythonThread, NULL);
  mainLoop();
  SDL_WaitThread(pyThread,NULL);//should kill itself...
  queueSimpleCallback(EVENT_ON_QUIT);
  pyObj = PyObject_CallMethod(gameMode,"onQuit",NULL);
  printPyStackTrace();
  Py_DECREF(pyObj);
  SDL_Quit();
  Py_DECREF(gameModule);
  Py_DECREF(gameState);
  Py_Finalize();
  exit(0);
}
