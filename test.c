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

#define maxZoom 70.0
#define minZoom 10.0
#define initZoom 30.0

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

#define CURSOR_POINTER_IMAGE "assets/cursors/gam372.png"
#define CURSOR_POINTER_INDEX 6

#define CURSOR_POINTER_ON_IMAGE "assets/cursors/gam375.png"
#define CURSOR_POINTER_ON_INDEX 7

#define CURSOR_MOVE_IMAGE "assets/cursors/gam378.png"
#define CURSOR_MOVE_INDEX 8

#define CURSOR_WIDTH 32
#define CURSOR_HEIGHT 29

#define PLAYER_START_BUTTON_IMAGE "assets/playerStartButton.png"
#define PLAYER_START_BUTTON_INDEX 9
#define PLAYER_START_BUTTON_WIDTH 13
#define PLAYER_START_BUTTON_HEIGHT 14
#define PLAYER_START_IMAGE "assets/playerStart.png"
#define PLAYER_START_INDEX 10
#define PLAYER_START_WIDTH 13
#define PLAYER_START_HEIGHT 14

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

#define DESERT_TILE_INDEX 0
#define GRASS_TILE_INDEX 1
#define MOUNTAIN_TILE_INDEX 2
#define FOREST_TILE_INDEX 3
#define WATER_TILE_INDEX 4
#define ROAD_TILE_INDEX 5
#define CITY_TILE_INDEX 6
#define PLAYER_START_TILE_INDEX 7//REMOVE THIS

#define DESERT_MOVE_COST 2.0
#define GRASS_MOVE_COST 1.0
#define MOUNTAIN_MOVE_COST 10.0
#define FOREST_MOVE_COST 1.0
#define WATER_MOVE_COST 10.0
//ROADS HALF THE COST OF ALL MOVEMENT

#define SIN60 0.8660
#define COS60 0.5

#define BUFSIZE 512


float screenRatio;
static SDL_Surface *gScreen;


int foo = 0;
int clickScroll = 0;
long focusNextUnit = 0;
int leftButtonDown = 0;

int done = 0;    
int moveUp = 0;
int moveRight = 0;
int previousTick = 0;
int deltaTicks = 0;

float translateX = -20.0;
float translateY = 15.0;
float scrollSpeed = 0.10;

GLdouble convertedX,convertedY,convertedZ;
float newTranslateX,newTranslateY;

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
/*float forestVertices[6][2] = {
  {(699.0/1280),1.0-(262.0/1280)},
  {(699.0/1280),1.0-(230.0/1280)},
  {(726.0/1280),1.0-(214.0/1280)},
  {(754.0/1280),1.0-(230.0/1280)},
  {(754.0/1280),1.0-(262.0/1280)},
  {(726.0/1280),1.0-(278.0/1280)}
  };*/
float forestVertices[6][2] = {
  {(643.0/1280),1.0-(360.0/1280)},
  {(643.0/1280),1.0-(328.0/1280)},
  {(670.0/1280),1.0-(312.0/1280)},
  {(696.0/1280),1.0-(328.0/1280)},
  {(696.0/1280),1.0-(360.0/1280)},
  {(670.0/1280),1.0-(376.0/1280)}
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


/************************************** opengl init **************************************/

static void initGL (){
  /** needs to be called on screen resize **/
  //unneeded with sdl?

  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);//default values anyway, so not needed but w/e
  glInitNames(); //init names stack	
  glClearColor(0.0, 0.0, 0.0, 0.0); //sets screen clear color
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);

  //glDepthMask(GL_TRUE);
  glClear(GL_COLOR_BUFFER_BIT);		
  glEnable(GL_DEPTH_TEST);
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

  vertexArrays[DESERT_TILE_INDEX] = *desertVertices;
  vertexArrays[GRASS_TILE_INDEX] = *grassVertices;
  vertexArrays[MOUNTAIN_TILE_INDEX] = *mountainVertices;
  vertexArrays[FOREST_TILE_INDEX] = *forestVertices;
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
  while(SDL_PollEvent(&event)){
    switch(event.type){
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

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		
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
  gameModule = PyImport_ImportModule("__init__");//New reference
  gameState = PyImport_ImportModule("gameState");
  mainLoop();
  Py_DECREF(gameModule);
  Py_Finalize();

  exit(0);
}
