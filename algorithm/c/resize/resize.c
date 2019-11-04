#include <image.h>
#include <resize.h>
#include <assert.h>
#include <stdio.h>

#define FBIT 13
#define HBIT (1 << (FBIT-1))

#define GOFLOAT 0

Image resize_nearestNeighbor(Image *img, int h, int w)
{
	Image im = createImageEmpty(h, w, img->c);
	int w_r = ((img->w << FBIT) + (w >> 1))/ w;
	int h_r = ((img->h << FBIT) + (h >> 1))/ h;
	int i, j, k;
	int im_wh = w * h;
	int img_wh = img->w * img->h;

	for (i = 0; i < img->c; i++) {
		int iwh = i * im_wh;
		int imwh = i * img_wh;
		for (j = 0; j < h; j++) {
			int ij   = iwh + j * w;
			int iijj = imwh + ((((j * h_r) + HBIT) >> FBIT) * img->w );
			for (k = 0; k < w; k++) {
				im.data[ij + k] = img->data[iijj + (((k * w_r) + HBIT) >> FBIT) ];
			}
		}
	}
	return im;


}

ImageN resizeN_nearestNeighbor(ImageN *img, int h, int w)
{
	ImageN im = createImageNEmpty(h, w, img->c);
	int w_r = ((img->w << FBIT) + (w >> 1)) / w;
	int h_r = ((img->h << FBIT) + (h >> 1)) / h;

	int i, j, k;
	for (i = 0; i < img->c; i++) {
		for (j = 0; j < h; j++) {
			int jh_r = (j * h_r + HBIT) >> FBIT;
			for (k = 0; k < w; k++) {
				im.data[i][j][k] =
				img->data[i][jh_r][(k * w_r + HBIT) >> FBIT];
			}
		}
	}
	return im;
}

Image resize(Image *img, int h, int w, RESIZE_FLAGS flag)
{
	if (flag == NEAREST) {
		return resize_nearestNeighbor(img, h, w);
	}
	else if (flag == INTER_LINEAR) {
		return (Image) {0};
	}
	else if (flag == BILINEAR) {
		return (Image) {0};
	}
	else assert(0);
	return (Image) {0};
}

ImageN resizeN(ImageN *img, int h, int w, RESIZE_FLAGS flag)
{
	if (flag == NEAREST) {
		return resizeN_nearestNeighbor(img, h, w);
	}
	else if (flag == INTER_LINEAR) {
		return (ImageN) {0};
	}
	else if (flag == BILINEAR) {
		return (ImageN) {0};
	}
	else assert(0);
	return (ImageN) {0};
}




