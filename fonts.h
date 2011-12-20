#include <stdio.h>
#include <SDL.h>
#include <SDL_opengl.h>
#include "libpngGL.h"

#define ARIAL 0
#define HERCULANUM 1

#define TRANSPARENT_PIXEL_IMAGE "assets/transparentPixel.png"
#define TRANSPARENT_PIXEL_INDEX 0
#define WHITE_PIXEL_IMAGE "assets/whitePixel.png"
#define WHITE_PIXEL_INDEX 1

#define FONT_NAME_SIZE 50

char fontFiles[3][FONT_NAME_SIZE] = {
  "assets/fonts/Arial.ttf",
  "assets/fonts/XXII ARABIAN-ONENIGHTSTAND.ttf",
  "assets/fonts/Herculanum.ttf",
};

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
void make_dlist ( FT_Face face, char charIndex, GLuint list_base, GLuint * tex_base ) {

  if(FT_Load_Glyph( face, FT_Get_Char_Index( face,charIndex), FT_LOAD_DEFAULT )){
    printf("FT_Load_Glyph failed");
    exit(1);
  }

  if(FT_Get_Glyph( face->glyph, &glyph )){
    printf("FT_Get_Glyph failed");
    exit(1);
  }
  FT_Glyph_To_Bitmap( &glyph, FT_RENDER_MODE_NORMAL, 0, 1 );
  
  bitmap_glyph = (FT_BitmapGlyph)glyph;
  bitmap = (FT_Bitmap)bitmap_glyph->bitmap;
  dataWidth = nextPowerOf2( bitmap.width );
  dataHeight = nextPowerOf2( bitmap.rows );
  expanded_data = malloc(2 * dataWidth * dataHeight * sizeof(GLubyte));
  if(bitmap.rows != 0){//space char has 0 height, but we need it for the 'empty' quads between chars, so we'll use the previous char's height
    glyphHeight = bitmap.rows;
  }
  glyphWidth = bitmap.width;
  for(j=0; j < dataHeight; j++){
    for(i=0; i < dataWidth; i++){
      expanded_data[2*(i+j*dataWidth)]= expanded_data[2*(i+j*dataWidth)+1] = 
	(i>=glyphWidth || j>=glyphHeight) ?
	0 : bitmap.buffer[i + glyphWidth*j];
    }
  }
  //TextureWidth = glyphWidth;
  //TextureHeight = glyphHeight;

  glBindTexture(GL_TEXTURE_2D, tex_base[charIndex]);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, dataWidth, dataHeight, 0, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE, expanded_data);
  //delete expanded_data;

  glNewList(list_base+charIndex,GL_COMPILE);

  glPushMatrix();

  // We Need To Account For The Fact That Many Of
  // Our Textures Are Filled With Empty Padding Space.
  // We Figure What Portion Of The Texture Is Used By 
  // The Actual Character And Store That Information In
  // The x And y Variables, Then When We Draw The
  // Quad, We Will Only Reference The Parts Of The Texture
  // That Contains The Character Itself.
  x=(float)glyphWidth / (float)dataWidth;
  y=(float)glyphHeight / (float)dataHeight;

  // Move Down A Little In The Case That The
  // Bitmap Extends Past The Bottom Of The Line 
  // This Is Only True For Characters Like 'g' Or 'y'.
  // We Need To Move Over A Little So That
  // The Character Has The Right Amount Of Space
  // Between It And The One Before It.
  glBlendFunc(GL_SRC_ALPHA, GL_ONE);
  glBegin(GL_QUADS);
  glVertex2f(-4,glyphHeight);
  glVertex2f(-4,0);
  //  glVertex2f(bitmap_glyph->left,0);
  //  glVertex2f(bitmap_glyph->left,glyphHeight);
  glVertex2f(face->glyph->advance.x>>6,0);
  glVertex2f(bitmap_glyph->left,glyphHeight);

  glEnd();
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  glTranslatef(bitmap_glyph->left,bitmap_glyph->top-glyphHeight,0);

  // Here We Draw The Texturemapped Quads.
  // The Bitmap That We Got From FreeType Was Not 
  // Oriented Quite Like We Would Like It To Be,
  // But We Link The Texture To The Quad
  // In Such A Way That The Result Will Be Properly Aligned.
  //  printf("%c %d %d %d %f %f %d\n",charIndex,charIndex,glyphHeight,glyphWidth,x,y,face->glyph->advance.x>>6);
  glBindTexture(GL_TEXTURE_2D,tex_base[charIndex]);
  glBegin(GL_QUADS);
  glTexCoord2d(0,0); glVertex2f(0,glyphHeight);
  glTexCoord2d(0,y); glVertex2f(0,0);
  glTexCoord2d(x,y); glVertex2f(glyphWidth,0);
  glTexCoord2d(x,0); glVertex2f(glyphWidth,glyphHeight);
  glEnd();
  glPopMatrix();
  //glTranslatef(glyphWidth+5,0,0);
  /*glBegin(GL_QUADS);
  glTexCoord2d(0,0); glVertex2f(glyphWidth,glyphHeight);
  glTexCoord2d(0,y); glVertex2f(glyphWidth,0);
  glTexCoord2d(x,y); glVertex2f((face->glyph->advance.x>>6),0);
  glTexCoord2d(x,0); glVertex2f((face->glyph->advance.x>>6),glyphHeight);
  glEnd();*/
  glTranslatef(face->glyph->advance.x >> 6 ,0,0);
 

  // Increment The Raster Position As If We Were A Bitmap Font.
  // (Only Needed If You Want To Calculate Text Length)
  glBitmap(0,0,0,0,face->glyph->advance.x >> 6,0,NULL);

  // Finish The Display List
  glEndList();

}


static void initFonts(){
  //loadFont(ARIAL,16);
  FT_Library library;
  FT_Face face; 
  int error = FT_Init_FreeType( &library );
  //  if(FT_New_Face(library,"assets/fonts/Ceria Lebaran.otf",0,&face)){
    //XXII ARABIAN-ONENIGHTSTAND.ttf
  
  long int fontCount = sizeof(fontFiles)/FONT_NAME_SIZE;
  GLuint textures[128*fontCount];
  list_base=glGenLists(128*fontCount);
  glGenTextures(128*fontCount,textures);

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
    // This Is Where We Actually Create Each Of The Fonts Display Lists.
    int i;
    for(i=0;i<128;i++){
      make_dlist(face,i,list_base+(128*index),textures+(128*index));
    }
    FT_Done_Face(face);
  }
  FT_Done_FreeType(library);
}
void drawCursor(){
  glPushMatrix();
  float currentColor[4];
  glGetFloatv(GL_CURRENT_COLOR,currentColor);
  glBindTexture(GL_TEXTURE_2D,0);
  glColor4f(currentColor[0],currentColor[1],currentColor[2],currentColor[3]);
  glTranslatef(-3.0,0.0,100.0);
  glBegin(GL_QUADS);
  glTexCoord2d(0,0); glVertex2f(0,60);
  glTexCoord2d(0,1); glVertex2f(0,-10);
  glTexCoord2d(1,1); glVertex2f(6,-10);
  glTexCoord2d(1,0); glVertex2f(6,60);
  glEnd();
  glPopMatrix();
}

int strCount;
float modelview_matrix[16];
void drawText(char* str,int fontIndex,int cursorPosition){
  textName = 0;
  glPushAttrib(GL_LIST_BIT | GL_CURRENT_BIT | GL_ENABLE_BIT | GL_TRANSFORM_BIT); 
  //glMatrixMode(GL_MODELVIEW);
  glDisable(GL_LIGHTING);
  glEnable(GL_TEXTURE_2D);
  //glDisable(GL_DEPTH_TEST);
  //glEnable(GL_BLEND);
  //glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);      
  glGetFloatv(GL_MODELVIEW_MATRIX, modelview_matrix);
  //glListBase(list_base);
  //glCallLists(strlen(str), GL_UNSIGNED_BYTE, str);
  for(strCount = 0;str[strCount] != 0;strCount++){
    if(strCount == cursorPosition){
      drawCursor();
    }
    glPushName(strCount);
    glCallList(list_base+(fontIndex*128)+str[strCount]);
    glPopName();
  }
  if(strCount == cursorPosition){
    drawCursor();
  }
  glPushName(strCount);
  glCallList(list_base+32);//draw a space at the end
  glPopName();
}
