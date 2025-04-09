from typing import TYPE_CHECKING, Callable, Any, Generic, NoReturn, Optional, TypeVar, overload

from .placeholder import PlaceHolder

if TYPE_CHECKING:
    from . import BaseConfig

GV = TypeVar("GV")

# TODO: typing using new syntax. use Never instead of Any
class Lazy(Generic[GV], PlaceHolder[GV]):
    """
    Represents a lazily computed value in configuration objects.
    
    Lazy extends PlaceHolder to add lazy (on-demand) computation of values. The value
    is computed only when first accessed and then cached for subsequent accesses.
    Lazy values are read-only by default.
    
    Example usage:
    ```python
    class MyConfig(BaseConfig):
        a = Option(type=int)
        b = Option(type=float)
        
        # Computed as a + b when first accessed
        sum_value = Lazy[float](lambda c: c.a + c.b)
        
        # Computed with a custom transformation
        formatted = Lazy[str](lambda c: f"The sum is {c.sum_value:.2f}")
    ```
    """
    readonly: bool = True

    def __init__(
        self,
        fn: Callable[[Any], GV],
        name: Optional[str] = None,
        description: Optional[str] = None,
        hidden: bool = False,
    ):
        """
        Initialize the lazy value with a function to compute it.
    
        :param fn: A function that computes the value when needed. Takes the config instance as its argument.
        :param name: Optional custom name for the lazy value (defaults to attribute name)
        :param description: Optional description of the lazy value
        :param hidden: Whether the lazy value should be hidden from to_dict output
        """
        super().__init__(name, description, hidden)
        self.fn = fn

    @overload
    def __get__(self, instance: "BaseConfig", owner) -> GV:
        ...
    @overload
    def __get__(self, instance: None, owner) -> "Lazy":  # TODO: Self
        ...
    def __get__(self, instance: Optional["BaseConfig"], owner):
        """
        Get the value of this lazy attribute.
        
        If accessed on a class, returns the Lazy object itself.
        If accessed on an instance:
        - If the value has already been computed, returns the cached value
        - Otherwise, computes the value using the provided function, caches it, and returns it
        
        :param instance: The instance on which the lazy value is accessed
        :param owner: The class that owns this lazy value
        :return: The computed value or the Lazy object itself
        """
        if instance is None:
            return self

        if not super().is_assigned(instance):
            vars(instance)[self.__name__] = self.fn(instance)
        return vars(instance)[self.__name__]

    def is_assigned(self, instance) -> bool:
        """
        Check if the lazy value is considered assigned.
        
        Lazy values are always considered assigned, as they can be computed on demand.
        
        :param instance: The instance to check
        :return: Always returns True
        """
        return True
