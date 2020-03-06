#ifndef HOG_H_
#define HOG_H_

#include <stdint.h>

#define HOG_F_BS 8

#define HOG_CELL_SIZE 8
#define HOG_CELL_BIN_NUM 9
#define HOG_BLOCK_CELL_NUM 4
#define HOG_BLOCK_STRIDE_PIX 8

typedef struct {
    float *bins;
    int bin_num;
    int bin_w;
    int bin_h;
    int bin_size;
} HOG_descriptor;

typedef struct {
    int *bins;
    int bin_num;
    int bin_w;
    int bin_h;
    int bin_size;
} HOG_descriptorF;

typedef struct {
    int cell_size;
    int cell_bin_num;
    int block_cell_num;
    int block_stride_pix;
} HOG_PARAM_S;

typedef struct {
    uint8_t *data;
    int w;
    int h;
} IMAGE_S;

typedef struct {
    int x;
    int y;
    int w;
    int h;
} ROI_S;

HOG_descriptor *hog_getDescriptor(const IMAGE_S *img);
HOG_descriptor *hog_getDescriptorRoi(const IMAGE_S *img, const ROI_S *roi);
HOG_descriptor *hog_getDescriptorParam(const IMAGE_S *img, const HOG_PARAM_S *param);

HOG_descriptorF *hog_getDescriptorF(const IMAGE_S *img);
HOG_descriptorF *hog_getDescriptorRoiF(const IMAGE_S *img, const ROI_S *roi);
HOG_descriptorF *hog_getDescriptorParamF(const IMAGE_S *img, const HOG_PARAM_S *param);

#endif /* HOG_H_ */



