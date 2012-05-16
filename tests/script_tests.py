#coding=utf-8

from __future__ import division, unicode_literals

import unittest
import sys

from measurement import *
from measurement.astronomical import *
from measurement.united_states_customary import *

class ScriptTestCase(unittest.TestCase):
    "Tests support for calculation scripts."

    @unittest.skipIf("PyPy" in sys.version,
                     "Semi-safe calculation scripts are NOT supported under PyPy yet.")
    def testSafetyOfCalculateFromImporting(self):
        try:
            calculate("import sys\nsys.path")
        except ImportError as e:
            assert str(e) == "__import__ not found", str(e)
        else:
            assert False, "It should not be possible to import packages in a calculation script."

    @unittest.skipIf("PyPy" in sys.version,
                     "Semi-safe calculation scripts are NOT supported under PyPy yet.")
    def testSafetyOfCalculateFromBuiltins(self):
        try:
            calculate("dir()")
        except NameError as e:
            assert str(e) == "name 'dir' is not defined", str(e)
        else:
            assert False, "It should not be possible to call built-ins, like dir()."

    def testSingleIntegerQuantity(self):
        result = calculate("5")
        assert result == 5 * One, result
    def testSingleFloatingPointQuantity(self):
        result = calculate("1.5")
        assert result == 1.5 * One, result
    def testSingleComplexQuantity(self):
        result = calculate("(2+3j)")
        assert result == (2 + 3j) * One, result

    def testSingleQuantityInSimpleMetric(self):
        result = calculate("12 V")
        assert result == 12 * Volt, result
        result = calculate("12 volt")
        assert result == 12 * Volt, result
        result = calculate("12 volts")
        assert result == 12 * Volt, result

    def testSingleQuantityInPluralizedSimpleMetric(self):
        result = calculate("5 candelas")
        assert result == 5 * Candela
        result = calculate("10 inches")
        assert result == 10 * Inch

    def testSingleQuantityInComplexMetric(self):
        result = calculate("20 m/s")
        assert result == 20 * (Meter / Second), result
        result = calculate("20 meter/second")
        assert result == 20 * (Meter / Second), result
        result = calculate("20 meters/second")
        assert result == 20 * (Meter / Second), result

    def testAdditionWithDefinedMetrics(self):
        result = calculate("6 V + 18 V")
        assert result == 24 * Volt, result
        result = calculate("6 volts + 18 volt")
        assert result == 24 * Volt, result
    def testAdditionWithComplexMetrics(self):
        result = calculate("5 m/s + 10 m/s")
        assert result == 15 * (Meter / Second), result
        result = calculate("5 meters/second + 10 meter/second")
        assert result == 15 * (Meter / Second), result

    def testSubtractionWithDefinedMetrics(self):
        result = calculate("18 V - 6 V")
        assert result == 12 * Volt, result
        result = calculate("18 volt - 6 volts")
        assert result == 12 * Volt, result
    def testSubtractionWithComplexMetrics(self):
        result = calculate("20 m/s - 8 m/s")
        assert result == 12 * (Meter / Second), result
        result = calculate("20 meter/second - 8 meters/second")
        assert result == 12 * (Meter / Second), result

    def testMultiplicationWithDefinedMetrics(self):
        result = calculate("4 A * 3 Ω")
        assert result == 12 * Volt, result
        result = calculate("4 amperes * 3 ohm")
        assert result == 12 * Volt, result
    def testMultiplicationWithComplexMetrics(self):
        result = calculate("12 kgm/s * 100 s/m")
        assert result == 1200 * (Kilo*Gram), result
        result = calculate("12 kilogrammeter/second * 100 second/meter")
        assert result == 1200 * (Kilo*Gram), result

    def testDivisionWithDefinedMetrics(self):
        result = calculate("12 V / 3 A")
        assert result == 4 * Ohm, result
        result = calculate("12 volts / 3 amperes")
        assert result == 4 * Ohm, result
    def testDivisionWithComplexMetrics(self):
        result = calculate("40 kgm / 5 m/s")
        assert result == 8 * ((Kilo*Gram) * Second), result
        result = calculate("40 kilogrammeters / 5 meters/second")
        assert result == 8 * ((Kilo*Gram) * Second), result

    def testPositivePower(self):
        result = calculate("2 m²")
        assert result == 2 * Meter**2

        result = calculate("2 meter²")
        assert result == 2 * Meter**2

        result = calculate("2 m^2")
        assert result == 2 * Meter**2

        result = calculate("2 meters^2")
        assert result == 2 * Meter**2

    def testNegativePower(self):
        result = calculate("2 m⁻²")
        assert result == 2 * Meter**-2

        result = calculate("2 meter⁻²")
        assert result == 2 * Meter**-2

        result = calculate("2 m^-2")
        assert result == 2 * Meter**-2

        result = calculate("2 meter^-2")
        assert result == 2 * Meter**-2

    def testVariables(self):
        result = calculate("v = 12 V" + "\n"
                           "i = 2 amperes" + "\n"
                           "v / i")
        assert result == 6 * Ohm

    def testEquality(self):
        result = calculate("12 volt / 2 A == 6 ohm")
        assert result == True, result
        result = calculate("12 V / 2 amperes == 3 Ω")
        assert result == False, result

    def testInequality(self):
        result = calculate("12 V / 2 A != 3 Ω")
        assert result == True, result
        result = calculate("12 V / 2 A != 6 ohm")
        assert result == False, result

    def testGreaterThan(self):
        result = calculate("12 V / 2 A > 6 Ω")
        assert result == False, result
        result = calculate("12 volts / 2 amperes >= 6 Ω")
        assert result == True, result
        result = calculate("12 V / 2 A > 3 Ω")
        assert result == True, result

    def testLessThan(self):
        result = calculate("12 volts / 2 A < 6 ohms")
        assert result == False, result
        result = calculate("12 V / 2 amperes <= 6 Ω")
        assert result == True, result
        result = calculate("12 V / 2 A < 8 Ω")
        assert result == True, result

    def testConversionsWithSimpleMetrics(self):
        result = calculate("12 meters to inches")
        assert result == (12 * Meter).to(Inch), result
    def testConversionsWithComplexMetrics(self):
        result = calculate("12 m/s to miles/hour")
        assert result == (12 * (Meter/Second)).to(Mile / Hour), result
