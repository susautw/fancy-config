from typing import Callable

from . import boolean, config, config_list
from ..typing import UnProcType


def auto_process_typ(typ: UnProcType) -> Callable:
    from .. import BaseConfig  # lazy import
    if isinstance(typ, list):  # https://github.com/susautw/fancy-config/issues/4
        return config_list(typ[0])
    if isinstance(typ, type):
        if issubclass(typ, bool):
            return boolean
        if issubclass(typ, BaseConfig):
            return config(typ)
    if isinstance(typ, Callable):
        return typ
    else:
        raise ValueError("_type must be Callable or subclass of BaseConfig")
