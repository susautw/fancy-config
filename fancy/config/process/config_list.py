from typing import TYPE_CHECKING, Callable, List, Type

if TYPE_CHECKING:
    from .. import BaseConfig


def config_list(config_type: Type["BaseConfig"]) -> Callable:
    from .. import DictConfigLoader, BaseConfig
    if not issubclass(config_type, BaseConfig):
        raise TypeError("config type must be instance of BaseConfig")

    def _inner(config_dicts_list: List[dict]) -> List[config_type]:
        return [config_type(DictConfigLoader(config_dict)) for config_dict in config_dicts_list]

    return _inner
