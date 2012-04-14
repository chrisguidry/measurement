#coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *

from . import arithmetic

class ConstantTestCase(unittest.TestCase):

    def testEulersFormula(self):
        "Euler's formula, our \"jewel\", states that e^(i*pi) + 1 = 0"
        arithmetic.assert_close(EulersNumber**(ImaginaryUnit*Pi) + Unity, Zero)

    def testPhi(self):
        "Phi, the Golden Ratio"
        arithmetic.assert_close(Phi, (1 + 5**0.5) / 2)

    def testBigG(self):
        "G, Newton's Gravitational Constant"
        arithmetic.assert_close(GravitationalConstant, 6.67428e11 * (Meter**3 / ( (Kilo*Gram) * Second**2 )))

    def testPlanckAndDiracsConstants(self):
        "Dirac's Constant = Planck's Constant / 2 pi"
        arithmetic.assert_close(DiracsConstant, PlancksConstant / ((2*One) * Pi))
        assert PlancksConstant.metric.dimension == Action
        assert DiracsConstant.metric.dimension == Action
