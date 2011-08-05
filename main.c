#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <SDL.h>
#include <SDL_opengl.h>

#include <libpng12/png.h>
#include <Python/Python.h>

#include <ft2build.h>
#include <freetype/freetype.h>
#include <freetype/ftglyph.h>
#include <freetype/ftoutln.h>
#include <freetype/fttrigon.h>

#include "libpngGL.h"
#include "fonts.h"

#define maxZoom 120.0
#define minZoom 10.0
#define zoomSpeed 0.3

#define SCREEN_WIDTH 1280
#define SCREEN_HEIGHT 800

#define TILES_IMAGE "assets/tiles2.png"
#define UI_IMAGE "assets/UI.png"
#define TILE_SELECT_BOX_IMAGE "assets/tileSelect.png"
#define TILE_SELECT_BOX_INDEX 0
#define UI_MAP_EDITOR_TOP_IMAGE "assets/UITop.png"
#define UI_MAP_EDITOR_TOP_IMAGE_HEIGHT 80
#define UI_MAP_EDITOR_TOP_IMAGE_WIDTH 1280
#define UI_MAP_EDITOR_TOP_INDEX 1
#define UI_MAP_EDITOR_BOTTOM_IMAGE "assets/UIBottom.png"
#define UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT 10
#define UI_MAP_EDITOR_BOTTOM_IMAGE_WIDTH 1280
#define UI_MAP_EDITOR_BOTTOM_INDEX 2
#define UI_MAP_EDITOR_LEFT_IMAGE "assets/UILeft.png"
#define UI_MAP_EDITOR_LEFT_IMAGE_HEIGHT 871
#define UI_MAP_EDITOR_LEFT_IMAGE_WIDTH 229
#define UI_MAP_EDITOR_LEFT_INDEX 3
#define UI_MAP_EDITOR_RIGHT_IMAGE "assets/UIRight.png"
#define UI_MAP_EDITOR_RIGHT_IMAGE_HEIGHT 871
#define UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH 10
#define UI_MAP_EDITOR_RIGHT_INDEX 4
#define UI_NEW_GAME_SCREEN_IMAGE "assets/newGameScreen.png"
#define UI_NEW_GAME_SCREEN_IMAGE_HEIGHT 960
#define UI_NEW_GAME_SCREEN_IMAGE_WIDTH 1280
#define UI_NEW_GAME_SCREEN_INDEX 5


#define CURSOR_POINTER_IMAGE "assets/cursors/pointer.png"
#define CURSOR_POINTER_INDEX 6
#define CURSOR_HAND_IMAGE "assets/cursors/hand.png"
#define CURSOR_HAND_INDEX 7

#define PLAYER_START_BUTTON_IMAGE "assets/playerStartButton.png"
#define PLAYER_START_BUTTON_INDEX 8
#define PLAYER_START_BUTTON_WIDTH 13
#define PLAYER_START_BUTTON_HEIGHT 14
#define PLAYER_START_IMAGE "assets/playerStart.png"
#define PLAYER_START_INDEX 9
#define PLAYER_START_WIDTH 13
#define PLAYER_START_HEIGHT 14

#define UI_SCROLLABLE_IMAGE "assets/scrollableElement.png"
#define UI_SCROLLABLE_IMAGE_HEIGHT 404
#define UI_SCROLLABLE_IMAGE_WIDTH 210
#define UI_SCROLLABLE_INDEX 10

#define UI_SCROLL_PAD_IMAGE "assets/scrollPad.png"
#define UI_SCROLL_PAD_IMAGE_HEIGHT 16
#define UI_SCROLL_PAD_IMAGE_WIDTH 16
#define UI_SCROLL_PAD_INDEX 11

#define UI_TEXT_INPUT_IMAGE "assets/textInput.png"
#define UI_TEXT_INPUT_IMAGE_HEIGHT 20
#define UI_TEXT_INPUT_IMAGE_WIDTH 200
#define UI_TEXT_INPUT_INDEX 12

#define DESERT_TILE_INDEX 0
#define GRASS_TILE_INDEX 1
#define MOUNTAIN_TILE_INDEX 2
#define JUNGLE_TILE_INDEX 3
#define WATER_TILE_INDEX 4
#define ROAD_TILE_INDEX 5
#define CITY_TILE_INDEX 6
#define PLAYER_START_TILE_INDEX 7//REMOVE THIS

#define SIN60 0.8660
#define COS60 0.5

#define BUFSIZE 512


float screenRatio;
static SDL_Surface *gScreen;

int clickScroll = 0;
int leftButtonDown = 0;

int done = 0;    
int moveUp = 0;
int moveRight = 0;
int previousTick = 0;
int deltaTicks = 0;

float translateX = -30.0;
float translateY = 30.0;
#define translateZ -100.0
float scrollSpeed = 0.04;

PyObject * gameModule;
PyObject * gameMode;
PyObject * theMap;
PyObject * mapName;
PyObject * nodes;
PyObject * mapIterator;
PyObject * UIElementsIterator;
PyObject * subUIElementsIterator;
PyObject * subSubUIElementsIterator;
PyObject * rowIterator;

GLuint tilesTexture;
/*GLuint uiTexture;
GLuint uiTopTexture;
GLuint uiBottomTexture;
GLuint tileSelectBoxTexture;
GLuint cursorPointerTexture;
GLuint cursorHandTexture;
*/
GLdouble mouseMapPosX, mouseMapPosY, mouseMapPosZ;
GLdouble mouseMapPosXPrevious, mouseMapPosYPrevious;

int mouseX = 0;
int mouseY = 0;
GLuint selectBuf[BUFSIZE];
int selectedName = -1;//the mousedover object's 'name'
int previousSelectedName = -2;
int theCursorIndex = -1;


float desertVertices[6][2] = {
  {(699.0/1280),1.0-(66.0/1280)},
  {(699.0/1280),1.0-(34.0/1280)},
  {(726.0/1280),1.0-(18.0/1280)},
  {(754.0/1280),1.0-(34.0/1280)},
  {(754.0/1280),1.0-(66.0/1280)},
  {(726.0/1280),1.0-(82.0/1280)}
};
float jungleVertices[6][2] = {
  {(699.0/1280),1.0-(262.0/1280)},
  {(699.0/1280),1.0-(230.0/1280)},
  {(726.0/1280),1.0-(214.0/1280)},
  {(754.0/1280),1.0-(230.0/1280)},
  {(754.0/1280),1.0-(262.0/1280)},
  {(726.0/1280),1.0-(278.0/1280)}
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
float * vertexArrays[8];

float hexagonVertices[6][2] = {
  {-SIN60, -COS60},
  {-SIN60, COS60},
  {0.0, 1.0},
  {SIN60, COS60},
  {SIN60, -COS60},
  {0.0, -1.0}
};

float *textureVertices;
GLuint texturesArray[60];

/****************************** SDL STUFF ********************************/
static void printAttributes (){
  // Print out attributes of the context we created
  int nAttr;
  int i;
    
  int  attr[] = { SDL_GL_RED_SIZE, SDL_GL_BLUE_SIZE, SDL_GL_GREEN_SIZE,
		  SDL_GL_ALPHA_SIZE, SDL_GL_BUFFER_SIZE, SDL_GL_DEPTH_SIZE };
                    
  char *desc[] = { "Red size: %d bits\n", "Blue size: %d bits\n", "Green size: %d bits\n",
		   "Alpha size: %d bits\n", "Color buffer size: %d bits\n", 
		   "Depth bufer size: %d bits\n" };

  nAttr = sizeof(attr) / sizeof(int);
    
  for (i = 0; i < nAttr; i++) {
    int value;
    SDL_GL_GetAttribute (attr[i], &value);
    printf (desc[i], value);
  } 
}
static void createSurface(int fullscreen){//DEPRECATED
  Uint32 flags = 0;
  flags = SDL_OPENGL;
  if(fullscreen)
    flags |= SDL_FULLSCREEN;
  gScreen = SDL_SetVideoMode (SCREEN_WIDTH, SCREEN_HEIGHT, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Couldn't set OpenGL video mode: %s\n",
	     SDL_GetError());
  }
}
/****************************** /SDL STUFF ********************************/

/**************************** mouse hover object selection ********************************/
void processTheHits(GLint hits, GLuint buffer[]){
  GLuint *bufferPtr,*ptrNames, numberOfNames;
  int count = 0;
  int nameValue = 0;
  bufferPtr = (GLuint *) buffer;
  selectedName = -1;
  while(count < hits){
    numberOfNames = *bufferPtr;
    nameValue = *(bufferPtr + 3);//the value of the name is stored +3 over in mem
    if(numberOfNames == 1){
      if(nameValue > selectedName){
	selectedName = nameValue;
      }
    }else if(numberOfNames == 0){
      //selectedName = -1;
    }else{
      printf("WARNING: WE ONLY EXPECT ONE NAME PER OBJECT WHEN PICKING\n");
    }
    bufferPtr = bufferPtr + 3 + numberOfNames;
    count = count + 1;
  }


  /*
  //each 'hit' gives a 'number of names', then two depth values, then each of the names in the buffer(array)
  if(hits > 0){
    //just assume there's one hit for now, can't think of a reason we'd need multiple moused-over objects anyway
    numberOfNames = *bufferPtr;
    //these are the names of the object that was 'hit', should only be one if our code is working as expected
    if(numberOfNames == 1){
      bufferPtr = bufferPtr + 3;
      //the value of the name name is stored +3 over in mem
      selectedName = *bufferPtr;
    }else if(numberOfNames == 0){
      selectedName = -1;
    }else{
      printf("WARNING: WE ONLY EXPECT ONE NAME PER OBJECT WHEN PICKING\n");
    }
  }else{
    selectedName = -1;
  }
  */
}

void startPicking(){
}
void stopPicking() {
}

//float glMouseCoords[3];
//void convertWinCoordsToMapCoords(int x, int y){
void convertWinCoordsToMapCoords(int x, int y, GLdouble* posX, GLdouble* posY, GLdouble* posZ){
  GLint viewport[4];
  GLdouble modelview[16];
  GLdouble projection[16];
  GLfloat winX, winY, winZ;
  //  GLdouble posX, posY, posZ;

  glGetDoublev( GL_MODELVIEW_MATRIX, modelview );
  glGetDoublev( GL_PROJECTION_MATRIX, projection );
  glGetIntegerv( GL_VIEWPORT, viewport );

  winX = (float)x;
  winY = (float)viewport[3] - (float)y;
  

  PyObject * pyTranslateZ = PyObject_GetAttrString(theMap,"translateZ");
  double transZ = PyFloat_AsDouble(pyTranslateZ);
  //Py_DECREF(pyTranslateZ);//This causes a SegFault????

  winZ = (float)((minZoom-transZ)/maxZoom);
  gluUnProject( winX, winY, winZ, modelview, projection, viewport, posX, posY, posZ);
  
  //  glMouseCoords[0] = posX;
  //  glMouseCoords[1] = posY;
  //  glMouseCoords[2] = posZ;
  //  return glMouseCoords;
}
/**************************** /mouse hover object selection ********************************/

/************************************* drawing subroutines ***************************************/
void drawTile(int tilesXIndex, int tilesYIndex, long name, long tileValue, long roadValue,long cityValue,long isSelected, long mapPolarity,long playerStartValue){
  float xPosition = (float)tilesXIndex*-(1.9*SIN60);
  float yPosition = (float)tilesYIndex*1.4;
  //pulling the xindex and yindex in a little cause the black lines between tiles to be less harsh
  //float xPosition = (float)tilesXPosition*-(2.0*SIN60);
  //float yPosition = (float)tilesYPosition*1.5;
  if(abs(tilesYIndex)%2 == mapPolarity){
    xPosition += SIN60;
  }
  textureVertices = vertexArrays[tileValue];
  if(name == selectedName){
    glColor3f(0.8f, 0.8f, 0.8f);
    if(leftButtonDown){
      if(previousSelectedName != selectedName){
	PyObject_CallMethod(gameMode,"handleClick","i",selectedName);
      }
      previousSelectedName = selectedName;
    }
  }else{
    glColor3f(1.0f, 1.0f, 1.0f);
  }
  if(isSelected == 1){
    glColor3f(0.4f, 0.4f, 0.4f);    
  }
  glPushName(name);	
  glBegin(GL_POLYGON);
  glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xPosition, hexagonVertices[0][1]+yPosition, 0.0);
  glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xPosition, hexagonVertices[1][1]+yPosition, 0.0);
  glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xPosition, hexagonVertices[2][1]+yPosition, 0.0);
  glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xPosition, hexagonVertices[3][1]+yPosition, 0.0);
  glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xPosition, hexagonVertices[4][1]+yPosition, 0.0);
  glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xPosition, hexagonVertices[5][1]+yPosition, 0.0);
  glEnd();
  glPopName();


  if(roadValue == 1){
    textureVertices = vertexArrays[ROAD_TILE_INDEX];
    glBegin(GL_POLYGON);
    glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xPosition, hexagonVertices[0][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xPosition, hexagonVertices[1][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xPosition, hexagonVertices[2][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xPosition, hexagonVertices[3][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xPosition, hexagonVertices[4][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xPosition, hexagonVertices[5][1]+yPosition, 0.0);
    glEnd();
  }
  if(cityValue == 1){
    textureVertices = vertexArrays[CITY_TILE_INDEX];
    glBegin(GL_POLYGON);
    glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xPosition, hexagonVertices[0][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xPosition, hexagonVertices[1][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xPosition, hexagonVertices[2][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xPosition, hexagonVertices[3][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xPosition, hexagonVertices[4][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xPosition, hexagonVertices[5][1]+yPosition, 0.0);
    glEnd();
  }
  if(playerStartValue >= 1){
    textureVertices = vertexArrays[PLAYER_START_TILE_INDEX];
    glBegin(GL_POLYGON);
    glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xPosition, hexagonVertices[0][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xPosition, hexagonVertices[1][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xPosition, hexagonVertices[2][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xPosition, hexagonVertices[3][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xPosition, hexagonVertices[4][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xPosition, hexagonVertices[5][1]+yPosition, 0.0);
    glEnd();

    char playerStartVal[2];
    sprintf(playerStartVal,"%ld",playerStartValue);
    glColor3f(1.0,1.0,1.0);
    //    glColor3f(0.0,0.0,0.0);
    glPushMatrix();
    glTranslatef(xPosition-0.7,yPosition-0.4,0.0);
    glScalef(0.02,0.02,0.0);
    drawText(playerStartVal);
    glPopMatrix();
  }
}

void drawTiles(){
  
  int rowNumber = 0;
  PyObject * node;
  PyObject * row;

  mapIterator = PyObject_CallMethod(theMap,"getIterator",NULL);//New reference
  PyObject * polarity = PyObject_GetAttrString(theMap,"polarity");//New reference
  long longPolarity = PyLong_AsLong(polarity);

  rowIterator = PyObject_GetIter(mapIterator);
  while (row = PyIter_Next(rowIterator)) {
    int colNumber = 0;
    rowNumber = rowNumber - 1;
    PyObject * nodeIterator = PyObject_GetIter(row);
    while(node = PyIter_Next(nodeIterator)) {
      glBindTexture(GL_TEXTURE_2D, tilesTexture);
      PyObject * nodeName = PyObject_GetAttrString(node,"name");//New reference
      PyObject * nodeValue = PyObject_CallMethod(node,"getValue",NULL);//New reference
      PyObject * roadValue = PyObject_GetAttrString(node,"roadValue");//New reference
      PyObject * pyCity = PyObject_GetAttrString(node,"city");//New reference
      PyObject * pyPlayerStartValue = PyObject_GetAttrString(node,"playerStartValue");//New reference                                 
      PyObject * isSelected = PyObject_GetAttrString(node,"selected");//New reference

      long longName = PyLong_AsLong(nodeName);
      long longValue = PyLong_AsLong(nodeValue);
      long longRoadValue = PyLong_AsLong(roadValue);
      long longCityValue = 0;
      if(pyCity != Py_None){
	longCityValue = 1;
      }
      long playerStartValue = PyLong_AsLong(pyPlayerStartValue);
      long longIsSelected = PyLong_AsLong(isSelected);

      Py_DECREF(nodeName);
      Py_DECREF(nodeValue);
      Py_DECREF(roadValue);
      Py_DECREF(pyCity);
      Py_DECREF(pyPlayerStartValue);
      Py_DECREF(isSelected);
      Py_DECREF(node);
      //      printf("%d\n",longRoadValue);
      drawTile(colNumber,rowNumber,longName,longValue,longRoadValue,longCityValue,longIsSelected,longPolarity,playerStartValue);
      colNumber = colNumber - 1;
    }
    Py_DECREF(row);
  }
  Py_DECREF(rowIterator); 
  Py_DECREF(mapIterator);
  Py_DECREF(polarity);
}
drawBoard(){
  //printf("drawBoard");
  if(theMap != Py_None){
    drawTiles();
  }
}

void drawTileSelect(double xPos, double yPos, int name, long tileType, long selected){
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
void drawUIElement(PyObject * uiElement){
    unsigned int red[1],green[1],blue[1];
    PyObject * pyXPosition = PyObject_GetAttrString(uiElement,"xPosition");
    PyObject * pyYPosition = PyObject_GetAttrString(uiElement,"yPosition");
    PyObject * pyWidth = PyObject_GetAttrString(uiElement,"width");
    PyObject * pyHeight = PyObject_GetAttrString(uiElement,"height");
    PyObject * pyHidden = PyObject_GetAttrString(uiElement,"hidden");
    PyObject * pyName = PyObject_GetAttrString(uiElement,"name");
    PyObject * pyTextureIndex = PyObject_GetAttrString(uiElement,"textureIndex");
    PyObject * pyCursorIndex = PyObject_GetAttrString(uiElement,"cursorIndex");
    PyObject * pyText = PyObject_GetAttrString(uiElement,"text");
    PyObject * pyTextColor = PyObject_GetAttrString(uiElement,"textColor");
    PyObject * pyTextSize = PyObject_GetAttrString(uiElement,"textSize");
    PyObject * pyColor = PyObject_GetAttrString(uiElement,"color");
    PyObject * pyMouseOverColor = PyObject_GetAttrString(uiElement,"mouseOverColor");
    PyObject * pyTextXPosition = PyObject_GetAttrString(uiElement,"textXPos");
    PyObject * pyTextYPosition = PyObject_GetAttrString(uiElement,"textYPos");

    double xPosition = PyFloat_AsDouble(pyXPosition);
    double yPosition = PyFloat_AsDouble(pyYPosition);
    double width = PyFloat_AsDouble(pyWidth);
    double height = PyFloat_AsDouble(pyHeight);
    int hidden = pyHidden==Py_True;
    long name = PyLong_AsLong(pyName);
    long textureIndex = PyLong_AsLong(pyTextureIndex);
    long cursorIndex = PyLong_AsLong(pyCursorIndex);
    char * text = PyString_AsString(pyText);
    char * textColor = PyString_AsString(pyTextColor);
    double textSize = PyFloat_AsDouble(pyTextSize);
    char * color = PyString_AsString(pyColor);
    char * mouseOverColor = PyString_AsString(pyMouseOverColor);
    double textXPosition = PyFloat_AsDouble(pyTextXPosition);
    double textYPosition = PyFloat_AsDouble(pyTextYPosition);
     
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
    Py_DECREF(pyMouseOverColor);
    Py_DECREF(pyTextXPosition);
    Py_DECREF(pyTextYPosition);

    //    printf("%d\n",selectedName);
    PyObject_CallMethod(gameMode,"handleMouseOver","i",selectedName);//New reference

    if(!hidden){
      if(PyObject_HasAttrString(uiElement,"tileType")){//gameModeTileSelectButton
	drawTileSelect(xPosition,yPosition,name,PyLong_AsLong(PyObject_GetAttrString(uiElement,"tileType")),PyLong_AsLong(PyObject_GetAttrString(uiElement,"selected")));
      }else{
	if(textureIndex > -1){
	  glLoadIdentity();
	  glBindTexture(GL_TEXTURE_2D, texturesArray[textureIndex]);
	  sscanf(color,"%X %X %X",red,green,blue);
	  //	glColor3f(red1.0f, 1.0f, 1.0f);
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  glPushName(name);
	  glBegin(GL_QUADS);	
	  glTexCoord2f(0.0,1.0); glVertex3f(xPosition,yPosition,0.0);
	  glTexCoord2f(1.0,1.0); glVertex3f(xPosition+width,yPosition,0.0);
	  glTexCoord2f(1.0,0.0); glVertex3f(xPosition+width,yPosition-height,0.0);
	  glTexCoord2f(0.0,0.0); glVertex3f(xPosition,yPosition-height,0.0);
	  glEnd();
	  glPopName();
	}
	//      printf("index: %ld %ld %f %f %f %f\n",name,textureIndex,xPosition,yPosition,width,height);
	if(PyObject_HasAttrString(uiElement,"text")){
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  if(selectedName == name){
	    sscanf(mouseOverColor,"%X %X %X",red,green,blue);
	  }else{
	    sscanf(textColor,"%X %X %X",red,green,blue);
	  }
	  glColor3f(*red/255.0, *green/255.0, *blue/255.0);
	  glLoadIdentity();
	  glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	  glScalef(textSize,textSize,0.0);
	  glPushName(name);
	  drawText(text);
	  glPopName();
	}
      }
      Py_DECREF(uiElement);
      if(name == selectedName && cursorIndex >= 0){
	theCursorIndex = cursorIndex;
      }
    }
}
void drawUI(){
  PyObject * uiElement;
  PyObject * subUIElement;
  PyObject * subSubUIElement;
  theCursorIndex = -1;
  //TODO: make sure CallMethod does not create a new reference and fix these two calls if it does
  UIElementsIterator = PyObject_GetIter(PyObject_CallMethod(gameMode,"getUIElementsIterator",NULL));//New reference
  

  while (uiElement = PyIter_Next(UIElementsIterator)) {
    drawUIElement(uiElement);
    subUIElementsIterator = PyObject_GetIter(PyObject_CallMethod(uiElement,"getUIElementsIterator",NULL));//New reference
    while (subUIElement = PyIter_Next(subUIElementsIterator)) {
      drawUIElement(subUIElement);

      subSubUIElementsIterator = PyObject_GetIter(PyObject_CallMethod(subUIElement,"getUIElementsIterator",NULL));//New reference
      while (subSubUIElement = PyIter_Next(subSubUIElementsIterator)) {
	drawUIElement(subSubUIElement);
      }

    }
    
  }

  /*draw cursor*/
  glLoadIdentity();
  if(theCursorIndex >= 0){
    glBindTexture(GL_TEXTURE_2D, texturesArray[theCursorIndex]);
  }else{
    glBindTexture(GL_TEXTURE_2D, texturesArray[CURSOR_POINTER_INDEX]);
  }
  glColor3f(1.0,1.0,1.0);
  glBegin(GL_QUADS);
  float xPos = (mouseX/(SCREEN_WIDTH/2.0))-1.0;
  float yPos = 1.0-(mouseY/(SCREEN_HEIGHT/2.0));
  float pointerWidth = 3.0*13.0/SCREEN_WIDTH;
  float pointerHeight = 3.0*21.0/SCREEN_HEIGHT;
  glTexCoord2f(0.0,1.0); glVertex3f(xPos,yPos,0.0);
  glTexCoord2f(1.0,1.0); glVertex3f(xPos+pointerWidth,yPos,0.0);
  glTexCoord2f(1.0,0.0); glVertex3f(xPos+pointerWidth,yPos-pointerHeight,0.0);
  glTexCoord2f(0.0,0.0); glVertex3f(xPos,yPos-pointerHeight,0.0);
  glEnd();

  /*frame rate display*/
  if(deltaTicks != 0){
    char frameRate[20];
    sprintf(frameRate,"%ld",(long)(1000.0/deltaTicks));
    glPushMatrix();
    glColor3f(1.0,1.0,1.0);
    glLoadIdentity();
    glTranslatef(-1.0,-1.0,0.0);
    glScalef(0.0005,0.0005,0.0);
    drawText(frameRate);
    glPopMatrix();
  }
  


}
/************************************* /drawing subroutines ***************************************/

/************************************** opengl init **************************************/

static void initGL (){
  /** needs to be called on screen resize **/
  //unneeded with sdl?
  //  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);//default values anyway, so not needed but w/e
  glInitNames(); //init names stack	
  glClearColor(0.0, 0.0, 0.0, 0.0); //sets screen clear color
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);
  char file[100] = TILES_IMAGE;




  pngLoad(&tilesTexture, TILES_IMAGE);	/******************** /image init ***********************/
  pngLoad(&texturesArray[TILE_SELECT_BOX_INDEX],TILE_SELECT_BOX_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_TOP_INDEX],UI_MAP_EDITOR_TOP_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_BOTTOM_INDEX],UI_MAP_EDITOR_BOTTOM_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_LEFT_INDEX],UI_MAP_EDITOR_LEFT_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_RIGHT_INDEX],UI_MAP_EDITOR_RIGHT_IMAGE);
  pngLoad(&texturesArray[UI_NEW_GAME_SCREEN_INDEX],UI_NEW_GAME_SCREEN_IMAGE);

  pngLoad(&texturesArray[CURSOR_POINTER_INDEX],CURSOR_POINTER_IMAGE);
  pngLoad(&texturesArray[CURSOR_HAND_INDEX],CURSOR_HAND_IMAGE);
  pngLoad(&texturesArray[PLAYER_START_BUTTON_INDEX],PLAYER_START_BUTTON_IMAGE);
  pngLoad(&texturesArray[UI_SCROLLABLE_INDEX],UI_SCROLLABLE_IMAGE);
  pngLoad(&texturesArray[UI_SCROLL_PAD_INDEX],UI_SCROLL_PAD_IMAGE);
  pngLoad(&texturesArray[UI_TEXT_INPUT_INDEX],UI_TEXT_INPUT_IMAGE);


  vertexArrays[DESERT_TILE_INDEX] = *desertVertices;
  vertexArrays[GRASS_TILE_INDEX] = *grassVertices;
  vertexArrays[MOUNTAIN_TILE_INDEX] = *mountainVertices;
  vertexArrays[JUNGLE_TILE_INDEX] = *jungleVertices;
  vertexArrays[WATER_TILE_INDEX] = *waterVertices;
  vertexArrays[ROAD_TILE_INDEX] = *roadVertices;
  vertexArrays[CITY_TILE_INDEX] = *cityVertices;
  vertexArrays[PLAYER_START_TILE_INDEX] = *playerStartVertices;

  screenRatio = (GLfloat)SCREEN_WIDTH/(GLfloat)SCREEN_HEIGHT;
  
}
static void initPython(){
  //http://docs.python.org/release/2.6.6/c-api/index.html
  char path[100] = "hello";
  //	sprintf(path,"%s","hello");
  Py_Initialize();
  char *pyArgv[1];
  pyArgv[0] = path;
  PySys_SetArgv(1, pyArgv);
	
  PyObject * main_module = PyImport_AddModule("__main__");//Borrowed reference
  PyObject * global_dict = PyModule_GetDict(main_module);//Borrowed reference
  //use this to create a new object: like "class()" in python //PyObject * instance = PyObject_CallObject(class,NULL);//New reference
}
static void handleInput(){
  SDL_Event event;

  deltaTicks = SDL_GetTicks()-previousTick;
  previousTick = SDL_GetTicks();


  //SDL_Delay(20);//for framerate testing...
  while(SDL_PollEvent(&event)){
    switch(event.type){
    case SDL_MOUSEMOTION:
      mouseX = event.motion.x;
      mouseY = event.motion.y;
      PyObject_CallMethod(gameMode,"handleMouseMovement","(iii)",selectedName,mouseX,mouseY);
      //					printf("x: %d\t\ty: %d\n",mouseX,mouseY);
      if(clickScroll > 0){
	translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
	translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
      }else{
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
      }
      mouseMapPosXPrevious = mouseMapPosX;
      mouseMapPosYPrevious = mouseMapPosY;
      break;
    case SDL_MOUSEBUTTONDOWN:

      if(event.button.button == SDL_BUTTON_WHEELUP){
	PyObject_CallMethod(gameMode,"handleScrollUp","(ii)",selectedName,deltaTicks);//New reference
      }else if(event.button.button == SDL_BUTTON_WHEELDOWN){
	PyObject_CallMethod(gameMode,"handleScrollDown","(ii)",selectedName,deltaTicks);//New reference
      }
      /*      if(event.button.button == SDL_BUTTON_WHEELUP){
	translateZ = translateZ + zoomSpeed*deltaTicks;
      }else if(event.button.button == SDL_BUTTON_WHEELDOWN){
	translateZ = translateZ - zoomSpeed*deltaTicks;
      }
      if(translateZ > -10.0-minZoom){
	translateZ = -10.0-minZoom;
	}*/


      if(event.button.button == SDL_BUTTON_MIDDLE){
	clickScroll = 1;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	//leftButtonDown = 1;
	PyObject_CallMethod(gameMode,"handleLeftClickDown","i",selectedName);//New reference
	previousSelectedName = selectedName;
      }
      if(event.button.button == SDL_BUTTON_RIGHT){
	PyObject_CallMethod(gameMode,"handleRightClick","i",selectedName);//New reference
      }
      break;
    case SDL_MOUSEBUTTONUP:
      if(event.button.button == SDL_BUTTON_MIDDLE){
	clickScroll = 0;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	PyObject_CallMethod(gameMode,"handleLeftClickUp","i",selectedName);//New reference
	
	leftButtonDown = 0;
      }
      break;
    case SDL_KEYDOWN:
      if(event.key.keysym.sym == SDLK_ESCAPE){
	done = 1;
      }else if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 1;
      }else if(
	       (event.key.keysym.sym >= 0x61 && event.key.keysym.sym <= 0x7A)//a-z
	       || (event.key.keysym.sym >= 0x30 && event.key.keysym.sym <= 0x39)//0-9
	       || event.key.keysym.sym == 8//backspace
	       || event.key.keysym.sym == 32//space
	       || event.key.keysym.sym == 45//-
	       || event.key.keysym.sym == 13//enter/return
	       || (event.key.keysym.sym >= 273 && event.key.keysym.sym <= 276)//arrow keys
	       ){
	if((event.key.keysym.mod & KMOD_CAPS | event.key.keysym.mod & KMOD_LSHIFT | event.key.keysym.mod & KMOD_RSHIFT) && (event.key.keysym.sym > 0x60 && event.key.keysym.sym <= 0x7A)){
	  char * key = SDL_GetKeyName(event.key.keysym.sym);
	  char capsKey[2];
	  capsKey[0] = (*key)-32;
	  capsKey[1] = 0;
	  PyObject_CallMethod(gameMode,"handleKeyDown","s",capsKey); 
	}else{
	  PyObject_CallMethod(gameMode,"handleKeyDown","s",SDL_GetKeyName(event.key.keysym.sym));
	}
      }else{
	printf("rejected: %d\n",event.key.keysym.sym);
      }
      break;
    case SDL_KEYUP:
      if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 0;
      }
      break;
    case SDL_QUIT:
      done = 1;
      break;
    default:
      break;
    }
  }
  if(moveRight > 0){// && translateX > -10.0){
    translateX -= scrollSpeed*deltaTicks;
  }else if(moveRight < 0){// && translateX < 10.0){
    translateX += scrollSpeed*deltaTicks;
  }
  if(moveUp > 0){// && translateY > -10.0){
    translateY -= scrollSpeed*deltaTicks;
  }else if(moveUp < 0){// && translateY < 10.0){
    translateY += scrollSpeed*deltaTicks;
  }
}
static void draw(){

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		
    //game board projection time
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0f,screenRatio,minZoom,maxZoom);

    //draw the game board
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    convertWinCoordsToMapCoords(mouseX,mouseY,&mouseMapPosX,&mouseMapPosY,&mouseMapPosZ);
    //glTranslatef(mouseMapPosX,mouseMapPosY,translateZ);//for some reason we need mouseMapPosZ instead of translateZ
    glTranslatef(translateX,translateY,mouseMapPosZ);

    //startPicking();
    GLint viewport[4];
    glSelectBuffer(BUFSIZE,selectBuf);
    glRenderMode(GL_SELECT);

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    //glViewport(0.0,0.0,SCREEN_WIDTH, SCREEN_HEIGHT);
    glViewport(UI_MAP_EDITOR_LEFT_IMAGE_WIDTH,UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT,SCREEN_WIDTH - UI_MAP_EDITOR_LEFT_IMAGE_WIDTH - UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH, SCREEN_HEIGHT - UI_MAP_EDITOR_TOP_IMAGE_HEIGHT - UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT);
    glGetIntegerv(GL_VIEWPORT,viewport);
    gluPickMatrix(mouseX,viewport[3]+UI_MAP_EDITOR_TOP_IMAGE_HEIGHT+UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT-mouseY,5,5,viewport);
    gluPerspective(45.0f,screenRatio,minZoom,maxZoom);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    //glInitNames();
    drawBoard();

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
    glGetIntegerv(GL_VIEWPORT,viewport);
    gluPickMatrix(mouseX,viewport[3]-mouseY,5,5,viewport);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    drawUI();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
    glPopMatrix();

    //stopPicking();
    int hits;
    //restoring the original projection matrix
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    //glViewport(0.0,0.0,SCREEN_WIDTH, SCREEN_HEIGHT);
    glViewport(UI_MAP_EDITOR_LEFT_IMAGE_WIDTH,UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT,SCREEN_WIDTH - UI_MAP_EDITOR_LEFT_IMAGE_WIDTH - UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH, SCREEN_HEIGHT - UI_MAP_EDITOR_TOP_IMAGE_HEIGHT - UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT);

    glMatrixMode(GL_MODELVIEW);
    glPopMatrix();
    glFlush();
    //returning to normal rendering mode
    hits = glRenderMode(GL_RENDER);
    //if (hits != 0){
    processTheHits(hits,selectBuf);
    //}
    drawBoard();
    
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    drawUI();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
    glPopMatrix();




    glFlush();//"all programs should call glFlush whenever they count on having all of their previously issued commands completed"
    SDL_GL_SwapBuffers ();	
  
}
static void mainLoop (){
  while ( !done ) {
    gameMode = PyObject_GetAttrString(gameModule, "theGameMode");
    theMap = PyObject_GetAttrString(gameMode, "map");//New reference
    if(theMap != Py_None){
      nodes = PyObject_CallMethod(theMap,"getNodes",NULL);//New reference
    }
    handleInput();
    draw();

    if(theMap != Py_None){
      Py_DECREF(nodes);
    }
    Py_DECREF(theMap);
    Py_DECREF(gameMode);
  }
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
  if ( SDL_Init (SDL_INIT_VIDEO) < 0 ) {
    fprintf(stderr, "Couldn't initialize SDL: %s\n",SDL_GetError());
    exit(1);
  }
  SDL_GL_SetAttribute (SDL_GL_DEPTH_SIZE, 16);
  SDL_GL_SetAttribute (SDL_GL_DOUBLEBUFFER, 1);
  Uint32 flags = SDL_OPENGL;
  //flags |= SDL_FULLSCREEN;
  gScreen = SDL_SetVideoMode (SCREEN_WIDTH, SCREEN_HEIGHT, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Could not set OpenGL video mode: %s\n",
	     SDL_GetError());
    SDL_Quit();
    exit(2);
  }
  SDL_ShowCursor(0);
  initGL();
  initPython();
  initFonts();
  //SDL_EnableUNICODE(1);
  gameModule = PyImport_ImportModule("__init__");//New reference
  mainLoop();
  Py_DECREF(gameModule);
  Py_Finalize();

  exit(0);
}
