"""
"""
from __future__ import absolute_import

import unittest

from .iterclass import IterableClassMeta, IterableClass


class IterClass(object):
    __metaclass__ = IterableClassMeta
    @classmethod
    def __iter__(cls):
        yield 1
        yield 2
        yield 3

class IterInstanceable(object):
    __metaclass__ = IterableClassMeta
    def __init__(self):
        pass
    def __iter__(self):
        yield 'a'
        yield 'b'
        yield 'c'





class IterableClassTests(unittest.TestCase):
    def test_class_iteration(self):
        self.assertEqual(list(IterClass), [1, 2, 3])

    def test_instance_iteration(self):
        obj = IterInstanceable()
        self.assertEqual(list(obj), ['a', 'b', 'c'])

    def test_iter_both(self):
        class IterBoth(IterClass):
            def __init__(self):
                pass
            def __iter__(self):
                yield 'foo'
                yield 'bar'
        obj = IterBoth()
        self.assertEqual(list(obj), ['foo', 'bar'])

    def test_inheritance_override(self):
        class Ancestor(IterClass):
            @classmethod
            def __iter__(cls):
                yield 'foo'
                yield 'bar'
        self.assertEqual(list(Ancestor), ['foo', 'bar'])

        class IterBoth(IterClass):
            def __init__(self):
                pass
            def __iter__(self):
                yield 'bing'
                yield 'bang'
        obj = IterBoth()
        self.assertEqual(list(obj), ['bing', 'bang'])

    def test_inheritable(self):
        class MyClass(IterableClass):
            @classmethod
            def __iter__(cls):
                yield ['x']
                yield ['y', 'z']

        self.assertEqual(list(MyClass), [['x'], ['y', 'z']])

if __name__ == "__main__":
    unittest.main()
