from copy import deepcopy
from typing import TypeVar, MutableMapping, MutableSequence

from . import flag_string

T = TypeVar("T", MutableMapping, MutableSequence)


def flag_container(container: T) -> T:
    if not isinstance(container, (MutableMapping, MutableSequence)):
        raise TypeError("the container must be a MutableMapping or MutableSequence")
    result = deepcopy(container)
    opening = [result]

    while len(opening) > 0:
        container = opening.pop()
        if isinstance(container, MutableMapping):
            keys = container.keys()
        else:
            keys = range(len(container))

        for k in keys:
            if isinstance(container[k], (MutableMapping, MutableSequence)):
                opening.append(container[k])
            else:
                container[k] = flag_string(container[k])
    return result
