"""
Very similar to 'not Iterable', except strings are considered atomic.
"""
import abc

from .shared import _hasattr

class Atomic(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def __iter__(self):
        while False:
            yield None
    @classmethod
    def __subclasshook__(cls, subclass):
        """
        If a class has been entered in the register (eg str), then
        this should not trigger.
        """
        if cls is Atomic:
            if not _hasattr(subclass, "__iter__"):
                return True
        return NotImplemented
