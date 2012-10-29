#coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *

from . import arithmetic
from . import string_representations

class MetricTestCase(unittest.TestCase):

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

    def testImmutability(self):
        faken = Metric("faken", "f", Dimension("Fake", "F"))
        "The faken is a unit of measuring how fake something is"

        try:
            faken.name = "faken"
        except AttributeError as e:
            assert str(e) == "Metric is immutable."
        else:
            assert False, "Metric should be immutable"

        try:
            faken.typographical_symbol = "f"
        except AttributeError as e:
            assert str(e) == "Metric is immutable."
        else:
            assert False, "Metric should be immutable"

        try:
            faken.terms = []
        except AttributeError as e:
            assert str(e) == "Metric is immutable."
        else:
            assert False, "Metric should be immutable"

        try:
            faken.dimension = Dimension("Untruth", "UT")
        except AttributeError as e:
            assert str(e) == "Metric is immutable."
        else:
            assert False, "Metric should be immutable"

        try:
            del faken.terms
        except AttributeError as e:
            assert str(e) == "Metric is immutable."
        else:
            assert False, "Metric should be immutable"

        try:
            faken.terms.append(object())
        except AttributeError as e:
            pass
        else:
            assert False, "Metric terms should be immutable"

    def testHashability(self):
        assert hash(Metric("faken", "f", Dimension("Fake", "F"))) != 0
        assert hash(Metric("faken", "f", Dimension("Fake", "F"))) == hash(Metric("faken", "f", Dimension("Fake", "F")))
        assert hash(Metric("faken", "f", Dimension("Fake", "F"))) != hash(Metric("untrut", "u", Dimension("Fake", "F")))
        assert hash(Metric("faken", "f", Dimension("Fake", "F"))) != hash(Metric("untrut", "u", Dimension("Untruth", "UT")))

    def testHashabilityOfTerms(self):
        assert hash(Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), 1)) != 0
        assert hash(Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), 1)) == hash(Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), 1))

    def testEquality(self):
        "Tests that a Metric has a sane definition of equality."
        assert Metric("faken", "f", Dimension("Fake", "F")) == Metric("faken", "f", Dimension("Fake", "F"))

        assert (Metric(terms = [Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), -1)]) ==
                Metric(terms = [Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), -1)]))

        assert (Metric(terms = [Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), -1), Metric.Term(None, Metric("untrut", "ut", Dimension("Untruthy", "UT")), -1)]) ==
                Metric(terms = [Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), -1), Metric.Term(None, Metric("untrut", "ut", Dimension("Untruthy", "UT")), -1)]))

    def testInequality(self):
        "Tests that a Metric has a sane definition of inequality."
        assert Metric("untrut", "ut", Dimension("Untruthy", "UT")) != Metric("faken", "f", Dimension("Fake", "F"))

        assert (Metric(terms = [Metric.Term(None, Metric("untrut", "ut", Dimension("Untruthy", "UT")), -1)]) !=
                Metric(terms = [Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), -1)]))

        assert (Metric(terms = [Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), -1), Metric.Term(None, Metric("untrut", "ut", Dimension("Untruthy", "UT")), -1)]) !=
                Metric(terms = [Metric.Term(None, Metric("untrut", "ut", Dimension("Untruthy", "UT")), -1), Metric.Term(None, Metric("untrut", "ut", Dimension("Untruthy", "UT")), -1)]))

        assert (Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), -1) !=
                Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), 1))

    def testUnicode(self):
        self.assertEqual(str(Metric.Term(None, Metric("faken", "f", Dimension("Fake", "F")), 11)), "f^11")

    def testArithmeticOutsideOfClassOnlySupportsNumbers(self):
        assert Meter.__mul__("hi") == NotImplemented
        assert Meter.__rmul__("hi") == NotImplemented
        assert Meter.__truediv__("hi") == NotImplemented
        assert Meter.__rtruediv__("hi") == NotImplemented
        assert Meter.__div__("hi") == NotImplemented
        assert Meter.__rdiv__("hi") == NotImplemented

    def testEqualityOutsideOfClassOnlySupportsNumbers(self):
        assert Meter.__eq__("hi") == NotImplemented
        assert Meter.__ne__("hi") == NotImplemented

    def testParsingWithLargeExponents(self):
        assert Metric.parse("m^15") == Meter**15
        assert Metric.parse("m^-15") == Meter**-15

    def testParsingEmpty(self):
        assert Metric.symbol_string_to_terms("") == []

    def testMultiplicationByOne(self):
        assert (One * One) == One
        assert (One * Meter) == Meter
        assert (One * (Meter / Second)) == Meter / Second

        assert (One * One * One) == One
        assert (One * Meter * One) == Meter
        assert (One * (Meter / Second) * One) == Meter / Second

    def testOne(self):
        assert One == One
        assert One == Ten**0
        assert Ten**0 == One
        assert One.reduce() == 1 * One
        assert (Ten**0).reduce() == 1 * One
        assert One**14 == One

    def testTen(self):
        assert Ten == Ten

        assert Ten**1 == Ten
        assert Ten**2 != Ten
        assert Ten**-2 != Ten

        assert Ten.reduce() == 10 * One
        assert (Ten**2).reduce() == 100 * One
        assert (Ten**-2).reduce() == 0.01 * One

    def testMultiplicationWithinASingleMetric(self):
        area = Meter * Meter
        assert area.name == "meter²", area.name
        assert area.typographical_symbol == "m²", area.typographical_symbol
        assert area.dimension == Area, area.dimension

        volume = Meter * Meter * Meter
        assert volume.name == "meter³", volume.name
        assert volume.typographical_symbol == "m³", volume.typographical_symbol
        assert volume.dimension == Volume, volume.dimension
        assert volume == area * Meter

    def testRaisingAMetricToAPower(self):
        assert (Meter**2) == (Meter * Meter)
        assert (Meter**3) == Meter * Meter * Meter

        assert ((Meter / Second)**2) == (Meter / Second) * (Meter / Second)
        assert ((Meter / Second)**3) == (Meter / Second) * (Meter / Second) * (Meter / Second)

    def testRaisingAMetricToAFractionalPowerIsOrthogonal(self):
        assert (Meter**0.5)**2 == Meter, (Meter**0.5)**2
        assert (Meter**2)**0.5 == Meter, (Meter**2)**0.5
        assert (Meter**0.5) * (Meter**0.5) == Meter, (Meter**0.5) * (Meter**0.5)
        assert (Meter**0.5) * (Meter**1.5) == Meter**2, (Meter**0.5) * (Meter**1.5)

    def testDivisionWithinASingleMetric(self):
        unitless = Meter / Meter
        assert unitless == One

        area = Meter * Meter
        volume = Meter * Meter * Meter

        assert area == volume / Meter
        assert Meter == volume / area

        assert unitless == volume / volume

    def testMultiplicationWithinTwoMetrics(self):
        acceleration = (Meter / Second) / Second

        speed = acceleration * Second
        assert speed.name == "meter/second", speed.name
        assert speed.typographical_symbol == "m/s", speed.typographical_symbol
        assert speed.dimension == Speed, speed.dimension

    def testDivisionWithinTwoMetrics(self):
        speed = Meter / Second
        assert speed.name == "meter/second", speed.name
        assert speed.typographical_symbol == "m/s", speed.typographical_symbol
        assert speed.dimension == Speed, speed.dimension
        assert (speed / speed) == One


    def testResolutionOfDerivedMetrics(self):
        old_ohm = Ohm
        new_ohm = ( (Meter**2 * (Kilo * Gram)) / (Second**3 * Ampere**2) )
        assert new_ohm == old_ohm
        assert new_ohm.name == "ohm", new_ohm.name
        assert new_ohm.typographical_symbol == "Ω", new_ohm.typographical_symbol
        assert new_ohm.dimension == Resistance, new_ohm.dimension

    def testOhmsLaw(self):
        "Ohm's Law (http://en.wikipedia.org/wiki/Ohm%27s_law) is a great test of complex dimensional math"
        assert Ampere == Volt / Ohm
        assert Volt == Ampere * Ohm
        assert Ohm == Volt / Ampere


    def testRegistrationOfFundamentalCountingUnitTen(self):
        assert Ten != None
        assert Ten.name == "ten", Ten.name
        assert Ten.typographical_symbol == "10", Ten.typographical_symbol
        assert Ten.dimension == Number, Ten.dimension
        arithmetic.axioms.hold_for(Ten)
        string_representations.should_represent_orthogonally(Ten)

    def testRegistrationOfFundamentalCountingUnitOne(self):
        assert One != None
        assert One.name == "one", One.name
        assert One.typographical_symbol == "1", One.typographical_symbol
        assert One.dimension == Number, One.dimension
        arithmetic.axioms.hold_for(One)
        string_representations.should_represent_orthogonally(One)

        assert One == Ten**0
        assert Ten**0 == One

    def testEqualityBetweenTheCountingUnitOneAndPythonNumbers(self):
        assert One == 1
        assert 1 == One
        assert One == 1.0
        assert 1.0 == One

        assert 0.9999999999999999 != One
        assert 1.000000000000001 != One
        assert One != 0.9999999999999999
        assert One != 1.000000000000001

    def testEqualityBetweenTheCountingUnitTenAndPythonNumbers(self):
        assert Ten == 10
        assert 10 == Ten
        assert Ten == 10.0
        assert 10.0 == Ten

        assert Ten !=  9.999999999999999
        assert  9.999999999999999 != Ten
        assert Ten != 10.000000000000001
        assert 10.000000000000001 != Ten

    def testRegistration(self):
        assert Meter in Metric.all()
        assert Meter == Metric.get_by_name("meter")
        assert Metric.get_by_name("foobar") == None
