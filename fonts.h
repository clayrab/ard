#include <stdio.h>
#include <SDL.h>
#include <SDL_opengl.h>


#define ARIAL 0
#define HERCULANUM 1
char fontFiles[2][30] = {
  "assets/fonts/Arial.ttf",
  "assets/fonts/Herculanum.ttf"
};

int TextureWidth;
int TextureHeight;
int BitmapWidth;
int BitmapHeight;
GLuint list_base;
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

void make_dlist ( FT_Face face, char charIndex, GLuint list_base, GLuint * tex_base ) {

  if(FT_Load_Glyph( face, FT_Get_Char_Index( face,charIndex), FT_LOAD_DEFAULT )){
    printf("FT_Load_Glyph failed");
    exit(1);
  }

  FT_Glyph glyph;
  if(FT_Get_Glyph( face->glyph, &glyph )){
    printf("FT_Get_Glyph failed");
    exit(1);
  }
  FT_Vector origin;
  FT_Glyph_To_Bitmap( &glyph, FT_RENDER_MODE_NORMAL, 0, 1 );
  
  FT_BitmapGlyph bitmap_glyph = (FT_BitmapGlyph)glyph;
  FT_Bitmap bitmap = (FT_Bitmap)bitmap_glyph->bitmap;
  int width = nextPowerOf2( bitmap.width );
  int height = nextPowerOf2( bitmap.rows );
  GLubyte* expanded_data = malloc(2 * width * height * sizeof(GLubyte));
  int i;
  int j;
  for(j=0; j < height; j++){
    for(i=0; i < width; i++){
      expanded_data[2*(i+j*width)]= expanded_data[2*(i+j*width)+1] = 
	(i>=bitmap.width || j>=bitmap.rows) ?
	0 : bitmap.buffer[i + bitmap.width*j];
    }
  }
  //TextureWidth = bitmap.width;
  //TextureHeight = bitmap.rows;

  glBindTexture(GL_TEXTURE_2D, tex_base[charIndex]);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE, expanded_data);
  //delete expanded_data;

  glNewList(list_base+charIndex,GL_COMPILE);

  glBindTexture(GL_TEXTURE_2D,tex_base[charIndex]);

  glPushMatrix();

  // First We Need To Move Over A Little So That
  // The Character Has The Right Amount Of Space
  // Between It And The One Before It.
  glTranslatef(bitmap_glyph->left,0,0);

  // Now We Move Down A Little In The Case That The
  // Bitmap Extends Past The Bottom Of The Line 
  // This Is Only True For Characters Like 'g' Or 'y'.
  glTranslatef(0,bitmap_glyph->top-bitmap.rows,0);

  // Now We Need To Account For The Fact That Many Of
  // Our Textures Are Filled With Empty Padding Space.
  // We Figure What Portion Of The Texture Is Used By 
  // The Actual Character And Store That Information In
  // The x And y Variables, Then When We Draw The
  // Quad, We Will Only Reference The Parts Of The Texture
  // That Contains The Character Itself.
  float   x=(float)bitmap.width / (float)width,
    y=(float)bitmap.rows / (float)height;

  // Here We Draw The Texturemapped Quads.
  // The Bitmap That We Got From FreeType Was Not 
  // Oriented Quite Like We Would Like It To Be,
  // But We Link The Texture To The Quad
  // In Such A Way That The Result Will Be Properly Aligned.
  glBegin(GL_QUADS);
  glTexCoord2d(0,0); glVertex2f(0,bitmap.rows);
  glTexCoord2d(0,y); glVertex2f(0,0);
  glTexCoord2d(x,y); glVertex2f(bitmap.width,0);
  glTexCoord2d(x,0); glVertex2f(bitmap.width,bitmap.rows);
  glEnd();
  glPopMatrix();
  glTranslatef(face->glyph->advance.x >> 6 ,0,0);

  // Increment The Raster Position As If We Were A Bitmap Font.
  // (Only Needed If You Want To Calculate Text Length)
  // glBitmap(0,0,0,0,face->glyph->advance.x >> 6,0,NULL);

  // Finish The Display List
  glEndList();

}


static void initFonts(){
  //loadFont(ARIAL,16);
  FT_Library library;
  FT_Face face; 
  int error = FT_Init_FreeType( &library );
  if(FT_New_Face(library,"assets/fonts/Arial.ttf",0,&face)){
    printf("FT_New_Face error");
    exit(1);
  }
  if(FT_Set_Char_Size(face, 16*64, 0, 300, 0)){
    printf("FT_Set_Char_Size error");
    exit(1);
  }

  GLuint textures[128];
  list_base=glGenLists(128);
  glGenTextures( 128, textures );

  // This Is Where We Actually Create Each Of The Fonts Display Lists.
  int i;
  for(i=0;i<128;i++){
    make_dlist(face,i,list_base,textures);
  }

  FT_Done_Face(face);
  FT_Done_FreeType(library);
}
void drawText(char* str){
  glPushAttrib(GL_LIST_BIT | GL_CURRENT_BIT  | GL_ENABLE_BIT | GL_TRANSFORM_BIT); 
  //glMatrixMode(GL_MODELVIEW);
  glDisable(GL_LIGHTING);
  glEnable(GL_TEXTURE_2D);
  //glDisable(GL_DEPTH_TEST);
  //glEnable(GL_BLEND);
  //glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);      
  
  glListBase(list_base);

  float modelview_matrix[16];     
  glGetFloatv(GL_MODELVIEW_MATRIX, modelview_matrix);
  glCallLists(strlen(str), GL_UNSIGNED_BYTE, str);

}
