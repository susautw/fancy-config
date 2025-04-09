from typing import Any


def identical(val: Any) -> Any:
    """
    Return the input value unchanged.
    
    This function serves as an identity function, useful as a default processor
    when no transformation is needed.
    
    :param val: Any value
    :return: The same value, unchanged
    """
    return val
