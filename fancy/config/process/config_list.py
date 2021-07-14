from typing import TYPE_CHECKING, Callable, Type, Union


if TYPE_CHECKING:
    from .. import BaseConfig


def config_list(
        _type: Union[Type["BaseConfig"], Callable]) -> Callable:
    from .. import ConfigListStructure

    def _inner(_):
        return ConfigListStructure(_type)
    return _inner
