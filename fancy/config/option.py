import warnings
from typing import Any, Callable, Type, TYPE_CHECKING, Union

from .process import boolean, config
from ..config import identical

if TYPE_CHECKING:
    from ..config import BaseConfig


class Option:
    _type: Callable[[Any], Any]
    _required: bool
    _nullable: bool
    _default: Any

    _description: str
    _deleted_suffix: str = "__deleted"

    _config_name: str = None

    def __init__(
            self,
            required=False,
            nullable=False, default=None,
            type=identical,
            preprocess=identical,
            description="",
            name: str = None
    ):
        self._config_name = name
        self._required = required
        self._nullable = nullable
        self._default = default
        self._description = description

        if preprocess is not identical:
            warnings.warn("preprocess has deprecated. use type to instead.", DeprecationWarning)
            type = preprocess
        self._type = self._auto_type_process(type)

    def __get__(self, instance: 'BaseConfig', owner):
        if instance is None:
            return self

        # initialize value
        if self._should_assign_default_value(instance):
            if self._default is None and not self._nullable:
                raise AttributeError("attribute must assign the value before access it.")

            self.__set__(instance, self._default)

        return vars(instance)[self.__name__]

    def __set__(self, instance, value):
        if value is None:
            if not self._nullable:
                raise ValueError('the value should not be none')
        else:
            value = self._type(value)

        vars(instance)[self.__name__] = value

    def __delete__(self, instance):
        del vars(instance)[self.__name__]

    def __set_name__(self, owner, name):
        self.__name__ = name
        if self._config_name is None:
            self._config_name = name

    def is_assigned(self, instance) -> bool:
        return self.__name__ in vars(instance)

    def _should_assign_default_value(self, instance):
        return not self.is_assigned(instance)

    def _auto_type_process(self, typ: Union[Type, Callable]) -> Callable:
        from ..config import BaseConfig  # lazy import
        if isinstance(typ, type):
            if issubclass(typ, bool):
                return boolean
            if issubclass(typ, BaseConfig):
                return config(typ)
        return typ

    @property
    def name(self) -> str:
        return self._config_name

    @property
    def type(self) -> Type:
        return self._type

    @property
    def required(self) -> bool:
        return self._required

    @property
    def description(self) -> str:
        return self._description
