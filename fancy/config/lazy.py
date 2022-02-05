from typing import TYPE_CHECKING, Callable, Any

from . import PlaceHolder

if TYPE_CHECKING:
    from . import BaseConfig


class Lazy(PlaceHolder):
    readonly: bool = True

    def __init__(self, fn: Callable[['BaseConfig'], Any], name: str = None, description: str = None):
        super().__init__(name, description)
        self.fn = fn

    def __get__(self, instance: 'BaseConfig', owner):
        if instance is None:
            return self

        if not self.is_assigned(instance):
            vars(instance)[self.__name__] = self.fn(instance)
        return vars(instance)[self.__name__]
