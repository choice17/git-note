 /* test.i */
 %module test
 %{
 #define SWIG_FILE_WITH_INIT
 #include "test.h"
 %}
 
 #include "test.h"
typedef struct {
	int a;
	int b;
	int c;
} module;

typedef long long module_handle;

module_handle create_module();
void set(module_handle mod, int a);
void free_module(module_handle mod);
int fact(int n);
int my_mod(int x, int y);
int access_modules(module_handle mod);
char *get_time(void);