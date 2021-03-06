#!/usr/bin/env python

"""
Apply a surface field to a shape
"""
from __future__ import print_function
import argparse
import time
import sys
import re
from numpy import linspace

from icqsol.shapes.icqShapeManager import ShapeManager
from icqsol import util

# time stamp
tid = re.sub(r'\.', '', str(time.time()))

description = 'Apply a surface field to a shape'
parser = argparse.ArgumentParser(description=description)

parser.add_argument('--input', dest='input', default='',
                    help='Input file (PLY or VTK)')

parser.add_argument('--expression', dest='expression', default='sin(pi*x)*cos(pi*y)*z',
                    help='Expression of x, y, z, and t')

parser.add_argument('--refine', dest='refine', default=0.0, type=float,
                    help='Maximum edge length (use 0 if no refinement)')

parser.add_argument('--name', dest='name', default='myField',
                    help='Set the name of the field')

parser.add_argument('--times', dest='times', default='',
                    help='Comma separated list of time values')

parser.add_argument('--location', dest='location', default='point',
                    help='"point" or "cell"')

parser.add_argument('--ascii', dest='ascii', action='store_true',
                    help='Save data in ASCII format (default is binary)')

parser.add_argument('--output', dest='output',
                    default='addSurfaceFieldFromExpressionToShape-{0}.vtk'.format(tid),
                    help='VTK Output file.')

args = parser.parse_args()

if not args.expression:
    print('ERROR: must specify --expression <expression>')
    sys.exit(2)

if not args.input:
    print('ERROR: must specify input file: --input <file>')
    sys.exit(3)

# make sure the field name contains no spaces
args.name = re.sub('\s', '_', args.name)

# Get the format of the input - either vtk or ply.
file_format = util.getFileFormat(args.input)

if file_format == util.PLY_FORMAT:
    shape_mgr = ShapeManager(file_format=util.PLY_FORMAT)
else:
    # We have a VTK file, so Get the dataset type.
    vtk_dataset_type = util.getVtkDatasetType(args.input)
    shape_mgr = ShapeManager(file_format=util.VTK_FORMAT,
                             vtk_dataset_type=vtk_dataset_type)

pdata = shape_mgr.loadAsVtkPolyData(args.input)
times = [0.0]
if args.times:
    times = eval(args.times)

maxEdgeLength = float('inf')
if args.refine > 0:
    maxEdgeLength = args.refine
pdataOut = shape_mgr.addSurfaceFieldFromExpressionToVtkPolyData(pdata, args.name,
                                                       args.expression, times,
                                                       max_edge_length=maxEdgeLength,
                                                       location=args.location)

if args.output:
    # Always produce VTK POLYDATA.
    shape_mgr.setWriter(file_format=util.VTK_FORMAT,
                        vtk_dataset_type=util.POLYDATA)
    if args.ascii:
        file_type = util.ASCII
    else:
        file_type = util.BINARY
    shape_mgr.saveVtkPolyData(vtk_poly_data=pdataOut,
                              file_name=args.output,
                              file_type=file_type)
