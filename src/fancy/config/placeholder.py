from typing import TYPE_CHECKING, Any, Generic, Optional, TypeVar, Union, overload

if TYPE_CHECKING:
    from fancy.config import BaseConfig

V = TypeVar("V")



# https://github.com/susautw/fancy-config/issues/3
class PlaceHolder(Generic[V]):
    _config_name: Optional[str]
    _description: str
    hidden: bool
    readonly: bool = False

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        hidden: bool = False,
    ):
        self._config_name = name
        self._description = "" if description is None else description
        self.hidden = hidden

    def __set_name__(self, owner, name):
        self.__name__ = name
        if self._config_name is None:
            self._config_name = name

    # TODO: typing using new syntax
    @overload
    def __get__(self, instance: "BaseConfig", owner) -> V:
        ...
    @overload
    def __get__(self, instance: None, owner) -> "PlaceHolder":
        ...
    def __get__(self, instance: Optional["BaseConfig"], owner) -> Union[V, "PlaceHolder"]:
        if instance is None:
            return self

        try:
            return vars(instance)[self.__name__]
        except KeyError:
            raise AttributeError(
                f"attribute '{self.__name__}' of '{owner.__name__}' object must be assigned before accessing."
            )

    def __set__(self, instance: "BaseConfig", raw_value: Any):
        if self.readonly:
            raise AttributeError(f"{self.name} can't be set")
        vars(instance)[self.__name__] = raw_value

    def __delete__(self, instance: "BaseConfig"):
        vars(instance).pop(self.__name__, None)

    @property
    def name(self) -> str:
        assert self._config_name is not None, (
            "placeholder does not attached to any config"
        )
        return self._config_name

    @property
    def description(self) -> str:
        return self._description

    def is_assigned(self, instance) -> bool:
        """
        :return true, if the placeholder is accessible.
        """
        return self.__name__ in vars(instance)
