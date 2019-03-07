from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

#ext_modules=[ Extension("cresize",
#              ["cresize.pyx"],
#              extra_compile_args = ["-O3"])]

setup(
  name = "cresize",
  cmdclass = {"build_ext": build_ext},
  ext_modules = cythonize('cresize.pyx'))
"""
* compile
$ python setup.py build_ext --inplace

* check for cdef
$ cython cresize.pyx -a
"""