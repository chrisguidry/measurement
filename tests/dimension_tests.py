#coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *

from . import arithmetic
from . import string_representations

class DimensionTestCase(unittest.TestCase):
    "Tests the Dimension class."

    def setUp(self):
        arithmetic.axioms.expectations = {
                                            "commutative": False,
                                            "associative": False,
                                            "identity_in_multiplication": False,
                                            "inverse": False
                                         }
        arithmetic.axioms.multiplicative_identity = Number
        arithmetic.axioms.fake_value = Dimension("fakiness", "F")
        arithmetic.axioms.another_fake_value = Dimension("untruthiness", "UT")
    def tearDown(self):
        arithmetic.axioms.expectations = None
        arithmetic.axioms.multiplicative_identity = None
        arithmetic.axioms.fake_value = None
        arithmetic.axioms.another_fake_value = None

    def testGettingAllDimensions(self):
        for dimension in Dimension.all():
            self.assertTrue(isinstance(dimension, Dimension))

    def testGettingByName(self):
        self.assertEqual(Dimension.get_by_name("length"), Length)
        self.assertFalse(Dimension.get_by_name("bogus"))

    def testListingMetrics(self):
        for dimension in Dimension.all():
            for metric in dimension.metrics():
                self.assertEqual(metric.dimension, dimension)

    def testImmutability(self):
        fake = Dimension("Fake", "F")
        "A dimension of how Fake something is."

        try:
            fake.name = "Foo"
        except AttributeError as e:
            assert str(e) == "Dimension is immutable."
        else:
            assert False, "Dimension should be immutable"

        try:
            fake.typographical_symbol = "Foo"
        except AttributeError as e:
            assert str(e) == "Dimension is immutable."
        else:
            assert False, "Dimension should be immutable"

        try:
            fake.terms = []
        except AttributeError as e:
            assert str(e) == "Dimension is immutable."
        else:
            assert False, "Dimension should be immutable"

        try:
            del fake.terms
        except AttributeError as e:
            assert str(e) == "Dimension is immutable."
        else:
            assert False, "Dimension should be immutable"

        try:
            fake.terms.append(object())
        except AttributeError as e:
            pass
        else:
            assert False, "Dimension terms should be immutable"

    def testHashability(self):
        "Tests that Dimension has good hashes."
        assert hash(Dimension("Fake", "F")) != 0
        assert hash(Dimension("Fake", "F")) == hash(Dimension("Fake", "F"))
        assert hash(Dimension("Fake", "F")) != hash(Dimension("Untruthy", "UT"))

    def testHashabilityOfTerms(self):
        "Tests that Dimension Terms have good hashes."
        assert hash(Dimension.Term(Dimension("Fake", "F"), 1)) != 0
        assert hash(Dimension.Term(Dimension("Fake", "F"), 1)) == hash(Dimension.Term(Dimension("Fake", "F"), 1))
        assert hash(Dimension.Term(Dimension("Fake", "F"), 1)) != hash(Dimension.Term(Dimension("Untruthy", "UT"), 1))

    def testEquality(self):
        "Tests that a Dimension has a sane definition of equality."
        assert Dimension("Fake", "F") == Dimension("Fake", "F")

        assert Dimension(terms = [Dimension.Term(Dimension("Fake", "F"), -1)]) == Dimension(terms = [Dimension.Term(Dimension("Fake", "F"), -1)])

        assert (Dimension(terms = [Dimension.Term(Dimension("Fake", "F"), -1), Dimension.Term(Dimension("Untruthy", "UT"), -1)]) ==
                Dimension(terms = [Dimension.Term(Dimension("Fake", "F"), -1), Dimension.Term(Dimension("Untruthy", "UT"), -1)]))

    def testInequality(self):
        "Tests that a Dimension has a sane definition of inequality."
        assert Dimension("Untruthy", "UT") != Dimension("Fake", "F")

        assert Dimension(terms = [Dimension.Term(Dimension("Untruthy", "UT"), -1)]) != Dimension(terms = [Dimension.Term(Dimension("Fake", "F"), -1)])

        assert (Dimension(terms = [Dimension.Term(Dimension("Fake", "F"), -1), Dimension.Term(Dimension("Untruthy", "UT"), -1)]) !=
                Dimension(terms = [Dimension.Term(Dimension("Untruthy", "UT"), -1), Dimension.Term(Dimension("Untruthy", "UT"), -1)]))

    def testArithmeticInASingleDimension(self):
        "Tests that basic arithmetic in a single dimension is supported."
        unitless = Length / Length
        assert unitless == Number
        assert unitless.name == "number", unitless.name
        assert unitless.typographical_symbol == "N", unitless.typographical_symbol
        assert len(unitless.terms) == 1, len(unitless.terms)
        assert Dimension.Term(Number, 1) in unitless.terms

        area = Length * Length
        assert area.name == "area", area.name
        assert area.typographical_symbol == "L²", area.typographical_symbol
        assert len(area.terms) == 1, len(area.terms)
        assert Dimension.Term(Length, 2) in area.terms

        volume = Length * Length * Length
        assert volume.name == "volume", volume.name
        assert volume.typographical_symbol == "L³", volume.typographical_symbol
        assert len(volume.terms) == 1, len(volume.terms)
        assert Dimension.Term(Length, 3) in volume.terms

        volume = area * Length
        assert volume.name == "volume", volume.name
        assert volume.typographical_symbol == "L³", volume.typographical_symbol
        assert len(volume.terms) == 1, len(volume.terms)
        assert Dimension.Term(Length, 3) in volume.terms

        area = (Length * Length * Length) / Length
        assert area.name == "area", area.name
        assert area.typographical_symbol == "L²", area.typographical_symbol
        assert len(area.terms) == 1, len(area.terms)
        assert Dimension.Term(Length, 2) in area.terms

    def testArithmeticInTwoDimensions(self):
        "Tests that basic arithmetic between two dimensions is supported."
        speed = Length / Time
        assert speed.name == "speed", speed.name
        assert speed.typographical_symbol == "L/T", speed.typographical_symbol
        assert len(speed.terms) == 2, len(speed.terms)
        assert Dimension.Term(Length, 1) in speed.terms
        assert Dimension.Term(Time, -1) in speed.terms

        acceleration = speed / Time
        assert acceleration.name == "acceleration", acceleration.name
        assert acceleration.typographical_symbol == "L/T²", acceleration.typographical_symbol
        assert len(acceleration.terms) == 2, len(acceleration.terms)
        assert Dimension.Term(Length, 1) in acceleration.terms
        assert Dimension.Term(Time, -2) in acceleration.terms

        speed = acceleration * Time
        assert speed.name == "speed", speed.name
        assert speed.typographical_symbol == "L/T", speed.typographical_symbol
        assert len(speed.terms) == 2, len(speed.terms)
        assert Dimension.Term(Length, 1) in speed.terms
        assert Dimension.Term(Time, -1) in speed.terms

        unitless = speed / speed
        assert unitless == Number
        assert unitless.name == "number", unitless.name
        assert unitless.typographical_symbol == "N", unitless.typographical_symbol
        assert len(unitless.terms) == 1, len(unitless.terms)
        assert Dimension.Term(Number, 1) in unitless.terms

    def testParsingNonsense(self):
        try:
            Dimension.parse("ASD")
        except MeasurementParsingException as e:
            assert str(e) == "'ASD' doesn't seem to correspond to any defined Dimension", str(e)
        else:
            assert False, "Dimension should have thrown an exception parsing nonsense."

    def testParsingLargeExponent(self):
        dimension = Dimension.parse("L^12")
        assert dimension == Length**12

    def testParsingEmpty(self):
        assert Dimension.symbol_string_to_terms("") == []

    def testOhmsLaw(self):
        "Ohm's Law (http://en.wikipedia.org/wiki/Ohm%27s_law) is a great test of complex dimensional math"
        assert Current == Voltage / Resistance
        assert Voltage == Current * Resistance
        assert Resistance == Voltage / Current

    def testFundamentalDimensions(self):
        "Tests that the fundamental dimensions of math are registered."
        assert Number != None
        assert Number.name == "number"
        assert Number.typographical_symbol == "N"
        arithmetic.axioms.hold_for(Number)
        string_representations.should_represent_orthogonally(Number)

    def testFundamentalPhysicalDimensions(self):
        "Tests that the fundamental dimensions of physics are registered."
        assert Length != None
        assert Length.name == "length"
        assert Length.typographical_symbol == "L"
        arithmetic.axioms.hold_for(Length)
        string_representations.should_represent_orthogonally(Length)

        assert Time != None
        assert Time.name == "time"
        assert Time.typographical_symbol == "T"
        arithmetic.axioms.hold_for(Time)
        string_representations.should_represent_orthogonally(Time)

        assert Mass != None
        assert Mass.name == "mass"
        assert Mass.typographical_symbol == "M"
        arithmetic.axioms.hold_for(Mass)
        string_representations.should_represent_orthogonally(Mass)

        assert Charge != None
        assert Charge.name == "charge"
        assert Charge.typographical_symbol == "Q"
        arithmetic.axioms.hold_for(Charge)
        string_representations.should_represent_orthogonally(Charge)

        assert Temperature != None
        assert Temperature.name == "temperature"
        assert Temperature.typographical_symbol == "Θ"
        arithmetic.axioms.hold_for(Temperature)
        string_representations.should_represent_orthogonally(Temperature)

        assert AmountOfSubstance != None
        assert AmountOfSubstance.name == "amount of substance"
        assert AmountOfSubstance.typographical_symbol == "amount of substance"
        arithmetic.axioms.hold_for(AmountOfSubstance)
        string_representations.should_represent_orthogonally(AmountOfSubstance)

        assert LuminousIntensity != None
        assert LuminousIntensity.name == "luminous intensity"
        assert LuminousIntensity.typographical_symbol == "luminous intensity"
        arithmetic.axioms.hold_for(LuminousIntensity)
        string_representations.should_represent_orthogonally(LuminousIntensity)

        assert Information != None
        assert Information.name == "information"
        assert Information.typographical_symbol == "information"
        arithmetic.axioms.hold_for(Information)
        string_representations.should_represent_orthogonally(Information)

    def testFundamentalEconomicDimensions(self):
        "Tests that the fundamental dimensions of the economy are registered."
        assert Exchange != None
        assert Exchange.name == "exchange"
        assert Exchange.typographical_symbol == "exchange"
        arithmetic.axioms.hold_for(Exchange)
        string_representations.should_represent_orthogonally(Exchange)

    def testDerivedPhysicalDimensions(self):
        "Tests that the basic derived physical dimensions are registered."
        assert Frequency != None
        assert Frequency == Number / Time
        arithmetic.axioms.hold_for(Frequency)
        string_representations.should_represent_orthogonally(Frequency)


        assert Area != None
        assert Area == Length**2
        arithmetic.axioms.hold_for(Area)
        string_representations.should_represent_orthogonally(Area)

        assert Volume != None
        assert Volume == Length**3
        arithmetic.axioms.hold_for(Volume)
        string_representations.should_represent_orthogonally(Volume)

        assert Density != None
        assert Density == Mass / Volume
        arithmetic.axioms.hold_for(Density)
        string_representations.should_represent_orthogonally(Density)


        assert Speed != None
        assert Speed == Length / Time
        arithmetic.axioms.hold_for(Speed)
        string_representations.should_represent_orthogonally(Speed)

        assert Acceleration != None
        assert Acceleration == Speed / Time
        arithmetic.axioms.hold_for(Acceleration)
        string_representations.should_represent_orthogonally(Acceleration)


        assert Momentum != None
        assert Momentum == Mass * Speed
        arithmetic.axioms.hold_for(Momentum)
        string_representations.should_represent_orthogonally(Momentum)

        assert Energy != None
        assert Energy == Mass * Length * Acceleration
        arithmetic.axioms.hold_for(Energy)
        string_representations.should_represent_orthogonally(Energy)

        assert Action != None
        assert Action == Energy * Time
        arithmetic.axioms.hold_for(Action)
        string_representations.should_represent_orthogonally(Action)

        assert Force != None
        assert Force == Mass * Acceleration
        arithmetic.axioms.hold_for(Force)
        string_representations.should_represent_orthogonally(Force)

        assert Power != None
        assert Power == Mass * Area / Time**3
        arithmetic.axioms.hold_for(Power)
        string_representations.should_represent_orthogonally(Power)

        assert Pressure != None
        assert Pressure == Mass / (Length * (Time**2))
        arithmetic.axioms.hold_for(Pressure)
        string_representations.should_represent_orthogonally(Pressure)


        assert Current != None
        assert Current == Charge / Time
        arithmetic.axioms.hold_for(Current)
        string_representations.should_represent_orthogonally(Current)

        assert Voltage != None
        assert Voltage == (Mass * Area) / ((Time**2) * Charge)
        arithmetic.axioms.hold_for(Voltage)
        string_representations.should_represent_orthogonally(Voltage)

        assert Resistance != None
        assert Resistance == (Mass * Area) / (Time * (Charge**2))
        arithmetic.axioms.hold_for(Resistance)
        string_representations.should_represent_orthogonally(Resistance)
