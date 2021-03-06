#!/usr/bin/env python

"""
Test subtraction operation on cylinders
@author alexander@gokliya.net
"""

from __future__ import print_function
from icqsol.shapes.icqShapeManager import ShapeManager
from icqsol import util

shape_mgr = ShapeManager(file_format=util.VTK_FORMAT, vtk_dataset_type=util.POLYDATA)
s1 = shape_mgr.createShape('cylinder', radius=1.0, origin=(0., 0., 0.5), length=0.5)

# need to make the cylinder to subtract a little longer to avoid
# floating point issues
s2 = shape_mgr.createShape('cylinder', radius=0.5, origin=(0., 0., 0.), length=1.1)
geom = s1 - s2
shape_mgr.showShape(geom, filename='testSubtractionCylinders.png')
