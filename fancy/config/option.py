from typing import Any, Callable, TYPE_CHECKING, Generic, Optional, TypeVar, Union, overload

from .placeholder import PlaceHolder
from .process import auto_process_typ, auto_process_value
from .typing import UnProcType
from ..config import identical

if TYPE_CHECKING:
    from ..config import BaseConfig

GV = TypeVar("GV")
SV = TypeVar("SV")
N = TypeVar("N")

class Option(Generic[GV, SV, N], PlaceHolder[Union[GV, N], Union[SV, N]]):
    raw_type: UnProcType
    _type: Callable[[Any], Any]
    _required: bool
    _nullable: bool
    _default: Any

    _description: str

    _config_name: Optional[str] = None
    readonly: bool = False

    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
            default=None,
            type: UnProcType = identical,
            name: Optional[str] = None,
            description: Optional[str] = None,
            hidden: bool = False
    ):
        super().__init__(name, description, hidden)
        self._required = required
        self._nullable = nullable

        # TODO resolve default value problem
        #  if type is a Config or ConfigList and "Option isn't required or nullable", the
        #  default value should assigned a empty dict or list in order to transfer control to sub configs
        #  ---
        #  the "transfer control" means that sub config decides what the default value
        #  or required value or nullable values
        self._default = default

        self.raw_type = type
        self._type = auto_process_typ(type)

    @overload
    def __get__(self, instance: "BaseConfig", owner) -> GV:
        ...
    @overload
    def __get__(self, instance: None, owner) -> "Option":  # TODO: Self
        ...
    def __get__(self, instance: Optional["BaseConfig"], owner):
        if instance is None:
            return self

        # initialize value
        if self._should_assign_default_value(instance):
            if self._default is None and not self._nullable:
                raise AttributeError(
                    f"attribute '{self.__name__}' of '{owner.__name__}' object must be assigned before accessing.")

            self.__set__(instance, self._default)

        return vars(instance)[self.__name__]

    def __set__(self, instance: "BaseConfig", raw_value: Union[SV, None]):
        # TODO Add Docs to explain how the None value works in this function
        if raw_value is None:
            if not self._nullable:
                raise ValueError('the value should not be none')
            value = None
        else:
            value = auto_process_value(raw_value, self._type, instance)

        vars(instance)[self.__name__] = value

    def __delete__(self, instance):
        del vars(instance)[self.__name__]

    def _should_assign_default_value(self, instance):
        return not super().is_assigned(instance)

    @property
    def required(self) -> bool:
        return self._required

    def is_assigned(self, instance) -> bool:
        return super().is_assigned(instance) or self._default is not None or self._nullable
