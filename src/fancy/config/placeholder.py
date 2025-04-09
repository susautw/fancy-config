from typing import TYPE_CHECKING, Any, Generic, Optional, TypeVar, Union, overload

if TYPE_CHECKING:
    from fancy.config import BaseConfig

V = TypeVar("V")


# https://github.com/susautw/fancy-config/issues/3
class PlaceHolder(Generic[V]):
    """
    A descriptor for storing custom state in configuration objects.
    
    PlaceHolder provides a mechanism for storing and retrieving custom state
    in configuration objects. Unlike Option, PlaceHolder doesn't participate
    in automatic loading from configuration sources, making it suitable for
    computed or derived values.
    
    Example usage:
    ```python
    class MyConfig(BaseConfig):
        a = Option(type=int)
        computed: PlaceHolder[str] = PlaceHolder()
        
        def post_load(self):
            self.computed = f"Value: {self.a}"
    ```
    """
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
        """
        Initialize the placeholder with optional name and description.
    
        :param name: Optional custom name for the placeholder (defaults to attribute name)
        :param description: Optional description of the placeholder
        :param hidden: Whether the placeholder should be hidden from to_dict output
        """
        self._config_name = name
        self._description = "" if description is None else description
        self.hidden = hidden

    def __set_name__(self, owner, name):
        """
        Set the name of this placeholder when it's assigned as a class attribute.
        
        This is automatically called by Python when a descriptor is assigned to a class.
        
        :param owner: The class that owns this placeholder
        :param name: The attribute name of this placeholder
        """
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
        """
        Get the value of this placeholder.
        
        If accessed on a class, returns the placeholder itself.
        If accessed on an instance, returns the stored value.
        
        :param instance: The instance on which the placeholder is accessed
        :param owner: The class that owns this placeholder
        :return: The value of this placeholder or the placeholder itself
        :raises AttributeError: If the placeholder hasn't been assigned a value
        """
        if instance is None:
            return self

        try:
            return vars(instance)[self.__name__]
        except KeyError:
            raise AttributeError(
                f"attribute '{self.__name__}' of '{owner.__name__}' object must be assigned before accessing."
            )

    def __set__(self, instance: "BaseConfig", raw_value: Any):
        """
        Set the value of this placeholder.
        
        :param instance: The instance on which to set the value
        :param raw_value: The value to set
        :raises AttributeError: If the placeholder is read-only
        """
        if self.readonly:
            raise AttributeError(f"{self.name} can't be set")
        vars(instance)[self.__name__] = raw_value

    def __delete__(self, instance: "BaseConfig"):
        """
        Delete the value of this placeholder.
        
        This removes the placeholder from the instance's dictionary,
        making it appear unassigned again.
        
        :param instance: The instance from which to delete the value
        """
        vars(instance).pop(self.__name__, None)

    @property
    def name(self) -> str:
        """
        Get the configuration name of this placeholder.
        
        :return: The configuration name
        :raises AssertionError: If the placeholder isn't attached to a config
        """
        assert self._config_name is not None, (
            "placeholder does not attached to any config"
        )
        return self._config_name

    @property
    def description(self) -> str:
        """
        Get the description of this placeholder.
        
        :return: The description
        """
        return self._description

    def is_assigned(self, instance) -> bool:
        """
        Check if the placeholder can be accessed without raising an AttributeError.
        
        :param instance: The instance to check
        :return: True if the placeholder has been assigned a value, False otherwise
        """
        return self.__name__ in vars(instance)
