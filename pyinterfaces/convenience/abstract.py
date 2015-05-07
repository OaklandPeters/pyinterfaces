"""
Abstract parent-class. Inheritable (ie this bears the metaclass)

@todo: Consider making this defined by being ABC with a nonempty __abstractmethods__.
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
