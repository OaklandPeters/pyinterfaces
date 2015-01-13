import collections
import abc
import functools

import meets




import original_abcview
class Cast(object):
    def __init__(self, obj, interface):
        self.obj = obj
        self.interface = interface

    def __enter__(self):
        view = original_abcview.ABCView(self.interface)
        wrapped = view(self.obj)
        return wrapped
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass



class Surrogate(object):
    @abc.abstractproperty
    def AbstractParent(self):
        return NotImplemented

    def __init__(self, wrapped):
        """
        wrapped: the original 'concrete' object
        AbstractParent: abstract class providing being used as a
            kind of 'restricted' viewpoint (a "type restriction")
        """
        if not meets.meets(wrapped, self.AbstractParent):
            raise TypeError(str.format(
                "'wrapped' must be an instance of '{0}'.",
                self.AbstractParent
            ))
        if hasattr(wrapped, '_wrapped'):
            raise AttributeError("'wrapped' must not have a '_wrapped' method.")
        self._wrapped = wrapped

    def __getattr__(self, name):
        if name == '_wrapped':
            return getattr(self, '_wrapped')

        parent = self.AbstractParent
        parents_method = getattr(parent, name)

        # Not abstract on parent --> treat noramlly
        #   ... should fallback to abstract method
        if not meets.is_abstract_method(parents_method):
            return parents_method
        # Abstract on parent --> use wrapped's implementation
        else:
            #@functools.wraps(parents_method)
            def redirection(*args, **kwargs):
                self_method = getattr(self._wrapped, name)
                return self_method(self, *args, **kwargs)
            return redirection


    def __repr__(self):
        if hasattr(self._wrapped, '__repr__'):
            return self._wrapped.__repr__()
        else:
            return object.__repr__(self)
    def __str__(self):
        if hasattr(self._wrapped, '__str__'):
            return self._wrapped.__str__()
        else:
            return object.__str__(self)



class SequenceSurrogate(Surrogate):
    AbstractParent = collections.Sequence

class MutableSequenceSurrogate(collections.MutableSequence, Surrogate):
    AbstractParent = collections.MutableSequence




class ABCView(object):
    @abc.abstractproperty
    def AbstractParent(self):
        return NotImplemented

    def __init__(self, wrapped):
        """
        wrapped: the original 'concrete' object
        AbstractParent: abstract class providing being used as a
            kind of 'restricted' viewpoint (a "type restriction")
        """
        if not meets.meets(wrapped, self.AbstractParent):
            raise TypeError(str.format(
                "'wrapped' must be an instance of '{0}'.",
                self.AbstractParent
            ))
        if hasattr(wrapped, '_wrapped'):
            raise AttributeError("'wrapped' must not have a '_wrapped' method.")
        self._wrapped = wrapped
    def __repr__(self):
        if hasattr(self._wrapped, '__repr__'):
            return self._wrapped.__repr__()
        else:
            return object.__repr__(self)
    def __str__(self):
        if hasattr(self._wrapped, '__str__'):
            return self._wrapped.__str__()
        else:
            return object.__str__(self)

class SequenceView(ABCView, collections.Sequence):
    AbstractParent = collections.Sequence
    # Re-implement abstract methods - referencing self._wrapped
    def __getitem__(self, key):
        return self._wrapped.__getitem__(key)
    def __len__(self):
        return self._wrapped.__len__()
    def __contains__(self, element):
        return self._wrapped.__contains__(element)
    def __iter__(self):
        return self._wrapped.__iter__()

class MutableSequenceView(ABCView, collections.MutableSequence):
    AbstractParent = collections.MutableSequence
    # Re-implement abstract methods - referencing self._wrapped
    def __getitem__(self, key):
        return self._wrapped.__getitem__(key)
    def __len__(self):
        return self._wrapped.__len__()
    def __contains__(self, element):
        return self._wrapped.__contains__(element)
    def __iter__(self):
        return self._wrapped.__iter__()
    def __setitem__(self, key, value):
        return self._wrapped.__setitem__(key, value)
    def __delitem__(self, key):
        return self._wrapped.__delitem__(key)
    def insert(self, index, value):
        return self._wrapped.insert(index, value)








class OriginalSequenceView(collections.Sequence):
    def __init__(self, wrapped):
        if not isinstance(wrapped, collections.Sequence):
            raise TypeError("'wrapped' must be a 'Sequence'.")
        if hasattr(wrapped, '_wrapped'):
            raise AttributeError("'wrapped' must not have a '_wrapped' method.")
        self._wrapped = wrapped
    
    # Re-implement abstract methods - referencing self._wrapped
    def __getitem__(self, key):
        return self._wrapped.__getitem__(key)
    def __len__(self):
        return self._wrapped.__len__()
    def __contains__(self, element):
        return self._wrapped.__contains__(element)
    def __iter__(self):
        return self._wrapped.__iter__()



# def recast(surrogate):
#     """
#     class SequenceView(collections.Sequence):
#         __getitem__ = recast('__geitem__')
#         @recast
#         def __setitem__(self, key, value):
#             pass
#     """
#     if isinstance(surrogate, str):
#         name = surrogate
#     else:
#         name = surrogate.__name__
#         
#     def wrapper(self, *args, **kwargs):
#         method = getattr(self._wrapped, name)
#         return method(*args, **kwargs)
#     return wrapper

class OriginalMutableSequenceView(collections.MutableSequence):
    def __init__(self, wrapped):
        if not isinstance(wrapped, collections.MutableSequence):
            raise TypeError("'wrapped' must be a 'Sequence'.")
        if hasattr(wrapped, '_wrapped'):
            raise AttributeError("'wrapped' must not have a '_wrapped' method.")
        self._wrapped = wrapped


    # Re-implement abstract methods - referencing self._wrapped
    def __getitem__(self, key):
        return self._wrapped.__getitem__(key)
    def __len__(self):
        return self._wrapped.__len__()
    def __contains__(self, element):
        return self._wrapped.__contains__(element)
    def __iter__(self):
        return self._wrapped.__iter__()
    def __setitem__(self, key, value):
        return self._wrapped.__setitem__(key, value)
    def __delitem__(self, key):
        return self._wrapped.__delitem__(key)
    def insert(self, index, value):
        return self._wrapped.insert(index, value)

