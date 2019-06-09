#include <stdio.h>
#include <stdint.h>

#define W 22
#define H 15

#define PICW 1920
#define PICH 1080

#define REGION_NUM_MAX 64

#define SYS_TRACE(fmt, ...) printf("[%s:%d] " fmt, __func__, __LINE__, ####__VA_ARGS__)

#define DEBUG

typedef struct {
    uint16_t sx;
    uint16_t sy;
    uint16_t ex;
    uint16_t ey;
} REGION_S;

typedef struct {
    int num;
    REGION_S rgn[REGION_NUM_MAX];
} REGION_LIST_S;

typedef struct {
    int grid_w;
    int grid_h;
    int res_w;
    int res_h;
} INFO_S;

uint8_t g_grid[W * H] = {
     0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 
     0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
     1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
 };

/**
 *@brief connected component into square blob using two pass
 */
int blobToBox(const uint8_t *grid, REGION_LIST_S *olist, const INFO_S *info)
{
#define EXPAND_RES

    int i, j;
    int16_t idx[REGION_NUM_MAX] = { 0 };
    REGION_LIST_S list = { 0 };
    list.num = -1;
    /* first pass by row */
    for (i = 0; i < info->grid_h; i++) {
        for (j = 0; j < info->grid_w; j++) {
            // connected by row
            if (j == 0) {
                if (grid[i * info->grid_w + j]) {
                    list.num++;
                    idx[list.num] = list.num;
                    list.rgn[list.num].sx = j;
                    list.rgn[list.num].sy = i;
                    list.rgn[list.num].ex = j;
                    list.rgn[list.num].ey = i;
                }
            } else {
                if (grid[i * info->grid_w + j - 1] && grid[i * info->grid_w + j]) {
                    list.rgn[list.num].ex = j;
                    //list.rgn[list.num].ey = i;
                } else if ((!grid[i * info->grid_w + j - 1]) && (grid[i * info->grid_w + j])) {
                    list.num++;
                    idx[list.num] = list.num;
                    list.rgn[list.num].sx = j;
                    list.rgn[list.num].sy = i;
                    list.rgn[list.num].ex = j;
                    list.rgn[list.num].ey = i;
                }
            } 
        }
    }
    list.num++;
    /* second pass on column */
    for (i = 0; i < list.num; i++) {
        if (idx[i] == -1)
            continue;
        for (j = i + 1; j < list.num; j++) {
            if (list.rgn[i].ey == list.rgn[j].sy - 1) {
                if ((list.rgn[i].sx == list.rgn[j].sx) &&
                    (list.rgn[i].ex == list.rgn[j].ex)) {
                    list.rgn[i].ey += 1;
                    idx[j] = -1;
                }
            } else if (list.rgn[j].sy > list.rgn[j].ey + 1) {
                break;
            }
        }
#ifdef EXPAND_RES
        olist->rgn[olist->num].sx = list.rgn[i].sx * info->res_w / info->grid_w;
        olist->rgn[olist->num].sy = list.rgn[i].sy * info->res_h / info->grid_h;
        olist->rgn[olist->num].ex = (list.rgn[i].ex + 1)* info->res_w / info->grid_w;
        olist->rgn[olist->num].ey = (list.rgn[i].ey + 1)* info->res_h / info->grid_h;
        olist->num++;
#else
        olist->rgn[olist->num++] = list.rgn[i]; 
#endif /* EXPAND_RES */
    }


#ifdef DEBUG
    SYS_TRACE("List num: %d\n", list.num);
    for (i = 0; i < list.num; i++) {
        SYS_TRACE("rgn %d idx:%d s(%d,%d) e(%d,%d)\n", i, idx[i], list.rgn[i].sy, list.rgn[i].sx, list.rgn[i].ey, list.rgn[i].ex);
    }
    SYS_TRACE("oList num: %d\n", olist->num);
    for (i = 0; i < olist->num; i++) {
        SYS_TRACE("rgn %d s(%d,%d) e(%d,%d)\n", i, olist->rgn[i].sy, olist->rgn[i].sx, olist->rgn[i].ey, olist->rgn[i].ex);
    }
#endif /* DEBUG */
}

/**
 *@brief connected component into grid cell from region list
 */
int blobToGrid(const REGION_LIST_S *list, uint8_t *grid, const INFO_S *info)
{
    int i, j, k;
    REGION_S rect;
    for (i = 0; i < list->num; i++) {
        //nbjbj
        rect.sx = (list->rgn[i].sx * info->grid_w + (info->res_w >> 1 )) / info->res_w;
        rect.sy = (list->rgn[i].sy * info->grid_h + (info->res_h >> 1 ))/ info->res_h;
        rect.ex = (list->rgn[i].ex * info->grid_w + (info->res_w >> 1 ))/ info->res_w;
        rect.ey = (list->rgn[i].ey * info->grid_h + (info->res_h >> 1 ))/ info->res_h;
        for (j = rect.sy; j < rect.ey; j++) {
            for (k = rect.sx; k < rect.ex; k++) {
                grid[j * info->grid_w + k] = 1;
            }
        }
    }

#ifdef DEBUG
    printf("[\n");
    for (j = 0; j < info->grid_h; j++) {
        for (k = 0; k < info->grid_w; k++) {
            printf("%d,", grid[j * info->grid_w + k]);
        }
        printf("\n");
    }
    printf("]\n");
#endif /* DEBUG */
}


void main(void)
{
    REGION_LIST_S list = { 0 };
    list.num = 0;
    INFO_S info = {.grid_w=W, .grid_h=H, .res_w=PICW, .res_h=PICH};

    blobToBox(g_grid, &list, &info);

    uint8_t grid[W * H] = { 0 };
    blobToGrid(&list, grid, &info);
}
