#coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *
from measurement.united_states_customary import *

from . import arithmetic
from . import string_representations

class UnitedStatesCustomaryTestCase(unittest.TestCase):
    "Tests the United States customary System of Units. "
    "See http://en.wikipedia.org/wiki/United_States_customary_units and "
    "http://www.law.cornell.edu/uscode/search/display.html?terms=unit%20measure&url=/uscode/html/uscode15/usc_sec_15_00000205----000-notes.html ."

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
        assert Mil != None
        assert Mil.name == "mil", Mil.name
        assert Mil.typographical_symbol == "mil", Mil.typographical_symbol
        assert Mil.dimension == Length, Mil.dimension
        arithmetic.axioms.hold_for(Mil)
        string_representations.should_represent_orthogonally(Mil)

        assert Inch != None
        assert Inch.name == "inch", Inch.name
        assert Inch.typographical_symbol == "\"", Inch.typographical_symbol
        assert Inch.dimension == Length, Inch.dimension
        arithmetic.axioms.hold_for(Inch)
        string_representations.should_represent_orthogonally(Inch)

        assert Foot != None
        assert Foot.name == "foot", Foot.name
        assert Foot.typographical_symbol == "\'", Foot.typographical_symbol
        assert Foot.dimension == Length, Foot.dimension
        arithmetic.axioms.hold_for(Foot)
        string_representations.should_represent_orthogonally(Foot)

        assert Yard != None
        assert Yard.name == "yard", Yard.name
        assert Yard.typographical_symbol == "yd", Yard.typographical_symbol
        assert Yard.dimension == Length, Yard.dimension
        arithmetic.axioms.hold_for(Yard)
        string_representations.should_represent_orthogonally(Yard)

        assert Mile != None
        assert Mile.name == "mile", Mile.name
        assert Mile.typographical_symbol == "mi", Mile.typographical_symbol
        assert Mile.dimension == Length, Mile.dimension
        arithmetic.axioms.hold_for(Mile)
        string_representations.should_represent_orthogonally(Mile)

    def testLengthConversions(self):
        arithmetic.assert_close(24 * Inch, 24000 * Mil)
        arithmetic.assert_close(24000 * Mil, 24 * Inch)

        arithmetic.assert_close(24 * Inch, 2 * Foot)
        arithmetic.assert_close(2 * Foot, 24 * Inch)

        arithmetic.assert_close(2 * Yard, 6 * Foot)
        arithmetic.assert_close(6 * Foot, 2 * Yard)

        arithmetic.assert_close(800.0 * Yard, 3.63636364 * Furlong, tolerance = 0.000000001)
        arithmetic.assert_close(3.63636364 * Furlong, 800.0 * Yard, tolerance = 0.00000001)

        arithmetic.assert_close(6000.0 * Foot, 1.13636364 * Mile, tolerance = 0.00000001)
        arithmetic.assert_close(1.13636364 * Mile, 6000.0 * Foot, tolerance = 0.00000001)

        arithmetic.assert_close(2.3 * Mile, 18.4 * Furlong)
        arithmetic.assert_close(18.4 * Furlong, 2.3 * Mile)

        arithmetic.assert_close(2.3 * Mile, 145728.0 * Inch)
        arithmetic.assert_close(145728.0 * Inch, 2.3 * Mile)

        arithmetic.assert_close(2.3 * Mile, 4048.0 * Yard)
        arithmetic.assert_close(4048.0 * Yard, 2.3 * Mile)

    def testSILengthConversions(self):
        arithmetic.assert_close(24.0 * Inch, 60.96 * (Centi*Meter))
        arithmetic.assert_close(60.96 * (Centi*Meter), 24.0 * Inch)

        arithmetic.assert_close(6000.0 * Foot, 1828.8 * Meter)
        arithmetic.assert_close(1828.8 * Meter, 6000.0 * Foot)

        arithmetic.assert_close(800.0 * Yard, 0.73152 * (Kilo*Meter))
        arithmetic.assert_close(0.73152 * (Kilo*Meter), 800.0 * Yard)

        arithmetic.assert_close(2.3 * Mile, 3701491200 * (Micro*Meter))
        arithmetic.assert_close(3701491200 * (Micro*Meter), 2.3 * Mile)

    def testGeneralVolumeRegistration(self):
        # these are all derived, but it's worth laying them out for consistency
        assert (Inch**3) != None
        assert (Inch**3).name == "inch³", (Inch**3).name
        assert (Inch**3).typographical_symbol == "\"³", (Inch**3).typographical_symbol
        assert (Inch**3).dimension == Volume, (Inch**3).dimension
        arithmetic.axioms.hold_for((Inch**3))
        string_representations.should_represent_orthogonally((Inch**3))

        assert (Foot**3) != None
        assert (Foot**3).name == "foot³", (Foot**3).name
        assert (Foot**3).typographical_symbol == "\'³", (Foot**3).typographical_symbol
        assert (Foot**3).dimension == Volume, (Foot**3).dimension
        arithmetic.axioms.hold_for(Foot**3)
        string_representations.should_represent_orthogonally(Foot**3)

        assert (Yard**3) != None
        assert (Yard**3).name == "yard³", (Yard**3).name
        assert (Yard**3).typographical_symbol == "yd³", (Yard**3).typographical_symbol
        assert (Yard**3).dimension == Volume, (Yard**3).dimension
        arithmetic.axioms.hold_for(Yard**3)
        string_representations.should_represent_orthogonally(Yard**3)

    def testGeneralVolumeConversions(self):
        arithmetic.assert_close(1728 * Inch**3, 1 * Foot**3)
        arithmetic.assert_close(1 * Foot**3, 1728 * Inch**3)

        arithmetic.assert_close(1 * Yard**3, 27 * Foot**3)
        arithmetic.assert_close(27 * Foot**3, 1 * Yard**3)


    #TODO: get this freaking test working
#    def testSIGeneralVolumeConversions(self):
#        arithmetic.assert_close(1 * Inch**3, 16.387064 * (Milli*Liter))
#        arithmetic.assert_close(16.387064 * (Milli*Liter), 1 * Inch**3)
#
#        arithmetic.assert_close(1 * Foot**3, 28.316846592 * Liter)
#        arithmetic.assert_close(28.316846592 * Liter, 1 * Foot**3)
#
#        arithmetic.assert_close(1 * Yard**3, 764.554857984 * Liter)
#        arithmetic.assert_close(764.554857984 * Liter, 1 * Yard**3)

    # TODO: liquid volumes

    # TODO: dry volumes

    # TODO: mass

    # TODO: force/weight

    # TODO: cooking measures

    # TODO: grain measures
