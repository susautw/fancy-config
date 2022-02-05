import types
from inspect import *


# noinspection PyShadowingBuiltins
def getmembers(object, predicate=None, *, sort=True):
    """Return all members of an object as (name, value) pairs sorted by name.
    Optionally, only return members that satisfy a given predicate."""
    if isclass(object):
        mro = (object,) + getmro(object)
    else:
        mro = ()
    results = []
    processed = set()
    names = dir(object) if sort else ordered_dir(object)
    # :dd any DynamicClassAttributes to the list of names if object is a class;
    # this may result in duplicate entries if, for example, a virtual
    # attribute with the same name as a DynamicClassAttribute exists
    try:
        for base in object.__bases__:
            for k, v in base.__dict__.items():
                if isinstance(v, types.DynamicClassAttribute):
                    names.append(k)
    except AttributeError:
        pass
    for key in names:
        # First try to get the value via getattr.  Some descriptors don't
        # like calling their __get__ (see bug #1785), so fall back to
        # looking in the __dict__.
        try:
            value = getattr(object, key)
            # handle the duplicate key
            if key in processed:
                raise AttributeError
        except AttributeError:
            for base in mro:
                if key in base.__dict__:
                    value = base.__dict__[key]
                    break
            else:
                # could be a (currently) missing slot member, or a buggy
                # __dir__; discard and move on
                continue
        if not predicate or predicate(value):
            results.append((key, value))
        processed.add(key)
    if sort:
        results.sort(key=lambda pair: pair[0])
    return results


def ordered_dir(obj):
    if not isclass(obj):
        obj = type(obj)

    result = {}

    for mro in reversed(getmro(obj)):
        result.update(mro.__dict__)

    return result.keys()
