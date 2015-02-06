"""

@todo: add abstractmethod for __iter__
"""

class MetaTypeMetaClass(type):
    """
    Metaclass for generating TypeUnion classes.
    Classes implementing this must be Iterable
    """
    def __new__(mcls, name, bases, namespace):
        """
        @type: name: str
        @type: bases: Sequence[type]
        @type: namespace: dict[str, Any]
        """

        # Construct class - uses type.__new__
        cls = super(MetaTypeMetaClass, mcls).__new__(mcls, name, bases, namespace)

        return cls

    def __call__(cls, *args, **kwargs):
        """
        Triggered whenever the newly created class is "called"
        to instantiate a new object.

        (mcls.__init__ controls the initialization of the new class,
         NOT the initialization of the instances of the new class)
        """
        return cls.__new__(cls, *args, **kwargs)


    def __instancecheck__(cls, instance):  # pylint: disable=unused-argument
        """
        @type: instance: Any
        @rtype: bool
        """
        if _hasattr(cls, "__instancecheck__"):
            return cls.__instancecheck__(instance)
        return NotImplemented

    def __subclasscheck__(cls, subclass):  # pylint: disable=unused-argument
        """
        @type: subclass: type
        @rtype: bool
        """        
        if _hasattr(cls, "__subclasscheck__"):
            return cls.__subclasscheck__(subclass)
        return NotImplemented

    def __repr__(cls):
        """
        @type: cls: Iterable
        """
        return str.format(
            "<'{0}': {1}>",
            cls.__name__, repr(iter(cls))
        )
    # Abstract method -- currently not enforced via code
    __abstractmethods__ = set(['__iter__'])
    def __iter__(cls):
        pass
    __iter__.__isabstractmethod__ = True


def _hasattr(C, attr):
    try:
        return any(attr in B.__dict__ for B in C.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(C, attr)
