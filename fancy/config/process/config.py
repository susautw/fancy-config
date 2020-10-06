from typing import Type, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from .. import BaseConfig


def config(config_type: Type["BaseConfig"]) -> Callable:
    from .. import DictConfigLoader

    def _inner(config_dict: dict) -> "BaseConfig":
        return config_type(DictConfigLoader(config_dict))  # lazy import to avoid circular import
    return _inner
