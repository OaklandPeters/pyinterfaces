"""


"""
import abc

class Validator(object):
    __instancecheck__ = abc.abstractmethod()
    exception = abc.abstractproperty()
    message = abc.abstractmethod()
    def validate(self, obj, name="object"):
        if not self.__instancecheck__(obj):
            raise self.exception(
                self.message(obj, name=name)
            )
        return obj

def validate(obj, validator, name="object"):
    """Generic function"""
    if not isinstance(validator, Validator):
        raise TypeError("Not a validator.")

    if hasattr(validator, 'validate'):
        # Check to ensure that this hasn't looped back to this already
        return validator.validate(obj, name=name)

    if not validator.__instancecheck__(obj):
        raise validator.exception(
            validator.message(obj, name=name)
        )

