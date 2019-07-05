#define NPY_NO_DEPRECATED_API NPY_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>
#include <immintrin.h>

//#include "arr_img.h"

/*
https://www.cs.uaf.edu/2009/fall/cs301/lecture/11_13_sse_intrinsics.html
*/

static char module_docstring[] =
    "This module provides an interface for calculating array summation.";
static char arr_img_docstring[] =
    "Calculate the array sum of some data given a model.";

// {module_name}_{function_name}
static PyObject *arr_img(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"arr_img", arr_img, METH_VARARGS, arr_img_docstring},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC PyInit_arr_img(void)
{
    /*static PyMethodDef methods[] =
        { {'arr_img', (PyCFunction)arr_img, METH_VARARGS | METH_KEYWORDS, arr_img_docstring},
         {}
        };*/

    /*static PyMethodDef methods[] =
        { {'arr_img', (PyCFunction)arr_img, METH_VARARGS, arr_img_docstring},
         {}
        };*/


    //PyImport_AddModule("arr_img");
    //Py_InitModule3("arr_img", methods,
    //               "Demo module to show binding numpy to C");
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "arr_img",
        module_docstring,
        -1,
        module_methods,
        NULL,
        NULL,
        NULL,
        NULL
    };
    PyObject *module;
    module = PyModule_Create(&moduledef);
    if (!module) return NULL;

    // Required to avoid mysterious segfaults
    import_array();

    return module;
}

static PyObject  *arr_img(PyObject *NPY_UNUSED(self), PyObject *args)
{
    int w, h;
    int i, j;

    PyArrayObject *arr;
    //PyObject* result = NULL;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "Odd", &arr, &w, &h))
        return NULL;

    if (arr == NULL) {
        Py_DECREF(arr);
        return NULL;
    }

    int        ndim     = PyArray_NDIM(arr);
    npy_intp*  dims     = PyArray_DIMS(arr);
    int        typenum  = PyArray_TYPE(arr);

    // assertion here //
    if( typenum != NPY_FLOAT )
    {
        PyArrayObject* arr2 =
            (PyArrayObject*)PyArray_FromArray(arr, PyArray_DescrFromType(NPY_FLOAT),
                                              NPY_ARRAY_ALIGNED);
        Py_DECREF(arr);
        arr = arr2;
    }

        // Useful metadata about this matrix
    /*__attribute__((unused))*/ char*      data0    = PyArray_DATA    (arr);
    /*__attribute__((unused))*/ char*      data1    = PyArray_BYTES   (arr);
    /*__attribute__((unused))*/ npy_intp  *strides  = PyArray_STRIDES (arr);
    /*__attribute__((unused))*/ //int        ndim     = PyArray_NDIM    (arr);
    /*__attribute__((unused))*/ //npy_intp*  dims     = PyArray_DIMS    (arr);
    /*__attribute__((unused))*/ npy_intp   itemsize = PyArray_ITEMSIZE(arr);
    /*__attribute__((unused))*/ //int        typenum  = PyArray_TYPE    (arr);
    /*for (i = 0; i < n; i += 4)
    {
        __m128i v = _mm_load_si128(&a[i]);  // load vector of 4 x 32 bit values
        vsum = _mm_add_epi3
    */
    float *sum;
    __m128 v;
    __m128 b;
    for (i = 0; i<dims[0]; i++) {
        for (j = 0; j<dims[1]; j+=4) {
            sum = (float*)&data0[i*strides[0] + j*strides[1]];
            v = _mm_load_ps(sum);
            b = _mm_load_ps(sum);
            v = _mm_mul_ps(v, b);
            _mm_store_ps(sum, v);
            //data0[i*strides[0] + j*strides[1]]
        }
    }
    /*
    float *sum;
    printf("\n");
    for (i = 0; i<dims[0]; i++) {
        for (j = 0; j<dims[1]; j++) {
            sum = (float*)&data0[i*strides[0] + j*strides[1]];
            printf("[%f]",*sum);
            *sum *= 2;
            //data0[i*strides[0] + j*strides[1]]
        }
    }
    printf("\n");*/

    //result = Py_BuildValue( "d", sum );
    //result = PyArray_Return(arr);
    //Py_DECREF(arr);
    return PyArray_Return(arr);
}


/*
#!/usr/bin/python2
''' import from lib

import numpy as np
import numpysane as nps
import sys

sys.path[:0] = ('/tmp/build/lib.linux-x86_64-2.7',)
import tst

x0 = np.arange(12).reshape(3,4)
x1 = nps.mv(x0, 0,1) # same matrix, with the axis order reversed

print tst.foo(x0, i=1, j=0)
print tst.foo(x1, i=0, j=1)
*/
