"""

Self Note: ... I don't think this actually needs ValueMeta/ValueABC, because
it can just have Any/Union be instances

@todo: Decide if Tuple and tuple should have an 'virtual' (abc.register) relationship.
"""
import abc
import types

from ..valueabc.valueabc import ValueABC
from .shared import TypeLogic

__all__ = [
    'Any',
    'Union',
    'Optional'
]


class Any(ValueABC):
    """
    Back port of typing.Any from PEP 483, into pyinterfaces/ 2.7 implementation.
    This version of `Any` differs in some major ways. For example, this version
    does not count as a subclass of all other classes, but the true PEP 483 version
    does.
        assert isinstance(typing.Any, SomeClass)
        assert not isinstance(metatypes.Any, SomeClass)
    """
    @classmethod
    def __instancecheck__(self, instance):  # pylint: disable=unused-argument
        """
        @type: instance: Any
        @rtype: bool
        """
        return True
    @classmethod
    def __subclasscheck__(self, subclass):  # pylint: disable=unused-argument
        """
        @type: subclass: type
        @rtype: bool
        """
        if not isinstance(subclass, type):
            raise TypeError(str.format(
                "'subclass' must be a class."
            ))
        return True


class UnionMeta(type):
    """
    Metaclass for generating TypeUnion classes.

    UnionMeta(...)
    --> Union(...)
    --> TypeUnion(...)

    """
    def __new__(mcls, name, bases, namespace):
        """
        Union(list, tuple) -->
            TypeUnion = UnionMeta('TypeUnion', (,), {})
            return TypeUnion

        Triggers type.__new__, which will cause different behavior
        for descendants, if mcls has __instancecheck__ and __subclasscheck__

        Unconfirmed Belief: methods on mcls become classmethods on cls. Classmethods on mcls do not appear on cls at all.

        @todo: Requires that namespaces includes 'types', and validate it.

        @type: name: str
        @type: bases: Sequence[type]
        @type: namespace: dict[str, Any]
        """

        # Construct class - uses type.__new__
        cls = super(UnionMeta, mcls).__new__(mcls, name, bases, namespace)

        return cls

    def __call__(cls, *args, **kwargs):
        """
        Triggered whenever the newly created class is "called"
        to instantiate a new object.

        (mcls.__init__ controls the initialization of the new class,
         NOT the initialization of the instances of the new class)
        
        I need to set Union(list, tuple) to return a class
        ... this can be done either here in UnionMeta.__call__, or in Union.__new__
        """
        return cls.__new__(cls, *args, **kwargs)


    def __instancecheck__(cls, instance):  # pylint: disable=unused-argument
        """
        @type: instance: Any
        @rtype: bool
        """
        if _hasattr(cls, "__instancecheck__"):
            return cls.__instancecheck__(instance)
        return NotImplemented
        
        # return any(
        #     isinstance(instance, _type)
        #     for _type in cls._types
        # )


    def __subclasscheck__(cls, subclass):  # pylint: disable=unused-argument
        """
        @type: subclass: type
        @rtype: bool
        """        
        if _hasattr(cls, "__subclasscheck__"):
            return cls.__subclasscheck__(subclass)
        return NotImplemented



class Union(object):
    __metaclass__ = UnionMeta
    def __new__(cls, *_types):
        class TypeUnion(Union):
            @classmethod
            def __instancecheck__(cls, instance):                
                return any(
                    isinstance(instance, _type)
                    for _type in cls._types
                )
            @classmethod
            def __subclasscheck__(cls, subclass):
                return any(
                    issubclass(subclass, _type)
                    for _type in cls._types
                )
        if len(_types) == 0:
            _types = tuple([Any])
        TypeUnion._types = _types  # pylint: disable=W0212
        return TypeUnion



# class Union(ValueABC):
#     """
#     ... trying to do this without a special metaclass

#     @todo: Create with metaclass, defining
#     __instancecheck__
#     __repr__
#     __subclasscheck__
#     """
#     _types = tuple()

#     def __new__(cls, *_types):
#         """
#         Create new class, inheriting from this one, and return it.
#         @todo: type-check _types

#         @type: _types: Sequence[type]
#         @rtype: Union
#         """
#         name = "UnionedTypes"
#         bases = tuple([Union])

#         def union_repr(cls):
#             return repr(cls).replace(
#                 "'>", "': "+repr(cls._types)+">"
#             )
#         namespace = {
#             '_types': _types,
#             '__repr__': classmethod(union_repr)
#             # '__instancecheck__': Union.__instancecheck__,
#             # '__subclasscheck__': Union.__subclasscheck__
#         }
#         return type(name, bases, namespace)


#     @classmethod
#     def __instancecheck__(cls, instance):  # pylint: disable=unused-argument
#         """
#         @type: instance: Any
#         @rtype: bool
#         """
#         # ... prevent recursion
#         if isinstance(instance, type):
#             if Union in instance.__mro__:
#                 return False
#         else: # is an instance
#             if Union in type(instance).__mro__:
#                 return False

#         return any(
#             isinstance(instance, _type)
#             for _type in cls._types
#         )

#     @classmethod
#     def __subclasscheck__(cls, subclass):  # pylint: disable=unused-argument
#         """
#         @type: subclass: type
#         @rtype: bool
#         """


#         print()
#         print("cls:", type(cls), cls)
#         print("subclass:", type(subclass), subclass)
#         print()
#         import pdb
#         pdb.set_trace()
#         print()
        

#         if not isinstance(subclass, type):
#             raise TypeError(str.format(
#                 "'subclass' must be a class."
#             ))
#         else:
#             # ... prevent recursion
#             if cls is Union:
#                 if Union in subclass.__mro__:
#                     return True  
#             return any(
#                 issubclass(subclass, _type)
#                 for _type in cls._types
#             )
#Union._types = tuple()





class Union_v1(TypeLogic):
    """
    Must be instanced before being used.
    """
    def __init__(self, *_types):
        TypeLogic.__init__(self, *_types)

    def __instancecheck__(self, instance):
        """
        Is instance an instance of any of self.types?
        @type: instance: Any
        @rtype: bool
        """
        return any(
            isinstance(instance, _type)
            for _type in self._types
        )

    def __subclasscheck__(self, subclass):
        """
        Is subclass a subclass of any of self.types?
        @type: subclass: type
        @rtype: bool
        """
        return any(
            issubclass(subclass, _type)
            for _type in self._types
        )


class Optional(Union):
    """
    `Optional[MyType]` is an alias of `Union[NoneType, MyType]`
    """
    def __init__(self, *_types):
        Union.__init__(self, tuple([types.NoneType]), *_types)


class Tuple(TypeLogic):
    """
    A tuple whose instances match the types passed into the constructor for Tuple.
    """
    def __instancecheck__(self, instance):
        """
        Element-by-element comparison for equal-length tuples; otherwise false.
        @type: instance: Any
        @rtype: bool
        """
        if isinstance(instance, tuple):
            if len(instance) == len(self.types):
                return all(
                    isinstance(element, _type)
                    for element, _type
                    in zip(instance, self.types)
                )
            else: # not same length
                return False
        else:  # not a tuple
            return False

    def __subclasscheck__(self, subclass):
        """
        @type: subclass: type
        @rtype: bool
        """
        if issubclass(subclass, tuple):
            if len(subclass) == len(self.types):
                return all(
                    issubclass(element, _type)
                    for element, _type
                    in zip(subclass, self.types)
                )
            else: # not same length
                return False
        else:  # not a tuple
            return False


def _hasattr(C, attr):
    try:
        return any(attr in B.__dict__ for B in C.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(C, attr)
