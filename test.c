#include <stdio.h>
#include "SDL/SDL.h"
// include the SDL headers you put in /mingw/include/SDL/

int main(int argc, char *argv[]){
  // with SDL, you need the argc and argv parameters

  printf("Hello world\n");
  // with SDL, anything you printf will get printed to the
  // file stdout.txt in the current directory, not to the screen
}
