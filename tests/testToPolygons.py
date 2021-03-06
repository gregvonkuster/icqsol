from __future__ import print_function
from icqsol.shapes.icqShapeManager import ShapeManager
from csg.core import CSG
from icqsol import util

"""
Test conversion from a shape to a list of polygons
@author alexander@gokliya.net
"""
shape_mgr = ShapeManager(file_format=util.VTK_FORMAT, vtk_dataset_type=util.POLYDATA)
shp = shape_mgr.createShape('box', origin=[0., 0., 0.], lengths=[1., 1., 1.],)

# check whether one can convert to a list of polygons
polys = shape_mgr.shapeToPolygons(shp)

# check whether each polygon can be cloned
map(lambda p: p.clone(), polys)

# check that we can load the polygons
a = CSG.fromPolygons(polys)

shp2 = shape_mgr.createShape('sphere', radius=1.0, origin=(0., 0., 0.), n_theta=5, n_phi=2)
polys2 = shape_mgr.shapeToPolygons(shp2)
a2 = CSG.fromPolygons(polys2)
