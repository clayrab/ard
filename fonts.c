#include <stdio.h>
#include <SDL.h>
#include <SDL_opengl.h>
#include "libpngGL.h"

#define ARIAL 0
#define HERCULANUM 1

#define FONT_NAME_SIZE 50

char fontFiles[4][FONT_NAME_SIZE] = {
  "assets/fonts/Arial.ttf",
  "assets/fonts/XXII ARABIAN-ONENIGHTSTAND.ttf",
  "assets/fonts/Herculanum.ttf",
  "assets/fonts/MinionPro-Regular.otf",
  //"assets/fonts/Courier New Bold.ttf",
};
GLuint textCursor;

int TextureWidth;
int TextureHeight;
int BitmapWidth;
int BitmapHeight;
GLuint list_base;
int textName;
//gluin fontTexture;

struct _font{
  char fontName[50];
  FT_Bitmap bitmaps[100];

} font;

struct _fontTexture{
  int width;
  int height;
  //GLUint texture;
} fontTexture;

//getFontTexture(ARIAL,16,"all your base are belong to us")
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
static void loadFont(int font, int fontSize){
  
}
GLuint fontTexturesArray[2];
FT_Glyph glyph;
FT_Vector origin;
FT_BitmapGlyph bitmap_glyph;
FT_Bitmap bitmap;
int dataWidth;
int dataHeight;
GLubyte* expanded_data;
float x,y;
int i;
int j;
int glyphHeight;
int glyphWidth;
void make_dlist(FT_Face face, char charIndex, GLuint list_base, GLuint * tex_base ) {

  if(FT_Load_Glyph(face, FT_Get_Char_Index(face,charIndex), FT_LOAD_DEFAULT)){
    printf("FT_Load_Glyph failed");
    exit(1);
  }

  if(FT_Get_Glyph(face->glyph, &glyph)){
    printf("FT_Get_Glyph failed");
    exit(1);
  }
  FT_Glyph_To_Bitmap(&glyph, FT_RENDER_MODE_NORMAL, 0, 1 );
  
  bitmap_glyph = (FT_BitmapGlyph)glyph;
  bitmap = (FT_Bitmap)bitmap_glyph->bitmap;
  dataWidth = nextPowerOf2( bitmap.width );
  dataHeight = nextPowerOf2( bitmap.rows );
  expanded_data = malloc(2 * dataWidth * dataHeight * sizeof(GLubyte));
  for(j=0; j < dataHeight; j++){
    for(i=0; i < dataWidth; i++){
      expanded_data[2*(i+j*dataWidth)] = 
	expanded_data[2*(i+j*dataWidth)+1] = 
	(i>=bitmap.width || j>=bitmap.rows) ? 0 : bitmap.buffer[i + bitmap.width*j];
    }
  }
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
  glBindTexture(GL_TEXTURE_2D, tex_base[charIndex]);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, dataWidth, dataHeight, 0, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE, expanded_data);

  if(bitmap.rows > 0){//space char has 0 height and width, but we need it for the 'empty' quads between chars, so we'll use the previous char's
    glyphHeight = bitmap.rows;
    glyphWidth = bitmap.width;
  }

  x=(float)glyphWidth / (float)dataWidth;
  y=(float)glyphHeight / (float)dataHeight;

  glNewList(list_base+(2*charIndex),GL_COMPILE);
  glPushMatrix();

  glBegin(GL_QUADS);//makes the space between letters clickable
  glVertex2f(-4,glyphHeight);
  glVertex2f(-4,0);
  glVertex2f(face->glyph->advance.x>>6,0);
  glVertex2f(bitmap_glyph->left,glyphHeight);
  glEnd();
  
  if(bitmap_glyph->top == 0){//draws quad for space at the correct height
    glTranslatef(bitmap_glyph->left,0,0);
  }else{
    glTranslatef(bitmap_glyph->left,bitmap_glyph->top-glyphHeight,0);
  }
  glBindTexture(GL_TEXTURE_2D,tex_base[charIndex]);
  glBegin(GL_QUADS);
  glTexCoord2d(0,0); glVertex2f(0,glyphHeight);
  glTexCoord2d(0,y); glVertex2f(0,0);
  glTexCoord2d(x,y); glVertex2f(glyphWidth,0);
  glTexCoord2d(x,0); glVertex2f(glyphWidth,glyphHeight);
  glEnd();
  glPopMatrix();
  glTranslatef(face->glyph->advance.x >> 6, 0, 0);

  // Increment The Raster Position As If We Were A Bitmap Font.
  // (Only Needed If You Want To Calculate Text Length)
  // glBitmap(0,0,0,0,face->glyph->advance.x >> 6,0,NULL);

  // Finish The Display List
  glEndList();

  //make another list with just the translations so we can call this to find the width of text before we draw it
  glNewList(list_base+(2*charIndex)+1,GL_COMPILE);
  //  glPushMatrix();
  glTranslatef(face->glyph->advance.x >> 6, 0, 0);
  glTranslatef(bitmap_glyph->left,0,0);
  //  glPopMatrix();
  glEndList();
}


static void initFonts(){
  //loadFont(ARIAL,16);
  pngLoad(&textCursor,"assets/cursor.png");

  FT_Library library;
  FT_Face face; 
  int error = FT_Init_FreeType( &library );
  //  if(FT_New_Face(library,"assets/fonts/Ceria Lebaran.otf",0,&face)){
    //XXII ARABIAN-ONENIGHTSTAND.ttf
  
  long int fontCount = sizeof(fontFiles)/FONT_NAME_SIZE;
  GLuint textures[256*fontCount];
  list_base=glGenLists(256*fontCount);
  glGenTextures(256*fontCount,textures);

  int index = 0;
  for(;index < fontCount;index++){
    if(FT_New_Face(library,fontFiles[index],0,&face)){
      printf("FT_New_Face error");
      exit(1);
    }
    if(FT_Set_Char_Size(face, 16*64, 0, 300, 0)){
      printf("FT_Set_Char_Size error");
      exit(1);
    }
    int i;
    for(i=0;i<128;i++){
      make_dlist(face,i,list_base+(256*index),textures+(128*index));
    }
    FT_Done_Face(face);
  }
  FT_Done_FreeType(library);
}
void drawCursor(){
  glPushMatrix();
  glTranslatef(-3.0,0.0,0.0);
  float currentColor[4];
  glGetFloatv(GL_CURRENT_COLOR,currentColor);
  glBindTexture(GL_TEXTURE_2D,textCursor);
  glColor4f(currentColor[0],currentColor[1],currentColor[2],currentColor[3]);
  //glBindTexture(GL_TEXTURE_2D,textures[124]);//drawing a | might be a bit more sophisticated...
  glBegin(GL_QUADS);
  glTexCoord2f(0.0,1.0); glVertex3f(-3.0,70.0,0.001);
  glTexCoord2f(0.0,0.0); glVertex3f(-3.0,-2.0,0.001);
  glTexCoord2f(1.0,0.0); glVertex3f(8.0,-2.0,0.001);
  glTexCoord2f(1.0,1.0); glVertex3f(8.0,70.0,0.001);
  glEnd();
  glPopMatrix();
}
int wordCount;
int strPosition;
GLdouble projMatrix[16];
int findWordWidth(int fontIndex, char* str, float rightMargin){
  //  rightMargin = rightMargin-0.12;
  glPushMatrix();
  wordCount = 0;
  strPosition = 0;
  while(str[strPosition] != 0){
    glCallList(list_base+(fontIndex*256)+(2*str[strPosition])+1);
    strPosition++;
    glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
    if(projMatrix[12] > rightMargin){
      glPopMatrix();
      return wordCount;
    }
    while(str[strPosition] != 32 && str[strPosition] != 0){
      glCallList(list_base+(fontIndex*256)+(2*str[strPosition])+1);
      strPosition++;
      glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
      if(projMatrix[12] > rightMargin){
	glPopMatrix();
	return wordCount;
      }
    }
    wordCount++;
  }
  glPopMatrix();
  return wordCount;
}
int numLines;
int checkRightMargin(int fontIndex, char* str, int strPosition, float rightMargin){
  if(rightMargin < -1.0){
    return 0;
  }
  glPushMatrix();
  while(str[strPosition] != 32 && str[strPosition] != 0){//while the next char is not a space or end of string
    glCallList(list_base+(fontIndex*256)+(2*str[strPosition])+1);
    glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
    if(projMatrix[12] > rightMargin){
      glPopMatrix();
      numLines++;
      return 1;
    }
    strPosition++;
  }
  glPopMatrix();
  return 0;
}

PyObject * pyObj;
void findTextWidthFromRight(PyObject * uiElement, int fontIndex, char* realStr, float rightMargin, int rightmostCharPosition){
  glPushMatrix();
  glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
  strPosition = rightmostCharPosition;
  while(strPosition >= 0){
    //    strPosition = strPosition - 1;
    glCallList(list_base+(fontIndex*256)+(2*realStr[strPosition])+1);
    glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
    if(projMatrix[12] > rightMargin){
      glPopMatrix();
      pyObj = PyObject_CallMethod(uiElement,"positionText","(ii)",strPosition-1,rightmostCharPosition);
      //  Py_DECREF(pyObj);
      return;
    }
    strPosition--;
  }
  printf("ERROR, THIS CODE SHOUDL NEVER RUN!!");
  glPopMatrix();  
  //  pyObj = PyObject_CallMethod(uiElement,"positionText","(ii)",strPosition-1,rightmostCharPosition);
  //  Py_DECREF(pyObj);
}
void findTextWidthFromLeft(PyObject * uiElement, int fontIndex, char* realStr, float rightMargin, int leftmostCharPosition){
  glPushMatrix();
  glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
  strPosition = leftmostCharPosition;
  while(realStr[strPosition] != 0){
    glCallList(list_base+(fontIndex*256)+(2*realStr[strPosition])+1);
    glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
    if(projMatrix[12] > rightMargin){
      glPopMatrix();
      pyObj = PyObject_CallMethod(uiElement,"positionText","(ii)",leftmostCharPosition,strPosition+1);
      //      Py_DECREF(pyObj);
      return;
    }
    strPosition++;
  }
  glPopMatrix();
  pyObj = PyObject_CallMethod(uiElement,"positionText","(ii)",leftmostCharPosition,strPosition+1);
  //  Py_DECREF(pyObj);
}
void findTextWidth(PyObject * uiElement, int fontIndex, char* realStr, float rightMargin, int leftmostCharPosition, int rightmostCharPosition, int cursorPosition, int recalcValu){
  rightMargin = rightMargin-0.003;
  strPosition = 0;
  glPushMatrix();
  glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
  while(realStr[strPosition] != 0){//while the next char is not a space or end of string
    glCallList(list_base+(fontIndex*256)+(2*realStr[strPosition])+1);
    glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
    if(projMatrix[12] > rightMargin){
      glPopMatrix();
      //recalcValu comes straight from python
      if(recalcValu > 0){//calculate length from left
	findTextWidthFromLeft(uiElement,fontIndex,realStr,rightMargin,leftmostCharPosition);
      }else{//calculate length from right
	findTextWidthFromRight(uiElement,fontIndex,realStr,rightMargin,rightmostCharPosition);
      }
      return;
    }
    strPosition++;
  }
  glPopMatrix();
  pyObj = PyObject_CallMethod(uiElement,"textOkay",NULL);
  //  Py_DECREF(pyObj);  
}
void drawChar(int fontIndex,char* str, int strPosition,int cursorPosition){
  /*  if(strPosition == cursorPosition){
    drawCursor();
    }*/
  //  printf("%s\t%d\n",str,strPosition);
  glPushName(strPosition);
  //  glGetDoublev(GL_MODELVIEW_MATRIX,projMatrix);
  glCallList(list_base+(fontIndex<<8)+(str[strPosition]<<1));
  glPopName();
}
//float modelview_matrix[16];
int drawText(char* str,int fontIndex,int cursorPosition,float rightMargin,GLdouble* initTranslation){
  numLines = 1;
  glPushMatrix();
  textName = 0;
  strPosition = 0;
  //glPushAttrib(GL_LIST_BIT | GL_CURRENT_BIT | GL_ENABLE_BIT | GL_TRANSFORM_BIT); 
  //glDisable(GL_LIGHTING);
  //glEnable(GL_TEXTURE_2D);
  //  glGetFloatv(GL_MODELVIEW_MATRIX, modelview_matrix);
  while(str[strPosition] != 0){
    drawChar(fontIndex, str, strPosition, cursorPosition);
    strPosition++;
        if(str[strPosition-1] == 32 && str[strPosition] != 32 && str[strPosition] != 0 && checkRightMargin(fontIndex, str, strPosition+1,rightMargin)){
      glPopMatrix();
      glTranslatef(0.0,-80.0,0.0);
      glPushMatrix();
      }
  }
  if(strPosition == cursorPosition){
    drawCursor();
  }
  glPushName(strPosition);
  glCallList(list_base+(2*32));//draw a space at the end for cursor position
  glPopName();
  glPopMatrix();
  return numLines;
}
