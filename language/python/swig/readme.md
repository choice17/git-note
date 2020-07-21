## Swig  

swig is a wrapper library used to link c/c++ to higher level language.

## content  

* **[download](http://www.swig.org/download.html)**  
* **[interface](#interface)**  
* **[compile](#compile)**  

## interface  

```c
/* test.h */
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
```

```c
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
```

```c
/* test.c */
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

```

```python
#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


example_module = Extension('_test',
                           sources=['test_wrap.c', 'test.c'],
                           include_dirs = ['.'],
                           extra_compile_args = ["-O3", "-Wall"]
                           )

setup (name = 'test',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig test from docs""",
       ext_modules = [example_module],
       py_modules = ["test"],
       )
```


##  compile  

```bash
$ python setup.py build_ext --inplace  
```

```python
import test
a = test.create_module()
set(a, 3)
print(access_modules(a)) ==> 3
```
