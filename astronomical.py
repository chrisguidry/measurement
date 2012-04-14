"""
Units of measurement used in Astronomy

http://en.wikipedia.org/wiki/Category:Units_of_length_in_astronomy
"""

from __future__ import division, unicode_literals

import measurement

# Time
JulianYear = measurement.Metric("julian year", "a", dimension = measurement.Time)
"""
The Julian year is 365.25 days of 86,400 seconds each.
http://en.wikipedia.org/wiki/Julian_year_(astronomy)
"""
measurement.Metric.ScalarConversion(
    measurement.Quantity(31557600,
                         measurement.Second / JulianYear))

# Length

AstronomicalUnit = measurement.Metric("astronomical unit", "AU", dimension = measurement.Length)
"""
The Astronomical Unit, or AU, is the average distance between the Earth and
the Sun, approximately 149,597,870,691 meters.
http://en.wikipedia.org/wiki/Astronomical_unit
"""
measurement.Metric.ScalarConversion(
    measurement.Quantity(149597870691,
                         measurement.Meter / AstronomicalUnit))

Parsec = measurement.Metric("parsec", "pc", dimension = measurement.Length)
"""
The parsec, or pc, is the parallax of one arcsecond, a measure of astronomical
distances.
http://en.wikipedia.org/wiki/Parsec
"""
measurement.Metric.ScalarConversion(
    measurement.Quantity(3.085678e16,
                         measurement.Meter / Parsec))


LightYear = measurement.Metric("light year", "ly", dimension = measurement.Length)
"""
The light-year, or ly, is the distance that light travels in one year.
http://en.wikipedia.org/wiki/Light-year
"""
measurement.Metric.ScalarConversion(
    measurement.Quantity(9460730472580800,
                         measurement.Meter / LightYear))
