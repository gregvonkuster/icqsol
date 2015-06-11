#!/usr/bin/env python

import numpy
import vtk

class Triangulation:

  def __init__(self):
    """
    Constructor
    """
    self.points = vtk.vtkPoints()
    self.polydata = vtk.vtkPolyData()
    self.delny = vtk.vtkDelaunay3D()

    self.polydata.SetPoints(self.points)
    self.delny.SetInputData(self.polydata)

  def setInputVertices(self, verts,):
    """
    Set input vertices
    @param verts vertices
    """
    numPoints = verts.shape[0]
    for i in range(numPoints):
      self.points.InsertPoint(i, verts[i, 0], verts[i, 1], verts[i, 2])

  def triangulate(self):
    """
    Triangulate
    """
    self.delny.Update()

  def getCells(self):
    """
    Get cells
    @return list of vertex indices
    """
    cells = self.delny.GetOutput().GetCells()
    numCells = cells.GetNumberOfCells()

    npts = 4 # number of points per cell
    cellArr = numpy.zeros( (numCells, npts), numpy.int )
    ptIds = vtk.vtkIdList()
    for i in range(numCells):
      cell = cells.GetCell(i, ptIds)
      for j in range(npts):
        cellArr[i, j] = int(ptIds.GetId(j))

    return cellArr

################################################################################

def test():

  numPoints = 8
  points = numpy.array([(0, 0, 0,),
                        (0, 0, 1),
                        (0, 1, 0), 
                        (0, 1, 1),
                        (1, 0, 0),
                        (1, 0, 1),
                        (1, 1, 0),
                        (1, 1, 1)
                        ], numpy.float64)
  tri = Triangulation()
  tri.setInputVertices(points)
  tri.triangulate()
  cells = tri.getCells()
  print 'cells = ', cells

if __name__ == '__main__': test()




