#coding=utf-8

from __future__ import division, unicode_literals

import unittest

from measurement import *

from . import arithmetic
from . import string_representations

class SIPrefixTestCase(unittest.TestCase):

    def testRegistrationOfSIPrefixes(self):
        assert Yotta.name == "yotta"
        assert Yotta.typographical_symbol == "Y"
        assert Yotta.base == 10
        assert Yotta.power == 24

        assert Zetta.name == "zetta"
        assert Zetta.typographical_symbol == "Z"
        assert Zetta.base == 10
        assert Zetta.power == 21

        assert Exa.name == "exa"
        assert Exa.typographical_symbol == "E"
        assert Exa.base == 10
        assert Exa.power == 18

        assert Peta.name == "peta"
        assert Peta.typographical_symbol == "P"
        assert Peta.base == 10
        assert Peta.power == 15

        assert Tera.name == "tera"
        assert Tera.typographical_symbol == "T"
        assert Tera.base == 10
        assert Tera.power == 12

        assert Giga.name == "giga"
        assert Giga.typographical_symbol == "G"
        assert Giga.base == 10
        assert Giga.power == 9

        assert Mega.name == "mega"
        assert Mega.typographical_symbol == "M"
        assert Mega.base == 10
        assert Mega.power == 6

        assert Kilo.name == "kilo"
        assert Kilo.typographical_symbol == "k"
        assert Kilo.base == 10
        assert Kilo.power == 3

        assert Hecto.name == "hecto"
        assert Hecto.typographical_symbol == "h"
        assert Hecto.base == 10
        assert Hecto.power == 2

        assert Deca.name == "deca"
        assert Deca.typographical_symbol == "da"
        assert Deca.base == 10
        assert Deca.power == 1


        assert Deci.name == "deci"
        assert Deci.typographical_symbol == "d"
        assert Deci.base == 10
        assert Deci.power == -1

        assert Centi.name == "centi"
        assert Centi.typographical_symbol == "c"
        assert Centi.base == 10
        assert Centi.power == -2

        assert Milli.name == "milli"
        assert Milli.typographical_symbol == "m"
        assert Milli.base == 10
        assert Milli.power == -3

        assert Micro.name == "micro"
        assert Micro.typographical_symbol == "µ"
        assert Micro.base == 10
        assert Micro.power == -6

        assert Nano.name == "nano"
        assert Nano.typographical_symbol == "n"
        assert Nano.base == 10
        assert Nano.power == -9

        assert Pico.name == "pico"
        assert Pico.typographical_symbol == "p"
        assert Pico.base == 10
        assert Pico.power == -12

        assert Femto.name == "femto"
        assert Femto.typographical_symbol == "f"
        assert Femto.base == 10
        assert Femto.power == -15

        assert Atto.name == "atto"
        assert Atto.typographical_symbol == "a"
        assert Atto.base == 10
        assert Atto.power == -18

        assert Zepto.name == "zepto"
        assert Zepto.typographical_symbol == "z"
        assert Zepto.base == 10
        assert Zepto.power == -21

        assert Yocto.name == "yocto"
        assert Yocto.typographical_symbol == "y"
        assert Yocto.base == 10
        assert Yocto.power == -24

    def testStringConversions(self):
        string_representations.should_represent_orthogonally(Yotta*Meter)
        string_representations.should_represent_orthogonally(Zetta*Meter)
        string_representations.should_represent_orthogonally(Exa*Meter)
        string_representations.should_represent_orthogonally(Peta*Meter)
        string_representations.should_represent_orthogonally(Tera*Meter)
        string_representations.should_represent_orthogonally(Giga*Meter)
        string_representations.should_represent_orthogonally(Mega*Meter)
        string_representations.should_represent_orthogonally(Hecto*Meter)
        string_representations.should_represent_orthogonally(Deca*Meter)

        string_representations.should_represent_orthogonally(Deci*Meter)
        string_representations.should_represent_orthogonally(Centi*Meter)
        string_representations.should_represent_orthogonally(Milli*Meter)
        string_representations.should_represent_orthogonally(Micro*Meter)
        string_representations.should_represent_orthogonally(Nano*Meter)
        string_representations.should_represent_orthogonally(Pico*Meter)
        string_representations.should_represent_orthogonally(Femto*Meter)
        string_representations.should_represent_orthogonally(Atto*Meter)
        string_representations.should_represent_orthogonally(Zepto*Meter)
        string_representations.should_represent_orthogonally(Yocto*Meter)
