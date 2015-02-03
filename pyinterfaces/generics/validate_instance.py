"""

Support of generic functions.
Pairs several concepts

1. generic function
2. interface to the generic
3. method-dispatching


@todo: this has become a confusion of half formed code.




"""
import abc



class ValidatorInterface(InterfaceType):

    __abstractmethods__ =[
        '__instancecheck__',
        'message',
        'exception'
    ]

#    @classmethod
    @abc.abstractmethod
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


def validate(validator, obj, name="object"):
    """Generic function. Defers to validator.validate if it exists,
    else uses a default implementation based on it.

    Usage:
    validate(myvar, collections.Sequence, name="myvar")
    """
    if not isinstance(validator, Validator):
        raise TypeError("Not a validator.")

    if hasattr(validator, 'validate'):
        # Check to ensure that this hasn't looped back to this already
        return validator.validate(obj, name=name)

    # For Generic Function: this part would be the function proper
    if not validator.__instancecheck__(obj):
        raise validator.exception(
            validator.message(obj, name=name)
        )

    return obj








interface = abc.abstractproperty(_NOT_IMPLEMENTED)  # type: InterfaceType
invoke = abc.abstractproperty(_NOT_IMPLEMENTED) # type: Callable[[AnyArgs], Any]
exception = abc.abstractproperty(_NOT_IMPLEMENTED)  # type: Exception
message = abc.abstractmethod(_NOT_IMPLEMENTED)  # type: Callable[[AnyArgs], Any]
            






class AssertInterface(GenericFunctionInterface):
    pass

class Assert(GenericFunction):
    inter

class Validate():
    def __new__(cls, *args, **kwargs):
        
    def __call__(self, validator, obj, name="object"):
        if not isinstance(validator, Validator):
            raise TypeError("Not a validator")

        # dispatch/defer on object
        if hasattr(validator, 'validate'):
            return validator.validate(obj, name=name)

        # this part requires
        if not validator.__instancecheck__(obj):
            raise validator.exception()
