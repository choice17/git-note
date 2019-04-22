#include <stdio.h>


void bubblesort(int *list, int len)
{
	int i, j, tmp;
	for (i = 0; i < len-1; i++) {
		for (j = 0; j < len-1; j++) {
			if (list[j] >= list[j+1]) {
				tmp = list[j+1];
				list[j+1] = list[j];
				list[j] = tmp;
			}
		}
	}
}



void main(void)
{
#define LEN 10

	int list[LEN] = {12, 23, 1234, 55, 34, 0, 231, 5467, 123, 435};
	int i;
	printf("list:[");
	for (i = 0; i < LEN; i++){
		printf("%d,",list[i]);
	}
	printf("]\n");
	bubblesort(&list[0], LEN);
	printf("list:[");
	for (i = 0; i < LEN; i++){
		printf("%d,",list[i]);
	}
	printf("]\n");


}