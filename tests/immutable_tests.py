#coding=utf-8

from __future__ import division, unicode_literals
import six

import unittest

from measurement import Immutable

class ImmutableTests(unittest.TestCase):
    class Frigid(Immutable):
        pass

    def test_setattr(self):
        f = ImmutableTests.Frigid()
        f.value = "x"
        self.assertEqual(f.value, "x")
        f.frozen = True
        try:
            f.value = "y"
            self.assertTrue(False, "The exception wasn't thrown.")
        except AttributeError as e:
            self.assertEqual(six.text_type(e), "Frigid is immutable.")

    def test_delattr(self):
        f = ImmutableTests.Frigid()
        f.value = "x"
        self.assertEqual(f.value, "x")
        del(f.value)
        self.assertTrue(not hasattr(f, "value"))
        f.value = "x"
        self.assertEqual(f.value, "x")
        f.frozen = True
        try:
            del(f.value)
            self.assertTrue(False, "The exception wasn't thrown.")
        except AttributeError as e:
            self.assertEqual(six.text_type(e), "Frigid is immutable.")
