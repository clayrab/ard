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

#define maxZoom 40.0
#define minZoom 1.0
#define initZoom 20.0

#define zoomSpeed 30.0//lower is faster
#define focusSpeed 15.0//lower is faster

#define SCREEN_WIDTH 1280
#define SCREEN_HEIGHT 800
//#define SCREEN_WIDTH 1920
//#define SCREEN_HEIGHT 1200

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

#define CURSOR_POINTER_IMAGE "assets/cursors/gam372.png"
#define CURSOR_POINTER_INDEX 6

#define CURSOR_POINTER_ON_IMAGE "assets/cursors/gam375.png"
#define CURSOR_POINTER_ON_INDEX 7

#define CURSOR_MOVE_IMAGE "assets/cursors/gam378.png"
#define CURSOR_MOVE_INDEX 8

#define CURSOR_WIDTH 32
#define CURSOR_HEIGHT 32

#define PLAYER_START_BUTTON_IMAGE "assets/playerStartButton.png"
#define PLAYER_START_BUTTON_WIDTH 13
#define PLAYER_START_BUTTON_HEIGHT 14
#define PLAYER_START_BUTTON_INDEX 9

#define PLAYER_START_IMAGE "assets/playerStart.png"
#define PLAYER_START_WIDTH 13
#define PLAYER_START_HEIGHT 14
#define PLAYER_START_INDEX 10

#define UI_SCROLLABLE_IMAGE "assets/scrollableElement.png"
#define UI_SCROLLABLE_IMAGE_HEIGHT 404
#define UI_SCROLLABLE_IMAGE_WIDTH 210
#define UI_SCROLLABLE_INDEX 11

#define UI_SCROLL_PAD_IMAGE "assets/scrollPad.png"
#define UI_SCROLL_PAD_IMAGE_HEIGHT 16
#define UI_SCROLL_PAD_IMAGE_WIDTH 16
#define UI_SCROLL_PAD_INDEX 12

#define UI_TEXT_INPUT_IMAGE "assets/textInput.png"
#define UI_TEXT_INPUT_IMAGE_HEIGHT 20
#define UI_TEXT_INPUT_IMAGE_WIDTH 200
#define UI_TEXT_INPUT_INDEX 13

#define MEEPLE_IMAGE "assets/meeple.png"
#define MEEPLE_IMAGE_HEIGHT 20
#define MEEPLE_IMAGE_WIDTH 200
#define MEEPLE_INDEX 14

#define HEALTH_BAR_IMAGE "assets/healthBar.png"
#define HEALTH_BAR_IMAGE_HEIGHT 6
#define HEALTH_BAR_IMAGE_WIDTH 52
#define HEALTH_BAR_INDEX 15

#define UNIT_BUILD_BAR_IMAGE "assets/unitBuildBar.png"
#define UNIT_BUILD_BAR_IMAGE_HEIGHT 12
#define UNIT_BUILD_BAR_IMAGE_WIDTH 180
#define UNIT_BUILD_BAR_INDEX 16

#define MAP_ICON_IMAGE "assets/mapIcon.png"
#define MAP_ICON_HEIGHT 35
#define MAP_ICON_WIDTH 56
#define MAP_ICON_INDEX 17

#define WALK_ICON_IMAGE "assets/walkIcon.png"
#define WALK_ICON_HEIGHT 36
#define WALK_ICON_WIDTH 36
#define WALK_ICON_INDEX 18

#define ADD_BUTTON_IMAGE "assets/addButton.png"
#define ADD_BUTTON_HEIGHT 20
#define ADD_BUTTON_WIDTH 20
#define ADD_BUTTON_INDEX 19

#define REMOVE_BUTTON_IMAGE "assets/removeButton.png"
#define REMOVE_BUTTON_HEIGHT 20
#define REMOVE_BUTTON_WIDTH 20
#define REMOVE_BUTTON_INDEX 20

#define CITY_VIEWER_BOX_IMAGE "assets/cityViewerBox.png"
#define CITY_VIEWER_BOX_HEIGHT 352
#define CITY_VIEWER_BOX_WIDTH 211
#define CITY_VIEWER_BOX_INDEX 21

#define UNIT_VIEWER_BOX_IMAGE "assets/unitViewerBox.png"
#define UNIT_VIEWER_BOX_HEIGHT 100
#define UNIT_VIEWER_BOX_WIDTH 211
#define UNIT_VIEWER_BOX_INDEX 22

#define UNIT_TYPE_VIEWER_BOX_IMAGE "assets/unitTypeViewerBox.png"
#define UNIT_TYPE_VIEWER_BOX_HEIGHT 241
#define UNIT_TYPE_VIEWER_BOX_WIDTH 211
#define UNIT_TYPE_VIEWER_BOX_INDEX 23

#define RESEARCH_BOX_IMAGE "assets/researchBox.png"
#define RESEARCH_BOX_HEIGHT 45
#define RESEARCH_BOX_WIDTH 190
#define RESEARCH_BOX_INDEX 24

#define SELECTION_BRACKET_IMAGE "assets/selectionBrackets.png"
#define SELECTION_BRACKET_HEIGHT 20
#define SELECTION_BRACKET_WIDTH 67
#define SELECTION_BRACKET_INDEX 25

#define ADD_BUTTON_SMALL_IMAGE "assets/addButtonSmall.png"
#define ADD_BUTTON_SMALL_HEIGHT 13
#define ADD_BUTTON_SMALL_WIDTH 13
#define ADD_BUTTON_SMALL_INDEX 26

#define REMOVE_BUTTON_SMALL_IMAGE "assets/removeButtonSmall.png"
#define REMOVE_BUTTON_SMALL_HEIGHT 13
#define REMOVE_BUTTON_SMALL_WIDTH 13
#define REMOVE_BUTTON_SMALL_INDEX 27

#define REMOVE_BUTTON_SMALL_IMAGE "assets/removeButtonSmall.png"
#define REMOVE_BUTTON_SMALL_HEIGHT 13
#define REMOVE_BUTTON_SMALL_WIDTH 13
#define REMOVE_BUTTON_SMALL_INDEX 27

#define UNIT_CIRCLE_RED_IMAGE "assets/selectionBoxRed.png"
#define UNIT_CIRCLE_RED_HEIGHT 40
#define UNIT_CIRCLE_RED_WIDTH 40
#define UNIT_CIRCLE_RED_INDEX 28

#define UNIT_CIRCLE_BLUE_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_BLUE_HEIGHT 40
#define UNIT_CIRCLE_BLUE_WIDTH 40
#define UNIT_CIRCLE_BLUE_INDEX 29

#define UNIT_CIRCLE_GREEN_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_GREEN_INDEX 30
#define UNIT_CIRCLE_YELLOW_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_YELLOW_INDEX 31
#define UNIT_CIRCLE_PINK_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_PINK_INDEX 32
#define UNIT_CIRCLE_ORANGE_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_ORANGE_INDEX 33
#define UNIT_CIRCLE_PURPLE_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_PURPLE_INDEX 34
#define UNIT_CIRCLE_BROWN_IMAGE "assets/selectionBoxBlue.png"
#define UNIT_CIRCLE_BROWN_INDEX 35

#define CURSOR_ATTACK_IMAGE "assets/cursors/swordIcon.png"
#define CURSOR_ATTACK_INDEX 36

#define CURSOR_HEAL_IMAGE "assets/cursors/healCursor.png"
#define CURSOR_HEAL_INDEX 37

#define ARCHER_IMAGE "assets/archer.png"
#define ARCHER_INDEX 38

#define SWORDSMAN_IMAGE "assets/swordsman.png"
#define SWORDSMAN_INDEX 39

#define SELECTION_BOX_IMAGE "assets/selectionBox.png"
#define SELECTION_BOX_INDEX 40

#define SUMMONER_IMAGE "assets/summoner.png"
#define SUMMONER_INDEX 41

#define CITY_IMAGE "assets/city.png"
#define CITY_INDEX 42

#define GATHERER_IMAGE "assets/gatherer.png"
#define GATHERER_INDEX 43

#define DRAGON_IMAGE "assets/dragon.png"
#define DRAGON_INDEX 44

#define WHITE_MAGE_IMAGE "assets/white_mage.png"
#define WHITE_MAGE_INDEX 45

#define DESERT_TILE_INDEX 0
#define GRASS_TILE_INDEX 1
#define MOUNTAIN_TILE_INDEX 2
#define FOREST_TILE_INDEX 3
#define BLUE_FOREST_TILE_INDEX 4
#define WATER_TILE_INDEX 5
#define ROAD_TILE_INDEX 6
#define CITY_TILE_INDEX 7
#define PLAYER_START_TILE_INDEX 8

#define DESERT_MOVE_COST 2.0
#define GRASS_MOVE_COST 1.0
#define MOUNTAIN_MOVE_COST 6.0
#define FOREST_MOVE_COST 1.0
#define WATER_MOVE_COST 6.0

#define SIN60 0.8660
#define COS60 0.5

#define BUFSIZE 512

float screenRatio;
static SDL_Surface *gScreen;

int clickScroll = 0;
long focusNextUnit = 0;
float focusXPos, focusYPos;
int isFocusing = 0;
int considerDoneFocusing = 0;
int leftButtonDown = 0;

int done = 0;    
int moveUp = 0;
int moveRight = 0;
int previousTick = 0;
int deltaTicks = 0;
int avgDeltaTicks = 0;
int totalDeltaTicksDataPoints = 0;

GLfloat mapDepth,mapDepthTest1,mapDepthTest2,mapDepthTest3;
float translateX = 0.0;
float translateY = 0.0;
float translateZ = 0.0;
float translateXPrev = 0.0;
float translateYPrev = 0.0;
float translateZPrev = 0.0;
float scrollSpeed = 0.10;

GLdouble convertedBottomLeftX,convertedBottomLeftY,convertedBottomLeftZ;
GLdouble convertedTopRightX,convertedTopRightY,convertedTopRightZ;

PyObject * pyUnitType;
PyObject * pyUnitTextureIndex;
PyObject * pyName;
PyObject * pyHealth;
PyObject * pyMaxHealth;
PyObject * pyPlayerNumber;
char * unitName;
long playerNumber;
long unitTextureIndex;
float healthBarLength;
PyObject * uiElement;
PyObject * gameModule;
PyObject * gameState;
PyObject * gameMode;
PyObject * theMap;
PyObject * mapName;
PyObject * mapIterator;
PyObject * UIElementsIterator;
PyObject * rowIterator;
PyObject * pyMapWidth;
PyObject * pyMapHeight;
PyObject * pyObj;
//PyObject * playableMode;
long mapWidth;
long mapHeight;

#define MAX_CITIES 40
#define MAX_CITY_NAME_LENGTH 50
#define MAX_UNITS 400
#define MAX_UNIT_NAME_LENGTH 50

/*float cityNamesXs[MAX_CITIES];
float cityNamesYs[MAX_CITIES];
char cityNames[MAX_CITIES][MAX_CITY_NAME_LENGTH];
int cityNamesCount = 0;
*/
/*float unitNamesXs[MAX_UNITS];
float unitNamesYs[MAX_UNITS];
char unitNames[MAX_UNITS][MAX_UNIT_NAME_LENGTH];
int unitNamesCount = 0;
*/
GLuint tilesTexture;
GLdouble mouseMapPosX, mouseMapPosY, mouseMapPosZ;
GLdouble mouseMapPosXPrevious, mouseMapPosYPrevious, mouseMapPosZPrevious = -initZoom;
GLint bufRenderMode;
float *textureVertices;
GLuint texturesArray[60];
GLuint tilesLists;
GLuint selectionBoxList;
GLuint unitList;
GLuint healthBarList;


int mouseX = 0;
int mouseY = 0;
GLuint selectBuf[BUFSIZE];
int selectedName = -1;//the mousedover object's 'name'
int previousClickedName = -2;
int previousMousedoverName = -2;
int theCursorIndex = -1;
float * vertexArrays[9];

float desertVertices[6][2] = {
  {(699.0/1280),1.0-(66.0/1280)},
  {(699.0/1280),1.0-(34.0/1280)},
  {(726.0/1280),1.0-(18.0/1280)},
  {(754.0/1280),1.0-(34.0/1280)},
  {(754.0/1280),1.0-(66.0/1280)},
  {(726.0/1280),1.0-(82.0/1280)}
};
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

float hexagonVertices[6][2] = {
  //cheated these all out by 0.01 so the black background doesn't bleed through
  {-SIN60-0.01, -COS60-0.01},
  {-SIN60-0.01, COS60+0.01},
  {0.01, 1.01},
  {SIN60+0.01, COS60+0.01},
  {SIN60+0.01, -COS60-0.01},
  {0.01, -1.01}
};
PyObject *exc_type, *exc_value, *exc_traceback;
static void printPyStackTrace(){
  //put this thing after the call that is causing your problem!
    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    if(exc_type && exc_traceback){
      pyObj = PyObject_CallMethodObjArgs(gameModule,PyString_FromString("printTraceBack"),exc_type,exc_value,exc_traceback,NULL);
      if(pyObj != NULL){
	//Py_DECREF(pyObj);
      }
      PyErr_Print();//This is supposed to print it but doesn't. i left it here so the exception gets cleared...
    }
}
/**************************** mouse hover object selection ********************************/
GLuint *bufferPtr,*ptrNames, numberOfNames;
int count;
int nameValue;
void processTheHits(GLint hitsCount, GLuint buffer[]){
  glFlush();
  count = 0;
  nameValue = 0;
  bufferPtr = (GLuint *) buffer;
  selectedName = -1;
  printf("hitscount: %d\n",hitsCount);
  while(count < hitsCount){
    numberOfNames = *bufferPtr;
    printf("numberofnames: %d\n",numberOfNames);
    nameValue = *(bufferPtr + 3);//the value of the name is stored +3 over in mem
    if(numberOfNames == 1){
      //elements are created from back to front, the names should be in this order so we return the largest name
      if(nameValue > selectedName){
	selectedName = nameValue;
      }
    }else if(numberOfNames == 0){
      //selectedName = -1;
    }else{
      //This is just if an object has multiple names, the number of objects hit is hitsCount
      printf("WARNING: WE ONLY EXPECT ONE NAME PER OBJECT WHEN PICKING\n");
    }
    bufferPtr = bufferPtr + 3 + numberOfNames;
    count = count + 1;
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
  glGetDoublev( GL_MODELVIEW_MATRIX, modelview );
  glGetDoublev( GL_PROJECTION_MATRIX, projection );
  glGetIntegerv(GL_VIEWPORT,viewport);//returns four values: the x and y window coordinates of the viewport, followed by its width and height.
  winX = (float)x;
  winY = (float)viewport[3] - (float)y;
  gluUnProject( winX, winY, mapDepth, modelview, projection, viewport, posX, posY, posZ);
}
/**************************** /mouse hover object selection ********************************/

/************************************* drawing subroutines ***************************************/
float returnVal;
float translateTilesXToPositionX(int tileX,int tileY,long mapPolarity){
  //return (float)tilesX*-(1.9*SIN60);
  returnVal = (float)tileX*-(2.0*SIN60);
  if(abs(tileY)%2 == mapPolarity){
    returnVal += SIN60;
  }
  return returnVal;
}
float translateTilesYToPositionY(int tileY){
    return (float)tileY*1.5;
}

double xPosition;
double yPosition;
float shading;
char playerStartVal[2];
void drawTile(int tilesXIndex, int tilesYIndex, long name, long tileValue, long roadValue,char * cityName,long isSelected, long isOnMovePath, long isVisible, long mapPolarity,long playerStartValue,PyObject * pyUnit, int isNextUnit, long cursorIndex){
  xPosition = translateTilesXToPositionX(tilesXIndex,tilesYIndex,mapPolarity);
  yPosition = translateTilesYToPositionY(tilesYIndex);
  textureVertices = vertexArrays[tileValue];
  shading = 1.0;
  if(!isVisible){
    shading = shading - 0.5;
  }
  if(name == selectedName){
    shading = shading - 0.4;
    if(cursorIndex >= 0){
      theCursorIndex = (int)cursorIndex;
    }
  }else if(isSelected == 1){
    shading = shading - 0.4;
  }
glBindTexture(GL_TEXTURE_2D, tilesTexture);

  glColor3f(shading,shading,shading);
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


  //  playableMode = PyObject_GetAttrString(gameMode, "units");//if the mode has units, it's playable
  if(playerStartValue >= 1 && !PyObject_HasAttrString(gameMode,"units")){
    textureVertices = vertexArrays[PLAYER_START_TILE_INDEX];
    glBegin(GL_POLYGON);
    glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xPosition, hexagonVertices[0][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xPosition, hexagonVertices[1][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xPosition, hexagonVertices[2][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xPosition, hexagonVertices[3][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xPosition, hexagonVertices[4][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xPosition, hexagonVertices[5][1]+yPosition, 0.0);
    glEnd();
    sprintf(playerStartVal,"%ld",playerStartValue);
    glColor3f(1.0,1.0,1.0);
    //    glColor3f(0.0,0.0,0.0);
    glPushMatrix();
    glTranslatef(xPosition-0.7,yPosition-0.4,0.0);
    glScalef(0.02,0.02,0.0);
    drawText(playerStartVal);
    glPopMatrix();
  }

  if(pyUnit != NULL && pyUnit != Py_None && isVisible){
      pyUnitType = PyObject_GetAttrString(pyUnit,"unitType");
      pyUnitTextureIndex = PyObject_GetAttrString(pyUnitType,"textureIndex");
      pyName = PyObject_GetAttrString(pyUnitType,"name");
      unitName = PyString_AsString(pyName);
      pyHealth = PyObject_GetAttrString(pyUnit,"health");
      pyMaxHealth = PyObject_GetAttrString(pyUnitType,"health");
      pyPlayerNumber = PyObject_GetAttrString(pyUnit,"player");
      playerNumber = PyLong_AsLong(pyPlayerNumber);
      unitTextureIndex = PyLong_AsLong(pyUnitTextureIndex);
      healthBarLength = 1.5*PyLong_AsLong(pyHealth)/PyLong_AsLong(pyMaxHealth);

      glColor3f(1.0,1.0,1.0);
      if(isNextUnit == 1){
glBindTexture(GL_TEXTURE_2D, texturesArray[SELECTION_BOX_INDEX]);
glBegin(GL_QUADS);
glTexCoord2f(0.0,0.0);
glVertex3f(xPosition-0.9, yPosition-1.0, 0.0);
glTexCoord2f(1.0,0.0);
glVertex3f(xPosition+0.78, yPosition-1.0, 0.0);
glTexCoord2f(1.0,1.0);
glVertex3f(xPosition+0.78, yPosition+1.0, 0.0);
glTexCoord2f(0.0,1.0);
glVertex3f(xPosition-0.9, yPosition+1.0, 0.0);
glEnd();
focusXPos = xPosition;
focusYPos = yPosition;
      }else{
glBindTexture(GL_TEXTURE_2D, texturesArray[UNIT_CIRCLE_RED_INDEX+playerNumber-1]);
glBegin(GL_QUADS);
glTexCoord2f(0.0,0.0);
glVertex3f(xPosition-0.9, yPosition-1.0, 0.0);
glTexCoord2f(1.0,0.0);
glVertex3f(xPosition+0.78, yPosition-1.0, 0.0);
glTexCoord2f(1.0,1.0);
glVertex3f(xPosition+0.78, yPosition+1.0, 0.0);
glTexCoord2f(0.0,1.0);
glVertex3f(xPosition-0.9, yPosition+1.0, 0.0);
glEnd();
      }

      glBindTexture(GL_TEXTURE_2D, texturesArray[unitTextureIndex]);
      glBegin(GL_QUADS);
      glTexCoord2f(0.0,0.0);
      glVertex3f(xPosition-0.8, yPosition-0.75, 0.0);
      glTexCoord2f(1.0,0.0);
      glVertex3f(xPosition+0.7, yPosition-0.75, 0.0);
      glTexCoord2f(1.0,1.0);
      glVertex3f(xPosition+0.7, yPosition+0.75, 0.0);
      glTexCoord2f(0.0,1.0);
      glVertex3f(xPosition-0.8, yPosition+0.75, 0.0);
      glEnd();

      glBindTexture(GL_TEXTURE_2D, texturesArray[HEALTH_BAR_INDEX]);
      glBegin(GL_QUADS);
      glTexCoord2f(0.0,0.0);
      glVertex3f(xPosition-.75, yPosition+1.05, 0.001);
      glTexCoord2f(1.0,0.0);
      glVertex3f(xPosition+.75, yPosition+1.05, 0.001);
      glTexCoord2f(1.0,1.0);
      glVertex3f(xPosition+.75, yPosition+0.85, 0.001);
      glTexCoord2f(0.0,1.0);
      glVertex3f(xPosition-.75, yPosition+0.85, 0.001);
      glEnd();
 
      glBegin(GL_QUADS);
      glColor3f(255.0, 0.0, 0.0);
      glTexCoord2f(0.0,0.0);
      glVertex3f(xPosition-.75, yPosition+1.05, 0.001);
      glTexCoord2f(1.0,0.0);
      glVertex3f(xPosition-.75+healthBarLength, yPosition+1.05, 0.001);
      glTexCoord2f(1.0,1.0);
      glVertex3f(xPosition-.75+healthBarLength, yPosition+0.85, 0.001);
      glTexCoord2f(0.0,1.0);
      glVertex3f(xPosition-.75, yPosition+0.85, 0.001);
      glEnd();

      /*      unitNamesXs[unitNamesCount] = xPosition+1.0;
      unitNamesYs[unitNamesCount] = yPosition-1.3;
      strcpy(unitNames[unitNamesCount],unitName);
      unitNamesCount = unitNamesCount + 1;
      */
      Py_DECREF(pyUnitType);
      Py_DECREF(pyUnitTextureIndex);
      Py_DECREF(pyName);
      Py_DECREF(pyHealth);
      Py_DECREF(pyMaxHealth);
      Py_DECREF(pyPlayerNumber);
  }
  if(cityName[0]!=0){
    glColor3f(1.0f, 1.0f, 1.0f);
    glBindTexture(GL_TEXTURE_2D, texturesArray[CITY_INDEX]);
    glBegin(GL_POLYGON);
    glTexCoord2f(0.0,0.0);
    glVertex3f(xPosition-0.6, yPosition-0.75, 0.0);
    glTexCoord2f(1.0,0.0);
    glVertex3f(xPosition+0.6, yPosition-0.75, 0.0);
    glTexCoord2f(1.0,1.0);
    glVertex3f(xPosition+0.6, yPosition+0.75, 0.0);
    glTexCoord2f(0.0,1.0);
    glVertex3f(xPosition-0.6, yPosition+0.75, 0.0);
    glEnd();

    /*    cityNamesXs[cityNamesCount] = xPosition;
    cityNamesYs[cityNamesCount] = yPosition;
    strcpy(cityNames[cityNamesCount],cityName);
    cityNamesCount = cityNamesCount + 1;
    */
  }
  if(isOnMovePath){
    glBindTexture(GL_TEXTURE_2D, texturesArray[WALK_ICON_INDEX]);
    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(xPosition+0.5,yPosition-0.5,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(xPosition-0.5,yPosition-0.5,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(xPosition-0.5,yPosition+0.5,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(xPosition+0.5,yPosition+0.5,0.0);
    glEnd();
    glBindTexture(GL_TEXTURE_2D, tilesTexture);
  }
  /*
  glPushMatrix();
  glColor3f(shading,shading,shading);
  glTranslatef(xPosition,yPosition,0.0);

  glPushName(name);
    glBindTexture(GL_TEXTURE_2D, tilesTexture);
    glBegin(GL_POLYGON);
    glTexCoord2f(*(vertexArrays[tileValue]+0),*(vertexArrays[tileValue]+1)); glVertex3f(hexagonVertices[0][0], hexagonVertices[0][1], 0.0);
    glTexCoord2f(*(vertexArrays[tileValue]+2),*(vertexArrays[tileValue]+3)); glVertex3f(hexagonVertices[1][0], hexagonVertices[1][1], 0.0);
    glTexCoord2f(*(vertexArrays[tileValue]+4),*(vertexArrays[tileValue]+5)); glVertex3f(hexagonVertices[2][0], hexagonVertices[2][1], 0.0);
    glTexCoord2f(*(vertexArrays[tileValue]+6),*(vertexArrays[tileValue]+7)); glVertex3f(hexagonVertices[3][0], hexagonVertices[3][1], 0.0);
    glTexCoord2f(*(vertexArrays[tileValue]+8),*(vertexArrays[tileValue]+9)); glVertex3f(hexagonVertices[4][0], hexagonVertices[4][1], 0.0);
    glTexCoord2f(*(vertexArrays[tileValue]+10),*(vertexArrays[tileValue]+11)); glVertex3f(hexagonVertices[5][0], hexagonVertices[5][1], 0.0);
    glEnd();
    //  glCallList(tilesLists+tileValue);
  glPopName();

  if(roadValue == 1){
    glCallList(tilesLists+ROAD_TILE_INDEX);
  }

  if(playerStartValue >= 1 && !PyObject_HasAttrString(gameMode,"units")){
    textureVertices = vertexArrays[PLAYER_START_TILE_INDEX];
    glCallList(tilesLists+PLAYER_START_TILE_INDEX);
    sprintf(playerStartVal,"%ld",playerStartValue);

    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(-0.4,0.3,0.0);
    glScalef(0.01,0.01,0.0);
    drawText(playerStartVal);
    glPopMatrix();
  }

  if(pyUnit != NULL && pyUnit != Py_None && isVisible){
      pyUnitType = PyObject_GetAttrString(pyUnit,"unitType");
      pyUnitTextureIndex = PyObject_GetAttrString(pyUnitType,"textureIndex");
      pyName = PyObject_GetAttrString(pyUnitType,"name");
      unitName = PyString_AsString(pyName);
      pyHealth = PyObject_GetAttrString(pyUnit,"health");
      pyMaxHealth = PyObject_GetAttrString(pyUnitType,"health");
      pyPlayerNumber = PyObject_GetAttrString(pyUnit,"player");
      playerNumber = PyLong_AsLong(pyPlayerNumber);
      unitTextureIndex = PyLong_AsLong(pyUnitTextureIndex);
      healthBarLength = 1.5*PyLong_AsLong(pyHealth)/PyLong_AsLong(pyMaxHealth);

      glColor3f(1.0,1.0,1.0);
      if(isNextUnit == 1){
	glBindTexture(GL_TEXTURE_2D, texturesArray[SELECTION_BOX_INDEX]);
	focusXPos = xPosition;
	focusYPos = yPosition;
      }else{
	glBindTexture(GL_TEXTURE_2D, texturesArray[UNIT_CIRCLE_RED_INDEX+playerNumber-1]);
      }
      glCallList(selectionBoxList);
      glBindTexture(GL_TEXTURE_2D, texturesArray[unitTextureIndex]);
      glCallList(unitList);
      glBindTexture(GL_TEXTURE_2D, texturesArray[HEALTH_BAR_INDEX]);
      glCallList(healthBarList);

      glColor3f(255.0, 0.0, 0.0);
      glBegin(GL_QUADS);
      glTexCoord2f(0.0,0.0);
      glVertex3f(-.75, 1.05, 0.001);
      glTexCoord2f(1.0,0.0);
      glVertex3f(-.75+healthBarLength, 1.05, 0.001);
      glTexCoord2f(1.0,1.0);
      glVertex3f(-.75+healthBarLength, 0.85, 0.001);
      glTexCoord2f(0.0,1.0);
      glVertex3f(-.75, 0.85, 0.001);
      glEnd();

      Py_DECREF(pyUnitType);
      Py_DECREF(pyUnitTextureIndex);
      Py_DECREF(pyName);
      Py_DECREF(pyHealth);
      Py_DECREF(pyMaxHealth);
      Py_DECREF(pyPlayerNumber);
  }
  if(cityName[0]!=0){
    glColor3f(1.0f, 1.0f, 1.0f);
    glBindTexture(GL_TEXTURE_2D, texturesArray[CITY_INDEX]);
    glBegin(GL_POLYGON);
    glTexCoord2f(0.0,0.0);
    glVertex3f(-0.6, -0.75, 0.0);
    glTexCoord2f(1.0,0.0);
    glVertex3f(0.6, -0.75, 0.0);
    glTexCoord2f(1.0,1.0);
    glVertex3f(0.6, 0.75, 0.0);
    glTexCoord2f(0.0,1.0);
    glVertex3f(-0.6, 0.75, 0.0);
    glEnd();

  }
  if(isOnMovePath){
    glBindTexture(GL_TEXTURE_2D, texturesArray[WALK_ICON_INDEX]);
    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(0.5,-0.5,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(-0.5,-0.5,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(-0.5,0.5,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(0.5,0.5,0.0);
    glEnd();
    glBindTexture(GL_TEXTURE_2D, tilesTexture);
  }
  glPopMatrix();
*/
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
    drawText(cityNames[i]);
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
    drawText(unitNames[i]);
    glPopMatrix();
  }
  unitNamesCount = 0;*/
}
int rowNumber;
PyObject * node;
PyObject * row;
PyObject * polarity;
long longPolarity;
int colNumber = 0;
PyObject * nodeIterator;
PyObject * nodeName;
PyObject * nodeValue;
PyObject * roadValue;
PyObject * pyCity;
PyObject * pyCursorIndex;
PyObject * pyPlayerStartValue;
PyObject * pyUnit;
PyObject * pyIsSelected;
PyObject * pyIsOnMovePath;
PyObject * pyIsVisible;
long longName;
long longValue;
long longRoadValue;
long cursorIndex;
PyObject * pyCityName;
char * cityName;
int isNextUnit;
PyObject * nextUnit;
PyObject * unit;
PyObject * pyPlayerNumber;
PyObject * pyUnitPlayer;
long playerNumber;
long unitPlayer;
long playerStartValue;
long isSelected;
long isOnMovePath;
long isVisible;
void drawTiles(){
  rowNumber = -1;
  mapIterator = PyObject_CallMethod(theMap,"getIterator",NULL);//New reference
  polarity = PyObject_GetAttrString(theMap,"polarity");//New reference
  longPolarity = PyLong_AsLong(polarity);
  rowIterator = PyObject_GetIter(mapIterator);
  while (row = PyIter_Next(rowIterator)) {
    colNumber = 0;
    rowNumber = rowNumber + 1;
    nodeIterator = PyObject_GetIter(row);
    while(node = PyIter_Next(nodeIterator)) {
      nodeName = PyObject_GetAttrString(node,"name");//New reference
      nodeValue = PyObject_CallMethod(node,"getValue",NULL);//New reference
      roadValue = PyObject_GetAttrString(node,"roadValue");//New reference
      pyCity = PyObject_GetAttrString(node,"city");//New reference
      pyCursorIndex = PyObject_GetAttrString(node,"cursorIndex");//New reference
      pyPlayerStartValue = PyObject_GetAttrString(node,"playerStartValue");//New reference                                 
      pyUnit = PyObject_GetAttrString(node,"unit");
      pyIsSelected = PyObject_GetAttrString(node,"selected");//New reference
      pyIsOnMovePath = PyObject_GetAttrString(node,"onMovePath");//New reference
      pyIsVisible = PyObject_GetAttrString(node,"visible");//New reference
      longName = PyLong_AsLong(nodeName);
      longValue = PyLong_AsLong(nodeValue);
      longRoadValue = PyLong_AsLong(roadValue);
      cursorIndex = PyLong_AsLong(pyCursorIndex);
      cityName = "";//TODO: REMOVE ME
      if(pyCity != Py_None){
	pyCityName = PyObject_GetAttrString(pyCity,"name");
	cityName = PyString_AsString(pyCityName);
      }
      isNextUnit = 0;
      nextUnit = PyObject_GetAttrString(gameMode,"nextUnit");
      unit = PyObject_GetAttrString(node,"unit");
      pyPlayerNumber = PyObject_CallMethod(gameState,"getPlayerNumber",NULL);//New reference
      pyUnitPlayer = PyObject_GetAttrString(unit,"player");
      playerNumber = PyLong_AsLong(pyPlayerNumber);
      unitPlayer = PyLong_AsLong(pyUnitPlayer);
      if(unit != Py_None && unit == nextUnit && (playerNumber == unitPlayer || playerNumber == -2)){
	  isNextUnit = 1;
	  Py_DECREF(unit);
	  Py_DECREF(pyUnitPlayer);
      }
      playerStartValue = PyLong_AsLong(pyPlayerStartValue);
      isSelected = PyLong_AsLong(pyIsSelected);
      isOnMovePath = PyLong_AsLong(pyIsOnMovePath);
      isVisible = PyLong_AsLong(pyIsVisible);
      Py_DECREF(nodeName);
      Py_DECREF(nodeValue);
      Py_DECREF(roadValue);
      Py_DECREF(pyCity);
      Py_DECREF(pyCursorIndex);
      Py_DECREF(pyPlayerStartValue);
      Py_DECREF(pyIsSelected);
      Py_DECREF(pyIsOnMovePath);
      if(pyIsVisible != NULL){
	Py_DECREF(pyIsVisible);
      }
      Py_DECREF(node);
      if(nextUnit != NULL){
	Py_DECREF(nextUnit);
      }
      Py_DECREF(pyPlayerNumber);
      drawTile(colNumber,rowNumber,longName,longValue,longRoadValue,cityName,isSelected,isOnMovePath,isVisible,longPolarity,playerStartValue,pyUnit,isNextUnit,cursorIndex);
      Py_DECREF(pyUnit);
      colNumber = colNumber - 1;
    }
    Py_DECREF(row);
    Py_DECREF(nodeIterator);
  }
  Py_DECREF(rowIterator); 
  Py_DECREF(mapIterator);
  Py_DECREF(polarity);
}


PyObject * pyTranslateZ;
float mapRightOffset;
float mapTopOffset;
void calculateTranslation(){
  mouseMapPosXPrevious = mouseMapPosX;
  mouseMapPosYPrevious = mouseMapPosY;
  pyMapWidth = PyObject_CallMethod(theMap,"getWidth",NULL);//New reference
  pyMapHeight = PyObject_CallMethod(theMap,"getHeight",NULL);//New reference
  mapWidth = PyLong_AsLong(pyMapWidth);
  mapHeight = PyLong_AsLong(pyMapHeight);
  convertWindowCoordsToViewportCoords(UI_MAP_EDITOR_LEFT_IMAGE_WIDTH,SCREEN_HEIGHT-UI_MAP_EDITOR_TOP_IMAGE_HEIGHT-UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT,translateZ,&convertedBottomLeftX,&convertedBottomLeftY,&convertedBottomLeftZ);
  convertWindowCoordsToViewportCoords(SCREEN_WIDTH-UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH,0.0,translateZ,&convertedTopRightX,&convertedTopRightY,&convertedTopRightZ);
  convertWindowCoordsToViewportCoords(mouseX,mouseY,translateZ,&mouseMapPosX,&mouseMapPosY,&mouseMapPosZ);
  pyTranslateZ = PyObject_GetAttrString(theMap,"translateZ");
  translateZ = PyFloat_AsDouble(pyTranslateZ);
  mapRightOffset = translateTilesXToPositionX(mapWidth+1,0,0);
  mapTopOffset = translateTilesYToPositionY(mapHeight);
  //printf("screen topright %f,%f\n",convertedTopRightX,convertedTopRightY);
  //printf("screen bottomleft %f,%f\n",convertedBottomLeftX,convertedBottomLeftY);
  //printf("translate %f,%f\n",translateX,translateY);
  //printf("%f\n",translateTilesYToPositionY(mapHeight));//setting translateY to this number will focus on it
  //printf("mouse %d:%f\t%d:%f\n",mouseX,mouseMapPosX,mouseY,mouseMapPosY);
  
  if(clickScroll > 0){
    translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
    translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
  }else{
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
  if(isFocusing){
    //printf("%f %f %f %f\n",translateXPrev,translateX,translateYPrev,translateY);
    if((considerDoneFocusing == 1) && abs(50.0*(translateXPrev - translateX)) == 0 && abs(50.0*(translateYPrev - translateY)) == 0){//this indicates the auto-scrolling code is not allowing us to move any more
      isFocusing = 0;
      considerDoneFocusing = 0;
      if(PyObject_HasAttrString(gameMode,"onDoneFocusing")){
	pyObj = PyObject_CallMethod(gameMode,"onDoneFocusing",NULL);//New reference
	Py_DECREF(pyObj);
      }
    }else if(abs(50.0*(translateXPrev - translateX)) == 0 && abs(50.0*(translateYPrev - translateY)) == 0){//this indicates the auto-scrolling code is not allowing us to move any more
      considerDoneFocusing = 1;
    }
    translateXPrev = translateX;
    translateYPrev = translateY;
    translateX = translateX-((translateX+focusXPos)/focusSpeed);
    translateY = translateY-((translateY+focusYPos)/focusSpeed);
  }
  if(abs(100.0*(translateZ - translateZPrev)) > 0){
    translateZ = translateZPrev + ((translateZ - translateZPrev)/zoomSpeed);
    translateZPrev = translateZ;
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
    translateY = convertedTopRightY-mapTopOffset;
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
  //glTranslatef(translateX,translateY,mouseMapPosZ);
  if(theMap != Py_None){
    Py_DECREF(pyMapWidth);
    Py_DECREF(pyMapHeight);
  }
}

drawBoard(){
  if(theMap != Py_None){
    drawTiles();
    drawTilesText();
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
PyObject * pyXPosition;
PyObject * pyYPosition;
PyObject * pyWidth;
PyObject * pyHeight;
PyObject * pyHidden;
PyObject * pyName;
PyObject * pyTextureIndex;
PyObject * pyCursorIndex;
PyObject * pyText;
PyObject * pyTextColor;
PyObject * pyTextSize;
PyObject * pyColor;
PyObject * pyMouseOverColor;
PyObject * pyTextXPosition;
PyObject * pyTextYPosition;

//double xPosition;
//double yPosition;
double width;
double height;
int hidden;
long name;
long textureIndex;
long cursorIndex;
char * text;
char * textColor;
double textSize;
char * color;
char * mouseOverColor;
double textXPosition;
double textYPosition;

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
    pyCursorIndex = PyObject_GetAttrString(uiElement,"cursorIndex");
    pyText = PyObject_GetAttrString(uiElement,"text");
    pyTextColor = PyObject_GetAttrString(uiElement,"textColor");
    pyTextSize = PyObject_GetAttrString(uiElement,"textSize");
    pyColor = PyObject_GetAttrString(uiElement,"color");
    pyMouseOverColor = PyObject_GetAttrString(uiElement,"mouseOverColor");
    pyTextXPosition = PyObject_GetAttrString(uiElement,"textXPos");
    pyTextYPosition = PyObject_GetAttrString(uiElement,"textYPos");

    xPosition = PyFloat_AsDouble(pyXPosition);
    yPosition = PyFloat_AsDouble(pyYPosition);
    width = PyFloat_AsDouble(pyWidth);
    height = PyFloat_AsDouble(pyHeight);
    hidden = pyHidden==Py_True;
    name = PyLong_AsLong(pyName);
    textureIndex = PyLong_AsLong(pyTextureIndex);
    cursorIndex = PyLong_AsLong(pyCursorIndex);
    text = PyString_AsString(pyText);
    textColor = PyString_AsString(pyTextColor);
    textSize = PyFloat_AsDouble(pyTextSize);
    color = PyString_AsString(pyColor);
    mouseOverColor = PyString_AsString(pyMouseOverColor);
    textXPosition = PyFloat_AsDouble(pyTextXPosition);
    textYPosition = PyFloat_AsDouble(pyTextYPosition);
     
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
    Py_DECREF(pyMouseOverColor);
    Py_DECREF(pyTextXPosition);
    Py_DECREF(pyTextYPosition);

    if(previousMousedoverName != selectedName){
      if(PyObject_HasAttrString(gameMode,"handleMouseOver")){
	pyObj = PyObject_CallMethod(gameMode,"handleMouseOver","(ii)",selectedName,leftButtonDown);//New reference
	Py_DECREF(pyObj);
      }
      previousMousedoverName = selectedName;
    }
    printPyStackTrace();

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
	  glTexCoord2f(0.0,1.0); glVertex3f(xPosition,yPosition,0.0);
	  glTexCoord2f(1.0,1.0); glVertex3f(xPosition+width,yPosition,0.0);
	  glTexCoord2f(1.0,0.0); glVertex3f(xPosition+width,yPosition-height,0.0);
	  glTexCoord2f(0.0,0.0); glVertex3f(xPosition,yPosition-height,0.0);
	  glEnd();
	  glPopName();
	  glPopMatrix();
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
	  glPushMatrix();
	  glLoadIdentity();
	  glTranslatef(xPosition+textXPosition,yPosition+textYPosition,0.0);
	  glScalef(textSize,textSize,0.0);
	  glPushName(name);
	  drawText(text);
	  glPopName();
	  glPopMatrix();
	}
      }
      Py_DECREF(uiElement);
      if(name == selectedName && cursorIndex >= 0){
	theCursorIndex = cursorIndex;
      }
    }
  }
}
float xPos;
float yPos;
float pointerWidth;
float pointerHeight;
char frameRate[20];
void drawUI(){
  pyObj = PyObject_CallMethod(gameMode,"getUIElementsIterator",NULL);
  UIElementsIterator = PyObject_GetIter(pyObj);//New reference
  while (uiElement = PyIter_Next(UIElementsIterator)) {
    drawUIElement(uiElement);
  }
  Py_DECREF(pyObj);
  Py_DECREF(UIElementsIterator);

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
    drawText(frameRate);
    glPopMatrix();
  }
}
/************************************* /drawing subroutines ***************************************/

/************************************** opengl init **************************************/
static void initGL (){
  /** needs to be called on screen resize **/
  //unneeded with sdl?

  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);//default values anyway, so not needed but w/e
  glInitNames(); //init names stack	
  glClearColor(0.0, 0.0, 0.0, 0.0); //sets screen clear color
  glClearDepth(0.0);

  //glClearColor(1.0, 1.0, 1.0, 1.0); //sets screen clear color
  //glClearColor(123.0/255.0,126.0/255.0,125.0/255.0,1.0);//grey that matches the UI...
  glEnable(GL_DEPTH_TEST);
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);     
  //  glClear(GL_COLOR_BUFFER_BIT);
  glDepthFunc(GL_LEQUAL);
  screenRatio = (GLfloat)SCREEN_WIDTH/(GLfloat)SCREEN_HEIGHT;

  char file[100] = TILES_IMAGE;

  pngLoad(&tilesTexture, TILES_IMAGE);	/******************** /image init ***********************/
  pngLoad(&texturesArray[TILE_SELECT_BOX_INDEX],TILE_SELECT_BOX_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_TOP_INDEX],UI_MAP_EDITOR_TOP_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_BOTTOM_INDEX],UI_MAP_EDITOR_BOTTOM_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_LEFT_INDEX],UI_MAP_EDITOR_LEFT_IMAGE);
  pngLoad(&texturesArray[UI_MAP_EDITOR_RIGHT_INDEX],UI_MAP_EDITOR_RIGHT_IMAGE);
  pngLoad(&texturesArray[UI_NEW_GAME_SCREEN_INDEX],UI_NEW_GAME_SCREEN_IMAGE);
  pngLoad(&texturesArray[CURSOR_POINTER_INDEX],CURSOR_POINTER_IMAGE);
  pngLoad(&texturesArray[CURSOR_POINTER_ON_INDEX],CURSOR_POINTER_ON_IMAGE);
  pngLoad(&texturesArray[CURSOR_MOVE_INDEX],CURSOR_MOVE_IMAGE);
  pngLoad(&texturesArray[PLAYER_START_BUTTON_INDEX],PLAYER_START_BUTTON_IMAGE);
  pngLoad(&texturesArray[UI_SCROLLABLE_INDEX],UI_SCROLLABLE_IMAGE);
  pngLoad(&texturesArray[UI_SCROLL_PAD_INDEX],UI_SCROLL_PAD_IMAGE);
  pngLoad(&texturesArray[UI_TEXT_INPUT_INDEX],UI_TEXT_INPUT_IMAGE);
  pngLoad(&texturesArray[MEEPLE_INDEX],MEEPLE_IMAGE);
  pngLoad(&texturesArray[HEALTH_BAR_INDEX],HEALTH_BAR_IMAGE);
  pngLoad(&texturesArray[UNIT_BUILD_BAR_INDEX],UNIT_BUILD_BAR_IMAGE);
  pngLoad(&texturesArray[MAP_ICON_INDEX],MAP_ICON_IMAGE);
  pngLoad(&texturesArray[WALK_ICON_INDEX],WALK_ICON_IMAGE);
  pngLoad(&texturesArray[ADD_BUTTON_INDEX],ADD_BUTTON_IMAGE);
  pngLoad(&texturesArray[REMOVE_BUTTON_INDEX],REMOVE_BUTTON_IMAGE);
  pngLoad(&texturesArray[CITY_VIEWER_BOX_INDEX],CITY_VIEWER_BOX_IMAGE);
  pngLoad(&texturesArray[UNIT_TYPE_VIEWER_BOX_INDEX],UNIT_TYPE_VIEWER_BOX_IMAGE);
  pngLoad(&texturesArray[UNIT_VIEWER_BOX_INDEX],UNIT_VIEWER_BOX_IMAGE);
  pngLoad(&texturesArray[RESEARCH_BOX_INDEX],RESEARCH_BOX_IMAGE);
  pngLoad(&texturesArray[SELECTION_BRACKET_INDEX],SELECTION_BRACKET_IMAGE);
  pngLoad(&texturesArray[ADD_BUTTON_SMALL_INDEX],ADD_BUTTON_SMALL_IMAGE);
  pngLoad(&texturesArray[REMOVE_BUTTON_SMALL_INDEX],REMOVE_BUTTON_SMALL_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_RED_INDEX],UNIT_CIRCLE_RED_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_BLUE_INDEX],UNIT_CIRCLE_BLUE_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_GREEN_INDEX],UNIT_CIRCLE_GREEN_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_YELLOW_INDEX],UNIT_CIRCLE_YELLOW_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_PINK_INDEX],UNIT_CIRCLE_PINK_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_ORANGE_INDEX],UNIT_CIRCLE_ORANGE_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_PURPLE_INDEX],UNIT_CIRCLE_PURPLE_IMAGE);
  pngLoad(&texturesArray[UNIT_CIRCLE_BROWN_INDEX],UNIT_CIRCLE_BROWN_IMAGE);
  pngLoad(&texturesArray[CURSOR_ATTACK_INDEX],CURSOR_ATTACK_IMAGE);
  pngLoad(&texturesArray[CURSOR_HEAL_INDEX],CURSOR_HEAL_IMAGE);
  pngLoad(&texturesArray[ARCHER_INDEX],ARCHER_IMAGE);
  pngLoad(&texturesArray[SWORDSMAN_INDEX],SWORDSMAN_IMAGE);
  pngLoad(&texturesArray[SELECTION_BOX_INDEX],SELECTION_BOX_IMAGE);
  pngLoad(&texturesArray[SUMMONER_INDEX],SUMMONER_IMAGE);
  pngLoad(&texturesArray[CITY_INDEX],CITY_IMAGE);
  pngLoad(&texturesArray[GATHERER_INDEX],GATHERER_IMAGE);
  pngLoad(&texturesArray[DRAGON_INDEX],DRAGON_IMAGE);
  pngLoad(&texturesArray[WHITE_MAGE_INDEX],WHITE_MAGE_IMAGE);

  vertexArrays[DESERT_TILE_INDEX] = *desertVertices;
  vertexArrays[GRASS_TILE_INDEX] = *grassVertices;
  vertexArrays[MOUNTAIN_TILE_INDEX] = *mountainVertices;
  vertexArrays[FOREST_TILE_INDEX] = *forestVertices;
  vertexArrays[BLUE_FOREST_TILE_INDEX] = *blueForestVertices;
  vertexArrays[WATER_TILE_INDEX] = *waterVertices;
  vertexArrays[ROAD_TILE_INDEX] = *roadVertices;
  vertexArrays[CITY_TILE_INDEX] = *cityVertices;
  vertexArrays[PLAYER_START_TILE_INDEX] = *playerStartVertices;
  
  /*  tilesLists = glGenLists(30);

  int c = 0;
  for(;c<9;c++){

    glNewList(tilesLists+c,GL_COMPILE);    
    glBindTexture(GL_TEXTURE_2D, tilesTexture);
    glBegin(GL_POLYGON);
    glTexCoord2f(*(vertexArrays[c]+0),*(vertexArrays[c]+1)); glVertex3f(hexagonVertices[0][0], hexagonVertices[0][1], 0.0);
    glTexCoord2f(*(vertexArrays[c]+2),*(vertexArrays[c]+3)); glVertex3f(hexagonVertices[1][0], hexagonVertices[1][1], 0.0);
    glTexCoord2f(*(vertexArrays[c]+4),*(vertexArrays[c]+5)); glVertex3f(hexagonVertices[2][0], hexagonVertices[2][1], 0.0);
    glTexCoord2f(*(vertexArrays[c]+6),*(vertexArrays[c]+7)); glVertex3f(hexagonVertices[3][0], hexagonVertices[3][1], 0.0);
    glTexCoord2f(*(vertexArrays[c]+8),*(vertexArrays[c]+9)); glVertex3f(hexagonVertices[4][0], hexagonVertices[4][1], 0.0);
    glTexCoord2f(*(vertexArrays[c]+10),*(vertexArrays[c]+11)); glVertex3f(hexagonVertices[5][0], hexagonVertices[5][1], 0.0);
    glEnd();
    glEndList();
  }

  selectionBoxList = tilesLists+c+1;
  unitList = selectionBoxList+1;
  healthBarList = unitList+1;

  glNewList(selectionBoxList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-0.9,-1.0,0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(0.78,-1.0,0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(0.78,1.0, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-0.9,1.0, 0.0);
  glEnd();
  glEndList();

  glNewList(unitList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-0.8, -0.75, 0.0);
  glTexCoord2f(1.0,0.0);
  glVertex3f(0.7, -0.75, 0.0);
  glTexCoord2f(1.0,1.0);
  glVertex3f(0.7, 0.75, 0.0);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-0.8, 0.75, 0.0);
  glEnd();
  glEndList();

  glNewList(healthBarList,GL_COMPILE);    
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,0.0);
  glVertex3f(-.75, 1.05, 0.001);
  glTexCoord2f(1.0,0.0);
  glVertex3f(.75, 1.05, 0.001);
  glTexCoord2f(1.0,1.0);
  glVertex3f(.75, 0.85, 0.001);
  glTexCoord2f(0.0,1.0);
  glVertex3f(-.75, 0.85, 0.001);
  glEnd();
  glEndList();
  */

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
  //todo: decref these
}
SDL_Event event;
PyObject * pyFocusNextUnit;
char * key;
char capsKey[2];
static void handleInput(){
  deltaTicks = SDL_GetTicks()-previousTick;
  previousTick = SDL_GetTicks();
  if(PyObject_HasAttrString(gameMode,"getFocusNextUnit")){
    pyFocusNextUnit = PyObject_CallMethod(gameMode,"getFocusNextUnit",NULL);
    focusNextUnit = PyLong_AsLong(pyFocusNextUnit);
    if(focusNextUnit){
      isFocusing = 1;
    }
  }
  //SDL_Delay(20);//for framerate testing...
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
	//moveRight = -1;
      }else if(mouseX >= SCREEN_WIDTH-1){
	//moveRight = 1;
      }else{
	//moveRight = 0;
      }
      if(mouseY == 0){
	//moveUp = 1;
      }else if(mouseY >= SCREEN_HEIGHT-1){
	//moveUp = -1;
      }else{
	//moveUp = 0;
      }
      break;
    case SDL_MOUSEBUTTONDOWN:
      if(event.button.button == SDL_BUTTON_WHEELUP){
	if(PyObject_HasAttrString(gameMode,"handleScrollUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleScrollUp","(ii)",selectedName,deltaTicks);//New reference
	  Py_DECREF(pyObj);
	}
      }else if(event.button.button == SDL_BUTTON_WHEELDOWN){
	if(PyObject_HasAttrString(gameMode,"handleScrollDown")){
	  PyObject_CallMethod(gameMode,"handleScrollDown","(ii)",selectedName,deltaTicks);//New reference
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
	clickScroll = 1;
	//	PyObject_CallMethod(gameMode,"handleRightClick","i",selectedName);//New reference
      }
      break;
    case SDL_MOUSEBUTTONUP:
      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 0;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	if(PyObject_HasAttrString(gameMode,"handleLeftClickUp")){
	  pyObj = PyObject_CallMethod(gameMode,"handleLeftClickUp","i",selectedName);//New reference
	  Py_DECREF(pyObj);
	  printPyStackTrace();
	}
	leftButtonDown = 0;
      }
      if(event.button.button == SDL_BUTTON_RIGHT){
	clickScroll = 0;
      }
      break;
    case SDL_KEYDOWN:
      if(event.key.keysym.sym == SDLK_ESCAPE){
	done = 1;
      }else if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 1;
	avgDeltaTicks = 0;
	totalDeltaTicksDataPoints = 0;
      }else if(
	       (event.key.keysym.sym >= 0x61 && event.key.keysym.sym <= 0x7A)//a-z
	       || (event.key.keysym.sym >= 0x30 && event.key.keysym.sym <= 0x39)//0-9
	       || event.key.keysym.sym == 8//backspace
	       || event.key.keysym.sym == 32//space
	       || event.key.keysym.sym == 45//-
	       || event.key.keysym.sym == 46//.
	       || event.key.keysym.sym == 13//enter/return
	       || event.key.keysym.sym == 303//rightshift
	       || event.key.keysym.sym == 304//leftshift
	       || (event.key.keysym.sym >= 273 && event.key.keysym.sym <= 276)//arrow keys
	       ){
	if((event.key.keysym.mod & KMOD_CAPS | event.key.keysym.mod & KMOD_LSHIFT | event.key.keysym.mod & KMOD_RSHIFT) && (event.key.keysym.sym > 0x60 && event.key.keysym.sym <= 0x7A)){
	  key = SDL_GetKeyName(event.key.keysym.sym);
	  capsKey[0] = (*key)-32;
	  capsKey[1] = 0;
	  if(PyObject_HasAttrString(gameMode,"handleKeyDown")){
	    pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",capsKey); 
	    Py_DECREF(pyObj);

	  }
	}else{
	  if(PyObject_HasAttrString(gameMode,"handleKeyDown")){
	    pyObj = PyObject_CallMethod(gameMode,"handleKeyDown","s",SDL_GetKeyName(event.key.keysym.sym));
	    Py_DECREF(pyObj);
	    
	  }
	}
	//	printPyStackTrace();
      }else{
	printf("rejected: %d\n",event.key.keysym.sym);
      }
      break;
    case SDL_KEYUP:
      if(event.key.keysym.sym == SDLK_BACKQUOTE){
	clickScroll = 0;
      }else if(event.key.keysym.sym == 303//rightshift
	       || event.key.keysym.sym == 304//leftshift
	       ){
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
GLint viewport[4];
GLint hitsCnt;
static void draw(){
  if(PyObject_HasAttrString(gameMode,"onDraw")){
    pyObj = PyObject_CallMethod(gameMode,"onDraw",NULL);//New reference
    Py_DECREF(pyObj);
  }

  printPyStackTrace();
  glClearDepth(1.0);
  //this needs to be done before glClear...
  //when the mouse is under the pixel this breaks, so we test three points and find any two that match
  glReadPixels( 1*SCREEN_WIDTH/4, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest1 );
  glReadPixels( 2*SCREEN_WIDTH/4, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest2 );
  glReadPixels( 3*SCREEN_WIDTH/4, SCREEN_HEIGHT/2, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &mapDepthTest3 );
  if(mapDepthTest1 == mapDepthTest2 || mapDepthTest1 == mapDepthTest3){
    mapDepth = mapDepthTest1;
  }else if(mapDepthTest2 == mapDepthTest3){
    mapDepth = mapDepthTest2;
  }
  glFlush();
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		
  glRenderMode(GL_SELECT);
  glViewport(UI_MAP_EDITOR_LEFT_IMAGE_WIDTH,UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT,SCREEN_WIDTH - UI_MAP_EDITOR_LEFT_IMAGE_WIDTH - UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH, SCREEN_HEIGHT - UI_MAP_EDITOR_TOP_IMAGE_HEIGHT - UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT);
  theCursorIndex = -1;
    
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(45.0f,screenRatio,minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();


  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  
  glGetIntegerv(GL_VIEWPORT,viewport);
  glFlush();
  glSelectBuffer(BUFSIZE,selectBuf);
  gluPickMatrix(mouseX,viewport[3]+UI_MAP_EDITOR_TOP_IMAGE_HEIGHT+UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT-mouseY,1,1,viewport);
  glFlush();
  gluPerspective(45.0f,screenRatio,minZoom,maxZoom);
  
  glMatrixMode(GL_MODELVIEW);
  glTranslatef(translateX,translateY,translateZ);
  drawBoard();
  //  glPushMatrix();

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  glGetIntegerv(GL_VIEWPORT,viewport);
  glFlush();
  gluPickMatrix(mouseX,viewport[3]-mouseY,1,1,viewport);
  glFlush();
  
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  drawUI();
  glFlush();
  hitsCnt = glRenderMode(GL_RENDER);
  processTheHits(hitsCnt,selectBuf);
  //glRenderMode(GL_RENDER);
  glFlush();

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		

  glFlush();
    
  glViewport(UI_MAP_EDITOR_LEFT_IMAGE_WIDTH,UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT,SCREEN_WIDTH - UI_MAP_EDITOR_LEFT_IMAGE_WIDTH - UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH, SCREEN_HEIGHT - UI_MAP_EDITOR_TOP_IMAGE_HEIGHT - UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT);

  gluPerspective(45.0f,screenRatio,minZoom,maxZoom);


  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(45.0f,screenRatio,minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  calculateTranslation();
  glTranslatef(translateX,translateY,translateZ);

  drawBoard();  

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);    
  drawUI();

  glFlush();
  SDL_GL_SwapBuffers ();	
}
static void mainLoop (){
  while ( !done ) {
    
    gameMode = PyObject_CallMethod(gameState,"getGameMode",NULL);
    
    if(PyObject_HasAttrString(gameMode,"map")){
      theMap = PyObject_GetAttrString(gameMode, "map");//New reference
    }
    
    handleInput();
    
    draw();
    
    if(PyObject_HasAttrString(gameMode,"map")){
      Py_DECREF(theMap);
    }
    Py_DECREF(gameMode); 
 }
  pyObj = PyObject_CallMethod(gameMode,"onQuit",NULL);
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
  //  SDL_GL_SetAttribute (SDL_GL_DOUBLEBUFFER, 1);
  Uint32 flags = SDL_OPENGL;
  //flags |= SDL_FULLSCREEN;
  gScreen = SDL_SetVideoMode (SCREEN_WIDTH, SCREEN_HEIGHT, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Could not set OpenGL video mode: %s\n",
	     SDL_GetError());
    SDL_Quit();
    exit(2);
  }
  int * value;
  //  SDL_GL_GetAttribute(SDL_GL_DEPTH_SIZE,value);
  //printf("depth size: %d\n",*value);
  
  SDL_ShowCursor(0);
  
  initGL();
  const GLubyte * glVersion = glGetString(GL_VERSION);
  printf("OpenGL Version: %s\n",glVersion);
  
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
