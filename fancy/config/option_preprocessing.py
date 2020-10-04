import warnings
from pathlib import Path
from typing import Any, List


def identical(val: Any) -> Any:
    return val


def to_string(val: Any) -> str:
    warnings.warn("to_string has deprecated.use str to instead.", DeprecationWarning)
    return str(val)


def to_integer(val: Any) -> int:
    warnings.warn("to_integer has deprecated.use int to instead.", DeprecationWarning)
    return int(val)


def to_float(val: Any) -> float:
    warnings.warn("to_float has deprecated.use float to instead.", DeprecationWarning)
    return float(val)


def to_bool(val: Any) -> bool:
    warnings.warn("to_bool has deprecated.use bool to instead.", DeprecationWarning)
    return bool(val)


def to_path(val: Any) -> Path:
    warnings.warn("to_path has deprecated.use path to instead.", DeprecationWarning)
    return path(val)


def path(val: Any) -> Path:
    return Path(val)


def to_list(val: Any) -> List:
    warnings.warn("to_list has deprecated.use list to instead.", DeprecationWarning)
    return list(val)
