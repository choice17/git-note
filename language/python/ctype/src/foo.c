#include <stdio.h>

#include "header.h"
#include "foo.h"

int foo(Array *arr,int w, int h)
{
	int sum=0;
	for (int i=0; i<h; ++i) {
		for (int j=0; j<w; ++j) {
			sum += arr->arr[i][j];
		}
	}
	printf("Sum is %d\n", sum);
	return sum;
}

int foo1(int w, int h)
{
	return w + h;
}

void foo2(int w, int h, int *ans)
{
	*ans = w+h;
}

int foo3(int **array, int w, int h)
{
	int sum=0;
	for (int i=0; i<h; ++i) {
		for (int j=0; j<w; ++j) {
			sum += array[i][j];
		}
	}
	printf("Sum is %d\n", sum);
	return sum;
}

void cFunc (int **x, int xLim, int yLim)
{
    int nx, ny;
    for (nx = 0; nx < xLim; nx++)
        for (ny = 0; ny < yLim; ny++)
            x[nx][ny] = nx+ny*100;
}

