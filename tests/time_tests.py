# coding=utf-8

import unittest

from measurement import *

import arithmetic
import string_representations

class TimeMeasurementsTestCase(unittest.TestCase):
    """
    Tests units used in measuring time.
    http://en.wikipedia.org/wiki/Time
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
        
    def testTimeRegistrations(self):
        assert Minute != None
        assert Minute.name == "minute", Minute.name
        assert Minute.typographical_symbol == "min", Minute.typographical_symbol
        assert Minute.dimension == Time, Minute.dimension
        arithmetic.axioms.hold_for(Minute)
        string_representations.should_represent_orthogonally(Minute)

        assert Hour != None
        assert Hour.name == "hour", Hour.name
        assert Hour.typographical_symbol == "h", Hour.typographical_symbol
        assert Hour.dimension == Time, Hour.dimension
        arithmetic.axioms.hold_for(Hour)
        string_representations.should_represent_orthogonally(Hour)

        assert Day != None
        assert Day.name == "day", Day.name
        assert Day.typographical_symbol == "d", Day.typographical_symbol
        assert Day.dimension == Time, Day.dimension
        arithmetic.axioms.hold_for(Day)
        string_representations.should_represent_orthogonally(Day)

        assert Week != None
        assert Week.name == "week", Week.name
        assert Week.typographical_symbol == "wk", Week.typographical_symbol
        assert Week.dimension == Time, Week.dimension
        arithmetic.axioms.hold_for(Week)
        string_representations.should_represent_orthogonally(Week)

        assert Year != None
        assert Year.name == "year", Year.name
        assert Year.typographical_symbol == "y", Year.typographical_symbol
        assert Year.dimension == Time, Year.dimension
        arithmetic.axioms.hold_for(Year)
        string_representations.should_represent_orthogonally(Year)
        

    def testTimeConversions(self):
        arithmetic.assert_close(1 * Minute, 60 * Second)
        arithmetic.assert_close(60 * Second, 1 * Minute)

        arithmetic.assert_close(1 * Hour, 3600 * Second)
        arithmetic.assert_close(3600 * Second, 1 * Hour)
        arithmetic.assert_close(1 * Hour, 60 * Minute)
        arithmetic.assert_close(60 * Minute, 1 * Hour)

        arithmetic.assert_close(1 * Day, 86400 * Second)
        arithmetic.assert_close(86400 * Second, 1 * Day)
        arithmetic.assert_close(1 * Day, 1440 * Minute)
        arithmetic.assert_close(1440 * Minute, 1 * Day)
        arithmetic.assert_close(1 * Day, 24 * Hour)
        arithmetic.assert_close(24 * Hour, 1 * Day)

        arithmetic.assert_close(1 * Year, 31536000 * Second)
        arithmetic.assert_close(31536000 * Second, 1 * Year)
        arithmetic.assert_close(1 * Year, 525600 * Minute)
        arithmetic.assert_close(525600 * Minute, 1 * Year)
        arithmetic.assert_close(1 * Year, 8760 * Hour)
        arithmetic.assert_close(8760 * Hour, 1 * Year)
        arithmetic.assert_close(1 * Year, 365 * Day)
        arithmetic.assert_close(365 * Day, 1 * Year)
