"""
GDAL is an important library for GIS programming. Basically you can do very little in GIS without it as many of the key
libraries such as Fiona, Shapely and Pyproj depend on it. GDAL is written in C++ and is known to be tricky to install
and use with Python. Python and C/C++ generally play well together but, in my experience, GDAL is an exception to this.

This is only a problem if you are using MS Windows. Linux and Mac should be fine.

I also recommend that you use Python 3.6 for the moment as I have tested the setup process with this version.

To install GDAL download the file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal. Choose GDAL‑2.3.3‑cp36‑cp36m‑win32.whl.
To install Fiona download the file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona. Choose Fiona‑1.8.4‑cp36‑cp36m‑win32.whl.
To install Shapely download the file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely. Choose Shapely‑1.6.4.post1‑cp36‑cp36m‑win32.whl.
To install Pyproj ddownload the file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj. Choose pyproj‑1.9.6‑cp36‑cp36m‑win32.whl.

For everything else, the standard pip install will be fine.

You should download this file to your project directory and import it as the first import in every GIS program that you
write. This will, hopefully, ensure a relatively painless experience when doing programming for GIS.

REMEMBER: THESE INSTRUCTIONS APPLY TO MS WINDOWS USERS ONLY.

Mark Foley
January 2019
"""

import os
import distutils

if os.name == 'nt':
    from distutils.sysconfig import get_python_lib
    os.environ["PATH"] += os.pathsep + get_python_lib() + "\\osgeo"
