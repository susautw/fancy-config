from typing import Any

from . import boolean


def flag_string(value: str) -> Any:
    """
    any_string => skip
    !type_name:real_value => type_cls(value)
    :param value:
    :return:
    """
    if not isinstance(value, str):
        return value
    if value.startswith("!"):
        type_name, real_val = value[1:].split(":", maxsplit=1)
        cls = eval(type_name)
        if type(cls) is not type:
            raise TypeError(f"{type_name} is not a type")
        if cls is bool:
            return boolean(real_val)
        return cls(real_val)
    return value
