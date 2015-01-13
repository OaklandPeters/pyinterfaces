"""
Wrappers for dyanmic wrapping/extension, based on Python abstract collections
(Sequence, Mapping, etc).

@todo: Make InterfaceWrapper check the interface .. this is problem for which I introduced AbstractParent (in view.py)
@todo: Add interface for 'Interfaces' (ie abstract with __abstractmethod)

Self note:
Alternative to `with Cast(instance, interface):` syntax.
"""
import collections
import abc

import meets
import support


class InterfaceWrapper(object):
    """Wraps an abstract interface object around an instance object
    which meets that interface."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, instance):
        support.validate_instance(
            instance, self.AbstractParent,
            exception=support.InterfaceTypeError
        )
        self._wrapped = instance
    def __repr__(self):
        if hasattr(self._wrapped, '__repr__'):
            return self._wrapped.__repr__()
        else:
            return object.__repr__(self)
    def __str__(self):
        if hasattr(self._wrapped, '__str__'):
            return self._wrapped.__str__()
        else:
            return object.__str__(self)
    AbstractParent = abc.abstractproperty(lambda *args, **kwargs: NotImplemented)


# class Hashable(collections.Hashable, InterfaceWrapper):
#     AbstractParent = collections.Hashable
#     def __hash__(self):
#         return self._wrapped.__hash__()


# class Sequence(collections.Sequence, InterfaceWrapper):
#     AbstractParent = collections.Sequence
#     # Re-implement abstract methods - referencing self._wrapped
#     def __getitem__(self, key):
#         return self._wrapped.__getitem__(key)
#     def __len__(self):
#         return self._wrapped.__len__()


# class MutableSequence(collections.MutableSequence, InterfaceWrapper):
#     AbstractParent = collections.MutableSequence
#     # Re-implement abstract methods - referencing self._wrapped
#     def __getitem__(self, key):
#         return self._wrapped.__getitem__(key)
#     def __len__(self):
#         return self._wrapped.__len__()
#     def __setitem__(self, key, value):
#         return self._wrapped.__setitem__(key, value)
#     def __delitem__(self, key):
#         return self._wrapped.__delitem__(key)
#     def insert(self, index, value):
#         return self._wrapped.insert(index, value)


# class Mapping(collections.Mapping, InterfaceWrapper):
#     AbstractParent = collections.Mapping
#     def __getitem__(self, key):
#         return self._wrapped.__getitem__(key)
#     def __iter__(self):
#         return self._wrapped.__iter__()
#     def __len__(self):
#         return self._wrapped.__len__()


# class MutableMapping(collections.Mapping, InterfaceWrapper):
#     AbstractParent = collections.MutableMapping
#     def __getitem__(self, key):
#         return self._wrapped.__getitem__(key)
#     def __iter__(self):
#         return self._wrapped.__iter__()
#     def __len__(self):
#         return self._wrapped.__len__()
#     def __setitem__(self, key, value):
#         return self._wrapped.__setitem__(key, value)
#     def __delitem__(self, key):
#         return self._wrapped.__delitem__(key)




def construct_interfacewrapper(interface, cls_name=None):
    """
    Metaclass (function-style, not Python class-constructing-class style).
    Makes a class which inherits from InterfaceWrapper and 'interface',
    but overrides all abstractmethods, by redirecting to the equivalent
    method on 'self._wrapped'.

    Note: Do not try to inherit from this.

    @type: interface: AbstractInterface
    @type: cls_name: str or NoneType
    @rtype: type
    """
    support.validate_subclass(interface, support.AbstractInterface, name="interface")
    bases = (interface, InterfaceWrapper)

    if cls_name is None:
        cls_name = interface.__name__ + "InterfaceWrapper"
    cls_name = support.validate_instance(cls_name, str, name='cls_name')

    namespace = {'AbstractParent': interface}

    for attr_name in meets.missing_abstracts(interface, interface):
        #redir = lambda self, *args, **kwargs: getattr(self._wrapped, method_name)(*args, **kwargs)
        #namespace[method_name] = redir
        namespace[attr_name] = wrapper_property(attr_name)

    return type(cls_name, bases, namespace)


def wrapper_property(name):
    """
    PROBLEM: distinguishing methods vs

    property()
    """

    def wrap_get(self):
        return getattr(self._wrapped, name)
    def wrap_set(self, value):
        setattr(self._wrapped, name, value)
    def wrap_del(self):
        delattr(self._wrapped)

    return property(wrap_get, wrap_set, wrap_del)


Hashable = construct_interfacewrapper(collections.Hashable)
Iterable = construct_interfacewrapper(collections.Iterable)
Iterator = construct_interfacewrapper(collections.Iterator)
Sized = construct_interfacewrapper(collections.Container)
Callable = construct_interfacewrapper(collections.Callable)
Set = construct_interfacewrapper(collections.Set)
MutableSet = construct_interfacewrapper(collections.MutableSet)
Mapping = construct_interfacewrapper(collections.Mapping)
MutableMapping = construct_interfacewrapper(collections.MutableMapping)
Sequence = construct_interfacewrapper(collections.Sequence)
MutableSequence = construct_interfacewrapper(collections.MutableSequence)
