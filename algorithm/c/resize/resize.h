#ifndef RESIZE_H_
#define RESIZE_H_

typedef enum {
	NEAREST,
	INTER_LINEAR,
	BILINEAR
} RESIZE_FLAGS;

Image resize(Image *img, int h, int w, RESIZE_FLAGS flag);
ImageN resizeN(ImageN *img, int h, int w, RESIZE_FLAGS flag);
#endif /* !RESIZE_H_ */
