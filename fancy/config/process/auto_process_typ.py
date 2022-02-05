from typing import Union, Type, Callable

from . import boolean, config


def auto_process_typ(typ: Union[Type, Callable]) -> Callable:
    from .. import BaseConfig  # lazy import
    if isinstance(typ, type):
        if issubclass(typ, bool):
            return boolean
        if issubclass(typ, BaseConfig):
            return config(typ)
    if isinstance(typ, Callable):
        return typ
    else:
        raise ValueError("_type must be Callable or subclass of BaseConfig")
