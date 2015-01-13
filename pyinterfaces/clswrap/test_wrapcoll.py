import collections
import unittest

import _wrapcoll as wc
import support
import meets





class WrapperTests(unittest.TestCase):
    """
    Test wrapper instantiation and value-comparison.
    """
    def test_typeerror(self):
        self.assertRaises(
            support.ClsWrapException,
            lambda: wc.Sequence({})
        )

    def test_sequence(self):
        obj = (1, 2, 3)
        wrapper = wc.Sequence
        wrapped = wrapper(obj)

        self.assertTrue(isinstance(wrapped, wc.InterfaceWrapper))
        self.assertTrue(isinstance(wrapped, collections.Sequence))
        self.assertRaises(
            support.ClsWrapException,
            lambda: wrapper(12)
        )
        self.assertTrue(sequence_equal(wrapped, (1, 2, 3)))

    def test_mutablesequence(self):
        not_mutable = (1, 2, 3)
        obj = [1, 2, 3]
        wrapped = wc.MutableSequence(obj)

        self.assertRaises(
            support.ClsWrapException,
            lambda: wc.MutableSequence(not_mutable)
        )
        self.assertTrue(sequence_equal(wrapped, (1, 2, 3)))

    def test_mutablemapping(self):
        class MyClass(dict):
            def extra(self):
                return "foo"

        obj = MyClass(a=1, b=2)
        wrapper = wc.MutableMapping
        wrapped = wrapper(obj)
        self.assertRaises(
            support.ClsWrapException,
            lambda: wrapper(12)
        )
        self.assertRaises(
            support.ClsWrapException,
            lambda: wrapper([])
        )
        self.assertTrue(hasattr(obj, 'extra'))
        self.assertFalse(hasattr(wrapped, 'extra'))
        self.assertTrue(isinstance(obj, dict))
        self.assertFalse(isinstance(wrapped, dict))
        self.assertTrue(isinstance(obj, collections.MutableMapping))
        self.assertTrue(isinstance(wrapped, collections.MutableMapping))
        self.assertFalse(isinstance(wrapped, collections.MutableSequence))

class ConstructInterfaceWrapperTests(unittest.TestCase):
    """Test class-factory 'construct_interfacewrapper'."""
    def test_sequence(self):
        obj = (1, 2, 3)
        wrapper = wc.construct_interfacewrapper(
            collections.Sequence, cls_name='Sequence'
        )
        wrapped = wrapper(obj)

        self.assertTrue(isinstance(wrapped, wc.InterfaceWrapper))
        self.assertTrue(isinstance(wrapped, collections.Sequence))
        self.assertRaises(
            support.ClsWrapException,
            lambda: wrapper(12)
        )
        self.assertTrue(sequence_equal(wrapped, (1, 2, 3)))


class InterfaceTests(unittest.TestCase):
    """Tests AbstractInterface, and other interface types used only
    for type-checking and static analysis."""
    def test_abstractinterface(self):
        self.assertFalse(isinstance(collections.Sequence, support.AbstractInterface))
        self.assertTrue(issubclass(collections.Sequence, support.AbstractInterface))

        self.assertFalse(isinstance(list, support.AbstractInterface))
        self.assertFalse(issubclass(list, support.AbstractInterface))

        wrapper = wc.Sequence
        wrapped = wrapper([1,2 ])

        self.assertFalse(isinstance(wrapper, support.AbstractInterface))
        self.assertTrue(issubclass(wrapper, support.AbstractInterface))

        self.assertTrue(isinstance(wrapped, support.AbstractInterface))
        self.assertFalse(issubclass(wrapped, support.AbstractInterface))



def sequence_equal(first, second):
    """
    Used in assertions, because .assertEqual() is failing for
    wrapped values
    """
    return all(
        (a == b)
        for a, b in zip(first, second)
    )


if __name__ == "__main__":

    isinst = isinstance(list, support.AbstractInterface)

    unittest.main()
