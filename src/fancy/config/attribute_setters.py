"""
Attribute setters for configuring how values are assigned to configuration objects.

This module defines different strategies for setting attribute values on configuration
objects. These strategies allow for flexible handling of configuration data, such as
strictly requiring all keys to be valid or ignoring invalid keys.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fancy.config import BaseConfig


class AttributeSetter(ABC):
    """
    Abstract base class for attribute setting strategies.
    
    Attribute setters define how configuration values are assigned to
    configuration objects. Different setters implement different policies
    for handling errors and unexpected keys.
    """
    
    @abstractmethod
    def set(self, config: "BaseConfig", key: str, val: Any) -> None:
        """
        Set a configuration value on a configuration object.
        
        :param config: The configuration object to modify
        :param key: The key/name of the value to set
        :param val: The value to set
        """

    @classmethod
    def get_setter_name(cls):
        """
        Get the name of this attribute setter.
        
        :return: The name of the setter
        :raises NotImplementedError: If not implemented by subclasses
        """
        raise NotImplementedError()


class StrictAttributeSetter(AttributeSetter):
    """
    Attribute setter that strictly requires all keys to be valid.
    
    This setter raises exceptions if any key is invalid or if there are
    type conversion errors.
    """
    
    def set(self, config: "BaseConfig", key: str, val: Any) -> None:
        """
        Set a configuration value, raising exceptions for any errors.
        
        :param config: The configuration object to modify
        :param key: The key/name of the value to set
        :param val: The value to set
        :raises ValueError: If there is a value error during conversion
        :raises TypeError: If there is a type error during conversion
        :raises KeyError: If the key doesn't exist in the configuration
        """
        config[key] = val

    @classmethod
    def get_setter_name(cls):
        """
        Get the name of this attribute setter.
        
        :return: "strict"
        """
        return "strict"


class IgnoreErrorAttributeSetter(AttributeSetter):
    """
    Attribute setter that ignores invalid keys.
    
    This setter silently skips keys that don't exist in the configuration,
    but still raises exceptions for type conversion errors.
    """
    
    def set(self, config: "BaseConfig", key: str, val: Any) -> None:
        """
        Set a configuration value, ignoring KeyError exceptions.
        
        :param config: The configuration object to modify
        :param key: The key/name of the value to set
        :param val: The value to set
        :raises ValueError: If there is a value error during conversion
        :raises TypeError: If there is a type error during conversion
        """
        try:
            config[key] = val
        except KeyError:
            pass

    @classmethod
    def get_setter_name(cls):
        """
        Get the name of this attribute setter.
        
        :return: "ignore"
        """
        return "ignore"
