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

#define maxZoom 120.0f
#define minZoom 10.0f

static int screenWidth = 1280;
static int screenHeight = 800;
float screenRatio;
static SDL_Surface *gScreen;

float translateX = 0.0f;
float translateY = 0.0f;
float translateZ = -40.0f;
float scrollSpeed = 0.04;

PyObject * gameModule;
PyObject * theMap;
PyObject * mapName;
PyObject * nodes;
PyObject * mapIterator;
PyObject * rowIterator;

GLuint tilesTexture;
GLuint uiTexture;
GLuint tileSelectBoxTexture;

  GLdouble mouseMapPosX, mouseMapPosY, mouseMapPosZ;
  GLdouble mouseMapPosXPrevious, mouseMapPosYPrevious;

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
  gScreen = SDL_SetVideoMode (screenWidth, screenHeight, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Couldn't set 640x480 OpenGL video mode: %s\n",
	     SDL_GetError());
  }
}
/****************************** /SDL STUFF ********************************/

/**************************** mouse hover object selection ********************************/
int mouseX = 0;
int mouseY = 0;
#define BUFSIZE 512
GLuint selectBuf[BUFSIZE];

int selectedName = -1;//the mousedover object's 'name'
void processTheHits(GLint hits, GLuint buffer[]){
  GLuint *bufferPtr,*ptrNames, numberOfNames;
  bufferPtr = (GLuint *) buffer;
  //each 'hit' gives a 'number of names', then two depth values, then each of the names in the buffer(array)
  if(hits > 0){
    //just assume there's one hit for now, can't think of a reason we'd need multiple moused-over objects anyway
    numberOfNames = *bufferPtr;
    //these are the names of the object that was 'hit', should only be one if our code is working as expected
    if(numberOfNames == 1){
      bufferPtr = bufferPtr + 3;
      //the value of the name name is stored +3 over in mem
      selectedName = *bufferPtr;
    }else if(numberOfNames ==0){
      selectedName = -1;
    }else{
      printf("WARNING: WE ONLY EXPECT ONE NAME PER OBJECT WHEN PICKING\n");
    }
  }else{
    selectedName = -1;
  }
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
  winZ = (float)((minZoom-translateZ)/maxZoom);
  gluUnProject( winX, winY, winZ, modelview, projection, viewport, posX, posY, posZ);
  
  //  glMouseCoords[0] = posX;
  //  glMouseCoords[1] = posY;
  //  glMouseCoords[2] = posZ;
  //  return glMouseCoords;
}
/**************************** /mouse hover object selection ********************************/

/************************************* drawing subroutines ***************************************/

#define SIN60 0.8660
#define COS60 0.5
#define TILE_GRASS 1
#define TILE_MOUNTAIN 2
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

float rockVertices[6][2] = {
  {(699.0/1280),1.0-(556.0/1280)},
  {(699.0/1280),1.0-(524.0/1280)},
  {(726.0/1280),1.0-(508.0/1280)},
  {(754.0/1280),1.0-(524.0/1280)},
  {(754.0/1280),1.0-(556.0/1280)},
  {(726.0/1280),1.0-(572.0/1280)}
};

float hexagonVertices[6][2] = {
  {-SIN60, -COS60},
  {-SIN60, COS60},
  {0.0, 1.0},
  {SIN60, COS60},
  {SIN60, -COS60},
  {0.0, -1.0}
};
float *textureVertices;
void drawTile(int tilesXIndex, int tilesYIndex, long name, long tileValue){
  float scale = 1.0;
  float xIndex = (float)tilesXIndex*-(2.0*SIN60);
  float yIndex = (float)tilesYIndex*1.5;
  if(abs(tilesYIndex)%2 == 1){
    xIndex += SIN60;
  }
  int choice = tileValue;
  if (choice == 0) {
    textureVertices = &jungleVertices[0][0];
  }else{
    textureVertices = &rockVertices[0][0];
  }
  if(name == selectedName){
    glColor3f(1.0f, 0.0f, 0.0f);
  }else{
    glColor3f(1.0f, 1.0f, 1.0f);
  }
  glPushName(name);	
  glBegin(GL_POLYGON);
  glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xIndex, hexagonVertices[0][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xIndex, hexagonVertices[1][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xIndex, hexagonVertices[2][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xIndex, hexagonVertices[3][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xIndex, hexagonVertices[4][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xIndex, hexagonVertices[5][1]+yIndex, 0.0);
  glEnd();
  glPopName();
}

GLuint tilesList;

void generateTilesList(){
  tilesList = glGenLists(1);
  glNewList(tilesList,GL_COMPILE);
  glEndList();
}
void drawTiles(){
  
  glBindTexture(GL_TEXTURE_2D, tilesTexture);
  int rowNumber = 0;
  PyObject * node;
  PyObject * row;

  mapIterator = PyObject_CallMethod(theMap,"getIterator",NULL);//New reference

  rowIterator = PyObject_GetIter(mapIterator);
  while (row = PyIter_Next(rowIterator)) {
    int colNumber = 0;
    rowNumber = rowNumber - 1;
    PyObject * nodeIterator = PyObject_GetIter(row);
    while(node = PyIter_Next(nodeIterator)) {
      PyObject * nodeName = PyObject_CallMethod(node,"getName",NULL);//New reference
      PyObject * nodeValue = PyObject_CallMethod(node,"getValue",NULL);//New reference
      long longName = PyLong_AsLong(nodeName);
      long longValue = PyLong_AsLong(nodeValue);
      drawTile(colNumber,rowNumber,longName,longValue);
      colNumber = colNumber - 1;
      Py_DECREF(node);
    }
    Py_DECREF(row);
  }
  Py_DECREF(rowIterator); 
  Py_DECREF(mapIterator);
}
drawBoard(){
  drawTiles();
  //  glOrtho(-100,100,-100,100,-1,1.0);
  glColor3f(1.0f, 1.0f, 1.0f);
  print("test");
}

void drawTileSelect(){
  
  glColor3f(1.0,1.0,1.0);
  glTranslatef(-0.93,0.92,0.0);
  glScalef(0.01,0.01,0.0);
  glBindTexture(GL_TEXTURE_2D, tilesTexture);
  textureVertices = &jungleVertices[0][0];
  glPushName(63636363);
  glBegin(GL_POLYGON);
  glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(3.0*hexagonVertices[0][0], 3.0*hexagonVertices[0][1], 0.0);
  glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(3.0*hexagonVertices[1][0], 3.0*hexagonVertices[1][1], 0.0);
  glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(3.0*hexagonVertices[2][0], 3.0*hexagonVertices[2][1], 0.0);
  glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(3.0*hexagonVertices[3][0], 3.0*hexagonVertices[3][1], 0.0);
  glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(3.0*hexagonVertices[4][0], 3.0*hexagonVertices[4][1], 0.0);
  glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(3.0*hexagonVertices[5][0], 3.0*hexagonVertices[5][1], 0.0);
  glEnd();
  glPopName();

  glLoadIdentity();
  glTranslatef(-0.97,0.88,0.0);
  glBindTexture(GL_TEXTURE_2D, tileSelectBoxTexture);
  glBegin(GL_POLYGON);
  glTexCoord2f(1.0,1.0); glVertex3f(0.08,0.08,0.0);
  glTexCoord2f(1.0,0.0); glVertex3f(0.08,0.0,0.0);
  glTexCoord2f(0.0,0.0); glVertex3f(0.0,0.0,0.0);
  glTexCoord2f(0.0,1.0); glVertex3f(0.0,0.08,0.0);
  glEnd();

  glLoadIdentity();
    glTranslatef(-0.975,0.86,0.0);
  glOrtho(-2000,2000,-2000,2000,-1,1.0);
  //  glColor3f(0.2,0.2,0.2);

  glColor3f(1.0,1.0,1.0);
  print("Grass");

}

void drawUI(){

  /*  glBindTexture(GL_TEXTURE_2D, uiTexture);
    
  glBegin(GL_POLYGON);
  glTexCoord2f(0.0,1.0); glVertex3f(-1.0,1.0,0.0);
  glTexCoord2f(1.0,1.0); glVertex3f(0.5,1.0,0.0);
  glTexCoord2f(1.0,0.0); glVertex3f(0.5,-1.0,0.0);
  glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,0.0);
  glEnd();
  */
  drawTileSelect();

}
/************************************* /drawing subroutines ***************************************/

/************************************** opengl init **************************************/

GLuint testTexture;

#define tilesImage "tiles2.png"
#define testImage "testEventImage1.png"
#define uiImage "UI.png"
#define tileSelectBoxImage "tileSelect.png"
static void initGL (){
  /** needs to be called on screen resize **/
  //unneeded with sdl?
  glViewport(0, 0, screenWidth, screenHeight);//default values anyway, so not needed but w/e
  glInitNames(); //init names stack	
  glClearColor(0.0, 0.0, 0.0, 0.0); //sets screen clear color
  glEnable(GL_TEXTURE_2D);
  glEnable(GL_BLEND);
  char file[100] = tilesImage;
  pngLoad(&tilesTexture, tilesImage);	/******************** /image init ***********************/
  pngLoad(&testTexture, testImage);	/******************** /image init ***********************/
  pngLoad(&uiTexture,uiImage);
  pngLoad(&tileSelectBoxTexture,tileSelectBoxImage);
  screenRatio = (GLfloat)screenWidth/(GLfloat)screenHeight;
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
static void initTextures(){

}
static void mainLoop (){
  SDL_Event event;
  int done = 0;    
  int moveUp = 0;
  int moveRight = 0;
  int clickScroll = 0;
  int previousTick = 0;
  int deltaTicks = 0;
  //GLdouble translateX, translateY;
  while ( !done ) {
    deltaTicks = SDL_GetTicks()-previousTick;
    if(deltaTicks != 0){
      //			printf("framerate: %d\n",1000/(SDL_GetTicks()-previousTick));
    }
    previousTick = SDL_GetTicks();
    //SDL_Delay(20);//for framerate testing...
    while(SDL_PollEvent(&event)){
      switch(event.type){
      case SDL_MOUSEMOTION:
	mouseX = event.motion.x;
	mouseY = event.motion.y;
	//					printf("x: %d\t\ty: %d\n",mouseX,mouseY);
	if(clickScroll > 0){
	  translateX = translateX + mouseMapPosX - mouseMapPosXPrevious;
	  translateY = translateY + mouseMapPosY - mouseMapPosYPrevious;
	}else{
	  if(mouseX == 0){
	    moveRight = -1;
	  }else if(mouseX >= screenWidth-1){
	    moveRight = 1;
	  }else{
	    moveRight = 0;
	  }
	  if(mouseY == 0){
	    moveUp = 1;
	  }else if(mouseY >= screenHeight-1){
	    moveUp = -1;
	  }else{
	    moveUp = 0;
	  }
	}
	mouseMapPosXPrevious = mouseMapPosX;
	mouseMapPosYPrevious = mouseMapPosY;
	break;
      case SDL_MOUSEBUTTONDOWN:
	if(event.button.button == SDL_BUTTON_WHEELUP && translateZ < (-10.0-minZoom)){
	  translateZ = translateZ + 1.2*deltaTicks;
	}else if(event.button.button == SDL_BUTTON_WHEELDOWN && translateZ > (10.0-maxZoom)){
	  translateZ = translateZ - 1.2*deltaTicks;
	}
	if(translateZ < 10.0-maxZoom){
	  translateZ = 10.0-maxZoom;
	}
	if(translateZ > -10.0-minZoom){
	  translateZ = -10.0-minZoom;
	}
	if(event.button.button == SDL_BUTTON_MIDDLE){
	  clickScroll = 1;
	}
	if(event.button.button == SDL_BUTTON_LEFT){
	  printf("left: %d\n",selectedName);
	}
	break;
      case SDL_MOUSEBUTTONUP:
	if(event.button.button == SDL_BUTTON_MIDDLE){
	  clickScroll = 0;
	}
	break;
      case SDL_KEYDOWN:
	if(event.key.keysym.sym == SDLK_ESCAPE){
	  done = 1;
	}
	if(event.key.keysym.sym == SDLK_BACKQUOTE){
	  clickScroll = 1;
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
    glGetIntegerv(GL_VIEWPORT,viewport);
    gluPickMatrix(mouseX,viewport[3]-mouseY,5,5,viewport);
    gluPerspective(45,screenRatio,0.1,1000);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    //glInitNames();

    //I don't understand why but drawing the UI first here caused it to be picked in higher priority to the board...
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    gluPickMatrix(mouseX,viewport[3]-mouseY,5,5,viewport);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    drawUI();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
    glPopMatrix();

    drawBoard();

    //stopPicking();
    int hits;
    //restoring the original projection matrix
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
    glPopMatrix();
    glFlush();//"all programs should call glFlush whenever they count on having all of their previously issued commands completed"
    //returning to normal rendering mode
    hits = glRenderMode(GL_RENDER);
    //if (hits != 0){
    processTheHits(hits,selectBuf);
    //}
  
    drawBoard();
    
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
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
  gScreen = SDL_SetVideoMode (screenWidth, screenHeight, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Could not set OpenGL video mode: %s\n",
	     SDL_GetError());
    SDL_Quit();
    exit(2);
  }
  initGL();
  initPython();

  gameModule = PyImport_ImportModule("__init__");//New reference
  theMap = PyObject_GetAttrString(gameModule, "map1");//New reference
  mapName = PyObject_CallMethod(theMap,"getName",NULL);//New reference
  nodes = PyObject_CallMethod(theMap,"getNodes",NULL);//New reference
  //mapIterator = PyObject_CallMethod(theMap,"getIterator",NULL);//New reference
  //char * theMapName = PyString_AsString(mapName);
  //printf("map name: %s\n",theMapName);
  //Py_DECREF(theMapName);

  initFonts();
  mainLoop();

  //Py_DECREF(mapIterator); 
  Py_DECREF(nodes);
  Py_DECREF(theMap);
  Py_DECREF(gameModule);
  Py_Finalize();

  exit(0);
}
