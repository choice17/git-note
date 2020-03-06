#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "hog.h"

#define HOG_DEBUG
#ifdef HOG_DEBUG
#define HOG_DEB_MSG(fmt, args...) printf("%s:%d " fmt, __func__, __LINE__)
#else
#define HOG_DEB_MSG(fmt, args...)
#endif /* HOG_DEBUG */

#define pr printf
#define prd() printf("%s:%d\n", __func__,__LINE__)

static inline int max(int x, int y) { return (x > y) ? (x) : (y) ;}
static inline int min(int x, int y) { return (x < y) ? (x) : (y) ;}
static inline int clip(int x, int min, int max)
{
    return ((x < min) ? (min) : ((x > max) ? max : x));
}

static inline int reflect(int x, int max)
{
    return ((x < 0) ? (-x) : ((x >= max)? (max - (x-max)-2):(x)));
}

static inline int op_mul(const uint8_t *x, const int *y, int size)
{
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += x[i] * y[i];
    }
    return sum;
}

static inline int op_mul_y(const uint8_t *x, const int *y, int xw, int size)
{
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += x[i * xw] * y[i];
    }
    return sum;
}

static inline int *op_conv(const uint8_t *x, int xw, int xh, const int *k, int kw, int kh, int *y)
{
}


static inline int get_pixel(const uint8_t *data, int dw, int dh, int x, int y)
{
    return (data[y * dw + x]);
}

static inline void **op_hog(const uint8_t *data, int dw, int dh)
{
    float *out_mag = (float *)malloc(sizeof(float) * dw * dh);
    float *out_rad = (float *)malloc(sizeof(float) * dw * dh);
    void **ptr = (void **)malloc(sizeof(void *) * 2);
    ptr[0] = (void *)out_mag;
    ptr[1] = (void *)out_rad;
    prd();
    int i, j, k, p, q, r;
    int tmp_r, d_idx, r_idx, c_idx;
    int dx, dy, mag, ang;

    const int kernel[] = {-1, 0, 1};
    int kh = 3; int kw = 3;
    int i_init = kh/2, i_end = kh - i_init; 
    int j_init = kw/2, j_end = kw - j_init;
    int x, y;
    prd();
    /* need to deal with padding problem */
    for (i = 0; i < i_init; i++) {
        for (j = 0; j < dw; j++) {
            dx = 0; dy = 0;
            for (p = -i_init, r=0; p < i_end; p++, r++) {
                y = reflect(i + p, dh);
                x = reflect(j, dw);
                dy += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dy:%d\n", i + p, dh, y, j, dw, x, dy);
            }
 
            for (q = -j_init, r = 0; q < j_end; q++, r++) {
                y = reflect(i, dh);
                x = reflect(j + q, dw);
                dx += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dx:%d\n", i, dh, y, j+q, dw, x, dx);
            }

            d_idx = i * dw + j;
            out_mag[d_idx] = sqrt((dx * dx + dy * dy));
            out_rad[d_idx] = atan((float)dy / (dx+0.0001f));
            printf("top:mag: [y:%d,x:%d], %.2f, %d**2 + %d**2\n", i, (j), out_mag[d_idx],
                dx, dy);
        }
    }

    for (i = 0; i < i_end; i++) {
        for (j = 0; j < dw; j++) {
            dx = 0; dy = 0;
            for (p = -i_init, r=0; p < i_end; p++, r++) {
                y = reflect(dh - i_end + p + i, dh);
                x = reflect(j, dw);
                dy += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dy:%d\n", dh - i + p -1, dh, y, j, dw, x, dy);
            }
            for (q = -j_init, r = 0; q < j_end; q++, r++) {
                y = reflect(dh - i -1, dh);
                x = reflect(j + q, dw);
                dx += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dx:%d\n", dh - i -1, dh, y, j + q, dw, x, dx);
            }

            d_idx = (dh - i_end + i)* dw + j;
            out_mag[d_idx] = sqrt((float)(dx * dx + dy * dy));
            out_rad[d_idx] = atan((float)dy / (dx+0.0001f));
            printf("bottom:mag: [y:%d,x:%d], %.2f, %d**2 + %d**2\n", dh - i_end + i, (j), out_mag[d_idx],
                dx, dy);
            out_rad[d_idx] = atan((float)dy / (dx+0.0001f));
        }
    }

    for (i = i_init; i < dh - i_end; i++) {
        for (j = 0; j < j_init; j++) {
            dx = 0; dy = 0;
            for (p = -i_init, r=0; p < i_end; p++, r++) {
                y = reflect(i + p, dh);
                x = reflect(j, dw);
                dy += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dx:%d\n", i + p, dh, y, j, dw, x, dy);
            }
            for (q = -j_init, r = 0; q < j_end; q++, r++) {
                y = reflect(i, dh);
                x = reflect(j + q, dw);
                dx += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dy:%d\n", i, dh, y, j + q, dw, x, dy);
            }
            d_idx = i * dw + j;
            out_mag[d_idx] = sqrt((float)(dx * dx + dy * dy));
            printf("left:mag: [y:%d,x:%d], %.2f, %d**2 + %d**2\n", i, (j), out_mag[d_idx],
                dx, dy);
            out_rad[d_idx] = atan((float)dy / (dx+0.0001f));
        }
    }
    for (i = i_init; i < dh - i_end; i++) {
        for (j = 0; j < j_end; j++) {
            dx = 0; dy = 0;
            for (p = -i_init, r=0; p < i_end; p++, r++) {
                y = reflect(dh - i + p -1, dh);
                x = reflect(j, dw);
                dy += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dy:%d\n", dh - i + p -1, dh, y, j, dw, x, dy);
            }
            for (q = -j_init, r = 0; q < j_end; q++, r++) {
                y = reflect(dh - i -1, dh);
                x = reflect(j + q, dw);
                dx += get_pixel(data, dw, dh, x, y) * kernel[r];
                printf("reflect: y:%d,%d->%d, %d,%d->%d dx:%d\n", dh - i -1, dh, y, j + q, dw, x, dx);
            }
            d_idx = i* dw + (dh - j_end + j);
            out_mag[d_idx] = sqrt((float)(dx * dx + dy * dy));
            printf("right:mag: [y:%d,x:%d], %.2f, %d**2 + %d**2\n", i, (dh - j_end+ j), out_mag[d_idx],
                dx, dy);
            out_rad[d_idx] = atan((float)dy / (dx+0.0001f));
        }
    }
    prd();
    for (i = i_init; i < dh - i_end; i++) {
        tmp_r = i * dw;
        for (j = j_init; j < dw - j_end; j++) {
            d_idx = tmp_r + j;
            dx = op_mul(&data[d_idx-kw/2], kernel, kw);
            dy = op_mul_y(&data[d_idx- (dw * (kw/2))], kernel, dw, kw);
            out_mag[d_idx] = sqrt((float)(dx * dx + dy * dy));
            out_rad[d_idx] = atan((float)dy / (dx+0.0001f));
        }
    }
    prd();
    return ptr;
}

HOG_descriptor *hog_getDescriptor(const IMAGE_S *img)
{
    int cell_size = HOG_CELL_SIZE;
    int cell_bin_num = HOG_CELL_SIZE;
    int block_cell_num = HOG_BLOCK_CELL_NUM;
    int block_stride_pix = HOG_BLOCK_STRIDE_PIX;

}

HOG_descriptor *hog_getDescriptorRoi(const IMAGE_S *img, const ROI_S *roi);
HOG_descriptor *hog_getDescriptorParam(const IMAGE_S *img, const HOG_PARAM_S *param);

void printFuncU(uint8_t *data, int w, int h)
{
#define pr printf

    pr("data: w:%d h:%d\n", w, h);
    for (int i = -1; i < w; i++) {
        pr("%3d ", i);
    }
    pr("\n");
    for (int i = 0; i < h; i++) {
        for (int j = -1; j < w; j++) {
            if (j == -1) {
                pr("%3d ", i);
            } else {
                pr("%3d ", data[i * w + j]);
            }
        }
        pr("\n");
    }
}

void printFunc(int *data, int w, int h)
{
#define pr printf

    pr("data: w:%d h:%d\n", w, h);
    for (int i = -1; i < w; i++) {
        pr("%3d ", i);
    }
    pr("\n");
    for (int i = 0; i < h; i++) {
        for (int j = -1; j < w; j++) {
            if (j == -1) {
                pr("%3d ", i);
            } else {
                pr("%3d ", data[i * w + j]);
            }
        }
        pr("\n");
    }
}

void printFuncF(float *data, int w, int h)
{

    pr("data: w:%d h:%d\n", w, h);
    for (int i = -1; i < w; i++) {
        pr("%4d ", i);
    }
    pr("\n");
    for (int i = 0; i < h; i++) {
        for (int j = -1; j < w; j++) {
            if (j == -1) {
                pr("%04d ", i);
            } else {
                pr("%02.2f ", data[i * w + j]);
            }
        }
        pr("\n");
    }
}

int main(void)
{
    int w = 16, h = 16;
    uint8_t *image = (uint8_t *)malloc( w * h *sizeof(uint8_t));
    int k = 0;
    for (int i = 0, k = 0; i < h; i++) {
        for (int j = 0; j < w; j++, k++) {
            image[i * w + j] = (k % 256);
        }
    }
    void **ptr =  op_hog(image, w, h);

    float *mag = (float *)ptr[0];
    float *ang = (float *)ptr[1];

    printFuncU(image, w, h);
    printFuncF(mag, w, h);
    printFuncF(ang, w, h);
    free(mag);
    free(ang);
    free(ptr);
    return 0;
}



