import warnings
from typing import Any, Callable, TYPE_CHECKING

from . import ConfigStructure
from .process import auto_process_typ
from ..config import identical

if TYPE_CHECKING:
    from ..config import BaseConfig


class Option:
    _type: Callable[[Any], Any]
    _required: bool
    _nullable: bool
    _default: Any

    _description: str

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
        self._type = auto_process_typ(type)

    def __get__(self, instance: 'BaseConfig', owner):
        if instance is None:
            return self

        # initialize value
        if self._should_assign_default_value(instance):
            if self._default is None and not self._nullable:
                raise AttributeError("attribute must assign the value before access it.")

            self.__set__(instance, self._default)

        return vars(instance)[self.__name__]

    def __set__(self, instance, raw_value):
        if raw_value is None:
            if not self._nullable:
                raise ValueError('the value should not be none')
            return None

        value = self._type(raw_value)
        if isinstance(value, ConfigStructure):
            value.load_by_context(instance, raw_value)

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

    @property
    def name(self) -> str:
        return self._config_name

    @property
    def required(self) -> bool:
        return self._required

    @property
    def description(self) -> str:
        return self._description
