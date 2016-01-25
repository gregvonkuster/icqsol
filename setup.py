#!/usr/bin/env python

"""
Set up script for icqsol
alexander@gokliya.net
"""

import os
from setuptools import setup, Extension
import __init__ # for version number

# Because we're linking C++ code to the VTK library, we 
# need to know where VTK was installed. 
VTK_LIBRARY_DIR = os.environ.get('VTK_LIBRARY_DIR', '')
VTK_INCLUDE_DIR = os.environ.get('VTK_INCLUDE_DIR', '')
OPENMP_COMPILER_ARG = os.environ.get('OPENMP_COMPILER_ARG', '-fopenmp')

setup(name='icqsol',
      version=__init__.__version__, 
      description='Solving engineering problems on the web',
      author='Alex Pletzer and Greg Von Kuster',
      author_email='alexander@gokliya.net',
      url='https://github.com/pletzer/icqsol/wiki',
      install_requires=['pytriangle>=1.0.6', 'pycsg>=0.3.6'],
      dependency_links=['http://github.com/pletzer/pytriangle/tarball/master#egg=pytriangle-1.0.6',
                        'http://github.com/pletzer/pycsg/tarball/master#egg=pycsg-0.3.6',
      ],
      package_dir = {'icqsol': ''}, # the present working directory maps to icqsol below
      data_files = [('icqsol/textures', ['textures/Swietenia_macrophylla_wood.jpg',
                                  'textures/220px-COnglomerate-sandstone_layers_Nerriga.jpg',
                                  'textures/checkerboard.png',])],
      packages=['icqsol',
                'icqsol.color', 
                'icqsol.bem',
                'icqsol.discretization',
                'icqsol.shapes',
                'icqsol.util'],
      ext_modules = [Extension('icqsol.icqLaplaceMatricesCpp', # name of the shared lib
                               ['bem/icqFunctor.cpp',
                                'bem/icqLaplaceFunctor.cpp',
                                'bem/icqQuadrature.cpp',
                                'bem/icqLaplaceMatrices.cpp'],
                               include_dirs=['bem', VTK_INCLUDE_DIR],
                               library_dirs=[VTK_LIBRARY_DIR],
                               extra_compile_args=[OPENMP_COMPILER_ARG],
                               ),
                      Extension('icqsol.icqInsideLocatorCpp', 
                                ['csg/icqInsideLocator.cpp'],
                                include_dirs=['csg', VTK_INCLUDE_DIR],
                                library_dirs=[VTK_LIBRARY_DIR]
                                ),
      ],
      requires = ['numpy', 'vtk',],
     )
