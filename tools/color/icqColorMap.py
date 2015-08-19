#!/usr/bin/env python

import math


class ColorMap:


    def __init__(self, fmin, fmax):
        """
        Constructor 
        @param fmin minimum field value
        @param fmax maximum field value
        """

        self.fmin = fmin
        self.fmax = fmax

    def hatFunc(self, x, x0, x1, x2, x3):
        """
        Hat function
        @param x normalized abscissa, between 0 and 1
        @param x0 x value where function rises from zero
        @param x1 x value where function reaches 1
        @param x2 x value where function drops from 1
        @param x3 x value where function reaches 0
        @return value
        """
        slope01 = 1./(x1 - x0)
        slope23 = 1./(x3 - x2)
        return min(1., max(0., slope01*(x - x0))) \
             - min(1., max(0., slope01*(x - x1))) \
             - min(1., max(0., slope23*(x - x2))) \
             + min(1., max(0., slope23*(x - x3)))

    def hot(self, f):
        """
        Get hot color 
        @param f field value
        @return red, green, blue components in range 0 to 255
        """
        x = (f - self.fmin)/(self.fmax - self.fmin)
        r = int(255*math.cos((1. - x)*math.pi)**2 + 0.5)
        g = int(255*math.sin(x*math.pi)**2 + 0.5)
        b = int(255*math.cos(x*math.pi)**2 + 0.5)
        return r, g, b

    def cold(self, f):
        """
        Get cold color 
        @param f field value
        @return red, green, blue components in range 0 to 255
        """
        r, g, b = self.hot(f)
        # reverse order
        return b, g, r

    def gnu(self, f):
        """
        Get gnu color
        @param f field value
        @return red, green, blue components in range 0 to 255
        """
        x = (f - self.fmin)/(self.fmax - self.fmin)
        r = self.hatFunc(x, 3./8., 5./8., 7./8., 9./8.)
        g = self.hatFunc(x, 1./8., 3./8., 5./8., 7./8.)
        b = self.hatFunc(x, -1./8., 1./8., 3./8., 5./8.)
        return r, g, b

    def blackbody(self, f):
        """
        Get black body color 
        @param f field value
        @return red, green, blue components in range 0 to 255
        """
        x = (f - self.fmin)/(self.fmax - self.fmin)
        r = int(255*min(1., 2*math.cos(x*math.pi/2.)**2) + 0.5)
        g = int(255*math.sin(x*math.pi)**2 + 0.5)
        b = int(255*min(1., 2*math.cos((1. - x)*math.pi/2.)**2) + 0.5)
        return r, g, b
