# class classproperty(property):
#     """Provides a getter-property for classmethods. Due to complicated reasons,
#     there is no way to make classmethod setter-properties work in Python
#     """
#     def __get__(self, cls, owner):
#         return self.fget.__get__(None, owner)()

class classproperty(object):
    def __init__(self, getter):
        self.getter = getter
    def __get__(self, instance, owner):
        return self.getter(owner)
