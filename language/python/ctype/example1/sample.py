"""
Demo code for accessing pointer array
https://stackoverflow.com/questions/22425921/pass-a-2d-numpy-array-to-c-using-ctypes/27737099
https://stackoverflow.com/questions/11384015/python-ctypes-multi-dimensional-array

Tutorials 1. 
function int foo(int, char)

Tutorials 2. 
function uint bar(Test test)

Tutorials 3.
function uint hor(Test *test, int[30])

Tutorials 4.
function void alp(int **arr,int w, int h)

"""

from ctypes import *
from numpy.ctypeslib import ndpointer 
import numpy as np 


_intpp = ndpointer(dtype=np.intp, ndim=1, flags='C') 

lib = CDLL("lib/sample.so", RTLD_GLOBAL)

class TEXT(Structure):
    _fields_ = [("name", c_char_p),
                ("cnt", c_int)]

class ARRAY(Structure):
	_fields_ = [("arr", _intpp)]

foo = lib.foo
foo.argtypes = [ndpointer(dtype=np.uintp, ndim=1)] +  [c_uint]*2
foo.restypes = c_int

foo1 = lib.foo1
foo1.argtypes = [c_int, c_int]
foo1.restypes = c_int

foo2 = lib.foo2
foo2.argtypes = [c_int, c_int, POINTER(c_int)]

foo3 = lib.foo3
foo3.argtypes = [_intpp , c_int, c_int]
foo3.restypes = c_int

cFunc = lib.cFunc
cFunc.argtypes = [ndpointer(dtype=np.uintp, ndim=1)] +  [c_uint]*2
cFunc.restypes = None

bar = lib.bar
bar.argtypes = [c_char_p, POINTER(TEXT)]

toDblPtr = lambda x: x.ctypes.data + x.strides[0]*np.arange(x.shape[0], dtype=np.uintp)

if __name__ == "__main__":
	w, h = 2,2
	x = np.arange(4).reshape((2, 2)) 

	"""
	ctype function int input and return int
	"""
	c = foo1(1,2)
	print("foo1 ans: c",c)

	"""
	ctype function byref int and return ref int
	"""
	d = c_int(c)
	foo2(3,2,byref(d))
	print("foo2 ans: &d",d.value)

	"""
	ctype func input poitner int
	"""
	d = pointer(c_int(c))
	foo2(4,6,d)
	print("foo2 ans: *d",d.contents.value)

	""" 
	ctype func input struct pointer
	"""
	text = TEXT(b"hi", 3)
	bar(b"img",byref(text))
	print("bar ans: &text.name", text.name)

	"""
	ctype func input array double pointer
	"""
	matrix = np.zeros([5, 7], np.int32, order='C')
	#h, w = 3, 4
	#img = np.random.randint(2,255,(w, h),dtype=np.int64)
	[xSz, ySz] = matrix.shape
	cFunc(toDblPtr(matrix), xSz, ySz)
	print(matrix)
	print("hello world")