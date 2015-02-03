"""
"""
import unittest
import collections

from .pep484 import Union


class ReverseTestCase(unittest.TestCase):
    def test_basic(self):
        combined = Union(list, tuple)
        self.assertTrue(issubclass(combined, collections.Sequence))
        # Currently this errors because Union produces an instance, not a class
