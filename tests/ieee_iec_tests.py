#coding=utf-8
import unittest

from measurement import *

import arithmetic
import string_representations

class IEEEAndIECTestCase(unittest.TestCase):
    "Tests the IEEE System of Units."
    
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
    
    def testIEEE1541IEC80000UnitsOfInformation(self):
        assert Bit != None
        assert Bit.name == "bit", Bit.name
        assert Bit.typographical_symbol == "bit", Bit.typographical_symbol
        assert Bit.dimension == Information, Bit.dimension
        arithmetic.axioms.hold_for(Bit)
        string_representations.should_represent_orthogonally(Bit)
        
        assert Byte != None
        assert Byte.name == "byte", Byte.name
        assert Byte.typographical_symbol == "B", Byte.typographical_symbol
        assert Byte.dimension == Information, Byte.dimension
        arithmetic.axioms.hold_for(Byte)
        string_representations.should_represent_orthogonally(Byte)
        
        assert Octet != None
        assert Octet.name == "octet", Bit.name
        assert Octet.typographical_symbol == "o", Octet.typographical_symbol
        assert Octet.dimension == Information, Octet.dimension
        arithmetic.axioms.hold_for(Octet)
        string_representations.should_represent_orthogonally(Octet)
        
    def testUnitsOfInformationFlow(self):
        assert (Bit / Second).dimension == InformationFlow, (Bit / Second)
        arithmetic.axioms.hold_for(Octet)
        string_representations.should_represent_orthogonally(Octet)
                
        assert (Byte / Second).dimension == InformationFlow, (Byte / Second)
        arithmetic.axioms.hold_for(Byte / Second)
        string_representations.should_represent_orthogonally(Byte / Second)
        
        assert (Octet / Second).dimension == InformationFlow, (Octet / Second)
        arithmetic.axioms.hold_for(Octet / Second)
        string_representations.should_represent_orthogonally(Octet / Second)
