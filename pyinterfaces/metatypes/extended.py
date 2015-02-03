"""
Extended functionality not officially part of PEP 483/484 (at least not yet).
"""
from .shared import TypeLogic

__all__ = [
    'Intersection',
    'Not'
]

class Intersection(TypeLogic):
    """
    Currently mentioned as a possibility in PEP 483
    """
    def __init__(self, *_types):
        TypeLogic.__init__(*_types)

    def __instancecheck__(self, instance):
        return not any(
            isinstance(instance, _type)
            for _type in self.types
        )

    def __subclasscheck__(self, subclass):
        return not any(
            issubclass(subclass, _type)
            for _type in self.types
        )


class Not(TypeLogic):
    """
    Checks that instance does not match ANY element of self.types
    """
    def __init__(self, *_types):
        TypeLogic.__init__(*_types)

    def __instancecheck__(self, instance):
        return not any(
            isinstance(instance, _type)
            for _type in self.types
        )

    def __subclasscheck__(self, subclass):
        return not any(
            issubclass(subclass, _type)
            for _type in self.types
        )
