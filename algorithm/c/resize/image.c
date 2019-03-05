/* ***********************************************************
 * Reference
 * https://openhome.cc/Gossip/CGossip/MallocFree.html
 *
 * Author tcyu@umich.edu @ 20190221
 * ******************************************************** */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <image.h>

#define DEBUG  1
#if DEBUG 
#define ASSERT             assert
#else 
#define ASSERT
#endif /* !DEBUG */


static inline int getoffset(int wX, int hX, int w, int h, int c)
{
	return c * wX * hX + h * wX + w;
}
UINT8 getpixel(Image *im, int w, int h, int c)
{
	return im->data[getoffset(im->w, im->h, w, h, c)];
}
/*
void setpixel(Image *im, int w, int h, int c, UINT8 pix)
{
	im->data[getoffset(im->w, im->h, w, h, c)] = pix;
} 

void setData(Image *image, int w, int to_w, 
                            int h, int to_h,
                            int c, int to_c,
                            UINT8 *data)
{
	int i, j, k, ii, jj, kk;
	for (i=c, ii=0; i<to_c; i++, ii++) {
		for (j=h, jj=0; j<to_h; j++, jj++) {
			int size = to_c - c;
			memcpy(&data[ii + jj + kk], &image->data[i + j + k], sizeof(UINT8) * size);
		}
	}
}
*/
void setImage(const Image *src, int h, int to_h, 
                          int w, int to_w,
                          int c, int to_c,
              Image *des, int hh, int ww, int cc)
{
	int i, j, ii, jj;
	int des_wh = des->w * des->h;
	int src_wh = src->w * src->h;

	int size = to_w - w;
	for (i=c, ii=cc; i<to_c; i++, ii++) {
		int iswh  = i * src_wh + w;
		int iidwh = ii  * des_wh + ww;
		for (j=h, jj=hh; j<to_h; j++, jj++) {

			memcpy(&des->data[iidwh  + jj  * des->w],
				   &src->data[iswh + j * src->w],
			       sizeof(UINT8) * size);
			
		}
	}
}
void printImageA(Image *img)
{
	int i, j, k;
	int wh = img->w * img->h;
	for (i=0; i<img->c; ++i) {
		int iwh = i * wh;
		INFO("c:%d\n[",i);
		for (j=0; j<img->h; ++j) {
			int jw = j*img->w;
			INFO("h:%d[",j);
			for (k=0; k<img->w-1; ++k) {
				INFO("%3hu,",img->data[iwh + jw + k]);
			}
			INFO("%hu",img->data[iwh + jw + img->w-1]);
			INFO("]\n");
		}

		INFO("]\n");
	}
}

void printImageN(ImageN *img)
{
	int i, j, k;
	for (i=0; i<img->c; ++i) {
		INFO("c:%d\n[",i);
		for (j=0; j<img->h; ++j) {
			INFO("h:%d[",j);
			for (k=0; k<img->w-1; ++k) {
				INFO("%3hu,",img->data[i][j][k]);
			}
			INFO("%hu",img->data[i][j][img->w-1]);
			INFO("]\n");
		}

		INFO("]\n");
	}
}

void printImage(Image *img, int h, int to_h,
	                        int w, int to_w,
	                        int c, int to_c)
{
	int i, j, k;
	int wh = img->w * img->h;
	for (i=c; i<to_c; i++) {
		int iwh = i * wh;
		INFO("c:%d[",i);
		for (j=h; j<to_h; j++) {
			int jw = j*w;
			INFO("h:%d[",j);
			for (k=w; k<to_w-1; ++k) {
				INFO("%hu,",img->data[iwh + jw + k]);
			}
			INFO("%hu",img->data[iwh + jw + to_w-1]);
			INFO("]\n");
		}
		INFO("]\n");
	}
}


Image createImageTest(int h, int w, int c)
{
	Image image = {0};
	int size = w * h * c;
	image.data = (UINT8 *) malloc(size * sizeof(UINT8));
	image.w = w;
	image.h = h;
	image.c = c;
	int i, j, k;
	for (i=0; i<c; ++i) {
		int cc = i * w * h;
		for (j=0; j<h; ++j) {
			int hh = j * w;
			for (k=0; k<w; ++k) {
				image.data[cc + hh + k] = cc + hh + k;
				//INFO("(%d,%d,%d): %hu\n",i,j,k,image.data[cc + hh + k]);
			}
		}
	}
	return image;
}


Image createImageEmpty(int h, int w, int c)
{
	Image image = {0};
	int size = w * h * c;
	image.data = (UINT8 *) malloc(size * sizeof(UINT8));
	image.w = w;
	image.h = h;
	image.c = c;
	return image;
}

Image createImageZero(int h, int w, int c)
{
	Image image = {0};
	int size = w * h * c;
	image.data = (UINT8 *) calloc(size, sizeof(UINT8));
	image.w = w;
	image.h = h;
	image.c = c;
	return image;
}

ImageN createImageNEmpty(int h, int w, int c)
{
	ImageN image;
	int i, j;
	image.data = (UINT8 ***) malloc(c * sizeof(UINT8**));
	for (i = 0; i < c; i++) {
		image.data[i] = (UINT8 **) malloc(h * sizeof(UINT8*));
		for (j = 0; j < h; j++) {
			image.data[i][j] = (UINT8 *) malloc(w * sizeof(UINT8));
		}
	}
	
	image.w = w;
	image.h = h;
	image.c = c;
	return image;
}

ImageN createImageNTest(int h, int w, int c)
{
	ImageN image = {0};

	int i, j, k;
	image.data = (UINT8 ***) malloc(c * sizeof(UINT8**));
	for (i = 0; i < c; i++) {
		image.data[i] = (UINT8 **) malloc(h * sizeof(UINT8*));
		for (j = 0; j < h; j++) {
			image.data[i][j] = (UINT8 *) malloc(w * sizeof(UINT8));
			for (k = 0; k < w; k++) {
				image.data[i][j][k] = i*h*w + j*w + k;
			}
		}
	}
	image.w = w;
	image.h = h;
	image.c = c;
	return image;
}


ImageN createImageNZero(int h, int w, int c)
{
	ImageN image = {0};

	int i, j;
	image.data = (UINT8 ***) calloc(c, sizeof(UINT8**));
	for (i = 0; i < c; i++) {
		image.data[i] = (UINT8 **) calloc(h, sizeof(UINT8*));
		for (j = 0; j < h; j++) {
			image.data[i][j] = (UINT8 *) calloc(w, sizeof(UINT8));
		}
	}
	image.w = w;
	image.h = h;
	image.c = c;
	return image;
}

void freeImage(Image *img)
{
	free(&img->data);
}
void freeImageN(ImageN *img)
{
	int i,j;
	for (i=0; i<img->c; ++i)
	{
		for (j=0; j<img->h; ++j)
		{
			free(img->data[i][j]);
		}
		free(img->data[i]);
	}
	free(img->data);
}
