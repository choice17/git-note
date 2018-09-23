#include "bar.h"
#include "foo.h"
#include <stdio.h>

void bar(char *x){
	foo();
	printf("%s %s\n","hello from bar",x);


}
