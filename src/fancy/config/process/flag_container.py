from copy import deepcopy
from typing import TypeVar, MutableMapping, MutableSequence

from . import flag_string

T = TypeVar("T", MutableMapping, MutableSequence)


def flag_container(container: T) -> T:
    """
    Process all string values in a container using flag_string.
    
    This function creates a deep copy of the container and processes each string 
    value within it using the flag_string processor. It works recursively on 
    nested containers (dictionaries and lists).
    
    :param container: A mutable mapping (like dict) or sequence (like list)
    :return: A new container with all string values processed
    :raises TypeError: If the container is not a MutableMapping or MutableSequence
    """
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
