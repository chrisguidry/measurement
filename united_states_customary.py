"""
United States customary units of measurement.

http://en.wikipedia.org/wiki/United_States_customary_units
"""

import measurement

### Length ###
Mil = measurement.Metric("mil", "mil", measurement.Length)
measurement.Metric.ScalarConversion(measurement.Quantity(0.0000254, measurement.Meter / Mil))

Inch = measurement.Metric("inch", "\"", measurement.Length)
measurement.Metric.ScalarConversion(measurement.Quantity(0.0254, measurement.Meter / Inch))

Foot = measurement.Metric("foot", "'", measurement.Length)
measurement.Metric.ScalarConversion(measurement.Quantity(0.3048, measurement.Meter / Foot))

Yard = measurement.Metric("yard", "yd", measurement.Length)
measurement.Metric.ScalarConversion(measurement.Quantity(0.9144, measurement.Meter / Yard))

Furlong = measurement.Metric("furlong", "furlong", measurement.Length)
measurement.Metric.ScalarConversion(measurement.Quantity(201.168, measurement.Meter / Furlong))

Mile = measurement.Metric("mile", "mi", measurement.Length)
measurement.Metric.ScalarConversion(measurement.Quantity(1609.344, measurement.Meter / Mile))

League = measurement.Metric("league", "league", measurement.Length)
measurement.Metric.ScalarConversion(measurement.Quantity(5556, measurement.Meter / League))

measurement.Metric.ScalarConversion(measurement.Quantity(1000, Mil / Inch))
measurement.Metric.ScalarConversion(measurement.Quantity(12, Inch / Foot))
measurement.Metric.ScalarConversion(measurement.Quantity(12 * 5280, Inch / Mile))
measurement.Metric.ScalarConversion(measurement.Quantity(3, Foot / Yard))
measurement.Metric.ScalarConversion(measurement.Quantity(5280, Foot / Mile))
measurement.Metric.ScalarConversion(measurement.Quantity(1760, Yard / Mile))
measurement.Metric.ScalarConversion(measurement.Quantity(220, Yard / Furlong))
measurement.Metric.ScalarConversion(measurement.Quantity(8, Furlong / Mile))
measurement.Metric.ScalarConversion(measurement.Quantity(3, Mile / League))
