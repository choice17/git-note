#include <image.h>
#include <resize.h>

#include <stdio.h>

#define IMAGE 0

int main(void)
{
	//Image img = createImageTest(3,4,1);
#if IMAGE
	Image imgN = createImageTest(18,80,1);
	/*printf("imgN shape w:%d, h:%d, c:%d, pixel0: %hu\n", 6, 8, 2, getpixel(&imgN, 6, 8, 2));
	printImageA(&img);
	//printImage(&img, 0, 3, 0, 4, 0, 3);
	printf("\n");
	printImageA(&imgN);
	//printImage(&imgN, 0, 7, 0, 9, 0, 3);
	printf("\n");
	setImage(&img, 0, 3, 0, 4, 0, 1, &imgN, 4, 5, 0);
	printf("img shape w:%d, h:%d, c:%d, pixel0: %hu\n", img.w, img.h, img.c, getpixel(&img, 2, 4, 2));
	printImageA(&img);
	//printImage(&img, 0, 3, 0, 4, 0, 3);
	*/
	printf("\n");
	printImageA(&imgN);
	Image nimg = resize(&imgN, 9, 20, 0);
	printImageA(&nimg);
	freeImage(&imgN);
	freeImage(&nimg);
	return 0;
#else
	ImageN img = createImageNTest(18,20,1);
	printImageN(&img);
	ImageN nimg = resizeN(&img, 5, 8, 0);
	printf("hih\n");
	printImageN(&nimg);
	freeImageN(&img);
	freeImageN(&nimg);
	return 0;
#endif 

}