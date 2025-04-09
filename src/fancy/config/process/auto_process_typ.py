from typing import Callable

from . import boolean, config, config_list
from ..typing import UnProcType


def auto_process_typ(typ: UnProcType) -> Callable:
    """
    Automatically select an appropriate processor for the given type.
    
    This function examines the provided type specification and returns
    an appropriate processor function:
    - For list types (like [int]), returns a config_list processor
    - For bool types, returns the boolean processor
    - For BaseConfig subclasses, returns a config processor
    - For other callable types, returns the callable itself
    
    :param typ: A type specification (type, list of types, or callable)
    :return: An appropriate processor function for the type
    :raises ValueError: If the type is not a recognized type specification
    """
    from .. import BaseConfig  # lazy import
    if isinstance(typ, list):  # https://github.com/susautw/fancy-config/issues/4
        return config_list(typ[0])
    if isinstance(typ, type):
        if issubclass(typ, bool):
            return boolean
        if issubclass(typ, BaseConfig):
            return config(typ)
    if callable(typ):
        return typ
    else:
        raise ValueError("typ must be callable or subclass of BaseConfig")
