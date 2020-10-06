from copy import deepcopy
from typing import TypeVar

from . import flag_string

T = TypeVar("T", list, dict)


def flag_container(container: T) -> T:
    result = deepcopy(container)
    opening = [result]

    while len(opening) >= 0:
        container = opening.pop()
        for k in container:
            if isinstance(container[k], (list, dict)):
                opening.append(container[k])
            else:
                container[k] = flag_string(container[k])
    return result
