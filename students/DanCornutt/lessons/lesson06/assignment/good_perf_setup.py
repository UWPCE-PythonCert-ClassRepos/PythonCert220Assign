"""
Cython setup file for Python

"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='good perf',
    ext_modules=cythonize("good_perf.py")
)
