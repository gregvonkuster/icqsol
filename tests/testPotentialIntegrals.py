#!/usr/bin/env python

from icqsol.bem.icqPotentialIntegrals import PotentialIntegrals
import numpy

def testObserverOnA(order):
    paSrc = numpy.array([0., 0., 0.])
    pbSrc = numpy.array([1., 0., 0.])
    pcSrc = numpy.array([0., 1., 0.])
    xObs = paSrc
    integral = PotentialIntegrals(xObs, pbSrc, pcSrc, order).getIntegralOneOverR()
    exact = numpy.sqrt(2.) * numpy.arcsinh(1.)
    print('testObserverOnA: order = {0} integral = {1} exact = {2} error = {3}'.format(\
        order, integral, exact, integral - exact))

def testObserverOnB(order):
    paSrc = numpy.array([0., 0., 0.])
    pbSrc = numpy.array([1., 0., 0.])
    pcSrc = numpy.array([0., 1., 0.])
    xObs = pbSrc
    integral = PotentialIntegrals(xObs, pcSrc, paSrc, order).getIntegralOneOverR()
    exact = numpy.arcsinh(1.)
    print('testObserverOnB: order = {0} integral = {1} exact = {2} error = {3}'.format(\
        order, integral, exact, integral - exact))

def testObserverOnC(order):
    paSrc = numpy.array([0., 0., 0.])
    pbSrc = numpy.array([1., 0., 0.])
    pcSrc = numpy.array([0., 1., 0.])
    xObs = pcSrc
    integral = PotentialIntegrals(xObs, paSrc, pbSrc, order).getIntegralOneOverR()
    exact = numpy.arcsinh(1.)
    print('testObserverOnC: order = {0} integral = {1} exact = {2} error = {3}'.format(\
        order, integral, exact, integral - exact))


if __name__ == '__main__':
    for order in range(1, 6):
        testObserverOnA(order)
        testObserverOnB(order)
        testObserverOnC(order)
        print('-'*80)

