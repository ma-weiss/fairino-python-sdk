# setup.py
# python3 setup.py build_ext --inplace
# python setup.py build_ext --inplace                   (used before Python 3.12)
# python setup.py build_ext --inplace  --compiler=msvc  (for Python 3.12)
# from distutils.core import setup                   #  (used before Python 3.12)
from setuptools import setup
from Cython.Build import cythonize

setup(name="Robot", ext_modules=cythonize("Robot.py"))
