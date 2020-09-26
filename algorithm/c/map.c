#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

#define MAX_ID (INT_MAX)
#define MAX_NUM (10)
#define MAX_MAP_NUM (32)

#define mod2(x,N) (((x) - (N-1)) & N)

typedef struct {
    int coord[4];
    int id;
} RECT;


typedef struct {
    RECT obj[MAX_NUM];
    int num;
} RECT_LIST;

typedef struct {
    int obj_id[MAX_NUM];
    int arr_id[MAX_NUM];
    int num;
} TABLE;

int cnt = 0;

int comp1(const void *elem1, const void *elem2)
{
    int *a = (*(int **)elem1);
    int *b = (*(int **)elem2);
    //printf("cnt:%d %p:%d vs %p:%d\n", cnt++, a, *a, b, *b);
    return *a > *b;
}

void printArr(int *v, int *vptr[], int n)
{
    for (int i = 0; i < n; i++) {
        printf("%d(%d) ", v[i], *vptr[i]);
    }
    printf("\n");
}

void ut_case_test()
{
    int num = 5;
    int val[5] = {0,2,72,3,5};
    int *valptr[5];
    for (int i = 0; i < num; i++) {
        valptr[i] = &val[i];
    }
    printArr(val, valptr, num);
    qsort(valptr, 5, sizeof(int*),comp1);
    printArr(val, valptr, num);
    return;
}

int comp(const void *elem1, const void *elem2)
{
    //printf("cnt :%d %d vs %d \n", cnt++,
    //   (*(RECT**)elem1)->id, (*(RECT **)elem2)->id);
        
    return (*((RECT **)elem1))->id > (*((RECT **)elem2))->id;
}

void map_table(const RECT_LIST *src, const TABLE *prev, TABLE *dst)
{
    // 1. sort
    const int src_num = src->num;
    int last_max_id = prev->arr_id[prev->num-1];
    RECT const *objs[MAX_NUM];
    for (int i = 0; i < src_num; i++) {
        objs[i] = &src->obj[i];
    }
    qsort(objs, src_num, sizeof(RECT*), comp);

    // debug
    for (int i = 0; i < src_num; i++) {
        printf("%d-%d ", i, objs[i]->id);
    } printf("\n");

    uint8_t set[MAX_MAP_NUM] = { 0 };
    //memset(set, 0, MAX_MAP_NUM);

    // 2. count
    const int prev_num = prev->num;
    int obj_id[MAX_NUM];
    uint8_t obj_val[MAX_NUM];
    for (int i=0, j=0; i<src_num; i++){
        obj_id[i] = objs[i]->id;
        if (obj_id[i] == prev->obj_id[j]) {
            dst->obj_id[i] = prev->obj_id[j];
            dst->arr_id[i] = prev->arr_id[j];
            set[dst->arr_id[i]] = 1;
            //obj_val[i] = 3;
            j++;
        } else if (obj_id[i] != prev->obj_id[j]) {
            //obj_val[i] = 2;
            dst->obj_id[i] = objs[i]->id;
            while (set[last_max_id]) {
                last_max_id++;
                last_max_id %= MAX_MAP_NUM;
                //printf("%d %d %d\n",last_max_id, set[last_max_id]);
            //sleep(1);
            }
            dst->arr_id[i] = last_max_id;
            set[last_max_id] = 1;
        }
    }
    for (int i = 0; i < src_num; i++) {
        printf("%d-%d-%d ", i, dst->obj_id[i], dst->arr_id[i]);
    } printf("\n");
}

void getCase0List0(RECT_LIST *list, TABLE *prev, TABLE *gt)
{
    list->num = 5;
    list->obj[0].id = 0;
    list->obj[1].id = 1;
    list->obj[2].id = 7;
    list->obj[3].id = 4;
    list->obj[4].id = 5;

    prev->num = 3;
    prev->obj_id[0] = 0;
    prev->obj_id[1] = 1;
    prev->obj_id[2] = 4;

    prev->arr_id[0] = 0;
    prev->arr_id[1] = 1;
    prev->arr_id[2] = 4;


    gt->num = 5;
    gt->obj_id[0] = 0;
    gt->obj_id[1] = 1;
    gt->obj_id[2] = 4;
    gt->obj_id[3] = 5;
    gt->obj_id[4] = 7;

    gt->arr_id[0] = 0;
    gt->arr_id[1] = 1;
    gt->arr_id[2] = 4;
    gt->arr_id[3] = 5;
    gt->arr_id[4] = 6;
}

void setPrevList0(TABLE *prev)
{

}


void ut_case_0()
{
    RECT_LIST list = { 0 };
    TABLE prev = { 0 };
    TABLE dst = { 0 };
    TABLE gt = { 0 };
    getCase0List0(&list, &prev, &gt);
    for (int i = 0; i < list.num; i++) {
        printf("%d ", list.obj[i].id);
    } printf("\n");
    for (int i = 0; i < prev.num; i++) {
        printf("%d-%d ", prev.obj_id[i],prev.arr_id[i]);
    } printf("\n");

    map_table(&list, &prev, &dst);

    for (int i = 0; i < list.num; i++) {
        printf("%d-%d-%d ", i, dst.obj_id[i], dst.arr_id[i]);
    } printf("\n");

}

int main()
{
    ut_case_test();
    ut_case_0();
    return 0;
}