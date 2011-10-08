#ifndef LIBPNG_GL_H
#define LIBPNG_GL_H

#include <SDL.h>
#include <SDL_opengl.h>

//shamelessly stolen from here:
//http://macdevcenter.com/pub/a/mac/2005/10/14/texture-maps.html?page=3
void pngLoad(GLuint *textur, char *file){
  //	GLuint texture;
  char *imageData;
  FILE         *infile;         /* PNG file pointer */
  png_structp   png_ptr;        /* internally used by libpng */
  png_infop     info_ptr;       /* user requested transforms */
	
  char         *image_data;      /* raw png image data */
  char         sig[8];           /* PNG signature array */
  /*char         **row_pointers;   */
	
  int           bit_depth;
  int           color_type;
	
  unsigned long width;            /* PNG image width in pixels */
  unsigned long height;           /* PNG image height in pixels */
  unsigned int rowbytes;         /* raw bytes at row n in image */
	
  image_data = NULL;
  int i;
  png_bytepp row_pointers = NULL;
	
  /* Open the file. */
  infile = fopen(file, "rb");
  if (!infile) {
    exit(0);
  }
	
  /* Check for the 8-byte signature */
  fread(sig, 1, 8, infile);
	
  if (!png_check_sig((unsigned char *) sig, 8)) {
    fclose(infile);
    exit(0);
  }
	
  /* 
   * Set up the PNG structs 
   */
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
	
	
  /*
   * block to handle libpng errors, 
   * then check whether the PNG file had a bKGD chunk
   */
  if (setjmp(png_jmpbuf(png_ptr))) {
    png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
    fclose(infile);
    exit(0);
  }
	
  /* 
   * takes our file stream pointer (infile) and 
   * stores it in the png_ptr struct for later use.
   */
  /* png_ptr->io_ptr = (png_voidp)infile;*/
  png_init_io(png_ptr, infile);
	
  /*
   * lets libpng know that we already checked the 8 
   * signature bytes, so it should not expect to find 
   * them at the current file pointer location
   */
  png_set_sig_bytes(png_ptr, 8);
	
  /* Read the image info.*/
	
  /*
   * reads and processes not only the PNG file's IHDR chunk 
   * but also any other chunks up to the first IDAT 
   * (i.e., everything before the image data).
   */
	
  /* read all the info up to the image data  */
  png_read_info(png_ptr, info_ptr);
	
  png_get_IHDR(png_ptr, info_ptr, &width, &height, &bit_depth, 
	       &color_type, NULL, NULL, NULL);
	
  //*pwidth = width;
  //*pheight = height;
	
  /* Set up some transforms. */
  if (color_type & PNG_COLOR_MASK_ALPHA) {
    png_set_strip_alpha(png_ptr);
  }
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
	
  /* Update the png info struct.*/
  png_read_update_info(png_ptr, info_ptr);
	
  /* Rowsize in bytes. */
  rowbytes = png_get_rowbytes(png_ptr, info_ptr);
	
	
  /* Allocate the image_data buffer. */
  if ((image_data = (unsigned char *) malloc(rowbytes * height))==NULL) {
    png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
    exit(4);
  }
	
  if ((row_pointers = (png_bytepp)malloc(height*sizeof(png_bytep))) == NULL) {
    png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
    free(image_data);
    image_data = NULL;
    exit(4);
  }
	
	
  /* set the individual row_pointers to point at the correct offsets */
	
  for (i = 0;  i < height;  ++i)
    row_pointers[height - 1 - i] = image_data + i*rowbytes;
	
	
  /* now we can go ahead and just read the whole image */
  png_read_image(png_ptr, row_pointers);
	
  /* and we're done!  (png_read_end() can be omitted if no processing of
   * post-IDAT text/time/etc. is desired) */
	
  /* Clean up. */
  free(row_pointers);
	
  /* Clean up. */
  png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
  fclose(infile);
  glGenTextures(1,textur);
  //	*image_data_ptr = image_data;
  glBindTexture(GL_TEXTURE_2D, *textur);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
	
  //	glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
  /*	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);*/
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data);//original tiles.png used this(perhaps GIMP too), output from photoshop uses the one below
  //glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data);
  //glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data);
 
  //	return texture;
}
#endif
