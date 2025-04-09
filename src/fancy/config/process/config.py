from typing import Type, Callable, TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from .. import BaseConfig

T = TypeVar("T", bound="BaseConfig")


def config(config_type: Type[T]) -> Callable[[Any], T]:
    from .. import BaseConfig

    if not issubclass(config_type, BaseConfig):
        raise TypeError(f"config type {config_type} must be instance of BaseConfig")

    def _inner(val: Any) -> T:
        if isinstance(val, config_type):
            return val
        return config_type()

    return _inner
