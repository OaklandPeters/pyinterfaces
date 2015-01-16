"""
Allows classes to be iterated over, without needing to instantiate them.
Reequires some meta-class magic.
"""
import abc

class IterableClassMeta(type):
    """
    To make __iter__ work on the class, it must be a classmethod
    on the inheriting class.
    """

    def __iter__(cls):
        """
        Allows __iter__ to be called on class.
        """
        if _hasattr(cls, '__iter__'):
            return cls.__iter__()
        else:
            raise AttributeError("{0} has no __iter__ method.".format(cls))

    def __repr__(cls):
        """
        """
        if _hasattr(cls, '__repr__'):
            return cls.__repr__()
        else:
            raise AttributeError("{0} has no __repr__ method.".format(cls))


class IterableClass(object):
    __metaclass__ = IterableClassMeta
    @classmethod
    def __repr__(cls):
        """
        Note: this can be dangerous for iterable classes which take a long time to iterate.
        """
        return str.format(
            "<{0}: {1}>",
            cls.__name__, repr(list(cls))
        )



class AbstractIterableClassMeta(abc.ABCMeta, IterableClassMeta):
    """
    Trying to mix IterableClassMeta and abc.ABCMeta (for interfaces)
    has some problems, unless you directly combine the metaclasses.
    """
    pass

class AbstractIterableClass(object):
    __metaclass__ = AbstractIterableClassMeta
    @classmethod
    def __repr__(cls):
        """
        Note: this can be dangerous for iterable classes which take a long time to iterate.
        """
        return str.format(
            "<{0}: {1}>",
            cls.__name__, repr(list(cls))
        )

def _hasattr(obj, attr):
    """
    Looks for attribute in inheritance hierarchy, but excludes metaclass methods
    from consideration. Necessary to prevent recursion inside metaclass methods.
    """
    try:
        return any(attr in ancestor.__dict__ for ancestor in obj.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(obj, attr)
