#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

pthread_t tid;

typedef struct image {
    void *data;
    int w;
    int h;
    int c;
    int size;
} image;

typedef struct box {
    int sx;
    int sy;
    int ex;
    int ey;
} box;

typedef struct color {
    int r;
    int g;
    int b;
} color;

typedef struct _color {
    union {
        struct {
        uint8_t r;
        uint8_t g;
        uint8_t b;
        };
        uint8_t v[3];
    };
} _color;

void printstr(char *str)
{
    printf("%s %d: %s\n", __func__,__LINE__,str);
}

void fill(image *img, color *cr)
{
    uint8_t *data = (uint8_t*)img->data;
    _color _cr;
    _cr.r = cr->r; _cr.g = cr->g; _cr.b = cr->b;

    printf("%s %d: w:%d, h:%d, c:%d\n", __func__,__LINE__,
        img->w, img->h, img->c);
    
    int addr = 0;
    int jaddr = 0;
    for (int i = 0; i <img->h; ++i) {
        addr = i * img->w * img->c;
        for (int j = 0; j <img->w; ++j) {
            jaddr = addr + j * img->c;
            for (int k = 0; k < img->c; ++k) {
                data[jaddr+k] = _cr.v[k];
            }
        }
    } 
}
int playing = 1;

void *runt(void *args)
{
    srand( time(NULL));
    image *img = (image*)args;
    int run_cnt = 0;
    pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
    while (1)
    {
        sleep(1);
        pthread_testcancel();
        printf("running...%3d...\n", run_cnt++);
        color cr = {rand()%255,rand()%255,rand()%255};
        fill(img, &cr);
        pthread_testcancel();
    }
    return NULL;
}

void run(image *img)
{
    if (pthread_create(&tid, NULL, runt, (void*)img) != 0) {
        printf("Cannot create thread!\n");
        return;
    }
}

void cclose(void)
{
    printf("entering closing!\n");
    playing = 0;
    void *res;
    printf("trying to cancel!\n");
    if (pthread_cancel(tid) != 0) {
        printf("Cancel thread fails\n");
        return;
    }
    printf("trying to join!\n");
    if (pthread_join(tid, &res) != 0) {
        printf("Join thread fails\n");
        return;
    }
    printf("close all thread!\n");
}

