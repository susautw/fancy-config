from typing import Type, Callable, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .. import BaseConfig


def config(config_type: Type["BaseConfig"]) -> Callable:
    from .. import BaseConfig
    if not issubclass(config_type, BaseConfig):
        raise TypeError(f"config type {config_type} must be instance of BaseConfig")

    def _inner(val: Any) -> config_type:
        if isinstance(val, config_type):
            return val
        return config_type(loader=None)
    return _inner
