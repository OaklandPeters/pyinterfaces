"""

@todo: Incorporate use of 'meets'
"""
import collections
import abc

__all__ = [
    'duck_type',
    'Interface',
]

def duck_type(obj, interface):
    """
    Predicate.
    @type obj: object
    @type interface: collections.Sequence or Interface
    @return: bool
    """
    if isinstance(interface, Interface):
        attributes = interface.__abstractmethods__
    elif isinstance(interface, basestring):
        attributes = [interface]
    elif (isinstance(interface, collections.Sequence)
          and not isinstance(interface, basestring)):
        # Sequence of strings
        return all(duck_type(obj, elm) for elm in interface)
    else:
        raise TypeError(str.format(
            "Unrecognized type for interface: {0}",
            type(interface).__name__
        ))

    if _missing_attributes(obj, attributes):
        return False
    else:
        return True

def _hasattr(obj, attr):
    """
    Convience function for checking for attribute in class, or any ancestor in
    its method resolution order (__mro__).
    @type obj: object
    @type attr: str
    @return: bool
    """
    try:
        return any(attr in B.__dict__ for B in obj.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(obj, attr)

def _missing_attributes(obj, attributes):
    """
    Find attributes missing from an object.
    """
    return [
        attr for attr in attributes
        if not _hasattr(obj, attr)
    ]

class Interface(object):
    """
    Used for checking whether class is a Pythonic abstract interface.
    Namely, if it has a __abstractmethods__ attribute.
    """
    __metaclass__ = abc.ABCMeta
    __abstractmethods__ = abc.abstractproperty(lambda self: NotImplemented)
    @classmethod
    def __subclasshook__(cls, subklass):
        if cls is Interface:
            if _hasattr(subklass, "__abstractmethods__"):
                return True
        return NotImplemented
