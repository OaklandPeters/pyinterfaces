"""
Example implementation of a GenericFunction


validate(Sequence, myvar, name="myvar")


class ExistingFile(Validator):
    ...

validate(ExistingFile, myvar, name="myvar")

"""
import abc

from ..ducktype import meets

from .generic_function import GenericFunction
from . import support


_NOT_IMPLEMENTED = lambda self, *args, **kwargs: NotImplemented




# interface = abc.abstractproperty(_NOT_IMPLEMENTED)  # type: InterfaceType
# invoke = abc.abstractproperty(_NOT_IMPLEMENTED) # type: Callable[[AnyArgs], Any]
# exception = abc.abstractproperty(_NOT_IMPLEMENTED)  # type: Exception
# message = abc.abstractmethod(_NOT_IMPLEMENTED)  # type: Callable[[AnyArgs], Any]


class GenericsValidatorTypeError(support.GenericsException, TypeError):
    pass


class ValidatorInterface(GenericFunction):
    @abc.abstractmethod
    def __instancecheck__(cls, instance):  # pylint: disable=no-self-argument
        return NotImplemented


class ValidatorType(ValidatorInterface):
    interface = ValidatorInterface
    exception = GenericsValidatorTypeError

    @classmethod
    def __instancecheck__(cls, instance):
        return meets.meets(instance, cls.interface)

    def message(self, subject, obj, name="object"):
        """
        Return message for exception.
        @type: subject: type
        @param: subject: An interface (such as collections.Sequence)
        @type: obj: Any
        @type: name: Optional[AnyStr]
        @rtype: str
        """
        return str.format(
            "{subject_name} does not meet the interface {interface_name}, "
            "which requires the methods: {methods}.",
            subject_name=name,
            interface_name=support.get_name(self.interface),
            methods=support.get_abstracts(self.interface)
        )

    def invoke(self, subject, obj, name="object"):
        if not isinstance(obj, subject):
            raise self.exception(self.message())
        

    def __init__(self):
        pass






Validate = ValidatorType()
