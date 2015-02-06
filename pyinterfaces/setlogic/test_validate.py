"""
"""
from __future__ import absolute_import

import unittest
import collections

from .setlogic import ConcreteSet
from . import validate
from .validate import Validator, validate
from . import errors


class ValidateTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(validate([], list), [])
        self.assertEqual(validate([], collections.Sequence), [])
        

        print()
        print("isinstance(ConcreteSet, Validator):", type(isinstance(ConcreteSet, Validator)), isinstance(ConcreteSet, Validator))
        print()
        import pdb
        pdb.set_trace()
        print()

        self.assertRaises(
            errors.ValidationError,
            lambda: validate([], collections.Mapping)
        )
