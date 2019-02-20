#include <stdio.h>
#include "bar.h"

void bar(char* chr, Text* text){
	text->name = chr;
	printf("From %s %d %s, char: %s\n", __FILE__, __LINE__, __func__, chr);
}

