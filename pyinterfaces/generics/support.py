

class GenericsException(Exception):
    """Base class for exceptions in generics package."""

class GenericsInterfaceFailed(GenericsException, TypeError):
    """When subject fails the interface of a generic function,
    and that generic has no callable 'default' to fall back to."""

class GenericsNoDispatch(GenericsException):
    """When no dispatch found."""


def get_name(obj):
    if hasattr(obj, '__name__'):
        name = obj.__name__
    else:
        name = type(obj).__name__ + " instance"

def get_abstracts(obj):
    return getattr(obj, '__abstractmethods__', [])
