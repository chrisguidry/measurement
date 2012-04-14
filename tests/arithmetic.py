from __future__ import division, unicode_literals

from decimal import Decimal

FloatingPointTolerance = 0.000000000001
DecimalTolerance = Decimal("0.000000000000000000000000001")

def assert_close(left, right, failure_message = "", tolerance = None):
    if (hasattr(left, "to") and hasattr(right, "to") and
        hasattr(left, "metric") and hasattr(right, "metric") and
        hasattr(left, "magnitude") and hasattr(right, "magnitude")):

        if left.metric != right.metric:
            assert right.metric.is_convertible_to(left.metric), failure_message + ": '%s' cannot be converted to '%s'" % (right.metric, left.metric)
            right = right.to(left.metric)

        assert left.metric == right.metric, failure_message + ": '%s' != '%s' (metrics don't match)" % (left.metric, right.metric)

        if (isinstance(left.magnitude, float) or isinstance(right.magnitude, float) or
            isinstance(left.magnitude, Decimal) or isinstance(right.magnitude, Decimal)):

            if tolerance == None:
                if isinstance(left.magnitude, Decimal) or isinstance(right.magnitude, Decimal):
                    tolerance = DecimalTolerance
                else:
                    tolerance = FloatingPointTolerance

            left_magnitude, right_magnitude = abs(left.magnitude), abs(right.magnitude)
            if left_magnitude < tolerance:
                left_magnitude = 0.0
            elif right_magnitude < tolerance:
                right_magnitude = 0.0

            if left_magnitude == 0.0 and right_magnitude == 0.0:
                percentage_difference = 0.0
            elif right_magnitude == 0.0:
                percentage_difference = (left_magnitude - right_magnitude) / left_magnitude
            else:
                percentage_difference = (left_magnitude - right_magnitude) / right_magnitude

            assert percentage_difference <= tolerance, failure_message + ": %s != %s (variance of %s%%)" % (left, right, percentage_difference)
            return

    assert left == right, failure_message + ": %s != %s" % (left, right)

def assert_different(left, right, expected_percentage, tolerance = None):
    left = left.reduce()
    right = right.reduce()

    if tolerance == None:
        if isinstance(left.magnitude, Decimal) or isinstance(right.magnitude, Decimal):
            tolerance = DecimalTolerance
        else:
            tolerance = FloatingPointTolerance

    difference = (left - right) / right
    assert_close(difference, expected_percentage, tolerance = tolerance)

class axioms(object):

    expectations = {}

    @classmethod
    def hold_for(cls, subject):
        results = {}
        for property in cls.expectations:
            results[property] = False

        for property in results:
            getattr(cls, property)(subject)

    @classmethod
    def commutative(cls, subject):
        assert_close((subject * cls.fake_value), (cls.fake_value * subject), "Commutative property did not hold")

    @classmethod
    def associative(cls, subject):
        assert_close(((subject * cls.fake_value) * cls.another_fake_value), (subject * (cls.fake_value * cls.another_fake_value)), "Associative property did not hold")

    @classmethod
    def distributive(cls, subject):
        assert_close((cls.fake_value * (subject + cls.distributable_with)), ((cls.fake_value * subject) + (cls.fake_value * cls.distributable_with)), "Distributive property did not hold")

    @classmethod
    def identity_in_multiplication(cls, subject):
        assert_close((subject * cls.multiplicative_identity), subject, "Multiplicative Identity (multiplication) did not hold")
        assert_close((subject / cls.multiplicative_identity), subject, "Multiplicative Identity (division) did not hold")

    @classmethod
    def identity_in_addition(cls, subject):
        assert_close((subject + cls.additive_identity), subject, "Additive Identity (addition) did not hold")
        assert_close((subject - cls.additive_identity), subject, "Additive Identity (subtraction) did not hold")

    @classmethod
    def inverse(cls, subject):
        assert_close(( subject * (cls.multiplicative_identity / subject) ), cls.multiplicative_identity, "Inverse did not hold")
