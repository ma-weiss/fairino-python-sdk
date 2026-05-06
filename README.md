# fairino-python-sdk 

Introduction
---------------
This is a Python language SDK library specially designed for fairino collaborative robots.

Documentation
----------------
Please see [Python SDK](https://fair-documentation.readthedocs.io/en/latest/SDKManual/python_intro.html)。



Building from source on Python >= 3.12 (Linux)
-------------------------------------------

The repository ships precompiled extensions for Python 3.10 and 3.11 in
`linux/libfairino/` (`Robot.cpython-310-x86_64-linux-gnu.so` and
`Robot.cpython-311-x86_64-linux-gnu.so`). There is no prebuilt binary for
Python 3.12, so you have to Cython-compile `linux/fairino/Robot.py` yourself.

### 1. Patch `setup.py` for Python 3.12

`distutils` was removed from the standard library in Python 3.12 (PEP 632),
so switch `linux/fairino/setup.py` to use `setuptools`:

```python
# from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize

setup(name='Robot', ext_modules=cythonize('Robot.py'))
```

### 2. Install build dependencies

On Debian/Ubuntu:

```bash
sudo apt install python3.12-dev build-essential
```

Then, inside a Python 3.12 virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install "Cython>=3.0"
```

Cython 3.0+ is required; older 0.29.x releases do not support the Python
3.12 C-API.

### 3. Build the extension in place

```bash
cd linux/fairino
python setup.py build_ext --inplace
```

This regenerates `Robot.c` and produces
`Robot.cpython-312-x86_64-linux-gnu.so` next to `Robot.py` (and a copy under
`build/lib.linux-x86_64-cpython-312/`).

If you previously built against an older Cython, delete the stale
`Robot.c` first so it gets re-emitted:

```bash
rm -f Robot.c
python setup.py build_ext --inplace
```

### 4. Install the new binary alongside the shipped ones

To match the layout of the 3.10 / 3.11 binaries, copy the new `.so` into
`linux/libfairino/`:

```bash
cp Robot.cpython-312-x86_64-linux-gnu.so ../libfairino/
```

### 5. Verify

```bash
cd ../example
PYTHONPATH=../libfairino python -c "import Robot; print(Robot.__file__)"
```

This should print the path to the `cpython-312` `.so` you just built.

### Troubleshooting

- `ModuleNotFoundError: No module named 'distutils'` — you forgot to
  switch `setup.py` to `setuptools` (step 1).
- `fatal error: Python.h: No such file or directory` — install the
  Python 3.12 development headers (`python3.12-dev` on Debian/Ubuntu,
  `python3-devel` on Fedora/RHEL).
- C compile errors referencing `_PyGen_Send`, `_PyEval_EvalFrameDefault`,
  or similar — your Cython is too old. Upgrade to Cython ≥ 3.0, delete
  `Robot.c`, and rebuild.
- The `--compiler=msvc` flag mentioned in `setup.py` only applies to
  Windows; leave it off on Linux so setuptools picks GCC.

  
