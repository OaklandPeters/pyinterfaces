"""


"""
import abc

from pyinterfaces.valueabc import valuemeta


class Validator(object):
    """Interface for type-validation."""
    __metaclass__ = valuemeta.ValueMeta

    __abstractmethods__ =[
        '__instancecheck__',
        'message',
        'exception'
    ]

    @classmethod
    def __instancecheck__(cls, instance):  # pylint: disable=E0213
        """
        This method is used two distinct ways.
        (1st) As abstract method required by classes meeting
            the Validator interface.
        (2nd) As function invoked during isinstance(obj, Validator)
        """

        print()
        print(cls, instance)
        print()
        import pdb
        pdb.set_trace()
        print()



    exception = abc.abstractproperty(TypeError)
    @abc.abstractmethod
    def message(self, obj, name="object"):
        abstracts = type(self).__abstractmethods__
        return str.format(
            "{obj_name} does not meet the interface {interface_name}, "
            "which requires the methods: {methods}.",
            obj_name=name,
            interface_name=get_name(self),
            methods=abstracts
        )

    message = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)



    def validate(self, obj, name="object"):
        """Mixin. Basic implementation."""
        if not self.__instancecheck__(obj):
            raise self.exception(
                self.message(obj, name=name)
            )
        return obj


def validate(obj, validator, name="object"):
    """Generic function. Defers to validator.validate if it exists,
    else uses a default implementation based on it."""
    if not isinstance(validator, Validator):
        raise TypeError("Not a validator.")

    if hasattr(validator, 'validate'):
        # Check to ensure that this hasn't looped back to this already
        return validator.validate(obj, name=name)

    if not validator.__instancecheck__(obj):
        raise validator.exception(
            validator.message(obj, name=name)
        )


def get_name(obj):
    if hasattr(obj, '__name__'):
        name = obj.__name__
    else:
        name = type(obj).__name__ + " instance"

