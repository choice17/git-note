extern "C"{
#include "bar.h"
}

int main(){
	char *x;
	x = "hi";
	bar(x);
	return 0;
}
