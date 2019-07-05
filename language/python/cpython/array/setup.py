#!/usr/bin/python

from setuptools import setup
from distutils.core import Extension
import numpy

setup(name         = 'arr_img',
      version      = '0.1',
      author       = 'Takchoiyu',
      author_email = 'tcyu@umich.edu',
      ext_modules  = [Extension('arr_img',
                                sources = ['_arr_img.c'],
                                include_dirs=[numpy.get_include()])])