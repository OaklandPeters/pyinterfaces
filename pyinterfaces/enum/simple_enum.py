"""
Creates Enumerator style data types, supporting pattern-matching.

Desire: 

HOSTS = Enumerant()
HOSTS.THEATLANTIC = RegexCase('github.com/theatlantic')
HOSTS.PYPI = RegexCase('pypi.python.org')
HOSTS.default = RegexCase('*')


@todo: Make .default a setable property
@todo: Add to EnumerantInterface: default = abc.abstractproperty()
@todo:

@todo: Rebuild this to be as close to a Mapping as possible. HOWEVER __iter__ should return values, not keys
@todo: SequencedEnumerant - which has a '_order_' method specifying order to check/iter non-fallback cases.
@todo: Make __eq__ magic method for cases. Think about inheritance, etc
@todo: Add capabilities to Enumerant to (optionally) set subtype/validity checking for Cases it accepts (_casecheck_ method)


"""
import abc
import re

from . import iterclass
from . import classproperty
from ..valueabc import InterfaceType # ~ ABCMeta + __instancecheck__

__all__ = [
    'CaseInterface',
    'RegexCase',
    'EnumerantInterface',
    'Enumerant',
    'EnumerantException',
    'EnumerantMatchError'
]

# Convenience function for abstractmethods
_NOT_IMPLEMENTED = lambda self, *args, **kwargs: NotImplemented


def caseproperty(obj):
    setattr(obj, '_iscase_', True)
    return obj

class CaseInterface(InterfaceType):
    __init__ = abc.abstractmethod(_NOT_IMPLEMENTED)
    __contains__ = abc.abstractmethod(_NOT_IMPLEMENTED)
    _iscase_ = True


class Case(CaseInterface):
    """
    Cases taking an arbitary function, which should be a predicate
    (ie. using PEP-0484 syntax: Callable[[Any], bool])
    """
    def __init__(self, predicate):
        self.predicate = predicate

    @property
    def predicate(self):
        """
        @rtype: Callable[[Any], bool]
        """
        if not hasattr(self, '_predicate'):
            self._predicate = None
        return self._predicate

    @predicate.setter
    def predicate(self, value):
        """
        @type: Callable[[Any], bool]
        @raises: TypeError
        """
        if not callable(predicate):
            raise TypeError(str.format(
                "argument to {0} must be callable.",
                type(self).__name__
            ))
        self._predicate = value

    @predicate.deleter
    def predicate(self):
        del self._predicate

    def __contains__(self, value):
        """
        Applies predicate function to value.
        Wraps result in `bool` to ensure results are boolean.
        @type: value: Any
        @rtype: bool
        """
        return bool(self.predicate(value))


class RegexCase(CaseInterface):
    def __init__(self, pattern):
        self.pattern = pattern
    def __contains__(self, _string):
        return bool(re.search(self.pattern, _string))
    def __repr__(self):
        return str.format(
            "<{name}: {pattern}>",
            name=type(self).__name__, pattern=self.pattern
        )
    def __eq__(self, other):
        return self.pattern == getattr(other, 'pattern', False)


class EnumerantInterface(InterfaceType):
    __iter__ = abc.abstractmethod(_NOT_IMPLEMENTED)
    matches = abc.abstractmethod(_NOT_IMPLEMENTED)
    cases = abc.abstractmethod(_NOT_IMPLEMENTED)
    default = abc.abstractmethod(_NOT_IMPLEMENTED)
    def matches(self, obj):
        """
        All cases which matches object.
        Only returns fallback cases if no standard
        cases were matched.
        @type: obj: Any
        @rtype: iter of (CaseInterface or None)
        """
        matched = False
        for case in self.cases:
            if obj in case:
                matched = True
                yield case

        # Fallbacks - if no regular cases matched
        if not matched:
            if self.default:
                yield self.default

        raise EnumerantMatchError(str.format(
            "Could not find a match in Enumerant of type '{0}'.",
            type(self).__name__
        ))

    def match(self, obj):
        """
        Returns first matching case.
        @type: obj: Any
        @type: CaseInterface or None
        """
        return _first(self.matches(obj))


class Enumerant(EnumerantInterface):
    """
    Best practice is to make all case values in capitals,
    to prevent overriding important methods.
    """

    def __iter__(self):
        """
        Yields all case attributes, with fallback cases
        coming last.
        @rtype: iter of CaseInterface
        """
        for case in _nonfallback_cases(self):
            yield case
        for case in _fallback_cases(self):
            yield case

    @property
    def default(self):
        """
        Return single default (fallback) case.
        @rtype: CaseInterface
        """
        #return _validate_fallback(self)
        if not hasattr(self, '_default'):
            self._default = None
        return self._default

    @default.setter
    def default(self, value):
        """

        """
        self._default = value

    @default.deleter
    def default(self):
        del self._default

    @property
    def cases(self):
        """
        Returns all non-default (fallback) cases.
        @rtype: dict[str, CaseInterface]
        """        
        return list(_nonfallback_cases(self))


# Local utility functions
class EnumerantException(Exception):
    pass

class EnumerantMatchError(EnumerantException, ValueError):
    pass

def _isfallback(name):
    return name.lower() == "fallback"

def _first(iterable):
    return iter(iterable).next()

def _case_attributes(obj):
    """
    All cases on this object - normal and fallback,
    in no specified order.
    @rtype: iter of (str, CaseInterface)
    """
    for name, attr in vars(obj).items():
        if isinstance(attr, CaseInterface):
            yield (name, attr)

def _nonfallback_cases(obj):
    """
    All non-fallback cases.
    @rtype: iter of CaseInterface
    """
    for name, attr in _case_attributes(obj):
        if not _isfallback(name):
            yield attr

def _fallback_cases(obj):
    """
    All fallback cases.
    @type: obj: Any
    @rtype: iter of CaseInterface
    """
    for name, attr in _case_attributes(obj):
        if _isfallback(name):
            yield attr

def _validate_fallback(obj):
    """
    Returns fallback. If multiple found - raises error.
    If no fallback found, returns None.
    @rtype: CaseInterface or None
    """
    fallbacks = list(_fallback_cases(obj))
    if len(fallbacks) == 0:
        return None
    elif len(fallbacks) == 1:
        return fallbacks[0]
    else: # len(fallbacks) > 1
        raise AttributeError(str.format(
            "Too many 'Fallback' cases specified."
        ))


