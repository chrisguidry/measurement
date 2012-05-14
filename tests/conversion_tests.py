#coding=utf-8

from __future__ import division, unicode_literals
import six

import unittest

from measurement import *
from measurement.united_states_customary import Inch, Foot, Mile

from . import arithmetic
from . import string_representations

class DimensionTestCase(unittest.TestCase):
    "Tests conversions among Metrics."

    def testMissingConversions(self):
        assert Metric.find_conversion(Meter, Fahrenheit) == None

        try:
            Meter.to(Fahrenheit)
        except MetricConversionError as e:
            assert six.text_type(e) == "There is no conversion between 'm' and '°F', because they measure different Dimensions.", six.text_type(e)
        else:
            assert False, "There shouldn't be a conversion between meter and Fahrenheit."

        assert Meter.is_convertible_to(Fahrenheit) == False

    def testIdentityConversion(self):
        assert Meter.is_convertible_to(Meter)
        assert Meter.to(Meter)(1 * Meter) == 1 * Meter

    def testErrorsPassingTheWrongValuesToConversionFunctions(self):
        try:
            Meter.to(Inch)(1 * Foot)
        except MetricConversionError as e:
            assert six.text_type(e) == "Quantity '1 '' is not convertible with scalar conversion '0.0254 m/\"'", six.text_type(e)
        else:
            assert False, "Passing the wrong value should have thrown an error."

        try:
            Rankine.to(Celsius)(1 * Foot)
        except MetricConversionError as e:
            assert six.text_type(e) == "Quantity '1 '' is not convertible with this conversion function between °R and °C", six.text_type(e)
        else:
            assert False, "Passing the wrong value should have thrown an error."

    def testInformationConversions(self):
        arithmetic.assert_close(16 * Bit, 2 * Octet)
        arithmetic.assert_close(3 * Octet, 24 * Bit)

        # the controversial choice that 1 byte == 1 octet == 8 bit
        arithmetic.assert_close(16 * Bit, 2 * Byte)
        arithmetic.assert_close(3 * Byte, 24 * Bit)
        arithmetic.assert_close(2 * Byte, 2 * Octet)
        arithmetic.assert_close(3 * Octet, 3 * Byte)

    def testTemperatureConversions(self):
        # absolute zero (from http://en.wikipedia.org/wiki/Absolute_zero)
        arithmetic.assert_close(AbsoluteZero, -273.15 * Celsius)
        arithmetic.assert_close(AbsoluteZero, -459.67 * Fahrenheit)
        arithmetic.assert_close(AbsoluteZero, 0.0 * Rankine)
        arithmetic.assert_close(-273.15 * Celsius, AbsoluteZero)
        arithmetic.assert_close(-273.15 * Celsius, -459.67 * Fahrenheit)
        arithmetic.assert_close(-273.15 * Celsius, 0.0 * Rankine)
        arithmetic.assert_close(-459.67 * Fahrenheit, AbsoluteZero)
        arithmetic.assert_close(-459.67 * Fahrenheit, -273.15 * Celsius)
        arithmetic.assert_close(-459.67 * Fahrenheit, 0.0 * Rankine)
        arithmetic.assert_close(0.0 * Rankine, AbsoluteZero)
        arithmetic.assert_close(0.0 * Rankine, -273.15 * Celsius)
        arithmetic.assert_close(0.0 * Rankine, -459.67 * Fahrenheit)

        # freezing point of water (from http://en.wikipedia.org/wiki/Rankine_scale)
        arithmetic.assert_close(273.15 * Kelvin, 0.0 * Celsius)
        arithmetic.assert_close(273.15 * Kelvin, 32.0 * Fahrenheit)
        arithmetic.assert_close(273.15 * Kelvin, 491.67 * Rankine)
        arithmetic.assert_close(0.0 * Celsius, 273.15 * Kelvin)
        arithmetic.assert_close(0.0 * Celsius, 32.0 * Fahrenheit)
        arithmetic.assert_close(0.0 * Celsius, 491.67 * Rankine)
        arithmetic.assert_close(32.0 * Fahrenheit, 273.15 * Kelvin)
        arithmetic.assert_close(32.0 * Fahrenheit, 0.0 * Celsius)
        arithmetic.assert_close(32.0 * Fahrenheit, 491.67 * Rankine)
        arithmetic.assert_close(491.67 * Rankine, 273.15 * Kelvin)
        arithmetic.assert_close(491.67 * Rankine, 0.0 * Celsius)
        arithmetic.assert_close(491.67 * Rankine, 32.0 * Fahrenheit)

        # boiling point of water (from http://en.wikipedia.org/wiki/Rankine_scale)
        arithmetic.assert_close(373.1339 * Kelvin, 99.9839 * Celsius)
        arithmetic.assert_close(373.1339 * Kelvin, 211.9710 * Fahrenheit, tolerance = 0.0000001)
        arithmetic.assert_close(373.1339 * Kelvin, 671.641 * Rankine, tolerance = 0.0000001)
        arithmetic.assert_close(99.9839 * Celsius, 373.1339 * Kelvin)
        arithmetic.assert_close(99.9839 * Celsius, 211.9710 * Fahrenheit, tolerance = 0.000001)
        arithmetic.assert_close(99.9839 * Celsius, 671.641 * Rankine, tolerance = 0.000001)
        arithmetic.assert_close(211.9710 * Fahrenheit, 373.1339 * Kelvin, tolerance = 0.0000001)
        arithmetic.assert_close(211.9710 * Fahrenheit, 99.9839 * Celsius, tolerance = 0.0000001)
        arithmetic.assert_close(211.9710 * Fahrenheit, 671.641 * Rankine)
        arithmetic.assert_close(671.641 * Rankine, 373.1339 * Kelvin, tolerance = 0.0000001)
        arithmetic.assert_close(671.641 * Rankine, 99.9839 * Celsius, tolerance = 0.0000001)
        arithmetic.assert_close(671.641 * Rankine, 211.9710 * Fahrenheit)

    def testFactorLabelConversion(self):
        """
        Factor-Label conversion
        (http://en.wikipedia.org/wiki/Units_conversion_by_factor-label) is a
        method of chaining simple conversions together to derive new
        conversions, as in the conversion between meter/second and miles/hour.
        """
        print("mi/h => m/s")
        arithmetic.assert_close(10 * (Mile / Hour), 4.4704 * (Meter / Second))
        print("m/s => mi/h")
        arithmetic.assert_close(4.4704 * (Meter / Second), 10 * (Mile / Hour))

        print("")

        print("mi/h => m/h")
        arithmetic.assert_close(10 * (Mile / Hour), 16093.44 * (Meter / Hour))
        print("m/h => mi/h")
        arithmetic.assert_close(16093.44 * (Meter / Hour), 10 * (Mile / Hour))

        print("")

        print("mi/h => km/h")
        arithmetic.assert_close(10 * (Mile / Hour), 16.09344 * ((Kilo*Meter) / Hour))
        print("km/h => mi/h")
        arithmetic.assert_close(16.09344 * ((Kilo*Meter) / Hour), 10 * (Mile / Hour))
