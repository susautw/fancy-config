from typing import TYPE_CHECKING, Callable, List, Type, Union, Any

from . import boolean

if TYPE_CHECKING:
    from .. import BaseConfig


def config_list(
        _type: Union[Type, Callable]) -> Callable:
    from .. import DictConfigLoader, BaseConfig

    is_class = isinstance(type(_type), type)
    if is_class and issubclass(_type, bool):
        def _inner(bool_list: List[Any]) -> List[bool]:
            return [boolean(item) for item in bool_list]
    elif is_class and issubclass(_type, BaseConfig):
        def _inner(config_dicts_list: List[dict]) -> List[_type]:
            return [_type(DictConfigLoader(config_dict)) for config_dict in config_dicts_list]
    elif isinstance(_type, Callable):
        def _inner(item_list: List[Any]) -> List[_type]:
            return [_type(item) for item in item_list]
    else:
        raise ValueError("_type must be Callable or subclass of BaseConfig")

    return _inner
