from typing import TYPE_CHECKING, Callable, Any, Generic, Optional, TypeVar, overload

from .placeholder import PlaceHolder

if TYPE_CHECKING:
    from . import BaseConfig

GV = TypeVar("GV")

# TODO: typing using new syntax. use Never instead of Any
class Lazy(Generic[GV], PlaceHolder[GV, Any]):
    readonly: bool = True

    def __init__(
        self,
        fn: Callable[["BaseConfig"], Any],
        name: Optional[str] = None,
        description: Optional[str] = None,
        hidden: bool = False,
    ):
        super().__init__(name, description, hidden)
        self.fn = fn

    @overload
    def __get__(self, instance: "BaseConfig", owner) -> GV:
        ...
    @overload
    def __get__(self, instance: None, owner) -> "Lazy":  # TODO: Self
        ...
    def __get__(self, instance: Optional["BaseConfig"], owner):
        if instance is None:
            return self

        if not super().is_assigned(instance):
            vars(instance)[self.__name__] = self.fn(instance)
        return vars(instance)[self.__name__]

    def is_assigned(self, instance) -> bool:
        return True
