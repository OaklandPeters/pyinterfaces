"""
Classes inheriting from ValueABC should be used for type hinting,
annotations, and sometimes type-checking.

IE Functional-language type-checking, not OOP-style type checking
Somewhat similar to the way that types are used in more functional languages.

Pythonicaly, when used as a type-annotation in a docstring annotation, the class implied
should bear the right methods (~as an interface), but it can ALSO be used as part of:
    isinstance(obj, value_interface)
... to confirm that the value is correct.

Pythonically, what it DOES NOT do:
Check the value when you create it. Value/type checking must be done explictly.

@todo: Consider removing ValueABC
@todo: Consider removing the instances contained here (ExistingFile, ExistingDirectory, PositiveInteger) - to their own files
@todo: Determine: Will ValueABC.__instancecheck__ classmethod will disrupt the ValueMeta.__instancecheck__ ?
"""
import abc
import os

class ValueMeta(abc.ABCMeta):
    """
    Classes inheriting from ValueABC should be used for type hinting,
    annotations, and sometimes type-checking.

    IE Functional-language type-checking, not OOP-style type checking
    Somewhat similar to the way that types are used in more functional languages.

    Pythonicaly, when used as a type-annotation in a docstring annotation, the class implied
    should bear the right methods (~as an interface), but it can ALSO be used as part of:
        isinstance(obj, value_interface)
    ... to confirm that the value is correct.

    Pythonically, what it DOES NOT do:
    Check the value when you create it. Value/type checking must be done explictly.

    @todo: Determine: Will ValueABC.__instancecheck__ classmethod will disrupt the ValueMeta.__instancecheck__ ?
    """

    def __instancecheck__(cls, instance):

        print()
        print(cls.__instancecheck__, ValueMeta.__instancecheck__)
        print(cls.__instancecheck__ == ValueMeta.__instancecheck__)
        print(cls.__dict__['__instancecheck__'], ValueMeta.__dict__['__instancecheck__'])
        import pdb
        pdb.set_trace()
        print()

        if hasattr(cls, '__instancecheck__'):
            #if (cls.__instancecheck__ == ValueMeta.__instancecheck__):
            return cls.__instancecheck__(instance)
        else:
            return abc.ABCMeta.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if hasattr(cls, '__subclasscheck__'):
            return cls.__subclasscheck__(subclass)
        else:
            return abc.ABCMeta.__subclasscheck__(cls, subclass)

    # ! INTENT is...
    # This should be method on the class descendants of value-interface,
    # ... but not appear on the instances of that class
    def _assert(cls, instance, **keywords):

        # Chain: keyword, cls attribute, default
        exc_type = keywords.get('exception',
            default=getattr(cls, 'exception',
                default=ValueABCAssertionError)) #

        getattr(cls, 'exception')
        if not isinstance(instance, cls):
            exc_type = getattr(cls, 'exception', default=ValueABCAssertionError)
            raise exc_type(str.format(
                "Invalid"
            ))


class abstractclassmethod(classmethod):

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


class ValueABCException(Exception):
    pass


class ValueABCAssertionError(ValueABCException, AssertionError):
    pass


class ValueABC(object):
    """
    Classes inheriting from ValueABC should be used for type hinting,
    annotations, and sometimes type-checking.

    IE Functional-language type-checking, not OOP-style type checking
    Somewhat similar to the way that types are used in more functional languages.

    Pythonicaly, when used as a type-annotation in a docstring annotation, the class implied
    should bear the right methods (~as an interface), but it can ALSO be used as part of:
        isinstance(obj, value_interface)
    ... to confirm that the value is correct.

    Pythonically, what it DOES NOT do:
    Check the value when you create it. Value/type checking must be done explictly.

    @todo: Determine: Will ValueABC.__instancecheck__ classmethod will disrupt the ValueMeta.__instancecheck__ ?
    """
    __metaclass__ = ValueMeta

    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented



# Examples
class ExistingDirectory(str):
    __metaclass__ = ValueMeta

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, basestring):
            if os.path.isdir(instance):
                return True
        return False


class PositiveInteger(int):
    __metaclass__ = ValueMeta
    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, int):
            if instance > 0:
                return True
        return False

    def __new__(cls, *args, **kwargs):
        self = int(*args, **kwargs)
        if not isinstance(self, cls):
            raise
