#coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *

from . import arithmetic
from . import string_representations

class SITestCase(unittest.TestCase):
    "Tests the SI System of Units."

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

    def testSIBaseUnits(self):
        assert Meter != None
        assert Meter.name == "meter", Meter.name
        assert Meter.typographical_symbol == "m", Meter.typographical_symbol
        assert Meter.dimension == Length, Meter.dimension
        arithmetic.axioms.hold_for(Meter)
        string_representations.should_represent_orthogonally(Meter)

        assert Gram != None
        assert Gram.name == "gram", Gram.name
        assert Gram.typographical_symbol == "g", Gram.typographical_symbol
        assert Gram.dimension == Mass, Gram.dimension
        arithmetic.axioms.hold_for(Gram)
        string_representations.should_represent_orthogonally(Gram)

        assert Second != None
        assert Second.name == "second", Second.name
        assert Second.typographical_symbol == "s", Second.typographical_symbol
        assert Second.dimension == Time, Second.dimension
        arithmetic.axioms.hold_for(Second)
        string_representations.should_represent_orthogonally(Second)

        assert Ampere != None
        assert Ampere.name == "ampere", Ampere.name
        assert Ampere.typographical_symbol == "A", Ampere.typographical_symbol
        assert Ampere.dimension == Current, Ampere.dimension
        arithmetic.axioms.hold_for(Ampere)
        string_representations.should_represent_orthogonally(Ampere)

        assert Kelvin != None
        assert Kelvin.name == "kelvin", Kelvin.name
        assert Kelvin.typographical_symbol == "K", Kelvin.typographical_symbol
        assert Kelvin.dimension == Temperature, Kelvin.dimension
        arithmetic.axioms.hold_for(Kelvin)
        string_representations.should_represent_orthogonally(Kelvin)

        assert Mole != None
        assert Mole.name == "mole", Mole.name
        assert Mole.typographical_symbol == "mol", Mole.typographical_symbol
        assert Mole.dimension == AmountOfSubstance, Mole.dimension
        arithmetic.axioms.hold_for(Mole)
        string_representations.should_represent_orthogonally(Mole)

        assert Candela != None
        assert Candela.name == "candela", Candela.name
        assert Candela.typographical_symbol == "cd", Candela.typographical_symbol
        assert Candela.dimension == LuminousIntensity, Candela.dimension
        arithmetic.axioms.hold_for(Candela)
        string_representations.should_represent_orthogonally(Candela)

    def testSIDerivedUnits(self):
        assert Radian != None
        assert Radian == (Meter / Meter)
        assert Radian.name == "radian", Radian.name
        assert Radian.typographical_symbol == "rad", Radian.typographical_symbol
        assert Radian.dimension == Number, Radian.dimension
        arithmetic.axioms.hold_for(Radian)
        string_representations.should_represent_orthogonally(Radian)

        assert Steradian != None
        assert Steradian == (Meter**2 / Meter**2)
        assert Steradian.name == "steradian", Steradian.name
        assert Steradian.typographical_symbol == "sr", Steradian.typographical_symbol
        assert Steradian.dimension == Number, Steradian.dimension
        arithmetic.axioms.hold_for(Steradian)
        string_representations.should_represent_orthogonally(Steradian)

        assert Hertz != None
        assert Hertz == (One / Second)
        assert Hertz.name == "hertz", Hertz.name
        assert Hertz.typographical_symbol == "Hz", Hertz.typographical_symbol
        assert Hertz.dimension == Frequency, Hertz.dimension
        arithmetic.axioms.hold_for(Hertz)
        string_representations.should_represent_orthogonally(Hertz)

        assert Coulomb != None
        assert Coulomb == (Ampere * Second)
        assert Coulomb.name == "coulomb", Coulomb.name
        assert Coulomb.typographical_symbol == "C", Coulomb.typographical_symbol
        assert Coulomb.dimension == Charge, Coulomb.dimension
        arithmetic.axioms.hold_for(Coulomb)
        string_representations.should_represent_orthogonally(Coulomb)

        assert Joule != None
        assert Joule == (Kilo*Gram) * ((Meter**2) / (Second**2))
        assert Joule.name == "joule", Joule.name
        assert Joule.typographical_symbol == "J", Joule.typographical_symbol
        assert Joule.dimension == Energy, Joule.dimension
        arithmetic.axioms.hold_for(Joule)
        string_representations.should_represent_orthogonally(Joule)

        assert Ohm != None
        assert Ohm == ( (Meter**2 * (Kilo * Gram)) / (Second**3 * Ampere**2) )
        assert Ohm.name == "ohm", Ohm.name
        assert Ohm.typographical_symbol == "Ω", Ohm.typographical_symbol
        assert Ohm.dimension == Resistance, Ohm.dimension
        assert (One / Ohm) * Ohm == One, (One / Ohm) * Ohm
        arithmetic.axioms.hold_for(Ohm)
        string_representations.should_represent_orthogonally(Ohm)

        assert Volt != None
        assert Volt == ( (Meter**2 * (Kilo * Gram)) / (Second**3 * Ampere) )
        assert Volt.name == "volt", Volt.name
        assert Volt.typographical_symbol == "V", Volt.typographical_symbol
        assert Volt.dimension == Voltage, Volt.dimension
        arithmetic.axioms.hold_for(Volt)
        string_representations.should_represent_orthogonally(Volt)

        assert Watt != None
        assert Watt == ((Kilo * Gram) * Meter**2) / Second**3
        assert Watt.name == "watt", Watt.name
        assert Watt.typographical_symbol == "W", Watt.typographical_symbol
        assert Watt.dimension == Power, Watt.dimension
        arithmetic.axioms.hold_for(Watt)
        string_representations.should_represent_orthogonally(Watt)

    def testSISynonyms(self):

        # the Liter is a cubic decimeter, or 0.001 m^3
        assert Liter != None
        assert Liter.name == "liter", Liter.name
        assert Liter.typographical_symbol == "L", Liter.typographical_symbol
        assert Liter.dimension == Volume, Liter.dimension
        assert Liter == (Deci * Meter)**3
        arithmetic.axioms.hold_for(Liter)
        string_representations.should_represent_orthogonally(Liter)

        arithmetic.axioms.hold_for(Milli*Liter)
        string_representations.should_represent_orthogonally(Milli*Liter)

        arithmetic.assert_close(1 * Liter, 0.001 * Meter**3)
        arithmetic.assert_close(0.001 * Meter**3, 1 * Liter)

        arithmetic.assert_close(Liter.reduce(), 0.001 * Meter**3)
        arithmetic.assert_close(0.001 * Meter**3, Liter.reduce())

        arithmetic.assert_close(1 * (Milli*Liter), 0.000001 * Meter**3)
        arithmetic.assert_close(0.000001 * Meter**3, 1 * (Milli*Liter))



        # the ångström (Å) is 0.1 nm or 1e-10 m
        assert Angstrom != None
        assert Angstrom.name == "ångström", Angstrom.name
        assert Angstrom.typographical_symbol == "Å", Angstrom.typographical_symbol
        assert Angstrom.dimension == Length, Angstrom.dimension
        arithmetic.axioms.hold_for(Angstrom)
        string_representations.should_represent_orthogonally(Angstrom)

        arithmetic.assert_close(1 * Angstrom, 0.1 * (Nano*Meter))
        arithmetic.assert_close(0.1 * (Nano*Meter), 1 * Angstrom)
