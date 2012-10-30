#coding=utf-8

from __future__ import division, unicode_literals

from decimal import Decimal

import unittest

from measurement import *

from . import arithmetic
from . import string_representations

class QuantityTestCase(unittest.TestCase):
    def setUp(self):
        arithmetic.axioms.expectations = {
                                            "commutative": False,
                                            "associative": False,
                                            "distributive": False,
                                            "identity_in_multiplication": False,
                                            "identity_in_addition": False,
                                            "inverse": False
                                         }
        arithmetic.axioms.multiplicative_identity = Quantity(1, One)
        arithmetic.axioms.fake_value = Quantity(123.4, Second)
        arithmetic.axioms.another_fake_value = Quantity(-32, Ohm)
    def tearDown(self):
        arithmetic.axioms.expectations = None
        arithmetic.axioms.multiplicative_identity = None
        arithmetic.axioms.additive_identity = None
        arithmetic.axioms.distributable_with = None
        arithmetic.axioms.fake_value = None
        arithmetic.axioms.another_fake_value = None

    def testImmutability(self):
        five_meters = Quantity(5, Meter)

        try:
            five_meters.magnitude = 10
        except AttributeError as e:
            assert six.text_type(e) == "Quantity is immutable."
        else:
            assert False, "Quantity should be immutable"

        try:
            five_meters.metric = Candela
        except AttributeError as e:
            assert six.text_type(e) == "Quantity is immutable."
        else:
            assert False, "Quantity should be immutable"

        try:
            del five_meters.metric
        except AttributeError as e:
            assert six.text_type(e) == "Quantity is immutable."
        else:
            assert False, "Quantity should be immutable"

    def testHashability(self):
        assert hash(Quantity(5, Meter)) != 0
        assert hash(Quantity(5, Meter)) == hash(Quantity(5, Meter))
        assert hash(Quantity(5, Meter)) != hash(Quantity(10, Meter))
        assert hash(Quantity(5, Meter)) != hash(Quantity(5, Candela))
        assert hash(Quantity(5, Meter)) != hash(Quantity(5, Meter / Second))

    def testEquality(self):
        "Tests that a Metric has a sane definition of equality."
        assert Quantity(5, Meter) == Quantity(5, Meter)
        assert Quantity(5, Meter / Second) == Quantity(5, Meter / Second)

    def testInequality(self):
        "Tests that a Metric has a sane definition of inequality."
        assert Quantity(5, Meter) != Quantity(10, Meter)
        assert Quantity(5, Meter) != Quantity(5, Candela)
        assert Quantity(5, Meter) != Quantity(5, Meter / Second)

    def testComparisons(self):
        assert Quantity(5, Meter) < Quantity(10, Meter)
        assert Quantity(5, Meter) <= Quantity(10, Meter)
        assert Quantity(10, Meter) > Quantity(5, Meter)
        assert Quantity(10, Meter) >= Quantity(5, Meter)


    def testEqualityBetween1And1Ones(self):
        assert (One * 1) == 1
        assert (One * 1.0) == 1
        assert (One * 5) == 5
        assert (One * 5.5) == 5.5
        assert (One * -5) == -5
        assert (One * -5.5) == -5.5

        assert 1 == (One * 1)
        assert 1.0 == (One * 1.0)
        assert 5 == (One * 5)
        assert 5.5 == (One * 5.5)
        assert -5 == (One * -5)
        assert -5.5 == (One * -5.5)

    def testEqualityOf0ZeroOnes(self):
        assert (0 * One) == 0
        assert 0 == (0 * One)

    def testInequalityBetweenOtherNumbersAndOnes(self):
        assert (One * 2) != 1
        assert (One * 2.2) != 1
        assert (One * -2) != -5
        assert (One * -2.2) != -5.5

        assert 2 != (One * 1)
        assert 2.2 == (One * 2.2)
        assert -5 != (One * -2)
        assert -5.5 != (One * -2.2)

    def testSorting(self):
        assert sorted([Quantity(3, Meter), Quantity(1, Meter), Quantity(2, Meter)]) == [Quantity(1, Meter), Quantity(2, Meter), Quantity(3, Meter)]

    def testConstructionThroughMultiplyingMetrics(self):
        assert (5 * Meter) == Quantity(5, Meter)
        assert (Meter * 5) == Quantity(5, Meter)

        assert (5 * (Meter / Second)) == Quantity(5, Meter / Second)
        assert ((Meter / Second) * 5) == Quantity(5, Meter / Second)

    def testArithmeticOperatorsNotImplementForAnythingButQuantities(self):
        assert Quantity(5, Meter).__add__(5) == NotImplemented
        assert Quantity(5, Meter).__sub__(5) == NotImplemented
        assert Quantity(5, Meter).__mul__(5) == NotImplemented
        assert Quantity(5, Meter).__floordiv__(5) == NotImplemented
        assert Quantity(5, Meter).__truediv__(5) == NotImplemented

    def testEqualityOperatorsOutsideOfQuantityAreOnlySupportedForNumbers(self):
        assert Quantity(5, Meter).__ge__(5) == NotImplemented
        assert Quantity(5, Meter).__gt__(5) == NotImplemented
        assert Quantity(5, Meter).__le__(5) == NotImplemented
        assert Quantity(5, Meter).__lt__(5) == NotImplemented
        assert Quantity(5, Meter).__eq__(5) == NotImplemented
        assert Quantity(5, Meter).__ne__(5) == NotImplemented

        assert Quantity(5, One).__ge__(5) == True
        assert Quantity(5, One).__gt__(5) == False
        assert Quantity(5, One).__le__(5) == True
        assert Quantity(5, One).__lt__(5) == False
        assert Quantity(5, One).__eq__(5) == True
        assert Quantity(5, One).__ne__(5) == False

    def testConstructionThroughDividingMetrics(self):
        assert 5 / Second == Quantity(5, Hertz)
        assert Second / 4 == Quantity(0.25, Second)

    def testNegationAndAbsolutePower(self):
        assert abs(Quantity(-5, Meter)) == Quantity(5, Meter)
        assert -Quantity(-5, Meter) == Quantity(5, Meter)
        assert -Quantity(5, Meter) == Quantity(-5, Meter)

    def testConstructionViaStrings(self):
        assert Quantity(5, "m") == 5 * Meter

    def testCompositeValues(self):
        assert Quantity(5, "m").__composite_values__() == (5, "m")

    def testNonZero(self):
        assert bool(Quantity(1, "m"))
        assert not bool(Quantity(0, "m"))

    def testParsingNonsense(self):
        try:
            Quantity.parse("foobar")
        except MeasurementParsingException as e:
            assert six.text_type(e) == "Could not parse 'foobar' to a Quantity.", six.text_type(e)
        else:
            assert False, "Parsing nonsense should have thrown"

    def testCoercion(self):
        self.assertEqual(Decimal("10.0") * Meter, 10.0 * Meter)
        self.assertEqual(10.0 * Meter, Decimal("10.0") * Meter)

    def testArithmeticAxiomsOverIntegers(self):
        arithmetic.axioms.additive_identity = Quantity(0, One)
        arithmetic.axioms.distributable_with = Quantity(4, One)
        arithmetic.axioms.hold_for(Quantity(10, One))

        arithmetic.axioms.additive_identity = Quantity(0, Meter)
        arithmetic.axioms.distributable_with = Quantity(4, Meter)
        arithmetic.axioms.hold_for(Quantity(4, Meter))

        arithmetic.axioms.additive_identity = Quantity(0, Meter / Second)
        arithmetic.axioms.distributable_with = Quantity(4, Meter / Second)
        arithmetic.axioms.hold_for(Quantity(5, Meter / Second))

        arithmetic.axioms.additive_identity = Quantity(0, Ohm)
        arithmetic.axioms.distributable_with = Quantity(4, Ohm)
        arithmetic.axioms.hold_for(Quantity(6, Ohm))

    def testStringConversionForIntegers(self):
        string_representations.should_represent_orthogonally(Quantity(10, One))
        string_representations.should_represent_orthogonally(Quantity(4, Meter))
        string_representations.should_represent_orthogonally(Quantity(5, Meter / Second))
        string_representations.should_represent_orthogonally(Quantity(6, Ohm))
        assert six.text_type(10 * Ten) == "100", six.text_type(10 * Ten)

    def testArithmeticAxiomsOverLongs(self):
        arithmetic.axioms.additive_identity = Quantity(int(0), One)
        arithmetic.axioms.distributable_with = Quantity(int(4), One)
        arithmetic.axioms.hold_for(Quantity(int(10), One))

        arithmetic.axioms.additive_identity = Quantity(int(0), Meter)
        arithmetic.axioms.distributable_with = Quantity(int(4), Meter)
        arithmetic.axioms.hold_for(Quantity(int(4), Meter))

        arithmetic.axioms.additive_identity = Quantity(int(0), Meter / Second)
        arithmetic.axioms.distributable_with = Quantity(int(4), Meter / Second)
        arithmetic.axioms.hold_for(Quantity(int(5), Meter / Second))

        arithmetic.axioms.additive_identity = Quantity(int(0), Ohm)
        arithmetic.axioms.distributable_with = Quantity(int(4), Ohm)
        arithmetic.axioms.hold_for(Quantity(int(6), Ohm))

    def testStringConversionForLongs(self):
        string_representations.should_represent_orthogonally(Quantity(int(10), One))
        string_representations.should_represent_orthogonally(Quantity(101231937212349871928471234, One))
        string_representations.should_represent_orthogonally(Quantity(int(4), Meter))
        string_representations.should_represent_orthogonally(Quantity(101231937212349871928471234, Meter))
        string_representations.should_represent_orthogonally(Quantity(int(5), Meter / Second))
        string_representations.should_represent_orthogonally(Quantity(101231937212349871928471234, Meter / Second))
        string_representations.should_represent_orthogonally(Quantity(int(6), Ohm))
        string_representations.should_represent_orthogonally(Quantity(101231937212349871928471234, Ohm))

    def testTrueAndFloorDivision(self):
        assert Quantity(1, Meter) / Quantity(2, Meter) == 0.5
        assert Quantity(1, Meter) // Quantity(2, Meter) == 0

    def testArithmeticAxiomsOverReals(self):
        arithmetic.axioms.additive_identity = Quantity(0.0, One)
        arithmetic.axioms.distributable_with = Quantity(4.0, One)
        arithmetic.axioms.hold_for(Quantity(10.5, One))

        arithmetic.axioms.additive_identity = Quantity(0.0, Meter)
        arithmetic.axioms.distributable_with = Quantity(4.0, Meter)
        arithmetic.axioms.hold_for(Quantity(4.8, Meter))

        arithmetic.axioms.additive_identity = Quantity(0.0, Meter / Second)
        arithmetic.axioms.distributable_with = Quantity(4.0, Meter / Second)
        arithmetic.axioms.hold_for(Quantity(6.5, Meter / Second))

        arithmetic.axioms.additive_identity = Quantity(0.0, Ohm)
        arithmetic.axioms.distributable_with = Quantity(4.0, Ohm)
        arithmetic.axioms.hold_for(Quantity(6.5, Ohm))

    def testStringConversionForReals(self):
        string_representations.should_represent_orthogonally(Quantity(1012.11115, One))
        string_representations.should_represent_orthogonally(Quantity(4.8123131, Meter))
        string_representations.should_represent_orthogonally(Quantity(6123.5213, Meter / Second))
        string_representations.should_represent_orthogonally(Quantity(613.232141245, Ohm))

    def testArithmeticAxiomsOverComplex(self):
        arithmetic.axioms.additive_identity = Quantity(complex(0, 0), One)
        arithmetic.axioms.distributable_with = Quantity(complex(1, 2), One)
        arithmetic.axioms.hold_for(Quantity(complex(2, 3), One))

        arithmetic.axioms.additive_identity = Quantity(complex(0, 0), Meter)
        arithmetic.axioms.distributable_with = Quantity(complex(1, 2), Meter)
        arithmetic.axioms.hold_for(Quantity(complex(2, 3), Meter))

        arithmetic.axioms.additive_identity = Quantity(complex(0, 0), Meter / Second)
        arithmetic.axioms.distributable_with = Quantity(complex(1, 2), Meter / Second)
        arithmetic.axioms.hold_for(Quantity(complex(2, 3), Meter / Second))

        arithmetic.axioms.additive_identity = Quantity(complex(0, 0), Ohm)
        arithmetic.axioms.distributable_with = Quantity(complex(1, 2), Ohm)
        arithmetic.axioms.hold_for(Quantity(complex(2, 3), Ohm))

    def testStringConversionForComplex(self):
        string_representations.should_represent_orthogonally(Quantity(complex(2, 3), One))
        string_representations.should_represent_orthogonally(Quantity(complex(3, 4), Meter))
        string_representations.should_represent_orthogonally(Quantity(complex(4, 5), Meter / Second))
        string_representations.should_represent_orthogonally(Quantity(complex(5, 6), Ohm))

    def testArithmeticAxiomsOverDecimals(self):
        arithmetic.axioms.multiplicative_identity = Quantity(Decimal("1.0"), One)
        arithmetic.axioms.fake_value = Quantity(Decimal("123.4"), Second)
        arithmetic.axioms.another_fake_value = Quantity(Decimal("-32"), Ohm)

        arithmetic.axioms.additive_identity = Quantity(Decimal("0.0"), One)
        arithmetic.axioms.distributable_with = Quantity(Decimal("4.0"), One)
        arithmetic.axioms.hold_for(Quantity(Decimal("10.5"), One))

        arithmetic.axioms.additive_identity = Quantity(Decimal("0.0"), Meter)
        arithmetic.axioms.distributable_with = Quantity(Decimal("4.0"), Meter)
        arithmetic.axioms.hold_for(Quantity(Decimal("8.0"), Meter))

        arithmetic.axioms.additive_identity = Quantity(Decimal("0.0"), Meter / Second)
        arithmetic.axioms.distributable_with = Quantity(Decimal("2.32222"), Meter / Second)
        arithmetic.axioms.hold_for(Quantity(Decimal("4.3"), Meter / Second))

        arithmetic.axioms.additive_identity = Quantity(Decimal("0.0"), Ohm)
        arithmetic.axioms.distributable_with = Quantity(Decimal("4.0"), Ohm)
        arithmetic.axioms.hold_for(Quantity(Decimal("6.5"), Ohm))

    def testStringConversionForDecimals(self):
        # use huge numbers to convince the parser that these are decimals
        string_representations.should_represent_orthogonally(Quantity(Decimal("1234234234234234234234234.2324234235134513425134613451234"), One))
        string_representations.should_represent_orthogonally(Quantity(Decimal("123416512342351432651234261.1235613461234134561346133123412"), Meter))
        string_representations.should_represent_orthogonally(Quantity(Decimal("12316341231346123513461346134513246134612354123512351346133215.1235"), Meter / Second))
        string_representations.should_represent_orthogonally(Quantity(Decimal("13412346123513461234512342341346512341231654123412.342312"), Ohm))

    def testAdditionInFundamentalMetrics(self):
        assert Quantity(1.5, Meter) + Quantity(2, Meter) == Quantity(3.5, Meter)

    def testSubtractionInFundamentalMetrics(self):
        assert Quantity(3.5, Meter) - Quantity(2.4, Meter) == Quantity(1.1, Meter)

    def testAdditionInComplexMetrics(self):
        assert Quantity(1.5, Ohm) + Quantity(2, Ohm) == Quantity(3.5, Ohm)

    def testSubtractionInComplexMetrics(self):
        assert Quantity(3.5, Ohm) - Quantity(2.4, Ohm) == Quantity(1.1, Ohm)

    def testMultiplication(self):
        assert Quantity(3.0, Meter) * Quantity(4.0, Second) == Quantity(12.0, Meter * Second)

    def testDivision(self):
        assert Quantity(12.0, Meter) / Quantity(4.0, Second) == Quantity(3.0, Meter / Second)

    def testSquareRoot(self):
        assert Quantity(16.0, Meter**2)**0.5 == Quantity(4.0, Meter)

    def testCubeRoot(self):
        arithmetic.assert_close(Quantity(64.0, Meter**3)**0.3333333333333333333, Quantity(4.0, Meter))

    def testNonNumericExponent(self):
        try:
            Quantity(10, Meter)**[]
        except TypeError as e:
            assert six.text_type(e) in (
                    "unsupported operand type(s) for ** or pow(): 'Quantity' and 'list'",
                    "operands do not support **"
                   ), six.text_type(e)
        else:
            assert False, "Quantity should be immutable"

    def testOhmsLaw(self):
        "Ohm's Law (http://en.wikipedia.org/wiki/Ohm%27s_law) is a great test of complex dimensional math"

        v = 12.0 * Volt
        i = 2.0 * Ampere
        r = 6.0 * Ohm

        assert i == v / r
        assert v == i * r
        assert r == v / i
