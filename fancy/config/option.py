
from typing import Any, Callable, Type, TYPE_CHECKING, Set

from ..config import identity

if TYPE_CHECKING:
    from ..config import BaseConfig


class Option:
    _preprocess: Callable[[Any, 'Option'], Any]
    _required: bool
    _nullable: bool
    _default: Any
    _type: Type

    _deleted: Set[int]
    _assigned: Set[int]
    _name: str

    def __init__(self, required=False, nullable=False, default=None, option_type=object, preprocess=identity):
        self._required = required
        self._nullable = nullable
        self._type = option_type
        self._default = default
        self._preprocess = preprocess

        self._assigned = set()
        self._deleted = set()

    def __get__(self, instance: 'BaseConfig', owner):
        self._raise_if_deleted(instance)

        # initialize value
        if id(instance) not in self._assigned:
            if self._default is None and not self._nullable:
                raise AttributeError("attribute must assign the value before access it.")

            self.__set__(instance, self._default)

        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        self._raise_if_deleted(instance)
        if value is None:
            if not self._nullable:
                raise ValueError('the value should not be none')
        else:
            value = self._preprocess(value, self)

        self._raise_if_not_valid(value)
        instance.__dict__[self._name] = value
        self._assigned.add(id(instance))

    def __delete__(self, instance):
        self._deleted.add(id(instance))
        del instance.__dict__[self._name]

    def __set_name__(self, owner, name):
        self._name = '_' + name

    def _raise_if_not_valid(self, val: Any):
        if not self._is_valid(val):
            raise TypeError(
                f'\'{self._name}\' type mismatch, expect {self._type.__name__} but got {val.__class__.__name__}'
            )

    def _is_valid(self, val: Any) -> bool:
        return isinstance(val, self._type) or self._nullable and val is None

    def _raise_if_deleted(self, instance):
        if id(instance) in self._deleted:
            raise AttributeError(f'attribute {self._name[1:]} has been deleted')

    def preprocess(self, func):
        self._preprocess = func
        return self

    @property
    def name(self) -> str:
        return self._name[1:]

    @property
    def type(self) -> Type:
        return self._type

    @type.setter
    def type(self, val: Type):
        self._type = val

    @property
    def required(self) -> bool:
        return self._required
