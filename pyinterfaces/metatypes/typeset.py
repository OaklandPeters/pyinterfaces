"""
Used by Union

This is not a properly recursive data-structure.
So, it will probably NOT support Intersection/Not

@todo: Add flatten function
@todo: Make recursive version to support boolean set logic.
"""
import types
import collections

__all__ = [
    'TypeSet',
    'subclass_comparison'
]

class TypeLogicInterface(collections.MutableSet):
    __contains__
    __iter__
    __len__
    add
    remove

class TypeSet(collections.MutableSet):
    """
    Set-class, used by Union and Optional.
    Holds types, subject to set-theoretic operations.

    Will eventually be used by Intersection and Not.
    """
    def __init__(self, *data):
        self.data = set()
        for elm in data:
            self.add(elm)
    def __contains__(self, other):
        return other in self.data
    def __iter__(self):
        return iter(self.data)
    def __len__(self):
        return len(self)
    def add(self, value):
        self.data.add(validate_type(value))
    def remove(self, value):
        self.data.remove(value)
    #New Non-MutableSet specific methods
    def flatten(self):
        self.data = set(_simplify(self.data))

def subclass_comparison(_class, subclass):
    if not isinstance(_class, TypeSet):
        _class = TypeSet(_class)
    if not isinstance(subclass, TypeSet):
        subclass = TypeSet(subclass)
    return subclass <= _class



def simplify(typeset):
    """
    @type: typeset: TypeSet
    @rtype: TypeSet
    """
    return TypeSet(*_simplify(typeset))

def _simplify(typeset):
    """
    @type: typset: TypeSet
    @rtype: Iterator[type]
    """
    for _type in typeset:
        if isinstance(_type, TypeSet):
            for _inner_type in _simplify(typeset):  # yield from _simplify(typset)
                yield _inner_type
        else:
            yield _type

def validate_typeset(*_types):
    """
    @type: _types: Iterable[Any]
    @rtype: MutableSet[type]
    @raises: TypeError
    """
    return set(validate_type(_type) for _type in _types)

def validate_type(_type):
    """
    ...also turns None into NoneType
    @type: Any
    @rtype: type
    @raises: TypeError
    """
    if isinstance(_type, types.NoneType):
        return types.NoneType
    if not isinstance(_type, type):
        raise TypeError(str.format(
            "Object must be a type, not '{0}'",
            type(_type).__name__
        ))
    return _type
