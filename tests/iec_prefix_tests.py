#coding=utf-8
import unittest

from measurement import *

import arithmetic
import string_representations

class IECPrefixTestCase(unittest.TestCase):
    
    def testRegistrationOfIECPrefixes(self):
        assert Yobi.name == "yobi"
        assert Yobi.typographical_symbol == "Yi"
        assert Yobi.base == 2
        assert Yobi.power == 80
        
        assert Zebi.name == "zebi"
        assert Zebi.typographical_symbol == "Zi"
        assert Zebi.base == 2
        assert Zebi.power == 70
        
        assert Exbi.name == "exbi"
        assert Exbi.typographical_symbol == "Ei"
        assert Exbi.base == 2
        assert Exbi.power == 60
        
        assert Pebi.name == "pebi"
        assert Pebi.typographical_symbol == "Pi"
        assert Pebi.base == 2
        assert Pebi.power == 50
        
        assert Tebi.name == "tebi"
        assert Tebi.typographical_symbol == "Ti"
        assert Tebi.base == 2
        assert Tebi.power == 40
        
        assert Gibi.name == "gibi"
        assert Gibi.typographical_symbol == "Gi"
        assert Gibi.base == 2
        assert Gibi.power == 30
        
        assert Mebi.name == "mebi"
        assert Mebi.typographical_symbol == "Mi"
        assert Mebi.base == 2
        assert Mebi.power == 20
        
        assert Kibi.name == "kibi"
        assert Kibi.typographical_symbol == "Ki"
        assert Kibi.base == 2
        assert Kibi.power == 10
        
    def testStringConversions(self):
        string_representations.should_represent_orthogonally(Yobi*Byte)
        string_representations.should_represent_orthogonally(Zebi*Byte)
        string_representations.should_represent_orthogonally(Exbi*Byte)
        string_representations.should_represent_orthogonally(Pebi*Byte)
        string_representations.should_represent_orthogonally(Tebi*Byte)
        string_representations.should_represent_orthogonally(Gibi*Byte)
        string_representations.should_represent_orthogonally(Mebi*Byte)
        string_representations.should_represent_orthogonally(Kibi*Byte)
        
    def testComparisonBetweenDecimalAndBinaryPrefixes(self):
        "Reproduces a table from http://en.wikipedia.org/wiki/Binary_prefix outlining \n"
        "the difference between binary and decimal prefixes"
        
        arithmetic.assert_different(Kibi*Byte, Kilo*Byte,  0.024 * One, tolerance = 0.01)
        arithmetic.assert_different(Mebi*Byte, Mega*Byte,  0.049 * One, tolerance = 0.01)
        arithmetic.assert_different(Gibi*Byte, Giga*Byte,  0.074 * One, tolerance = 0.01)
        arithmetic.assert_different(Tebi*Byte, Tera*Byte,  0.100 * One, tolerance = 0.01)
        arithmetic.assert_different(Pebi*Byte, Peta*Byte,  0.126 * One, tolerance = 0.01)
        arithmetic.assert_different(Exbi*Byte, Exa*Byte,   0.153 * One, tolerance = 0.01)
        arithmetic.assert_different(Zebi*Byte, Zetta*Byte, 0.181 * One, tolerance = 0.01)
        arithmetic.assert_different(Yobi*Byte, Yotta*Byte, 0.209 * One, tolerance = 0.01)
