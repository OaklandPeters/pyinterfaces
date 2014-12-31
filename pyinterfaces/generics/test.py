from __future__ import absolute_import

import unittest
import abc

from pyinterfaces.generics.validate_instance import Validator, validate


class MyValidator(object):
    exception = TypeError
    def message(self, obj, name=None):
        pass
    def __instancecheck__(self, other):
        pass

class NotAValidator(object):
    """Already inherits __instancecheck__ from object"""
    exception = RuntimeError


class MeetsTests(unittest.TestCase):

    def test_interface_check(self):
        self.assertTrue(isinstance(MyValidator, Validator))
        self.assertTrue(not isinstance(NotAValidator, Validator))


if __name__ == "__main__":
    unittest.main()
