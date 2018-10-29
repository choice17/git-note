# Python C extension  

## reference  
`https://gist.github.com/douglas-larocca/099bf7460d853abb7c17`  
`https://dfm.io/posts/python-c-extensions/`

## code directories  

* module -> chi2  

```
proj/
    |-chi2.h # library header
    |-chi2.c # library function
    |-_chi2.c # wrapper function
```

## Wrapper

* include  
```
#include <Python.h>
#include <numpy/arrayobject.h>
#include "chi2.h"
```

* define wrapper function  
** docstring  
```
static char chi2_docstring[] =
    "Calculate the chi-squared of some data given a model.";
```
** define wrapper function  
```
static PyObject *chi2_chi2(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"chi2", chi2_chi2, METH_VARARGS, chi2_docstring},
    {NULL, NULL, 0, NULL}
};
```

* define module  
```
PyMODINIT_FUNC PyInit__chi2(void)
{
    
    PyObject *module;
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_chi2",
        module_docstring,
        -1,
        module_methods,
        NULL,
        NULL,
        NULL,
        NULL
    };
    module = PyModule_Create(&moduledef);
    if (!module) return NULL;

    /* Load `numpy` functionality. */
    import_array();

    return module;
}
```

* define wrapper func content  
```
static PyObject *chi2_chi2(PyObject *self, PyObject *args){
	
}
```

## python objects  

* PyObject  
all python struct are from PyObject  

* PyArg_ParseTuple
function to parse args tuple  

* PyArray_FROM_OTF(numpy)  
numpy array ptr from object  

* Py_XDECREF  
throw python exception if error happens  

* PyArray_DIM(numpy)  
get numpy array dim  

* PyArray_DATA(numpy)  
transfer python numpy ptr to c typical ptr  

* Py_DECREF  
1. python memory management is to count how many reference in the global interpreter  
2. declare a pyObject do actually inc a reference count in sys  
3. Py_DECREF is needed to ack sys to remove pyobj in sys  or else there will be mem leak

## compile  
```
# setup.py
from distutils.core import setup, Extension
import numpy.distutils.misc_util

setup(
	ext_modules=[Extension("_chi2", ["_chi2.c", "chi2.c"])],
	include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)
```

`$python setup.py build_ext --inplace` to compile 
```
in window, it will output {}.pyd
in linux, it will output {}.so
```