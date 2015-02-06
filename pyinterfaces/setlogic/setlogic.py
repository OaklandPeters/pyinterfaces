"""

"""
import collections

__all__ = ['ConcreteSet']

class ConcreteSet(collections.MutableSet):
    """
    Set-class, used by Union and Optional.
    Holds types, subject to set-theoretic operations.

    Will eventually be used by Intersection and Not.
    """
    def __init__(self, *data):
        self.data = set()
        for elm in data:
            self.add(elm)
    def __contains__(self, other):
        return other in self.data
    def __iter__(self):
        return iter(self.data)
    def __len__(self):
        return len(self)
    def add(self, value):
        self.data.add(self.__validate__(value))
    def remove(self, value):
        self.data.remove(value)
    #-----
    def __validate__(self, value):
        """Default validation is a passthrough.
        Override to add validation."""
        return value



