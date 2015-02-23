"""
A type of recursive data-structure, representing 
'suspended'/'hanging' operations on sets.

Maybe.... TypeLogicIterator?

Needs to be able to combine:
    Concrete, Union, Intersection, Not
And have a deferred TypeLogic object returned
And it does not collapse until isinstance/issubclass is called
... maybe when 'simplify' is called
... these are basically just a 'map' + collapse command (recursive map)




"""
import abc

_NOT_IMPLEMENTED = lambda self, *args, **kwargs: NotImplemented

class TypeLogicInterface(collections.Set):
    """
    Non-mutable set.
    Might require at least some comparison operations to be
    overridden.
    Comparison operations should return a new object
    """
    __init__ = abc.abstractmethod(_NOT_IMPLEMENTED)
    __contains__ = abc.abstractmethod(_NOT_IMPLEMENTED)
    __iter__ = abc.abstractmethod(_NOT_IMPLEMENTED)
    __len__ = abc.abstractmethod(_NOT_IMPLEMENTED)    


class TypeLogic(object):
    """
    This will need to reimplement the comparison methods, so that
    they return TypeLogic classes.
    """

class Union
