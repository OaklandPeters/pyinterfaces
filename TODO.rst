Priority
-------------
- Rebuild this as small seperate repos, with requirements and versions combining them here.
    - pyinterfaces/ --> aggregation package, only really a requirements.txt to the small ones

Refactoring
-------------
- Consider replacing pyinterfaces/enum with the simpler funkyenum/ package.
    - Or possibly combine features from both. (/enum/s complexity comes from the 'matches' functionality -- which funkyenum/ does not have)
- Rename metatypes/ --> typelogic/
- setlogic/ removed: add funkylogic/ to the requirements.txt
- Rename typecheck/'s ValueMeta/ValueABC --> TypeCheckableMeta and TypeCheckable
    - Will require changing imports from sibling packages (clswrap and metatype)
- InterfaceType currently appears in both convenience/ and typecheck/ 

Functionality
--------------
- enum: Quick rebuild to follow usage templates in ENUM_USAGE.py and ENUM_STUBS.py
- metatypes: Logical portion implemented via funkylogic/
- metatypes: Allow Union to accept 'None', and validate it into NoneType.
- metatypes: Simplification inside Union:
    - Results in Union(A, Union(B, C))-->Union(A, B, C)
        - def flatten(iterable, recurse_on=Iterable) --> flatten(_a_union, recurse_on=Union)
    - Union(single) --> single
- Convenience ABCs: Atomic (-Iterable + str), NonAtomic, Record, Abstract 
- Fill in convenience/nonstring/ NonStringSequence & NonStringABCs
- Concretes: subpackage providing minimalist implementations of ABCs. ConcreteSequence, ConcreteSet, ConcreteMapping, ConcreteMutableMapping, ConcreteRecord, ConcreteMutableRecord
- convenience/record/ add dependency on itemize/ and import interfaces here.

Packaging
-----------
- Decide if ABCView should actually be located inside ducktype.
- metatypes/ unittests: test inheritance
- metatypes/ unittests: different TypeUnion are recognized as distinct classes

Bugs
-----------
- Recursive loops occur when Union is used to instance/subclass check itself, and likely also when it is used on an inheritor (eg. isinstance(Union(NoneType, dict), Union))
