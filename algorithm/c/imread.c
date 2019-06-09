#include <string.h>
#include <stdlib.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

void load_image_stb(char *filename, int channels)
{
    int w, h, c;
    unsigned char *data = stbi_load(filename, &w, &h, &c, channels);
    if (!data) {
        fprintf(stderr, "Cannot load image \"%s\"\nSTB Reason: %s\n", filename, stbi_failure_reason());
        exit(0);
    }
    if(channels) c = channels;
    int i,j,k;

    //for(k = 0; k < c; ++k){
    k = 0;
        for(j = 0; j < h; ++j){
            for(i = 0; i < w; ++i){
                //int dst_index = i + w*j + w*h*k;
                int src_index = k + c*i + c*w*j;
                printf("%3d,",data[src_index]);
                //im.data[dst_index] = (float)data[src_index]/255.;
            }
            printf("\n");
        }
    //}

    free(data);
    printf("w:%d h:%d c:%d [0,0]: %d\n",w,h,c,data[0]);
}

int main(void)
{
    char *filename = "../../files/blob.jpg";
    load_image_stb(filename, 3);
}