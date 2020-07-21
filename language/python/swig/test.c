#include "test.h"

int fact(int n)
{
 if (n <= 1) return 1;
 else return n*fact(n-1);
}

int my_mod(int x, int y)
{
 return (x%y);
}

int access_modules(module_handle mod)
{
	return ((module*)mod)->a;
}

void set(module_handle mod, int a)
{
	((module*)mod)->a = a;	
}

void free_module(module_handle mod)
{
	free((module*)mod);
}

char *get_time(void)
{
 time_t ltime;
 time(&ltime);
 return ctime(&ltime);
}

module_handle create_module()
{
	module_handle handler = (long long)malloc(sizeof(module));
	return handler;
}

int main(void)
{
	return 0;
}
