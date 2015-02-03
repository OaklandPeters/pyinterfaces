"""
This should be the authoritative location for duck-typing/structural
functionality, along with the related 'meets' functions - which do
structural checking based on abstract methods.

@todo: Determine if this is really the correct place for abcview.
@todo: Remove name confusion between ducktype (module) and duck_type (function).
"""

__all__ = [
    'ABCView',
    'Cast',
    'duck_type',
    'Interface',
    'meets',
]

from .abcview import ABCView, Cast
from .ducktype import duck_type, Interface
from .meets import meets

