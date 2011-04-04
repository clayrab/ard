#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <SDL.h>
#include <SDL_opengl.h>

//#include <SDL_ttf/SDL_TTF.h>
#include <libpng12/png.h>
#include <Python/Python.h>

#include <ft2build.h>
//#include FT_FREETYPE_H
#include <freetype/freetype.h>
#include <freetype/ftglyph.h>
#include <freetype/ftoutln.h>
#include <freetype/fttrigon.h>

#include "libpngGL.h"
#include "fonts.h"

static int screenWidth = 1280;
static int screenHeight = 1024;
float screenRatio;
static SDL_Surface *gScreen;

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
static void createSurface (int fullscreen)
{
  Uint32 flags = 0;
  flags = SDL_OPENGL;
  if (fullscreen)
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

int selectedTriangle = -1;
void processTheHits(GLint hits, GLuint buffer[]){
  GLuint *bufferPtr,*ptrNames, numberOfNames;
  bufferPtr = (GLuint *) buffer;
  //each 'hit' gives a 'number of names', then two depth values, then each of the names in the buffer(array)
  if(hits > 0){
    //just assume there's one hit for now
    numberOfNames = *bufferPtr;
    if(numberOfNames == 1){
      bufferPtr = bufferPtr + 3;
      selectedTriangle = *bufferPtr;
    }
  }else{
    selectedTriangle = -1;
  }
}

void startPicking(){
  GLint viewport[4];
	
  glSelectBuffer(BUFSIZE,selectBuf);
  glRenderMode(GL_SELECT);
	
  glMatrixMode(GL_PROJECTION);
  glPushMatrix();
  glLoadIdentity();
	
  glGetIntegerv(GL_VIEWPORT,viewport);
  gluPickMatrix(mouseX,viewport[3]-mouseY,
		5,5,viewport);
  gluPerspective(45,screenRatio,0.1,1000);
  glMatrixMode(GL_MODELVIEW);
  //glInitNames();
}
void stopPicking() {
  int hits;
  //restoring the original projection matrix
  glMatrixMode(GL_PROJECTION);
  glPopMatrix();
  glMatrixMode(GL_MODELVIEW);
  glFlush();//"all programs should call glFlush whenever they count on having all of their previously issued commands completed"
  //returning to normal rendering mode
  hits = glRenderMode(GL_RENDER);
  //if (hits != 0){
  processTheHits(hits,selectBuf);
  //}
}
/**************************** /mouse hover object selection ********************************/

/************************************* drawing subroutines ***************************************/
void drawTrianglesList(GLuint list, int selected){
  int i;
  for(i = 0; i < 6; i++){
    //char str[12];
    //sprintf(str,"%d",i);
    glPushName(i); 
    glPushMatrix();
    glLoadIdentity();
    glTranslatef(i*2.0-5.0,1.0,0.0);
    if(selected == i){
      glColor3f(1.0f, 0.0f, 0.0f);
    }else{
      glColor3f(1.0f, 1.0f, 1.0f);
    }
    glCallList(list);
    glPopMatrix();
		
    glPopName();
  }
  glColor3f(1.0f, 1.0f, 1.0f);
}
GLuint drawTriangle1(){
  GLuint triangle1List;
  triangle1List = glGenLists(1);
  glNewList(triangle1List,GL_COMPILE);
	
  glBegin(GL_TRIANGLES);
  glVertex3f(-1.0,1.0,0.0);
  glVertex3f(1.0,1.0,0.0);
  glVertex3f(0.0,0.0,0.0);
  glEnd();
	
  glEndList();
	
  return(triangle1List);	
}

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
void drawTile(float x, float y, int tilesXIndex, int tilesYIndex){
  float scale = 1.0;
  float xIndex = (float)tilesXIndex*-(2.0*SIN60);
  float yIndex = (float)tilesYIndex*1.5;
  if(abs(tilesYIndex)%2 == 1){
    xIndex += SIN60;
  }
	
  int choice = tilesXIndex%2;
  if (choice == 0) {
    textureVertices = &jungleVertices[0][0];
  }else{
    textureVertices = &rockVertices[0][0];
  }
	
  glBegin(GL_POLYGON);
  glTexCoord2f(*(textureVertices+0),*(textureVertices+1)); glVertex3f(hexagonVertices[0][0]+xIndex, hexagonVertices[0][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+2),*(textureVertices+3)); glVertex3f(hexagonVertices[1][0]+xIndex, hexagonVertices[1][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+4),*(textureVertices+5)); glVertex3f(hexagonVertices[2][0]+xIndex, hexagonVertices[2][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+6),*(textureVertices+7)); glVertex3f(hexagonVertices[3][0]+xIndex, hexagonVertices[3][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+8),*(textureVertices+9)); glVertex3f(hexagonVertices[4][0]+xIndex, hexagonVertices[4][1]+yIndex, 0.0);
  glTexCoord2f(*(textureVertices+10),*(textureVertices+11)); glVertex3f(hexagonVertices[5][0]+xIndex, hexagonVertices[5][1]+yIndex, 0.0);
  glEnd();
}

GLuint tilesList;

GLuint tilesTexture;
void generateTilesList(){
  tilesList = glGenLists(1);
  glNewList(tilesList,GL_COMPILE);
  glEndList();
}
void drawTiles(){
	
  glBindTexture(GL_TEXTURE_2D, tilesTexture);
  drawTile(1.0,1.0,0,-1);
  drawTile(1.0,1.0,1,-1);
  drawTile(1.0,1.0,2,-1);
  drawTile(1.0,1.0,3,-1);
  drawTile(1.0,1.0,0,0);
  drawTile(1.0,1.0,1,0);
  drawTile(1.0,1.0,2,0);
  drawTile(1.0,1.0,3,0);
  drawTile(1.0,1.0,0,1);
  drawTile(1.0,1.0,1,1);
  drawTile(1.0,1.0,2,1);
  drawTile(1.0,1.0,3,1);
  drawTile(1.0,1.0,0,2);
  drawTile(1.0,1.0,1,2);
  drawTile(1.0,1.0,2,2);
  drawTile(1.0,1.0,3,2);
  drawTile(1.0,1.0,5,5);	
}
/************************************* /drawing subroutines ***************************************/

/************************************** opengl init **************************************/

PyObject * gameModule;
PyObject * map;
#define maxZoom 120.0f
#define minZoom 10.0f
GLuint testTexture;

#define tilesImage "tiles.png"
#define testImage "testEventImage1.png"
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
  gameModule = PyImport_ImportModule("__init__");//New reference
  map = PyObject_GetAttrString(gameModule, "map1");//New reference
  //use this to create a new object: like "class()" in python //PyObject * instance = PyObject_CallObject(class,NULL);//New reference
}
static void initTextures(){

}
float translateX = 0.0f;
float translateY = 0.0f;
float translateZ = -40.0f;
float scrollSpeed = 0.04;
float cnt1 = 0.0;
static void mainLoop (){
  SDL_Event event;
  int done = 0;    
  int moveUp = 0;
  int moveRight = 0;
  int clickScroll = 0;
  int previousTick = 0;
  int deltaTicks = 0;
  while ( !done ) {
    deltaTicks = SDL_GetTicks()-previousTick;
    if(deltaTicks != 0){
      //			printf("framerate: %d\n",1000/(SDL_GetTicks()-previousTick));
    }
    previousTick = SDL_GetTicks();
    //SDL_Delay(20);//for framerate testing...
    while ( SDL_PollEvent (&event) ) {
      switch (event.type) {
      case SDL_MOUSEMOTION:
	mouseX = event.motion.x;
	mouseY = event.motion.y;
	//					printf("x: %d\t\ty: %d\n",mouseX,mouseY);
	if(clickScroll > 0){
	  translateX += event.motion.xrel*0.0000385*(0-translateZ)*deltaTicks;
	  translateY -= event.motion.yrel*0.0000385*(0-translateZ)*deltaTicks;
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
	break;
      case SDL_MOUSEBUTTONDOWN:
	if(event.button.button == SDL_BUTTON_WHEELUP && translateZ < (-10.0-minZoom)){
	  translateZ = translateZ + 0.2*deltaTicks;
	}else if(event.button.button == SDL_BUTTON_WHEELDOWN && translateZ > (10.0-maxZoom)){
	  translateZ = translateZ - 0.2*deltaTicks;
	}
	if(event.button.button == SDL_BUTTON_LEFT){
	  clickScroll = 1;
	}else{
						
	}
	break;
      case SDL_MOUSEBUTTONUP:
	if(event.button.button == SDL_BUTTON_LEFT){
	  clickScroll = 0;
	}
	break;
      case SDL_KEYDOWN:
	if(event.key.keysym.sym == SDLK_ESCAPE){
	  done = 1;
	}
	break;
      case SDL_QUIT:
	done = 1;
	break;
      default:
	break;
      }
    }
    if(moveRight > 0 && translateX > -10.0){
      translateX -= scrollSpeed*deltaTicks;
    }else if(moveRight < 0 && translateX < 10.0){
      translateX += scrollSpeed*deltaTicks;
    }
    if(moveUp > 0 && translateY > -10.0){
      translateY -= scrollSpeed*deltaTicks;
    }else if(moveUp < 0 && translateY < 10.0){
      translateY += scrollSpeed*deltaTicks;
    }

    //game board projection time
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    screenRatio = (GLfloat)screenWidth/(GLfloat)screenHeight;
    gluPerspective(45.0f,screenRatio,minZoom,maxZoom);

    //draw the game board
    glMatrixMode(GL_MODELVIEW);
    //glPushMatrix();
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		
    glLoadIdentity();
    glTranslatef(translateX,translateY,translateZ);
    glColor3f(1.0f, 1.0f, 1.0f);
    drawTiles();
    GLuint list = drawTriangle1();
    startPicking();
    drawTrianglesList(list,-1);
    stopPicking();
    drawTrianglesList(list,selectedTriangle);
    //    glTranslatef(0,0,-60);
    print("test");
    //glPopMatrix();

    //GUI projection time
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    screenRatio = (GLfloat)screenWidth/(GLfloat)screenHeight;
    glOrtho(-100.0,100.0,-100.0,100.0,0.0,1.0);

        glMatrixMode(GL_MODELVIEW);
    
    //glPushMatrix();

    glLoadIdentity();
    //    glTranslatef(-90.0f,-10.0f,0.0f);

    glLoadIdentity();
    glRotatef(cnt1,0,0,1);
    glScalef(1,.8+.3*cos(cnt1/5),1);
    glTranslatef(-90,-10,0);

    print("<3 Hi Ban <3");

    cnt1+=0.051f;// Increase The First Counter
    //    cnt2+=0.005f;

    glFlush();//"all programs should call glFlush whenever they count on having all of their previously issued commands completed"
    SDL_GL_SwapBuffers ();	
  }
}

/*

inline int next_p2 (int a )
{
int rval=1;
// rval<<=1 Is A Prettier Way Of Writing rval*=2; 
while(rval<a) rval<<=1;
return rval;
}
 */
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
  //  flags |= SDL_FULLSCREEN;
  gScreen = SDL_SetVideoMode (screenWidth, screenHeight, 0, flags);
  if (gScreen == NULL) {
    fprintf (stderr, "Couldn't set 640x480 OpenGL video mode: %s\n",
	     SDL_GetError());
    SDL_Quit();
    exit(2);
  }
  initGL();
  initPython();

  char getName[20] ="getName";
  PyObject * mapName = PyObject_CallMethod(map,getName,NULL);//New reference
  char * theMapName = PyString_AsString(mapName);
  //  printf("%s\n",theMapName);
  Py_DECREF(mapName);

  initFonts();

  mainLoop();
  
  Py_DECREF(map);
  Py_DECREF(gameModule);
  Py_Finalize();
  exit(0);
}
