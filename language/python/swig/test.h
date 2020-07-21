#include <time.h>
#include <stdlib.h>

typedef struct {
	int a;
	int b;
	int c;
} module;

typedef long long module_handle;

module_handle create_module();
void free_module(module_handle mod);
int fact(int n);
void set(module_handle mod, int a);
int my_mod(int x, int y);
int access_modules(module_handle mod);
char *get_time(void);

