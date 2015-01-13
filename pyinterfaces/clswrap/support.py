"""
@todo: Import ValueMeta from valueabc subpackage
"""
import abc

import meets

# Support functions
class ClsWrapException(Exception):
    """Base exception type for clswrap package."""
    pass

class InterfaceTypeError(ClsWrapException, TypeError):
    """Raised during wrapper instantiation, when a passed-in
    object fails to meet abstract interface."""
    pass



def _hasattr(C, attr):
    try:
        return any(attr in B.__dict__ for B in C.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(C, attr)

class ValueMeta(abc.ABCMeta):
    def __instancecheck__(cls, instance):
        if _hasattr(cls, '__instancecheck__'):
            #if (cls.__instancecheck__ == ValueMeta.__instancecheck__):
            return cls.__instancecheck__(instance)
        else:
            return abc.ABCMeta.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if _hasattr(cls, '__subclasscheck__'):
            return cls.__subclasscheck__(subclass)
        else:
            return abc.ABCMeta.__subclasscheck__(cls, subclass)

class AbstractInterface(object):
    """
    Abstract interface for abstract interfaces.
    ... How meta.

    NOTE: this needs ValueMeta, because ABCMeta introduced bugs
    when checking against classes eg.
    isinstance(list, AbstractInterface)
    """
    __metaclass__ = ValueMeta

    @abc.abstractproperty
    def __abstractmethods__(self):
        return NotImplemented

    @classmethod
    def __instancecheck__(cls, instance):
        if not isinstance(instance, type) and meets.meets(instance, cls):
            return True
        return False
    @classmethod
    def __subclasscheck__(cls, subclass):
        if isinstance(subclass, type) and meets.meets(subclass, cls):
            return True
        return False

def validate_instance(obj, _type, name="object", exception=TypeError):
    """
    @type: obj: Any
    @type: _type: type or Tuple[type]
    @type: name: str
    @type: exception: Exception
    @raises: Exception
    @rtype: Any
    """
    if not isinstance(obj, _type):
        raise exception(str.format(
            "{name} of type '{obj_type}' is not {valid}",
            name=name,
            obj_type=type(obj).__name__,
            valid=_type
        ))
    return obj


def validate_subclass(obj, _type, name="object", exception=TypeError):
    """
    @type: obj: Any
    @type: _type: type or Tuple[type]
    @type: name: str
    @type: exception: Exception
    @raises: Exception
    @rtype: Any
    """
    try:
        is_subclass = issubclass(obj, _type)
    except TypeError:
        # When obj is not a type - issubclass fails
        obj_type = getattr(obj, '__name__', "instance of " + type(obj).__name__)
        raise exception(str.format(
            "{name} is an instance of type '{obj_type}', and not {valid}",
            name=name,
            obj_type=obj_type,
            valid=_type
        ))

    if not is_subclass:
        obj_type = getattr(obj, '__name__', "instance of " + type(obj).__name__)
        raise exception(str.format(
            "{name} of type '{obj_type}' is not {valid}",
            name=name,
            obj_type=obj_type,
            valid=_type
        ))
    return obj
