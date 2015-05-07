"""

A BaseClass inheriting from TypeCheckable, which defines
__instancecheck__ and __subclasscheck__ to check based
on abstractmethods and abstractproperties.

Similar to using ABCMeta and overriding __subclasshook__,
but allows __instancecheck__ access to the value of the instance.
"""
