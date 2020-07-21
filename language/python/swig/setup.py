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