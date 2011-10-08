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

//#include "libpngGL.h"
//#include "fonts.h"

// include the SDL headers you put in /mingw/include/SDL/
static void handleInput(){
  SDL_Event event;
  deltaTicks = SDL_GetTicks()-previousTick;
  previousTick = SDL_GetTicks();
  while(SDL_PollEvent(&event)){
    switch(event.type){
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
}
static void mainLoop (){
  while ( !done ) {
    handleInput();
  }
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
  //SDL_EnableUNICODE(1);
  mainLoop();

  exit(0);
}

