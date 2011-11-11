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

#define maxZoom 50.0
#define minZoom 10.0
#define initZoom 30.0

#define zoomSpeed 30.0//lower is faster
#define focusSpeed 15.0//lower is faster

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

#define UNIT_CIRCLE_RED_IMAGE "assets/unitCircleRed.png"
#define UNIT_CIRCLE_RED_HEIGHT 40
#define UNIT_CIRCLE_RED_WIDTH 40
#define UNIT_CIRCLE_RED_INDEX 28

#define UNIT_CIRCLE_BLUE_IMAGE "assets/unitCircleBlue.png"
#define UNIT_CIRCLE_BLUE_HEIGHT 40
#define UNIT_CIRCLE_BLUE_WIDTH 40
#define UNIT_CIRCLE_BLUE_INDEX 29

#define UNIT_CIRCLE_GREEN_IMAGE "assets/unitCircleBlue.png"
#define UNIT_CIRCLE_GREEN_HEIGHT 40
#define UNIT_CIRCLE_GREEN_WIDTH 40
#define UNIT_CIRCLE_GREEN_INDEX 30
#define UNIT_CIRCLE_YELLOW_IMAGE "assets/unitCircleBlue.png"
#define UNIT_CIRCLE_YELLOW_HEIGHT 40
#define UNIT_CIRCLE_YELLOW_WIDTH 40
#define UNIT_CIRCLE_YELLOW_INDEX 31
#define UNIT_CIRCLE_PINK_IMAGE "assets/unitCircleBlue.png"
#define UNIT_CIRCLE_PINK_HEIGHT 40
#define UNIT_CIRCLE_PINK_WIDTH 40
#define UNIT_CIRCLE_PINK_INDEX 32
#define UNIT_CIRCLE_ORANGE_IMAGE "assets/unitCircleBlue.png"
#define UNIT_CIRCLE_ORANGE_HEIGHT 40
#define UNIT_CIRCLE_ORANGE_WIDTH 40
#define UNIT_CIRCLE_ORANGE_INDEX 33
#define UNIT_CIRCLE_PURPLE_IMAGE "assets/unitCircleBlue.png"
#define UNIT_CIRCLE_PURPLE_HEIGHT 40
#define UNIT_CIRCLE_PURPLE_WIDTH 40
#define UNIT_CIRCLE_PURPLE_INDEX 34
#define UNIT_CIRCLE_BROWN_IMAGE "assets/unitCircleBlue.png"
#define UNIT_CIRCLE_BROWN_HEIGHT 40
#define UNIT_CIRCLE_BROWN_WIDTH 40
#define UNIT_CIRCLE_BROWN_INDEX 35

#define CURSOR_ATTACK_IMAGE "assets/cursors/swordIcon.png"
#define CURSOR_ATTACK_INDEX 36

#define CURSOR_GATHER_IMAGE "assets/cursors/gatherCursor.png"
#define CURSOR_GATHER_INDEX 37

#define DESERT_TILE_INDEX 0
#define GRASS_TILE_INDEX 1
#define MOUNTAIN_TILE_INDEX 2
#define FOREST_TILE_INDEX 3
#define BLUE_FOREST_TILE_INDEX 4
#define WATER_TILE_INDEX 5
#define ROAD_TILE_INDEX 6
#define CITY_TILE_INDEX 7
#define PLAYER_START_TILE_INDEX 8//REMOVE THIS

#define DESERT_MOVE_COST 2.0
#define GRASS_MOVE_COST 1.0
#define MOUNTAIN_MOVE_COST 10.0
#define FOREST_MOVE_COST 1.0
#define WATER_MOVE_COST 10.0

#define SIN60 0.8660
#define COS60 0.5

#define BUFSIZE 512

float screenRatio;
static SDL_Surface *gScreen;

int clickScroll = 0;
long focusNextUnit = 0;
float focusXPos, focusYPos;
int isFocusing = 0;
int leftButtonDown = 0;

int done = 0;    
int moveUp = 0;
int moveRight = 0;
int previousTick = 0;
int deltaTicks = 0;

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
long mapWidth;
long mapHeight;

#define MAX_CITIES 40
#define MAX_CITY_NAME_LENGTH 50
#define MAX_UNITS 400
#define MAX_UNIT_NAME_LENGTH 50

float cityNamesXs[MAX_CITIES];
float cityNamesYs[MAX_CITIES];
char cityNames[MAX_CITIES][MAX_CITY_NAME_LENGTH];
int cityNamesCount = 0;

float unitNamesXs[MAX_UNITS];
float unitNamesYs[MAX_UNITS];
char unitNames[MAX_UNITS][MAX_UNIT_NAME_LENGTH];
int unitNamesCount = 0;

GLuint tilesTexture;
GLdouble mouseMapPosX, mouseMapPosY, mouseMapPosZ;
GLdouble mouseMapPosXPrevious, mouseMapPosYPrevious, mouseMapPosZPrevious = -initZoom;

int mouseX = 0;
int mouseY = 0;
GLuint selectBuf[BUFSIZE];
int selectedName = -1;//the mousedover object's 'name'
int previousClickedName = -2;
int previousMousedoverName = -2;
int theCursorIndex = -1;

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
float * vertexArrays[9];

float hexagonVertices[6][2] = {
  //cheated these all out by 0.01 so the black background doesn't bleed through
  {-SIN60-0.01, -COS60-0.01},
  {-SIN60-0.01, COS60+0.01},
  {0.01, 1.01},
  {SIN60+0.01, COS60+0.01},
  {SIN60+0.01, -COS60-0.01},
  {0.01, -1.01}
};

float *textureVertices;
GLuint texturesArray[60];

static void printPyStackTrace(){
  //put this thing after the call that is causing your problem!
  PyObject *exc_type, *exc_value, *exc_traceback;
    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    if(exc_type && exc_traceback){
      PyObject_CallMethodObjArgs(gameModule,PyString_FromString("printTraceBack"),exc_type,exc_value,exc_traceback,NULL);
      PyErr_Print();//This is supposed to print it but doesn't. i left it here so the exception gets cleared...
    }
}

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
void processTheHits(GLint hitsCount, GLuint buffer[]){
  GLuint *bufferPtr,*ptrNames, numberOfNames;
  int count = 0;
  int nameValue = 0;
  bufferPtr = (GLuint *) buffer;
  selectedName = -1;
  while(count < hitsCount){
    numberOfNames = *bufferPtr;
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
  //  printf("selectedname %d\n",selectedName);
}

//float glMouseCoords[3];
//void convertWindowCoordsToViewportCoords(int x, int y){
void convertWindowCoordsToViewportCoords(int x, int y, float z, GLdouble* posX, GLdouble* posY, GLdouble* posZ){
  //strange things happen with this when zoom/maxZoom is greater than 45...
  GLint viewport[4];
  GLdouble modelview[16];
  GLdouble projection[16];
  GLfloat winX, winY, winZ, winZOld;
  glGetDoublev( GL_MODELVIEW_MATRIX, modelview );
  glGetDoublev( GL_PROJECTION_MATRIX, projection );
  glGetIntegerv(GL_VIEWPORT,viewport);//returns four values: the x and y window coordinates of the viewport, followed by its width and height.
  winX = (float)x;
  winY = (float)viewport[3] - (float)y;
  gluUnProject( winX, winY, mapDepth, modelview, projection, viewport, posX, posY, posZ);
}
/**************************** /mouse hover object selection ********************************/

/************************************* drawing subroutines ***************************************/
float translateTilesXToPositionX(int tileX,int tileY,long mapPolarity){
  //return (float)tilesX*-(1.9*SIN60);
  float returnVal = (float)tileX*-(2.0*SIN60);
  if(abs(tileY)%2 == mapPolarity){
    returnVal += SIN60;
  }
  return returnVal;
}
float translateTilesYToPositionY(int tileY){
    //return (float)tileY*1.4;
    return (float)tileY*1.5;
}
void drawTile(int tilesXIndex, int tilesYIndex, long name, long tileValue, long roadValue,char * cityName,long isSelected, long isOnMovePath, long isVisible, long mapPolarity,long playerStartValue,PyObject * pyUnit, int isNextUnit, long cursorIndex){
  float xPosition = translateTilesXToPositionX(tilesXIndex,tilesYIndex,mapPolarity);
  float yPosition = translateTilesYToPositionY(tilesYIndex);
  textureVertices = vertexArrays[tileValue];
  float shading = 1.0;
  if(!isVisible){
    shading = shading - 0.5;
  }
  if(name == selectedName){
    shading = shading - 0.1;
    if(cursorIndex >= 0){
      theCursorIndex = (int)cursorIndex;
    }
  }
  //else{
  //  glColor3f(1.0f, 1.0f, 1.0f);
  //}
  if(isSelected == 1){
    shading = shading - 0.1;
  }
  if(isNextUnit == 1){
    shading = shading - 0.2;
    focusXPos = xPosition;
    focusYPos = yPosition;
  }
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
  if(cityName[0]!=0){

    textureVertices = vertexArrays[CITY_TILE_INDEX];
    glBegin(GL_POLYGON);
    glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xPosition, hexagonVertices[0][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xPosition, hexagonVertices[1][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xPosition, hexagonVertices[2][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xPosition, hexagonVertices[3][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xPosition, hexagonVertices[4][1]+yPosition, 0.0);
    glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xPosition, hexagonVertices[5][1]+yPosition, 0.0);
    glEnd();

    cityNamesXs[cityNamesCount] = xPosition;
    cityNamesYs[cityNamesCount] = yPosition;
    strcpy(cityNames[cityNamesCount],cityName);
    cityNamesCount = cityNamesCount + 1;

  }

  PyObject * playableMode = PyObject_GetAttrString(gameMode, "units");//if the mode has units, it's playable
  if(playerStartValue >= 1 && playableMode == NULL){
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

  if(pyUnit != NULL && pyUnit != Py_None && isVisible){
      PyObject * pyUnitType = PyObject_GetAttrString(pyUnit,"unitType");
      PyObject * pyUnitTextureIndex = PyObject_GetAttrString(pyUnitType,"textureIndex");
      PyObject * pyName = PyObject_GetAttrString(pyUnitType,"name");
      char * unitName = PyString_AsString(pyName);
      PyObject * pyHealth = PyObject_GetAttrString(pyUnit,"health");
      PyObject * pyMaxHealth = PyObject_GetAttrString(pyUnitType,"health");
      PyObject * pyPlayerNumber = PyObject_GetAttrString(pyUnit,"player");
      long playerNumber = PyLong_AsLong(pyPlayerNumber);
      float healthBarLength = 1.5*PyLong_AsLong(pyHealth)/PyLong_AsLong(pyMaxHealth);

      glColor3f(255.0, 255.0, 255.0);

      glBindTexture(GL_TEXTURE_2D, texturesArray[UNIT_CIRCLE_RED_INDEX+playerNumber-1]);
      glBegin(GL_QUADS);
      glTexCoord2f(0.0,0.0);
      glVertex3f(xPosition-0.7, yPosition-0.7, 0.0);
      glTexCoord2f(1.0,0.0);
      glVertex3f(xPosition+0.7, yPosition-0.7, 0.0);
      glTexCoord2f(1.0,1.0);
      glVertex3f(xPosition+0.7, yPosition+0.7, 0.0);
      glTexCoord2f(0.0,1.0);
      glVertex3f(xPosition-0.7, yPosition+0.7, 0.0);
      glEnd();

      glBindTexture(GL_TEXTURE_2D, texturesArray[MEEPLE_INDEX]);
      glBegin(GL_QUADS);
      glTexCoord2f(0.0,0.0);
      glVertex3f(xPosition-0.5, yPosition-0.5, 0.0);
      glTexCoord2f(1.0,0.0);
      glVertex3f(xPosition+0.5, yPosition-0.5, 0.0);
      glTexCoord2f(1.0,1.0);
      glVertex3f(xPosition+0.5, yPosition+0.5, 0.0);
      glTexCoord2f(0.0,1.0);
      glVertex3f(xPosition-0.5, yPosition+0.5, 0.0);
      glEnd();

      glBindTexture(GL_TEXTURE_2D, texturesArray[HEALTH_BAR_INDEX]);
      glBegin(GL_QUADS);
      glTexCoord2f(0.0,0.0);
      glVertex3f(xPosition-.75, yPosition-0.2, 0.0);
      glTexCoord2f(1.0,0.0);
      glVertex3f(xPosition+.75, yPosition-0.2, 0.0);
      glTexCoord2f(1.0,1.0);
      glVertex3f(xPosition+.75, yPosition-0.5, 0.0);
      glTexCoord2f(0.0,1.0);
      glVertex3f(xPosition-.75, yPosition-0.5, 0.0);
      glEnd();
 
      glBegin(GL_QUADS);
      glColor3f(255.0, 0.0, 0.0);
      glTexCoord2f(0.0,0.0);
      glVertex3f(xPosition-.75, yPosition-0.2, 0.0);
      glTexCoord2f(1.0,0.0);
      glVertex3f(xPosition-.75+healthBarLength, yPosition-0.2, 0.0);
      glTexCoord2f(1.0,1.0);
      glVertex3f(xPosition-.75+healthBarLength, yPosition-0.5, 0.0);
      glTexCoord2f(0.0,1.0);
      glVertex3f(xPosition-.75, yPosition-0.5, 0.0);
      glEnd();

      unitNamesXs[unitNamesCount] = xPosition+1.0;
      unitNamesYs[unitNamesCount] = yPosition-1.3;
      strcpy(unitNames[unitNamesCount],unitName);
      unitNamesCount = unitNamesCount + 1;
      
      Py_DECREF(pyUnitType);
      Py_DECREF(pyUnitTextureIndex);
      Py_DECREF(pyName);
      Py_DECREF(pyHealth);
      Py_DECREF(pyMaxHealth);
  }
  if(isOnMovePath){
    glBindTexture(GL_TEXTURE_2D, texturesArray[WALK_ICON_INDEX]);
    //    glPushMatrix();
    glColor3f(1.0f, 0.0f, 0.0f);
    glBegin(GL_QUADS);
    glTexCoord2f(0.0,0.0); glVertex3f(xPosition+0.5,yPosition-0.5,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(xPosition-0.5,yPosition-0.5,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(xPosition-0.5,yPosition+0.5,0.0);
    glTexCoord2f(0.0,1.0); glVertex3f(xPosition+0.5,yPosition+0.5,0.0);
    glEnd();
    //    glPopMatrix();
    glBindTexture(GL_TEXTURE_2D, tilesTexture);
  }
}
void drawTilesText(){
  int i,j,cityNameLength,unitNameLength = 0;
  for(i=0; i<cityNamesCount; i++){
    for(j=0; j<MAX_CITY_NAME_LENGTH; j++){
      if(cityNames[i][j] == 0){
	cityNameLength = j;
	break;
      }
    }
    glColor3f(1.0,1.0,1.0);
    glPushMatrix();
    glTranslatef(cityNamesXs[i]-(0.3*j),cityNamesYs[i]+0.5,0.0);
    glScalef(0.02,0.02,0.0);
    drawText(cityNames[i]);
    glPopMatrix();
  }
  cityNamesCount = 0;
  for(i=0; i<unitNamesCount; i++){
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
  unitNamesCount = 0;
}
void drawTiles(){
  
  int rowNumber = -1;
  PyObject * node;
  PyObject * row;

  mapIterator = PyObject_CallMethod(theMap,"getIterator",NULL);//New reference
  PyObject * polarity = PyObject_GetAttrString(theMap,"polarity");//New reference
  long longPolarity = PyLong_AsLong(polarity);

  rowIterator = PyObject_GetIter(mapIterator);
  while (row = PyIter_Next(rowIterator)) {
    int colNumber = 0;
    rowNumber = rowNumber + 1;
    PyObject * nodeIterator = PyObject_GetIter(row);
    while(node = PyIter_Next(nodeIterator)) {
      glBindTexture(GL_TEXTURE_2D, tilesTexture);
      PyObject * nodeName = PyObject_GetAttrString(node,"name");//New reference
      PyObject * nodeValue = PyObject_CallMethod(node,"getValue",NULL);//New reference
      PyObject * roadValue = PyObject_GetAttrString(node,"roadValue");//New reference
      PyObject * pyCity = PyObject_GetAttrString(node,"city");//New reference
      PyObject * pyCursorIndex = PyObject_GetAttrString(node,"cursorIndex");//New reference
      PyObject * pyPlayerStartValue = PyObject_GetAttrString(node,"playerStartValue");//New reference                                 
      PyObject * pyUnit = PyObject_GetAttrString(node,"unit");
      PyObject * pyIsSelected = PyObject_GetAttrString(node,"selected");//New reference
      PyObject * pyIsOnMovePath = PyObject_GetAttrString(node,"onMovePath");//New reference
      PyObject * pyIsVisible = PyObject_GetAttrString(node,"visible");//New reference
      long longName = PyLong_AsLong(nodeName);
      long longValue = PyLong_AsLong(nodeValue);
      long longRoadValue = PyLong_AsLong(roadValue);
      long cursorIndex = PyLong_AsLong(pyCursorIndex);
      long longCityValue = 0;
      PyObject * pyCityName;
      char * cityName = "";
      if(pyCity != Py_None){
	pyCityName = PyObject_GetAttrString(pyCity,"name");
	cityName = PyString_AsString(pyCityName);
	longCityValue = 1;
      }

      int isNextUnit = 0;
      PyObject * nextUnit = PyObject_GetAttrString(gameMode,"nextUnit");
      PyObject * unit = PyObject_GetAttrString(node,"unit");
      if(unit != Py_None){
	if(unit == nextUnit){
	  isNextUnit = 1;
	}
      }
      long playerStartValue = PyLong_AsLong(pyPlayerStartValue);
      long isSelected = PyLong_AsLong(pyIsSelected);
      long isOnMovePath = PyLong_AsLong(pyIsOnMovePath);
      long isVisible = PyLong_AsLong(pyIsVisible);

      Py_DECREF(nodeName);
      Py_DECREF(nodeValue);
      Py_DECREF(roadValue);
      Py_DECREF(pyCity);
      Py_DECREF(pyCursorIndex);
      Py_DECREF(pyPlayerStartValue);
      Py_DECREF(pyIsSelected);
      Py_DECREF(pyIsOnMovePath);
      Py_DECREF(pyIsVisible);
      Py_DECREF(node);
      drawTile(colNumber,rowNumber,longName,longValue,longRoadValue,cityName,isSelected,isOnMovePath,isVisible,longPolarity,playerStartValue,pyUnit,isNextUnit,cursorIndex);
      Py_DECREF(pyUnit);
      colNumber = colNumber - 1;
    }
    Py_DECREF(row);
  }
  Py_DECREF(rowIterator); 
  Py_DECREF(mapIterator);
  Py_DECREF(polarity);
}


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
  PyObject * pyTranslateZ = PyObject_GetAttrString(theMap,"translateZ");
  translateZ = PyFloat_AsDouble(pyTranslateZ);
  float mapRightOffset = translateTilesXToPositionX(mapWidth+1,0,0);
  float mapTopOffset = translateTilesYToPositionY(mapHeight);
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
    if(!focusNextUnit && abs(50.0*(translateXPrev - translateX)) == 0 && abs(50.0*(translateYPrev - translateY)) == 0){//this indicates the auto-scrolling code is not allowing us to move any more
      isFocusing = 0;
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
  //    Py_DECREF(pyMapWidth);//TODO: SEG FAULT????
  //    Py_DECREF(pyMapHeight);//TODO: SEG FAULT????
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
void drawUIElement(PyObject * uiElement){
  int isNode = PyObject_HasAttrString(uiElement,"tileValue");
  if(!isNode){
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

    if(previousMousedoverName != selectedName){
      PyObject_CallMethod(gameMode,"handleMouseOver","(ii)",selectedName,leftButtonDown);//New reference
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
void drawUI(){

  //TODO: make sure CallMethod does not create a new reference and fix these two calls if it does
  UIElementsIterator = PyObject_GetIter(PyObject_CallMethod(gameMode,"getUIElementsIterator",NULL));//New reference
  while (uiElement = PyIter_Next(UIElementsIterator)) {
    drawUIElement(uiElement);
  }

  GLint buf;
  glGetIntegerv(GL_RENDER_MODE,&buf);
  if(buf==GL_SELECT){
    //    printf("sleect%d\n",1);
  }
  if(buf==GL_RENDER){
    //    printf("render%d\n",1);
  }
  if(buf==GL_SELECT && buf==GL_RENDER){
    printf("both%d\n",1);
  }
  if(buf==GL_RENDER){
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
    float xPos = (mouseX/(SCREEN_WIDTH/2.0))-1.0;
    float yPos = 1.0-(mouseY/(SCREEN_HEIGHT/2.0));
    //  float pointerWidth = 3.0*13.0/SCREEN_WIDTH;
    //  float pointerHeight = 3.0*21.0/SCREEN_HEIGHT;
    float pointerWidth = 2.0*CURSOR_WIDTH/SCREEN_WIDTH;
    float pointerHeight = 2.0*CURSOR_HEIGHT/SCREEN_HEIGHT;
    
    glTexCoord2f(0.0,1.0); glVertex3f(xPos,yPos,0.0);
    glTexCoord2f(1.0,1.0); glVertex3f(xPos+pointerWidth,yPos,0.0);
    glTexCoord2f(1.0,0.0); glVertex3f(xPos+pointerWidth,yPos-pointerHeight,0.0);
    glTexCoord2f(0.0,0.0); glVertex3f(xPos,yPos-pointerHeight,0.0);
    glEnd();
    glPopMatrix();
  }

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

  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);//default values anyway, so not needed but w/e
  glInitNames(); //init names stack	
  glClearColor(0.0, 0.0, 0.0, 0.0); //sets screen clear color
  glClearDepth(0.5);

  //glClearColor(1.0, 1.0, 1.0, 1.0); //sets screen clear color
  //glClearColor(123.0/255.0,126.0/255.0,125.0/255.0,1.0);//grey that matches the UI...
  glEnable(GL_DEPTH_TEST);
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);     
  glClear(GL_COLOR_BUFFER_BIT);
  glDepthFunc(GL_ALWAYS);

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
  pngLoad(&texturesArray[CURSOR_GATHER_INDEX],CURSOR_GATHER_IMAGE);

  vertexArrays[DESERT_TILE_INDEX] = *desertVertices;
  vertexArrays[GRASS_TILE_INDEX] = *grassVertices;
  vertexArrays[MOUNTAIN_TILE_INDEX] = *mountainVertices;
  vertexArrays[FOREST_TILE_INDEX] = *forestVertices;
  vertexArrays[BLUE_FOREST_TILE_INDEX] = *blueForestVertices;
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
  if(PyObject_HasAttrString(gameMode,"getFocusNextUnit")){
    PyObject * pyFocusNextUnit;
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
      PyObject_CallMethod(gameMode,"handleMouseMovement","(iii)",selectedName,mouseX,mouseY);
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
	PyObject_CallMethod(gameMode,"handleScrollUp","(ii)",selectedName,deltaTicks);//New reference
      }else if(event.button.button == SDL_BUTTON_WHEELDOWN){
	PyObject_CallMethod(gameMode,"handleScrollDown","(ii)",selectedName,deltaTicks);//New reference
      }

      if(event.button.button == SDL_BUTTON_MIDDLE){
	//	clickScroll = 1;
      }
      if(event.button.button == SDL_BUTTON_LEFT){
	leftButtonDown = 1;
	PyObject_CallMethod(gameMode,"handleLeftClickDown","i",selectedName);//New reference
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
	PyObject_CallMethod(gameMode,"handleLeftClickUp","i",selectedName);//New reference
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
	  char * key = SDL_GetKeyName(event.key.keysym.sym);
	  char capsKey[2];
	  capsKey[0] = (*key)-32;
	  capsKey[1] = 0;
	  PyObject_CallMethod(gameMode,"handleKeyDown","s",capsKey); 
	}else{
	  PyObject_CallMethod(gameMode,"handleKeyDown","s",SDL_GetKeyName(event.key.keysym.sym));
	}
	printPyStackTrace();
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
	       PyObject_CallMethod(gameMode,"handleKeyUp","s",SDL_GetKeyName(event.key.keysym.sym));
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
static void draw(){
  PyObject_CallMethod(gameMode,"onDraw",NULL);//New reference
  printPyStackTrace();
  glClearDepth(1.1);
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

  glRenderMode(GL_SELECT);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		
  glViewport(UI_MAP_EDITOR_LEFT_IMAGE_WIDTH,UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT,SCREEN_WIDTH - UI_MAP_EDITOR_LEFT_IMAGE_WIDTH - UI_MAP_EDITOR_RIGHT_IMAGE_WIDTH, SCREEN_HEIGHT - UI_MAP_EDITOR_TOP_IMAGE_HEIGHT - UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT);
  theCursorIndex = -1;
    
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(45.0f,screenRatio,minZoom,maxZoom);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  GLint viewport[4];
  glSelectBuffer(BUFSIZE,selectBuf);

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();

  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPickMatrix(mouseX,viewport[3]+UI_MAP_EDITOR_TOP_IMAGE_HEIGHT+UI_MAP_EDITOR_BOTTOM_IMAGE_HEIGHT-mouseY,5,5,viewport);
  gluPerspective(45.0f,screenRatio,minZoom,maxZoom);
  
  glMatrixMode(GL_MODELVIEW);
  glTranslatef(translateX,translateY,translateZ);
  drawBoard();
  //  glPushMatrix();

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPickMatrix(mouseX,viewport[3]-mouseY,5,5,viewport);
  
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  drawUI();

  processTheHits(glRenderMode(GL_RENDER),selectBuf);

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
    theMap = PyObject_GetAttrString(gameMode, "map");//New reference
    handleInput();
    draw();
    Py_DECREF(theMap);
    Py_DECREF(gameMode);
  }
  gameMode = PyObject_CallMethod(gameMode,"onQuit",NULL);
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
  SDL_GL_GetAttribute(SDL_GL_DEPTH_SIZE,value);
  printf("depth size: %d\n",*value);

  SDL_ShowCursor(0);
  initGL();
  initPython();
  initFonts();
  //SDL_EnableUNICODE(1);
  gameModule = PyImport_ImportModule("gameModes");//New reference
  gameState = PyImport_ImportModule("gameState");
  mainLoop();
  Py_DECREF(gameModule);
  Py_Finalize();

  exit(0);
}
