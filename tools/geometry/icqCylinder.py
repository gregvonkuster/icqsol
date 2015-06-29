#!/usr/bin/env python

import vtk
import numpy

from icqShape import Shape
from icqUniformGrid import uniformGrid2D, uniformIndexGrid2D

class Cylinder(Shape):

  def __init__(self, radius, origin, length,
               n_rho=10, n_theta=32, n_z=2):
    """
    Constructor
    @param radius radius
    @param origin center of low end disk
    @param length length of the cylinder in the z direction
    @param n_rho number of radial cells
    @param n_theta number of theta cells
    @param n_z number of z cells
    """

    Shape.__init__(self)
    
    # data structure holding array of points
    self.pointArray = vtk.vtkDoubleArray()
    self.pointArray.SetNumberOfComponents(3)
    
    # data structire holding points
    self.points = vtk.vtkPoints()
    self.points.SetData(self.pointArray)
    
    # data structure holding cell indices
    self.cellInds = vtk.vtkIdTypeArray()
    
    # data structure holding cell connectivity data
    self.cells = vtk.vtkCellArray()
    
    # list of numpy arrays, one element for each surface mesh
    pointList = []
    connectivityList = []
    
    # create outer, side mesh
    pointsOuter, connectivityOuter = self._createSideMesh(origin, radius, length,
                                                          n_theta=n_theta,
                                                          n_z=n_z)
    pointList.append(pointsOuter)
    connectivityList.append(connectivityOuter)
    
    
    # create low end side mesh
    pointsLo, connectivityLo = self._createLoMesh(origin, radius, length,
                                                  n_rho=n_rho,
                                                  n_theta=n_theta)
    pointList.append(pointsLo)
    connectivityList.append(connectivityLo)

    # create high end side mesh
    pointsHi, connectivityHi = self._createHiMesh(origin, radius, length,
                                                  n_rho=n_rho,
                                                  n_theta=n_theta)
    pointList.append(pointsHi)
    connectivityList.append(connectivityHi)
    
    # concatenate all the meshes
    totNumPoints = 0
    totNumCells = 0
    numMeshes = len(pointList)
    for i in range(numMeshes):
      cl = connectivityList[i]
      # increment the connectivity
      cl[:, 1:] += totNumPoints
      numPoints = pointList[i].shape[0]
      numCells = cl.shape[0]
      totNumPoints += numPoints
      totNumCells += numCells
    
    self.allPoints = numpy.zeros( (totNumPoints, 3), numpy.float64 )
    self.allConnectivity = numpy.zeros( (totNumCells, 4), numpy.int )
    
    totNumPoints = 0
    totNumCells = 0
    for i in range(numMeshes):
      pl = pointList[i]
      cl = connectivityList[i]
      numPoints = pl.shape[0]
      numCells = cl.shape[0]
      self.allPoints[totNumPoints: totNumPoints + numPoints, :] = pl
      self.allConnectivity[totNumCells: totNumCells + numCells, :] = cl
      totNumPoints += numPoints
      totNumCells += numCells

    # set the points and connectivity array
    self.pointArray.SetNumberOfTuples(totNumPoints)
    self.pointArray.SetVoidArray(self.allPoints, totNumPoints*3, 1)
    
    self.cellInds.SetNumberOfTuples(totNumCells)
    self.cellInds.SetVoidArray(self.allConnectivity, totNumCells*4, 1)
    
    self.cells.SetCells(totNumCells, self.cellInds)

    self.surfPolyData.SetPoints(self.points)
    self.surfPolyData.SetPolys(self.cells)

  def _createSideMesh(self, origin, radius, length, n_theta, n_z):
    """
    Create side mesh
    @param origin origin of the disk on the lower end
    @param radius radius
    @param length cylinder length
    @param n_theta number of poloidal cells
    @param n_z number of z cells
    @return points, connectivity
    """
    # u ~ theta, v ~ z
    uu, zz = uniformGrid2D([0., 0.], [2*numpy.pi, length], (n_theta, n_z))
    xx = radius*numpy.cos(uu)
    yy = radius*numpy.sin(uu)
    xx += origin[0]
    yy += origin[1]
    zz += origin[2]
    numPoints = len(xx.flat)
    points = numpy.zeros( (numPoints, 3), numpy.float64 )
    points[:, 0] = xx.flat
    points[:, 1] = yy.flat
    points[:, 2] = zz.flat
      
    # cell connectivity
    numQuadCells = n_theta * n_z
    numCells = 2 * numQuadCells
    iiTheta, jjZ = uniformIndexGrid2D((0, 0), (n_theta, n_z))
    bigII = iiTheta*(n_z + 1) + jjZ
      
    connectivity = numpy.zeros( (numCells, 4), numpy.int )
      
    # lower triangles
    connectivity[:numQuadCells, 1] = numpy.ravel(bigII[:-1, :-1])
    connectivity[:numQuadCells, 2] = numpy.ravel(bigII[1:, :-1])
    connectivity[:numQuadCells, 3] = numpy.ravel(bigII[1:, 1:])
    
    # upper triangles
    connectivity[numQuadCells:, 1] = numpy.ravel(bigII[:-1, :-1])
    connectivity[numQuadCells:, 2] = numpy.ravel(bigII[1:, 1:])
    connectivity[numQuadCells:, 3] = numpy.ravel(bigII[:-1, 1:])
    connectivity[:, 0] = 3 # triangles

    return points, connectivity

  def _createLoMesh(self, origin, radius, length, n_rho, n_theta):
    """
    Create low end disk mesh
    @param origin origin of the disk on the lower end
    @param radius radius
    @param length cylinder length
    @param n_rho number of radial cells
    @param n_theta number of poloidal cells
    @return points, connectivity
    """
    # u ~ rho, v ~ theta
    uu, vv = uniformGrid2D([0., 0.], [radius, 2*numpy.pi], (n_rho, n_theta))
    xx = uu*numpy.cos(vv)
    yy = uu*numpy.sin(vv)
    zz = numpy.zeros( xx.shape, xx.dtype )
    xx += origin[0]
    yy += origin[1]
    zz += origin[2]
    numPoints = len(xx.flat)
    points = numpy.zeros( (numPoints, 3), numpy.float64 )
    points[:, 0] = xx.flat
    points[:, 1] = yy.flat
    points[:, 2] = zz.flat
        
    # cell connectivity
    numQuadCells = n_rho * n_theta
    numCells = 2 * numQuadCells
    iiRho, jjTheta = uniformIndexGrid2D((0, 0), (n_rho, n_theta))
    bigII = iiRho*(n_theta + 1) + jjTheta
        
    connectivity = numpy.zeros( (numCells, 4), numpy.int )
        
    # lower triangles
    connectivity[:numQuadCells, 1] = numpy.ravel(bigII[:-1, :-1])
    connectivity[:numQuadCells, 2] = numpy.ravel(bigII[1:, :-1])
    connectivity[:numQuadCells, 3] = numpy.ravel(bigII[1:, 1:])
        
    # upper triangles
    connectivity[numQuadCells:, 1] = numpy.ravel(bigII[:-1, :-1])
    connectivity[numQuadCells:, 2] = numpy.ravel(bigII[1:, 1:])
    connectivity[numQuadCells:, 3] = numpy.ravel(bigII[:-1, 1:])
    connectivity[:, 0] = 3 # triangles

    return points, connectivity

  def _createHiMesh(self, origin, radius, length, n_rho, n_theta):
    """
    Create high end disk mesh
    @param origin origin of the disk on the lower end
    @param radius radius
    @param length cylinder length
    @param n_rho number of radial cells
    @param n_theta number of poloidal cells
    @return points, connectivity
    """
    # u ~ rho, v ~ theta
    uu, vv = uniformGrid2D([0., 0.], [radius, 2*numpy.pi], (n_rho, n_theta))
    xx = uu*numpy.cos(vv)
    yy = uu*numpy.sin(vv)
    zz = length*numpy.ones( xx.shape, xx.dtype )
    xx += origin[0]
    yy += origin[1]
    zz += origin[2]
    numPoints = len(xx.flat)
    points = numpy.zeros( (numPoints, 3), numpy.float64 )
    points[:, 0] = xx.flat
    points[:, 1] = yy.flat
    points[:, 2] = zz.flat
    
    # cell connectivity
    numQuadCells = n_rho * n_theta
    numCells = 2 * numQuadCells
    iiRho, jjTheta = uniformIndexGrid2D((0, 0), (n_rho, n_theta))
    bigII = iiRho*(n_theta + 1) + jjTheta
    
    connectivity = numpy.zeros( (numCells, 4), numpy.int )
    
    # lower triangles
    connectivity[:numQuadCells, 1] = numpy.ravel(bigII[:-1, :-1])
    connectivity[:numQuadCells, 2] = numpy.ravel(bigII[1:, 1:])
    connectivity[:numQuadCells, 3] = numpy.ravel(bigII[1:, :-1])
    
    # upper triangles
    connectivity[numQuadCells:, 1] = numpy.ravel(bigII[:-1, :-1])
    connectivity[numQuadCells:, 2] = numpy.ravel(bigII[:-1, 1:])
    connectivity[numQuadCells:, 3] = numpy.ravel(bigII[1:, 1:])
    connectivity[:, 0] = 3 # triangles
    
    return points, connectivity

################################################################################
def test():

  cyl = Cylinder(radius=1.0, origin=(0., 0., 0.), length=1.,
                 n_rho=5, n_theta=8, n_z=3)
  cyl.save('cyl.vtk', file_format='vtk', file_type='ascii')
  cyl.show()

if __name__ == '__main__':
  test()

