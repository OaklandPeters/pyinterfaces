"""
@todo: Make __obj a weakref.weakref(obj)
@todo: *Hard*: Make ABCView into a class
"""
import abc
import types

__all__ = [
    'ABCView',
    'Cast'
]

#    Essentially a TypeRestriction(), 'type promotion' in C-terms
def ABCView(interface, **extra_attributes):
    """Create class which is the intersection of 'obj', with
    the abstract methods and properties of 'interface'; then inherits
    from 'interface' -- receiving its Mixin methods.    
    
    
    >>> obj = [0,1,2]
    >>> SeqView = ABCView(Sequence)
    >>> seq     = SeqView(obj)
      
    #Confirm that it DOES NOT have non-Sequence methods from list
    #    Such as .append (which list has, but Sequence does not)
    >>> seq.append(3)
    Traceback (most recent call last):
    AttributeError: 'SequencePromotion' object has no attribute 'append'
    
    #Observe: Changes to mutable view change the original object
    >>> MSeqView = ABCView(MutableSequence)
    >>> mseq     = MSeqView(obj)
    >>> mseq.append(3)
    >>> mseq
    [0, 1, 2, 3]
    >>> obj
    [0, 1, 2, 3]
    """
    if not isinstance(interface, abc.ABCMeta):
        raise TypeError("'interface' must be an abstract class.")

    def init(self, obj):
        """Initialize ABCView object."""
        interface = self.__interface
        if not isinstance(obj, interface):
            raise TypeError(str.format(
                "'obj' does not meet {0}.",
                interface.__name__
            ))
        if isinstance(obj, type):
            raise TypeError("'obj' is not an instance.")
        self.__obj = obj
    redirector = lambda self: self.__obj

    new_attrs = {
        '__interface': interface,
        '__init__': init,
    }
    new_attrs.update(extra_attributes)


    for name in get_abstracts(interface):
        interface_attr = getattr(interface, name)
        if isinstance(interface_attr, types.MethodType):
            new_attrs[name] = binding_wrapper(name, redirector)
        #abstractproperty ...
        else:
            new_attrs[name] = property(lambda self: getattr(self.__obj, name))

    #Tentative: Add repr
    if hasattr(interface, '__repr__'):
        new_attrs['__repr__'] = binding_wrapper('__repr__', redirector)

    new_name = interface.__name__ + 'Promotion'
    #new_bases: will ensure that the new object inherits mixin methods from VOG
    new_bases = (interface, )
    new_cls = type(new_name, new_bases, new_attrs)
    return new_cls


class Cast(object):
    """
    Context manager.

    >>> sequence = list("mysubl")
    >>> with Cast(sequence, collections.MutableSequence) as mseq:
    >>>     print(mseq)
    ['m', 'y', 's', 'u', 'b', 'l']
    >>>     mseq.extend('ime')
    >>> print(sequence)
    ['m', 'y', 's', 'u', 'b', 'l', 'i', 'm', 'e']
    """
    # def __init__(self, obj, interface):
    #     self.obj = obj
    #     self.interface = interface

    # def __enter__(self):
    #     view = ABCView(self.interface)
    #     wrapped = view(self.obj)
    #     return wrapped
    # def __exit__(self, exc_type, exc_value, exc_traceback):
    #     pass
    def __new__(cls, obj, interface):
        view = ABCView(interface,
            __exit__=cls.__dict__['__exit__'],
            __enter__=cls.__dict__['__enter__']
        )
        self = view(obj)
        return self

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

#==============================================================================
#    Local Utility Functions
#==============================================================================
def binding_wrapper(name, redirector=None):
    """
    @binding_wrapper()
    """
    if redirector == None:
        redirector = lambda self: self
    assert(callable(redirector)), "Redirector not Callable."
        
    def wrapped(self,*args,**kwargs):
        #obj = self.__obj
        obj = redirector(self)
        attr = getattr(obj,name)
        return attr(*args,**kwargs)
    return wrapped
#    if wraps == None:
#        return wrapped
#    elif isinstance(wraps,Callable):
#        return functools.wraps(wraps)(wrapped)
#    else:
#        raise TypeError("Invalid 'wraps' of type: "+type(wraps).__name__)


def is_abstract(func):
    try:
        return func.__isabstractmethod__
    except AttributeError:
        return False
    
def get_abstracts(interface):
    """Where 'interface' is an abstract base class
    >>> 
    >>> get_abstracts(Sequence)
    ['__getitem__', '__len__']
    """
    return [
        name
        for name in dir(interface)
        if is_abstract(getattr(interface, name))
    ]




