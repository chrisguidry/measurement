# coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *
from measurement.astronomical import *

from . import arithmetic
from . import string_representations

class AstronomicalMeasurementsTestCase(unittest.TestCase):
    """
    Tests units used in astronomical measurement.
    http://en.wikipedia.org/wiki/Category:Units_of_length_in_astronomy
    """

    def setUp(self):
        arithmetic.axioms.expectations = {
                                            "commutative": False,
                                            "associative": False,
                                            "identity_in_multiplication": False,
                                            "inverse": False
                                         }
        arithmetic.axioms.multiplicative_identity = One
        arithmetic.axioms.fake_value = Metric("faken", "f", Dimension("Fake", "F"))
        arithmetic.axioms.another_fake_value = Metric("untrut", "u", Dimension("Untruth", "UT"))
    def tearDown(self):
        arithmetic.axioms.expectations = None
        arithmetic.axioms.multiplicative_identity = None
        arithmetic.axioms.fake_value = None
        arithmetic.axioms.another_fake_value = None

    def testLengthRegistrations(self):
        assert AstronomicalUnit != None
        assert AstronomicalUnit.name == "astronomical unit", AstronomicalUnit.name
        assert AstronomicalUnit.typographical_symbol == "AU", AstronomicalUnit.typographical_symbol
        assert AstronomicalUnit.dimension == Length, AstronomicalUnit.dimension
        arithmetic.axioms.hold_for(AstronomicalUnit)
        string_representations.should_represent_orthogonally(AstronomicalUnit)

        assert Parsec != None
        assert Parsec.name == "parsec", Parsec.name
        assert Parsec.typographical_symbol == "pc", Parsec.typographical_symbol
        assert Parsec.dimension == Length, Parsec.dimension
        arithmetic.axioms.hold_for(Parsec)
        string_representations.should_represent_orthogonally(Parsec)

        assert LightYear != None
        assert LightYear.name == "light year", LightYear.name
        assert LightYear.typographical_symbol == "ly", LightYear.typographical_symbol
        assert LightYear.dimension == Length, LightYear.dimension
        arithmetic.axioms.hold_for(LightYear)
        string_representations.should_represent_orthogonally(LightYear)

    def testLengthConversions(self):
        arithmetic.assert_close(1 * AstronomicalUnit, 1.58128588e-5 * LightYear, tolerance = 0.00003)
        arithmetic.assert_close(1 * LightYear, 63241.1 * AstronomicalUnit, tolerance = 0.0000004)

        arithmetic.assert_close(1 * LightYear, 0.306601 * Parsec, tolerance = 0.000002)
        arithmetic.assert_close(1 * Parsec, 3.261564 * LightYear, tolerance = 0.00000007)

        arithmetic.assert_close(1 * Parsec, 206264.806 * AstronomicalUnit, tolerance = 0.0000002)
        arithmetic.assert_close(1 * AstronomicalUnit, 4.84813681e-6 * Parsec, tolerance = 0.0000002)


    def testLengthSIConversion(self):
        arithmetic.assert_close(1 * AstronomicalUnit, 149597870691 * Meter)
        arithmetic.assert_close(149597870691 * Meter, 1 * AstronomicalUnit)

        arithmetic.assert_close(1 * Parsec, 3.085678e16 * Meter)
        arithmetic.assert_close(3.085678e16 * Meter, 1 * Parsec)

        arithmetic.assert_close(1 * LightYear, 9460730472580800 * Meter)
        arithmetic.assert_close(1 * LightYear, (1 * JulianYear) * (SpeedOfLight))
        arithmetic.assert_close(9460730472580800 * Meter, 1 * LightYear)
