from typing import Type, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from .. import BaseConfig


def config(config_type: Type["BaseConfig"]) -> Callable:
    from .. import BaseConfig
    if not issubclass(config_type, BaseConfig):
        raise TypeError("config type must be instance of BaseConfig")

    def _inner(_: dict) -> config_type:
        return config_type(loader=None)
    return _inner
