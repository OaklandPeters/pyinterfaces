"""
Provides example of how I would like `enum` to be used.

Implementation details:
(1) Uses Metaclass for two reasons:
    (1.1) So that the subclasses can be iterable (we want class objects, not instance objects)
    (1.2) To automatically collect Enumeratee


enum.Enumerator
    EnumSet, Partition, Basis
    Product of all possibilities...
    An alternative term, mathematically correct, but misleading, would be 'Partition'
    Another alternative term: Basis (as of, group of independent vectors). Note, a basis is a 'linearly independent spanning set'.
enum.Enumeratee
    EnumCase, Dimension



@todo: Handle issue: How are the cases ordered?
    In Python 3, there is a mechanism for preserving the order of metaclasses.
        (see https://www.python.org/dev/peps/pep-3115/)

"""

import ENUM_STUBS as enum


class Beatles(enum.Enumerator):

    John = enum.Enumeratee("John Lennon")
    Paul = enum.Enumeratee("Paul McCartney")
    George = enum.Enumeratee("George Harrison")
    Ringo = enum.Enumeratee("Ringo Starr")

    @classmethod
    def __iter__(cls):
        """__iter__ provides the order cases are returned, while
        cls.cases does not.
        """
        # Return in alphabetic order, based on attribute name
        for name, case in sorted(cls.cases, key=lambda name, case: name):
            yield name, case

# Cases in Enumerator: Directly referencable via attribute name
str(Beatles.John) == "John Lennon"

# Cases: equality based on descriptor's return
Beatles.John == "John Lennon"
Beatles.Paul == "Paul McCartney"
Beatles.George == "George Harrison"
Beatles.Ringo == "Ringo Starr"


# Iterable: returns cases
iterator = iter(Beatles)
iterator.next() == Beatles.John
iterator.next() == Beatles.George
iterator.next() == Beatles.Paul
iterator.next() == Beatles.Ringo

# Cases: returns case methods with names
# ... no particular order imposed here
("John", Beatles.John) 
Beatles.cases == (("John", "John Lennon"))
