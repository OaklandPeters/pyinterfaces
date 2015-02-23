Refactoring
-------------
- Rename metatypes/ --> typelogic/
- setlogic/ replaced with the independent package: funkylogic/
- Rename ValueMeta/ValueABC --> TypeCheckable and TypeCheckable
    - Will require changing imports from sibling packages (clswrap and metatype)

Functionality
--------------
- enum: Quick rebuild to follow usage templates in ENUM_USAGE.py and ENUM_STUBS.py
- metatypes: Logical portion implemented via funkylogic/
- metatypes: Allow Union to accept 'None', and validate it into NoneType.
- metatypes: Simplification inside Union: Union(single)-->single
- metatypes: Simplification inside Union: Union(A, Union(B, C))-->Union(A, B, C)


Packaging
-----------
- Decide if ABCView should actually be located inside ducktype.
- metatypes/ unittests: test inheritance
- metatypes/ unittests: different TypeUnion are recognized as distinct classes

Bugs
-----------
- Recursive loops occur when Union is used to instance/subclass check itself, and likely also when it is used on an inheritor (eg. isinstance(Union(NoneType, dict), Union))
