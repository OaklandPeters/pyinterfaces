"""
Exceptions used in setlogic package.
"""
__all__ = [
    'SetLogicException',
    'ValidationError',
]


class SetLogicException(Exception):
    """Base exception type for this pacakge."""
    pass


class ValidationError(TypeError, SetLogicException):
    """Used in validation."""
    pass
