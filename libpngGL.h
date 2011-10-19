#ifndef LIBPNG_GL_H
#define LIBPNG_GL_H

#include <SDL.h>
//#include <SDL_opengl.h>

//shamelessly stolen from here:
//http://macdevcenter.com/pub/a/mac/2005/10/14/texture-maps.html?page=3
void pngLoad(GLuint *textur, char *file){
  //  char *imageData;
  FILE         *infile;         /* PNG file pointer */
  png_structp   png_ptr;        /* internally used by libpng */
  png_infop     info_ptr;       /* user requested transforms */
  char         *image_data;      /* raw png image data */
  char         sig[8];           /* PNG signature array */
  int           bit_depth;
  int           color_type;
  unsigned long width;            /* PNG image width in pixels */
  unsigned long height;           /* PNG image height in pixels */
  unsigned int rowbytes;         /* raw bytes at row n in image */
  image_data = NULL;
  int i;
  png_bytepp row_pointers = NULL;
  infile = fopen(file, "rb");
  if (!infile) {
    exit(0);
  }
  fread(sig, 1, 8, infile);
  if (!png_check_sig((unsigned char *) sig, 8)) {
    fclose(infile);
    exit(0);
  }
  png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
  if (!png_ptr) {
    fclose(infile);
    exit(4);    /* out of memory */
  }
	
  info_ptr = png_create_info_struct(png_ptr);
  if (!info_ptr) {
    png_destroy_read_struct(&png_ptr, (png_infopp) NULL, (png_infopp) NULL);
    fclose(infile);
    exit(4);    /* out of memory */
  }
  if (setjmp(png_jmpbuf(png_ptr))) {
    png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
    fclose(infile);
    exit(0);
  }
  png_init_io(png_ptr, infile);
  png_set_sig_bytes(png_ptr, 8);
  png_read_info(png_ptr, info_ptr);
  png_get_IHDR(png_ptr, info_ptr, &width, &height, &bit_depth, &color_type, NULL, NULL, NULL);

  //  if (color_type & PNG_COLOR_MASK_ALPHA) {
  //  png_set_strip_alpha(png_ptr);
  //}
  if (bit_depth > 8) {
    png_set_strip_16(png_ptr);
  }
  if (color_type == PNG_COLOR_TYPE_GRAY ||
      color_type == PNG_COLOR_TYPE_GRAY_ALPHA) {
    png_set_gray_to_rgb(png_ptr);
  }
  if (color_type == PNG_COLOR_TYPE_PALETTE) {
    png_set_palette_to_rgb(png_ptr);
  }

  png_set_tRNS_to_alpha(png_ptr);   
  png_set_strip_16(png_ptr);

  png_read_update_info(png_ptr, info_ptr);
  rowbytes = png_get_rowbytes(png_ptr, info_ptr);
  image_data = (unsigned char *) malloc(rowbytes * height);
  row_pointers = (png_bytepp)malloc(height*sizeof(png_bytep));
	
  for (i = 0;  i < height;  ++i)
    row_pointers[height - 1 - i] = image_data + i*rowbytes;

  png_read_image(png_ptr, row_pointers);
  png_read_end(png_ptr, NULL);
  //cleanup
  free(row_pointers);
  png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
  fclose(infile);

   glGenTextures(1,textur);
   glBindTexture(GL_TEXTURE_2D, *textur);
    //  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
    //glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
	
  //	glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
  /*	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);*/
    //    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND);
    printf("%s\n",file);
    printf("colortype: %d\n",color_type);
  if(file[7] == 't' && file[9] == 's'){
    printf("PNG_COLOR_TYPE_RGB_ALPHA: %d\n",PNG_COLOR_TYPE_RGB_ALPHA);
    printf("PNG_COLOR_TYPE_PALETTE: %d\n",PNG_COLOR_TYPE_PALETTE);
    printf("%ld\n",height);
    printf("%d\n",rowbytes);
    printf("%ld\n",rowbytes * height);
    int i;
    for(i=0;i<16;i++){
      printf("%d %d\n",i,image_data[i]);
    }
    printf("done\n");
  }
  //  gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image_data);
  //  glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data);
  glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data);

  //glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data);
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);


  //glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data);
  //glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data);
 
  //	return texture;
}
#endif
