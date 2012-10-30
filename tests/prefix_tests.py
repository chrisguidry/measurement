#coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *

from . import arithmetic
from . import string_representations

class PrefixTestCase(unittest.TestCase):
    def setUp(self):
        arithmetic.axioms.expectations = {
                                            "commutative": False,
                                            "associative": False,
                                            "identity_in_multiplication": False,
                                            "inverse": False
                                         }
        arithmetic.axioms.multiplicative_identity = One
        arithmetic.axioms.fake_value = Kilo * Metric("faken", "f", Dimension("Fake", "F"))
        arithmetic.axioms.another_fake_value = Nano * Metric("untrut", "u", Dimension("Untruth", "UT"))
    def tearDown(self):
        arithmetic.axioms.expectations = None
        arithmetic.axioms.multiplicative_identity = None
        arithmetic.axioms.fake_value = None
        arithmetic.axioms.another_fake_value = None

    def testHashibility(self):
        assert hash(Kilo * Meter) != 0
        assert hash(Kilo * Meter) == hash(Kilo * Meter)
        assert hash(Kilo * Meter) != hash(Kilo)
        assert hash(Kilo * Meter) != hash(Meter)
        assert hash(Kilo * Meter) != hash(Nano * Meter)

    def testReregistration(self):
        try:
            Metric.Prefix.define(Metric.Prefix("FOO", "BAR", 10, 3))
        except KeyError as e:
            self.assertEqual(six.text_type(e), repr("Multiple definitions of Metric.Prefix with base 10 and power 3"))
        else:
            assert False, "Metric.Prefix.define should have thrown an exception re-defining a prefix."

    def testMultiplicationByAnythingButAMetricIsNotSupported(self):
        try:
            Kilo * 10
        except Exception as e:
            assert six.text_type(e) == "unsupported operand type(s) for *: 'Prefix' and 'int'", six.text_type(e)
        else:
            assert False, "Metric.Prefix.register should have thrown an exception re-registering a prefix."

    def testReductionOfSimpleMetric(self):
        one_thousand_meters = (Kilo*Meter).reduce()
        assert one_thousand_meters.metric == Meter, one_thousand_meters.metric
        assert one_thousand_meters.magnitude == 1000, one_thousand_meters.magnitude

    def testReductionOfInvertedSimpleMetric(self):
        one_thousandth_meter = (One / (Kilo*Meter)).reduce()
        assert one_thousandth_meter.metric == One / Meter, one_thousandth_meter.metric
        assert one_thousandth_meter.magnitude == 0.001, one_thousandth_meter.magnitude

    def testReductionOfDerivedMetricAllPositive(self):
        one_million_metergrams = ((Kilo*Meter) * (Kilo*Gram)).reduce()
        assert one_million_metergrams.metric == Meter * Gram, one_million_metergrams.metric
        assert one_million_metergrams.magnitude == 1000000, one_million_metergrams.magnitude

    def testReductionOfDerivedMetricMixedPrefixes(self):
        one_billion_metergrams = ((Kilo*Meter) * (Mega*Gram)).reduce()
        assert one_billion_metergrams.metric == Meter * Gram, one_billion_metergrams.metric
        assert one_billion_metergrams.magnitude == 1000000000, one_billion_metergrams.magnitude

    def testReductionOfDerivedMetricPositiveAndNegative(self):
        one_meters_per_gram = ((Kilo*Meter) / (Kilo*Gram)).reduce()
        assert one_meters_per_gram.metric == Meter / Gram, one_meters_per_gram.metric
        assert one_meters_per_gram.magnitude == 1, one_meters_per_gram.magnitude

    def testReductionOfDerivedMetricPositiveAndNegativeMixedPrefixes(self):
        one_thousandth_meters_per_gram = ((Kilo*Meter) / (Mega*Gram)).reduce()
        assert one_thousandth_meters_per_gram.metric == Meter / Gram, one_thousandth_meters_per_gram.metric
        assert one_thousandth_meters_per_gram.magnitude == 0.001, one_thousandth_meters_per_gram.magnitude

    def testReductionOfSquaredMetrics(self):
        one_million_square_meters = ((Kilo*Meter)**2).reduce()
        assert one_million_square_meters.metric == Meter**2, one_million_square_meters.metric
        assert one_million_square_meters.magnitude == 1000000, one_million_square_meters.magnitude

    def testMultiplicationByPositivePowerSIPrefix(self):
        kilometer = Kilo * Meter
        assert kilometer.name == "kilometer", kilometer.name
        assert kilometer.typographical_symbol == "km", kilometer.typographical_symbol
        assert kilometer.dimension == Length, kilometer.dimension
        arithmetic.axioms.hold_for(kilometer)
        string_representations.should_represent_orthogonally(kilometer)

    def testMultiplicationByNegativePowerSIPrefix(self):
        nanometer = Nano * Meter
        assert nanometer.name == "nanometer", nanometer.name
        assert nanometer.typographical_symbol == "nm", nanometer.typographical_symbol
        assert nanometer.dimension == Length, nanometer.dimension
        arithmetic.axioms.hold_for(nanometer)
        string_representations.should_represent_orthogonally(nanometer)

    def testPositivePoweredSIPrefixPrecedenceForSquaring(self):
        kilometer = Kilo * Meter
        square_kilometer = kilometer**2

        assert square_kilometer.name == "kilometer²", square_kilometer.name
        assert square_kilometer.typographical_symbol == "km²", square_kilometer.typographical_symbol
        assert square_kilometer.dimension == Area, square_kilometer.dimension
        arithmetic.axioms.hold_for(square_kilometer)
        string_representations.should_represent_orthogonally(square_kilometer)

    def testPositivePoweredSIPrefixPrecedenceForCubing(self):
        kilometer = Kilo * Meter
        cubic_kilometer = kilometer**3

        assert cubic_kilometer.name == "kilometer³", cubic_kilometer.name
        assert cubic_kilometer.typographical_symbol == "km³", cubic_kilometer.typographical_symbol
        assert cubic_kilometer.dimension == Volume, cubic_kilometer.dimension
        arithmetic.axioms.hold_for(cubic_kilometer)
        string_representations.should_represent_orthogonally(cubic_kilometer)

    def testPositivePoweredSIPrefixPrecedenceForACubeBySquaring(self):
        kilometer = Kilo * Meter
        square_kilometer = kilometer**2
        cubic_kilometer = kilometer**3
        this_cubic_kilometer = square_kilometer * kilometer

        assert this_cubic_kilometer == cubic_kilometer
        assert this_cubic_kilometer.name == "kilometer³", this_cubic_kilometer.name
        assert this_cubic_kilometer.typographical_symbol == "km³", this_cubic_kilometer.typographical_symbol
        assert this_cubic_kilometer.dimension == Volume, this_cubic_kilometer.dimension
        arithmetic.axioms.hold_for(this_cubic_kilometer)
        string_representations.should_represent_orthogonally(this_cubic_kilometer)

    def testNegativePoweredSIPrefixPrecedenceForSquaring(self):
        nanometer = Nano * Meter
        square_nanometer = nanometer**2

        assert square_nanometer.name == "nanometer²", square_nanometer.name
        assert square_nanometer.typographical_symbol == "nm²", square_nanometer.typographical_symbol
        assert square_nanometer.dimension == Area, square_nanometer.dimension
        arithmetic.axioms.hold_for(square_nanometer)
        string_representations.should_represent_orthogonally(square_nanometer)

    def testNegativePoweredSIPrefixPrecedenceForCubing(self):
        nanometer = Nano * Meter
        cubic_nanometer = nanometer**3

        assert cubic_nanometer.name == "nanometer³", cubic_nanometer.name
        assert cubic_nanometer.typographical_symbol == "nm³", cubic_nanometer.typographical_symbol
        assert cubic_nanometer.dimension == Volume, cubic_nanometer.dimension
        arithmetic.axioms.hold_for(cubic_nanometer)
        string_representations.should_represent_orthogonally(cubic_nanometer)

    def testNegativePoweredSIPrefixPrecedenceForACubeBySquaring(self):
        nanometer = Nano * Meter
        square_nanometer = nanometer**2
        cubic_nanometer = nanometer**3
        this_cubic_nanometer = square_nanometer * nanometer

        assert this_cubic_nanometer == cubic_nanometer
        assert this_cubic_nanometer.name == "nanometer³", this_cubic_nanometer.name
        assert this_cubic_nanometer.typographical_symbol == "nm³", this_cubic_nanometer.typographical_symbol
        assert this_cubic_nanometer.dimension == Volume, this_cubic_nanometer.dimension
        arithmetic.axioms.hold_for(this_cubic_nanometer)
        string_representations.should_represent_orthogonally(this_cubic_nanometer)

    def testApplicationOfPrefixesInQuantityArithmetic(self):
        assert 5 * (Centi * Meter) == 50 * (Milli * Meter), "%s != %s" % (5 * (Centi * Meter), 50 * (Milli * Meter))
        assert 5 * (Deci * Meter) == 0.5 * Meter, "%s != %s" % (5 * (Deci * Meter), 0.5 * Meter)
        assert (5 * (Centi * Meter)) + (5 * (Deci * Meter)) == 5.5 * (Deci * Meter), "%s != %s" % (5 * (Centi * Meter)) + (5 * (Deci * Meter), 5.5 * (Deci * Meter))
        assert (5 * (Centi * Meter)) + (5 * (Deci * Meter)) == 55 * (Centi * Meter), "%s != %s" % ((5 * (Centi * Meter)) + (5 * (Deci * Meter)), 55 * (Centi * Meter))

        arithmetic.assert_close((5.0 * (Centi * Meter)) + (5.0 * (Deci * Meter)), 550000.0 * (Micro * Meter))
        arithmetic.assert_close(550000 * (Micro * Meter) - 5 * (Centi * Meter), (5 * (Deci * Meter)))
        arithmetic.assert_close(550000 * (Micro * Meter) - 5 * (Centi * Meter), 0.5 * Meter)

    def testPrecedenceOfSIPrefixesAccordingToSIBrochureExample1(self):
        "SI Brochure, Chapter 3 (http://www.bipm.org/en/si/si_brochure/chapter3/prefixes.html), Example 1: 2.3 cm³ = 2.3 (cm)³ = 2.3 (10⁻²m)³ = 2.3 x 10⁻⁶ m³"
        arithmetic.assert_close(2.3 * ((Centi*Meter)**3), (2.3 * One) * (1e-2 * Meter)**3)
        arithmetic.assert_close(2.3 * ((Centi*Meter)**3), (2.3 * One) * (1e-6 * One) * (1 * Meter**3))

    def testPrecedenceOfSIPrefixesAccordingToSIBrochureExample2(self):
        "SI Brochure, Chapter 3 (http://www.bipm.org/en/si/si_brochure/chapter3/prefixes.html), Example 2: 1 cm⁻¹ = 1 (cm)⁻¹ = 1 (10⁻²m)⁻¹ = 10² m⁻¹ = 100 m⁻¹"
        arithmetic.assert_close(1 * ((Centi*Meter)**-1), (1 * One) * (1e-2 * Meter)**-1)
        arithmetic.assert_close(1 * ((Centi*Meter)**-1), (1 * One) * (1e2 * One) * (1 * Meter**-1))
        arithmetic.assert_close(1 * ((Centi*Meter)**-1), 100 / Meter)

    def testPrecedenceOfSIPrefixesAccordingToSIBrochureExample3(self):
        "SI Brochure, Chapter 3 (http://www.bipm.org/en/si/si_brochure/chapter3/prefixes.html), Example 3: 1 V/cm = (1 V)/(10⁻² m) = 10² V/m = 100 V/m"
        arithmetic.assert_close(1 * (Volt / (Centi*Meter)), (1 * Volt) / (1e-2 * Meter), tolerance = 0.1)
        arithmetic.assert_close(1 * (Volt / (Centi*Meter)), 1e2 * (Volt / Meter))

    def testPrecedenceOfSIPrefixesAccordingToSIBrochureExample4(self):
        "SI Brochure, Chapter 3 (http://www.bipm.org/en/si/si_brochure/chapter3/prefixes.html), Example 4: 5000 µs⁻¹ = 5000 (µs⁻¹) = 5000 (10⁻⁶s)⁻¹ = 5 x 10⁹ s⁻¹"
        arithmetic.assert_close(5000 / (Micro*Second), (5000 * One) / (1e-6 * Second))
        arithmetic.assert_close(5000 / (Micro*Second), 5e9 / Second)

    def testPrecedenceOfSIPrefixApplication(self):
        kilometer = (Kilo * Meter)

        three_thousand_meters = 3000 * Meter
        three_kilometers = 3 * kilometer

        assert three_thousand_meters == three_kilometers, "%s != %s" % (three_thousand_meters, three_kilometers)
        assert three_kilometers == three_thousand_meters, "%s != %s" % (three_kilometers, three_thousand_meters)

    def testPrecedenceOfSIPrefixApplicationWhenRaisedToPowers(self):
        kilometer = (Kilo * Meter)

        three_million_square_meters = 3000000 * Meter**2
        three_square_kilometers = 3 * kilometer**2

        assert three_million_square_meters == three_square_kilometers, "%s != %s" % (three_million_square_meters, three_square_kilometers)
        assert three_square_kilometers == three_million_square_meters, "%s != %s" % (three_square_kilometers, three_million_square_meters)

    def testPrecedenceOfSIPrefixApplicationWithReallyComplexMetrics(self):
        three_thousand_ohms = 3000 * Ohm
        three_kiloohms = 3 * (Kilo*Ohm)

        arithmetic.assert_close(three_thousand_ohms, three_kiloohms)
        arithmetic.assert_close(three_kiloohms, three_thousand_ohms)

    def testPrecedenceOfSIPrefixApplicationWithReallyComplexMetricsWhenRaisedToPowers(self):
        three_million_square_ohms = 3000000 * Ohm**2
        three_square_kiloohms = 3 * (Kilo*Ohm)**2

        arithmetic.assert_close(three_million_square_ohms, three_square_kiloohms)
        arithmetic.assert_close(three_square_kiloohms, three_million_square_ohms)

    def testSIPrefixesInEqualityComparisons(self):
        assert 31 * (Milli * Meter) > 3 * (Centi * Meter)
        assert 31 * (Milli * Meter) >= 3 * (Centi * Meter)
        assert 30 * (Milli * Meter) >= 3 * (Centi * Meter)

        assert 29 * (Milli * Meter) < 3 * (Centi * Meter)
        assert 29 * (Milli * Meter) <= 3 * (Centi * Meter)
        assert 30 * (Milli * Meter) <= 3 * (Centi * Meter)

    def testAddingPrefixes(self):
        assert Kilo + Mega == Giga
        assert Kilo + Milli == None

        try:
            Kilo + Kibi
        except TypeError as e:
            assert six.text_type(e) == "unsupported operand type(s) for +: 'Prefix' and 'Prefix'", six.text_type(e)
        else:
            assert False, "You can't add prefixes in different bases."

        try:
            Kilo + 1
        except TypeError as e:
            assert six.text_type(e) == "unsupported operand type(s) for +: 'Prefix' and 'int'", six.text_type(e)
        else:
            assert False, "You can't add Prefixes to anything besides Prefixes."

    def testSubtractingPrefixes(self):
        assert Giga - Kilo == Mega
        assert Kilo - Kilo == None

        unnamed = Mega - Hecto
        self.assertEqual(unnamed.name, "10^4")
        self.assertEqual(unnamed.typographical_symbol, "10^4")
        self.assertEqual(unnamed.base, 10)
        self.assertEqual(unnamed.power, 4)

        try:
            Kilo - Kibi
        except TypeError as e:
            assert six.text_type(e) == "unsupported operand type(s) for -: 'Prefix' and 'Prefix'", six.text_type(e)
        else:
            assert False, "You can't subtract prefixes in different bases."

        try:
            Kilo - 1
        except TypeError as e:
            assert six.text_type(e) == "unsupported operand type(s) for -: 'Prefix' and 'int'", six.text_type(e)
        else:
            assert False, "You can't subtract Prefixes to anything besides Prefixes."

    def testPrefixInequality(self):
        assert Giga != Kilo
        assert Kilo != Milli

    def testUnicode(self):
        assert str(Kilo) == Kilo.typographical_symbol
