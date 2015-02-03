"""
Interfaces and classes for GenericFunction.
Needs to be subclassed before being used.


@todo: Change GenericFunction to my enum thing

"""
import abc

from ..valueabc.interface_type import InterfaceType

from . import support

_NOT_IMPLEMENTED = lambda self, *args, **kwargs: NotImplemented

class GenericFunctionInterface(InterfaceType):
    """
    Operator (non-instanced, function-like class).

    In .invoke(): if no invocation was possible, and you want to attempt default,
        then raise GenericsNoDispatch
    """
    interface = abc.abstractproperty(_NOT_IMPLEMENTED)  # type: InterfaceType
    invoke = abc.abstractproperty(_NOT_IMPLEMENTED) # type: Callable[[AnyArgs], Any]
    #exception = abc.abstractproperty(_NOT_IMPLEMENTED)  # type: Exception
    #message = abc.abstractmethod(_NOT_IMPLEMENTED)  # type: Callable[[AnyArgs], Any]
    default = None # type: Optional[Callable[[AnyArgs], Any]]
    # Mixin
    def __call__(self, subject, *args, **kwargs):
        """
        Strategy function, when a generic function is called.


        Complication: two distinct error conditions are possible:
            (error #1): subject fails to meet interface
            (error #2): subject met interface, but invoke failed


        """
        if isinstance(subject, self.interface):
            # dispatch
            self.invoke(subject, *args, **kwargs)
        else: 
            # try default
            default = getattr(self, 'default', None)
            if callable(default):
                return default(subject, *args, **kwargs)
            else:
                raise support.GenericsInterfaceFailed(str.format(
                    "'subject' does not satisfy generics interface "
                    "'{interface_name}', and no default exists.",
                    interface_name=support.get_name(self.interface)
                ))


class GenericFunction(GenericFunctionInterface):
    def __call__(self, subject, *args, **kwargs):
        """
        Complication: two distinct error conditions are possible:
        # (error #1): subject fails to meet interface
        # (error #2): subject met interface, but invoke failed
        """
        default = getattr(self, 'default', None)


        print()
        print("subject:", type(subject), subject)
        print("self.interface:", type(self.interface), self.interface)
        print()
        import pdb
        pdb.set_trace()
        print()
        

        if not isinstance(subject, self.interface):
            if callable(default):
                return default(subject, *args, **kwargs)
            else:
                raise support.GenericsInterfaceFailed(str.format(
                    "'subject' does not satisfy generics interface "
                    "'{interface_name}', and no default exists.",
                    interface_name=support.get_name(self.interface)
                ))

        else:
            self.invoke(subject, *args, **kwargs)
