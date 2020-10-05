import warnings
from typing import Any, Callable, Type, TYPE_CHECKING

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

    def __init__(
            self,
            required=False,
            nullable=False, default=None,
            option_type=object,
            type=identical,
            preprocess=identical,
            description="",
            name: str = None
    ):
        self.__name__ = name
        self._required = required
        self._nullable = nullable
        self._type = option_type
        self._default = default
        self._description = description

        if preprocess is not identical:
            warnings.warn("preprocess has deprecated. use type to instead.", DeprecationWarning)
            type = preprocess
        self._type = type

    def __get__(self, instance: 'BaseConfig', owner):

        # initialize value
        if self._should_assign_default_value(instance):
            if self._default is None and not self._nullable:
                raise AttributeError("attribute must assign the value before access it.")

            self.__set__(instance, self._default)

        return vars(instance)[self.name]

    def __set__(self, instance, value):
        if value is None:
            if not self._nullable:
                raise ValueError('the value should not be none')
        else:
            value = self._type(value)

        vars(instance)[self.name] = value

    def __delete__(self, instance):
        del vars(instance)[self.name]

    def __set_name__(self, owner, name):
        if self.name is None:
            self.__name__ = name

    def _should_assign_default_value(self, instance):
        return self.name not in vars(instance)

    def preprocess(self, func):
        self._type = func
        return self

    @property
    def name(self) -> str:
        return self.__name__

    @property
    def type(self) -> Type:
        return self._type

    @property
    def required(self) -> bool:
        return self._required

    @property
    def description(self) -> str:
        return self._description
