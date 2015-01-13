import collections
import unittest

import _wrapcoll as wc
import support
import meets

def sequence_equal(first, second):
    """
    Used in assertions, because .assertEqual() is failing for
    wrapped values
    """
    return all(
        (a == b)
        for a, b in zip(first, second)
    )



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



if __name__ == "__main__":

    isinst = isinstance(list, support.AbstractInterface)

    unittest.main()
