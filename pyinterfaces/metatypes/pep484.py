"""

Self Note: ... I don't think this actually needs ValueMeta/ValueABC, because
it can just have Any/Union be instances

@todo: Decide if Tuple and tuple should have an 'virtual' (abc.register) relationship.
"""
import types

from .shared import TypeLogic

__all__ = [
    'Any',
    'Union',
    'Optional'
]

class AnyType(object):
    """
    Back port of typing.Any from PEP 483, into pyinterfaces/ 2.7 implementation.
    This version of `Any` differs in some major ways. For example, this version
    does not count as a subclass of all other classes, but the true PEP 483 version
    does.
        assert isinstance(typing.Any, SomeClass)
        assert not isinstance(metatypes.Any, SomeClass)
    """
    def __init__(self, *args, **kwargs):
        pass

    def __instancecheck__(self, instance):  # pylint: disable=unused-argument
        """
        @type: instance: Any
        @rtype: bool
        """
        return True

    def __subclasscheck__(self, subclass):  # pylint: disable=unused-argument
        """
        @type: subclass: type
        @rtype: bool
        """
        return True

# Instantiate Any
Any = AnyType()  # pylint: disable=invalid-name


class Union(TypeLogic):
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

