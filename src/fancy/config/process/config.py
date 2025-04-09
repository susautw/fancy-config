from typing import Type, Callable, TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from .. import BaseConfig

T = TypeVar("T", bound="BaseConfig")


def config(config_type: Type[T]) -> Callable[[Any], T]:
    """
    Create a function that returns instances of a specific config type.
    
    This factory function creates a processor that either returns the input
    if it's already the correct type (usually a loaded value), or creates a 
    new instance of the specified config type.
    
    :param config_type: The configuration class to create instances of
    :return: A function that returns instances of the specified config type
    :raises TypeError: If config_type is not a subclass of BaseConfig
    """
    from .. import BaseConfig

    if not issubclass(config_type, BaseConfig):
        raise TypeError(f"config type {config_type} must be instance of BaseConfig")

    def _inner(val: Any) -> T:
        if isinstance(val, config_type):
            return val
        return config_type()

    return _inner
