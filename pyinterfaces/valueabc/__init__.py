"""
Provides ValueMeta metaclass - which allows its descendants to override
__instancecheck__ and __subclasscheck__ to be used as *classmethods*
"""
from __future__ import absolute_import

__all__ = [
    'ValueMeta',
    'ValueABC',
    'InterfaceType',
    'ExistingDirectory',
    'ExistingFile'
]

from .existing_directory import ExistingDirectory
from .existing_file import ExistingFile
from .interface_type import InterfaceType
from .valueabc import ValueABC
from .valuemeta import ValueMeta
