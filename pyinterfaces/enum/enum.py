"""
TEMP MESSAGE: Version of enumerant, but which avoids need for metaclasses
by operating on instances.

"""
import abc
import re

__all__ = [
    'CaseInterface',
    'RegexCase',
    'EnumerantInterface',
    'Enumerant',
    'EnumerantException',
    'EnumerantMatchError'
]

class CaseInterface(object):
    __metaclass__ = abc.ABCMeta
    __abstractmethods__ = [
        '__init__',
        '__contains__'
    ]

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


class EnumerantInterface(iterclass.AbstractIterableClass):
    __abstractmethods__ = [
        '__iter__',
        'matches',
        'cases',
        'default'
    ]
    # Mixins
    @classmethod
    def matches(cls, obj):
        """
        All cases which matches object.
        Only returns fallback cases if no standard
        cases were matched.
        @type: obj: Any
        @rtype: iter of (CaseInterface or None)
        """
        matched = False
        for case in cls.cases:
            if obj in case:
                matched = True
                yield case

        # Fallbacks - if no regular cases matched
        if not matched:
            if cls.default:
                yield cls.default

        raise EnumerantMatchError(str.format(
            "Could not find a match in Enumerant '{0}'.",
            cls.__name__
        ))

    @classmethod
    def match(cls, obj):
        """
        Returns first matching case.
        @type: obj: Any
        @type: CaseInterface or None
        """
        return _first(cls.matches(obj))


class Enumerant(iterclass.IterableClass, EnumerantInterface):
    """
    Best practice is to make all case values in capitals,
    to prevent overriding important methods.
    """

    @classmethod
    def __iter__(cls):
        """
        Yields all case attributes, with fallback cases
        coming last.
        @rtype: iter of CaseInterface
        """
        for case in _nonfallback_cases(cls):
            yield case
        for case in _fallback_cases(cls):
            yield case



    @classproperty.classproperty
    def cases(cls): # pylint: disable=no-self-argument
        """
        Returns all non-default (fallback) cases.
        @rtype: iter of CaseInterface
        """
        return _nonfallback_cases(cls)

    @classproperty.classproperty
    def default(cls): # pylint: disable=no-self-argument
        """
        Return single default (fallback) case.
        @rtype: CaseInterface
        """
        return _validate_fallback(cls)

    @classmethod
    def todict(cls):  # pylint: disable=no-self-argument
        return dict(_case_attributes(cls))

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


