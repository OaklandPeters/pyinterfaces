"""
TypeInfo objects are those accepted by isinstance(obj, typeinfo).
It also bundles some convenience validation-related methods - which are
left over from the original use of this class. I may or may not remove them.

"""
from valuemeta import ValueMeta

class TypeInfo(object):
    """
    This is meant to be instanced - and checked from there.
    HOWEVER - I would like all of the methods to be callable as
    classmethods. ... this may require the use of one of the
    custom decorators.

    @todo: Remake as instanceable class, using ValueMeta.
    @todo: Unittests for this.
    """
    @classmethod
    def instancecheck(cls, typeinfo):
        """Is typeinfo valid for an isinstance call?
        IE a type, class, or tuple of types or classes?"""
        try:
            isinstance({}, typeinfo)
        except TypeError:
            return False
        return True
    @classmethod
    def names(cls, typeinfo):
        # Already assumes it is a valid typeinfo
        # assert(cls.instancecheck(typeinfo))
        if isinstance(typeinfo, tuple):
            return tuple([cls.names(klass) for klass in typeinfo])
        else:
            return getname(typeinfo)
    @classmethod
    def _ensure_types(cls, typeinfo):
        """If not already valid type or tuple of types, then
        gets type of object (or type of each object in tuple).
        """
        if isinstance(typeinfo, tuple):
            return tuple(cls._ensure_types(elm) for elm in typeinfo)
        else:
            if isinstance(typeinfo, type):
                return typeinfo
            else:
                return type(typeinfo)
    exception = TypeError
    @classmethod
    def message(cls, typeinfo, name="object"):
        # Assumes typeinfo is invalid
        # assert(not cls.instancecheck(typeinfo))
        types_names = cls.names(cls._ensure_types(typeinfo))
        return str.format(
            "'{name}' must be a class, type or tuple of "
            "classes and types, not {types_names}.",
            name=name, types_names=types_names
        )
    @classmethod
    def validate(cls, typeinfo, name="object"):
        if not cls.instancecheck(typeinfo):
            raise cls.exception(
                cls.message(typeinfo, name=name)
            )
        return typeinfo


def getname(obj):
    if hasattr(obj, '__name__'):
        name = obj.__name__
    else:
        name = type(obj).__name__ + " instance"
