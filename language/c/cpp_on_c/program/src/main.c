#include "_opencv.h"
#include "foo.h"
#include <stdio.h>


int main(void)
{
    CASCADE *cas = new_cas();
    MAT *mat = new_mat();

    int a = cas_add(cas, 3, 4);
    int b = mat_sum(mat, 5, 6);
    printf("%d, %d from main!\n", a, b);
}