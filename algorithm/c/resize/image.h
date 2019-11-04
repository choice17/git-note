#ifndef IMAGE_H_
#define IMAGE_H_

#define INFO  printf

typedef char                   INT8;
typedef unsigned char          UINT8;

typedef short int              INT16;
typedef unsigned short int     UINT16;

typedef int                    INT32;
typedef unsigned int           UINT32;

typedef long long int          INT64;
typedef unsigned long long int UINT64;

typedef float                  FLOAT32;
typedef double                 FLOAT64;

#define IMAGE_FORMAT "BCHW"

typedef enum {
	COLOR_BGR,
	COLOR_RGB,
	COLOR_YUV,
	COLOR_GRAY,
} COLOR_MODE;


#define     _uint8      8
#define     _int8       8
#define     _uint16     16
#define     _int16      16    
#define     _uint32     32
#define     _int32      32    
#define     _uint64     64
#define     _int64      64
#define     _float32    32
#define     _float64    64

typedef struct {
	int w;
	int h;
	int c;
	UINT8 *data;
	COLOR_MODE mode;
	int dtype;
} Image;

typedef struct {
	int b;
	int w;
	int h;
	int c;
	UINT8 *data;
	COLOR_MODE mode;
	int dtype;
} Image_s;

typedef struct {
	int w;
	int h;
	int c;
	UINT8 ***data;
	COLOR_MODE mode;
} ImageN;

Image createImageTest(int h, int w, int c);
ImageN createImageNTest(int h, int w, int c);
Image createImageEmpty(int h, int w, int c);
Image createImageZero(int h, int w, int c);
ImageN createImageNEmpty(int h, int w, int c);
ImageN createImageNZero(int h, int w, int c);

void printImage(Image *img, int h, int to_h,
	                        int w, int to_w,
	                        int c, int to_c);
void printImageA(Image *img);
void printImageN(ImageN *img);

void setImage(const Image *src, int h, int to_h,
	                      int w, int to_w,
                          int c, int to_c,
              Image *des, int hh, int ww, int cc);
void freeImage(Image *img);
void freeImageN(ImageN *img);

void setpixel(Image *img, int h, int w, int c, UINT8 pix);
UINT8 getpixel(Image *img, int h, int w, int c);

#endif /* !IMAGE_H_ */
