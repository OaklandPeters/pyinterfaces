"""
Abstract parent-class. Inheritable (ie this bears the metaclass)
"""

import abc

import six

@six.add_metaclass(abc.ABCMeta)
class Abstract(object):
    """
    Abstract parent class. Bears metaclass ABCMeta.
    Intended for inheritance.
    """
    pass
