from pathlib import Path
from typing import Any, TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..config import Option


def identity(val: Any, option: 'Option') -> Any:
    return val


def to_string(val: Any, option: 'Option') -> str:
    option.type = str
    return str(val)


def to_integer(val: Any, option: 'Option') -> int:
    option.type = int
    return int(val)


def to_float(val: Any, option: 'Option') -> float:
    option.type = float
    return float(val)


def to_bool(val: Any, option: 'Option') -> bool:
    option.type = bool
    return bool(val)


def to_path(val: Any, option: 'Option') -> Path:
    option.type = Path
    return Path(val)


def to_list(val: Any, option: 'Option') -> List:
    option.type = list
    return list(val)
