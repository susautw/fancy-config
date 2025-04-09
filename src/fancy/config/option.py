from typing import Any, Callable, TYPE_CHECKING, Generic, Optional, TypeVar, Union, overload

from .placeholder import PlaceHolder
from .process import auto_process_typ, auto_process_value
from .typing import UnProcType
from ..config import identical

if TYPE_CHECKING:
    from ..config import BaseConfig

GV = TypeVar("GV")
SV = TypeVar("SV")
N = TypeVar("N")  # TODO: should bound to None or Never

class Option(Generic[GV, SV, N], PlaceHolder[Union[GV, N]]):
    """
    Represents a configuration option with validation, type conversion, and other features.
    
    Option extends PlaceHolder to add features specific to configuration options:
    - Type validation and conversion
    - Required/optional status
    - Nullability
    - Default values
    
    Example usage:
    ```python
    class MyConfig(BaseConfig):
        # A required integer option
        a = Option(type=int, required=True)
        
        # An optional string option with a default value
        b = Option(type=str, default="default text")
        
        # A nullable option that can be None or an integer
        c = Option(type=int, nullable=True)
        
        # A list of integers
        d = Option(type=[int])
    ```
    """
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
        """
        Represents a configuration option with validation, type conversion, and other features.

        :param required: Whether the option must be specified in the configuration data
        :param nullable: Whether the option can have a null (None) value
        :param default: Default value for the option if not specified in the configuration data
        :param type: Type specification for validation and conversion
        :param name: Optional custom name for the option (defaults to attribute name)
        :param description: Optional description of the option
        :param hidden: Whether the option should be hidden from to_dict output
        """
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
        """
        Get the value of this option.
        
        If accessed on a class, returns the option itself.
        If accessed on an instance and the option doesn't have a value yet:
        - If a default value exists, it will be assigned and returned
        - If nullable is True and no default value exists, None will be returned
        - Otherwise, raises an AttributeError
        
        :param instance: The instance on which the option is accessed
        :param owner: The class that owns this option
        :return: The value of this option or the option itself
        :raises AttributeError: If the option has no value and no default value
        """
        if instance is None:
            return self

        # initialize value
        if self._should_assign_default_value(instance):
            if self._default is None and not self._nullable:
                raise AttributeError(
                    f"attribute '{self.__name__}' of '{owner.__name__}' object must be assigned before accessing.")

            self.__set__(instance, self._default)

        return vars(instance)[self.__name__]

    def __set__(self, instance: "BaseConfig", raw_value: Optional[Union[SV, N]]):
        """
        Set the value of this option.
        
        This method handles type conversion and validation:
        - None values are only allowed if nullable=True
        - Non-None values are processed according to the type specification
        
        When raw_value is None:
        - If nullable=True, None is stored directly
        - If nullable=False, a ValueError is raised
        
        When raw_value is not None:
        - The value is processed using auto_process_value with the configured type
        
        :param instance: The instance on which to set the value
        :param raw_value: The value to set (before processing)
        :raises ValueError: If None is provided for a non-nullable option
        """
        # TODO Add Docs to explain how the None value works in this function
        if raw_value is None:
            if not self._nullable:
                raise ValueError('the value should not be none')
            value = None
        else:
            value = auto_process_value(raw_value, self._type, instance)

        vars(instance)[self.__name__] = value

    def __delete__(self, instance):
        """
        Delete the value of this option.
        
        This removes the option from the instance's dictionary,
        making it appear unassigned again.
        
        :param instance: The instance from which to delete the value
        """
        del vars(instance)[self.__name__]

    def _should_assign_default_value(self, instance):
        """
        Determine if a default value should be assigned.
        
        :param instance: The instance to check
        :return: True if a default value should be assigned, False otherwise
        """
        return not super().is_assigned(instance)

    @property
    def required(self) -> bool:
        """
        Check if this option is required.
        
        :return: True if the option is required, False otherwise
        """
        return self._required

    def is_assigned(self, instance) -> bool:
        """
        Check if the option has been assigned a value or has a default value.
        
        Unlike PlaceHolder.is_assigned, this method returns True if:
        - The option has been assigned a value in the instance
        - The option has a default value
        - The option is nullable (in which case None is the implicit default)
        
        :param instance: The instance to check
        :return: True if the option is considered assigned, False otherwise
        """
        return super().is_assigned(instance) or self._default is not None or self._nullable
