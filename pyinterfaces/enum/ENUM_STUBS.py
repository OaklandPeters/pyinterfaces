"""
Example of implementation detail for the desired functionality of enum.
This is the compliment to ENUM_USAGE.py


@todo: Provide interfaces for EnumeratorMetaInterface, EnumeratorInterface, EnumerateeInterface
@todo: Rebuild cls.cases as a class (inherit from Sequence)
@todo: Provide some mechanism to ensure that cls.cases is structured correctly (as (name, value))
    @todo: Have the cls.cases object confirm that the attribute also exists - if not, create it. (cls.cases.__setitem__) ... this is impossible in Python 2.
@todo: Allow this to handle ordered cases. Maybe via a subclass.
@todo: Ensure that post-class construction, changing a Enumeratee also changes the value inside cls.cases
"""
from . import iterclass
from . import basic_property

class EnumeratorMeta(iterclass.IterableClassMeta):
    """
    Responsible for several details.
    (1st) Making Enumerator an iterable class (__iter__ as classmethod)
    (2nd) Automatically registers all Enumeratee methods (~auto registration)
        This registration should include the names of the new methods.
    """
    def __new__(mcs, name, bases, namespace):
        """
        Auto register Enumeratee methods
        """
        cls = super(EnumeratorMeta, mcs).__new__(mcs, name, bases, namespace)

        # Ordered Iterable, supports __add__ (in lieu of append)
        # Cases an be directly mutated
        cls.cases = []

        # Register cases
        for name, value in iter_enumeratees(vars(cls)):
            cls.register(name, value)

        return cls

    def register(cls, name, value):
        """
        Adds a new case to the ordered list.
        """
        cls.cases = cls.cases + ((name, value), )


def iter_enumeratees(namespace):
    """
    Filter namespace for Enumeratee objects.
    @type: namespace: Mapping
    @rtype: Iterator[str, Any]
    """
    for name, value in namespace.items():
        if isinstance(value, Enumeratee):
            yield name, value



class DynamicEnumeratorMeta(type):
    """
    Complication: handling post-initialization addition of a new Enumeratee....
    """


class Enumerator(object):
    """

    Potential bug-case: Adding an Enumeratee directly to cases, but not
    adding it as an attribute.
    """
    __metaclass__ = EnumeratorMeta

    @classmethod
    def __iter__(cls):
        """
        Default iterator - generates ordering of cases.
        To get a particular ordering, override this method.
        """
        return iter(cls.cases)

    def __setattr__(self, name, value):
        """
        Handles case of assigning new Enumeratee, after initialization.
        """
        if isinstance(value, Enumeratee):
            self.register(name, value)
        # Invoke attribute setter of parent.
        # ... should this be object.__setattr__ ???
        EnumeratorMeta.__setattr__(self, name, value)


class Enumeratee(basic_property.BasicProperty):
    """
    Descriptor, similar to property
    """
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return (self.data == other)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str.format(
            "<{typename}: {data}>",
            typename=type(self).__name__,
            data=repr(self.data)
        )


def enumeratee(getter, setter=None, deleter=None, doc=None):
    """
    Similar to @property, this is a decorator returning a descriptor (Enumeratee)
    """
    return Enumeratee(getter, setter, deleter, doc)


def find_case_name(enumerator, value):
    """
    @todo: Have this have a more intelligent equality comparison.
        ... maybe EnumerateeInterface.__eq__(case, value)
    @assumption: name is unique
    """
    for name, case in enumerator.cases:
        if case == value:
            return case
