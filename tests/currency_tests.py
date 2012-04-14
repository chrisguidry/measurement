#coding=utf-8
import unittest

from measurement import *
from measurement.currencies import *

import arithmetic
import string_representations

class CurrenciesTestCase(unittest.TestCase):
    "Tests the currency metrics. "
    
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
        
    def testCurrencyRegistrations(self):
        assert UnitedStatesDollar != None
        assert UnitedStatesDollar.name == "United States Dollar", UnitedStatesDollar.name
        assert UnitedStatesDollar.typographical_symbol == "USD", UnitedStatesDollar.typographical_symbol
        assert UnitedStatesDollar.dimension == Exchange, UnitedStatesDollar.dimension
        arithmetic.axioms.hold_for(UnitedStatesDollar)
        string_representations.should_represent_orthogonally(UnitedStatesDollar)
        
        assert Euro != None
        assert Euro.name == "Euro", Euro.name
        assert Euro.typographical_symbol == "EUR", Euro.typographical_symbol
        assert Euro.dimension == Exchange, Euro.dimension
        arithmetic.axioms.hold_for(Euro)
        string_representations.should_represent_orthogonally(Euro)
