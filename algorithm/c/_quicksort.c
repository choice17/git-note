#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void printArray(int *list, int len)
{
	int i;
	printf("[");
	for (i = 0; i < len; i++) {
		printf("%d,",list[i]);
	}
	printf("]\n");
}

static inline void swap(int *x, int *y)
{
	int tmp = *x;
	*x = *y;
	*y = tmp;
}

int parition(int *list, int front, int end)
{
	int i, j = front-1;
	int pivot = list[end];
	for (i = front; i < end - 1; i++) {
		if (list[i] < list[end]) {
			j++;
			swap(&list[i], &list[j]);
			
		}
	}
	j++;
	swap(&list[end], &list[j]);
	return j;

}

int paritionR(int *list, int front, int end)
{
	int index = (rand() % (end - front)) + front;
	swap(&list[index], &list[end]);
	return parition(list, front, end);
}

void quicksort(int *list, int front, int end)
{
	if (front < end) {
		int pivot = paritionR(list, front, end);
		printf("[pivot:%d(%d)]",pivot,list[pivot]);
		printArray(list, 10);
		quicksort(list, front, pivot - 1);
		quicksort(list, pivot + 1, end);
	}
}

void main(void)
{
#define LEN 10
	srand(time(NULL));
	int list[LEN] = {-2, 3, 232, -343, 2, 10, 3 ,0, 1934, 4566};
	printArray(list, LEN);
	quicksort(list, 0, LEN-1);

	//printArray(list, LEN);
}
