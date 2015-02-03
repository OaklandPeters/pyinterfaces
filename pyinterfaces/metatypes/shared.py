"""
Functionality shared between modules, and local-utility funtions.
"""
import collections

import six

class TypeLogic(object):
    """
    Ancestor class, provides `types' property.
    """
    def __init__(self, *_types):
        self._types = None
        self.types = _types

    @property
    def types(self):
        """
        Property holding types in the union.
        @rtype: Tuple[*type]
        """
        if not hasattr(self, '_types'):
            self._types = tuple()
        return self._types

    @types.setter
    def types(self, value):
        """
        Validates assignments. Must be None, a type, or sequence of types.
        """
        if value is None:
            self._types = value
        elif _is_nonstring_sequence(value):
            if not all(isinstance(elm, type) for elm in value):
                raise TypeError("Sequence contains non-type elements.")
            else:
                self._types = tuple(value)
        elif isinstance(value, type):
            self._types = tuple([value])
        else:
            raise TypeError(str.format(
                "Must be None, a type, or a sequence of types; not {0}",
                type(value).__name__
            ))

    @types.deleter
    def types(self):
        """Delete self._types."""
        del self._types


def _is_nonstring_sequence(value):
    """Predicate. Is value an instance of a non-string sequence?"""
    return (
        isinstance(value, collections.Sequence)
        and not isinstance(value, six.string_types)
    )
