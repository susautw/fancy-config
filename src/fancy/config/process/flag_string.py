from typing import Any

from . import boolean


def flag_string(value: str) -> Any:
    """
    Process a string value that may contain type information.
    
    This function allows type conversion from string representations using a special
    syntax. If the string starts with '!', it is parsed as a type conversion request.
    
    Format: !type_name:real_value
    
    Examples:
      - "regular string" -> unchanged
      - "!int:42" -> 42 (as int)
      - "!bool:true" -> True (using boolean converter)
    
    :param value: The value to process
    :return: The original value if not a flagged string, otherwise the converted value
    :raises TypeError: If the specified type name is not a valid type
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
