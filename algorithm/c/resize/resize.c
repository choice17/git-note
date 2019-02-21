#include <image.h>
#include <resize.h>
#include <assert.h>

#define FBIT 13
#define HBIT (1 << (FBIT-1))

#define GOFLOAT 0

Image resize_nearestNeighbor(int h, int w, Image *img)
{
	Image im = createImageEmpty(h, w, img->c);
#if GOFLOAT
	int w_r = ((img->w << FBIT) + (w >> 1))/ w;
	int h_r = ((img->h << FBIT) + (h >> 1))/ h;
#else
	float w_r = (float) (img->w) / w;
	float h_r = (float) (img->h) / h;
#endif 
	int i, j, k;
	int im_wh = w * h;
	int img_wh = img->w * img->h;

	for (i = 0; i < img->c; i++) {
		int iwh = i * im_wh;
		int imwh = i * img_wh;
		for (j = 0; j < h; j++) {
			int ij   = iwh + j * w;
#if GOFLOAT
			int iijj = imwh + ((((j * h_r) + HBIT) >> FBIT) * img->w );
			for (k = 0; k < w; k++) {
				im.data[ij + k] = img->data[iijj + (((k * w_r) + HBIT) >> FBIT) ];
#else
			int iijj = imwh + (int) ((float) j * h_r * img->w) ;
			for (k = 0; k < w; k++) {
				im.data[ij + k] = img->data[iijj + (int) ((float) k * w_r) ];
#endif 
			}
		}
	}
	return im;


}

Image resize(Image *img, int h, int w, RESIZE_FLAGS flag)
{
	if (flag == NEAREST) {
		return resize_nearestNeighbor(h, w, img);
	}
	//else if (RESIZE_FLAGS == INTER_LINEAR)
	//	return NULL;
	//else if (RESIZE_FLAGS == BILINEAR)
	//	return NULL;
	else assert(0);

	Image im = createImageEmpty(1,1,1);
	return im;
}
/*
ImageN *resizeN(int w, int h, ImageN *img, RESIZE_FLAGS flag)
{
	if (RESIZE_FLAGS == NEAREST)
		return resizeN_nearestNeighbor(w, h, img);
	else if (RESIZE_FLAGS == INTER_LINEAR)
		return NULL;
	else if (RESIZE_FLAGS == BILINEAR)
		return NULL;
	else assert(0);
}
*/


/*
inline ImageN resizeN_nearestNeighbor(int w, int h, Image *img)
{
	ImageN im = createImageNEmpty(w, h, img->c);
	int w_r = w << FBIT / img->w;
	int h_r = h << FBIT / img->h;

	int i, j, k;
	for (i = 0; i < img->c; i++) {
		for (j = 0; j < h; j++) {
			int jh_r = j * h_r >> FBIT;
			for (k = 0; k < w; k++) {
				im.data[i][j][k] =
				img->data[i][jh_r][(k * w_r) >> FBIT];
			}
		}
	}
	return im;
}
*/