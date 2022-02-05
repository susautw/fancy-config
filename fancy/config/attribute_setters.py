from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fancy.config import BaseConfig


class AttributeSetter(ABC):
    @abstractmethod
    def set(self, config: "BaseConfig", key: str, val: Any) -> None:
        pass

    @classmethod
    def get_setter_name(cls):
        raise NotImplementedError()


class StrictAttributeSetter(AttributeSetter):
    def set(self, config: "BaseConfig", key: str, val: Any) -> None:
        """
        :raise ValueError, TypeError
        """
        config[key] = val

    @classmethod
    def get_setter_name(cls):
        return "strict"


class IgnoreErrorAttributeSetter(AttributeSetter):
    """
    :raise ValueError, TypeError
    """

    def set(self, config: "BaseConfig", key: str, val: Any) -> None:
        try:
            config[key] = val
        except KeyError:
            pass

    @classmethod
    def get_setter_name(cls):
        return "ignore"
