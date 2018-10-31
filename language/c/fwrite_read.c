#include <stdio.h>
#include <errno.h>
#include "func.h"

extern int data;

typedef struct People{
	int age;
	int weight;
	char name[50];
	int chunk[100];
}People;

char fname[50] = "dump.dat";

int main(void)
{
	People ppl_dummy;
	People ppl = {.age = 12, .weight=50, .name="choi", .chunk = {0}, };
	printf("ppl age %d weight %d name %s chunk %d\n", ppl.age, 
		ppl.weight, ppl.name, ppl.chunk[0]);
	
	FILE* fw = fopen(fname, "wb");
	fwrite(&ppl, sizeof(People), 1, fw);
	fclose(fw);

	FILE* fr = fopen(fname, "rb");
	fread(&ppl_dummy, sizeof(People), 1, fr);
	printf("ppl_dummy age %d weight %d name %s chunk %d\n", ppl_dummy.age, 
		ppl_dummy.weight, ppl_dummy.name, ppl_dummy.chunk[0]);
	fclose(fr);
	int ret;
	ret = remove(fname);
	if (ret)
		perror("Following error occured");
	ret = remove(fname);
	if (ret)
		perror("Following error occured");
		//fprintf(stderr, "Error: %s", strerror(errno), 30); 
	printf("data : %d\n", data);
	func();
	printf("data : %d\n", data);
	func();
	printf("data : %d\n", data);
	
}