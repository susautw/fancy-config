"""
Factory for creating configuration loader objects dynamically by name.

This module provides a factory class for creating configuration loader objects from their
class names, with support for automatic suffix matching.
"""

from typing import Dict, Type

from .. import config as cfg
from fancy.config import utils, exc

# TODO: Instead of using complex logic about suffixes, we can use a simple class variable 
#       with registration of the class name. This will make it easier to understand and maintain.


class ConfigLoaderFactory:
    """
    Factory for dynamically creating configuration loader objects by name.
    
    This class provides functionality to instantiate configuration loader objects
    from their class names, with automatic handling of naming conventions.
    It automatically discovers all subclasses of BaseConfigLoader and can create
    instances by name with flexible matching of class names.
    """
    
    suffix: str = "ConfigLoader"
    loaders = None

    @classmethod
    def create_loader(cls, method: str = 'yaml') -> cfg.BaseConfigLoader:
        """
        Create a configuration loader object by name.
        
        This method creates an instance of a configuration loader class based on
        its name. It supports several naming formats:
        - Exact class name
        - Method name without suffix (suffix is appended)
        - Method name with lowercase first letter (first letter is capitalized and suffix is appended)
        
        :param method: The name of the configuration loader method/class to instantiate
        :return: An instance of the specified configuration loader class
        :raises exc.ClassNotFoundException: If no matching configuration loader class is found
        """
        loaders = cls.get_all_loaders()
        if method + cls.suffix in loaders:
            method += cls.suffix
        elif method.capitalize() + cls.suffix in loaders:
            method = method.capitalize() + cls.suffix
        elif method not in loaders:
            raise exc.ClassNotFoundException(method)
        return loaders[method]()

    @classmethod
    def get_all_loaders(cls) -> Dict[str, Type[cfg.BaseConfigLoader]]:
        """
        Get all available configuration loader classes.
        
        This method discovers and caches all subclasses of BaseConfigLoader,
        making them available for instantiation by name.
        
        :return: A dictionary mapping class names to configuration loader classes
        """
        if cls.loaders is None:
            cls.loaders = {
                loader.__name__: loader for loader in utils.reflections.find_subclasses(cfg.BaseConfigLoader)
            }
        return cls.loaders

    @classmethod
    def get_suffix(cls) -> str:
        """
        Get the current class name suffix.
        
        :return: The current suffix used for matching class names
        """
        return cls.suffix

    @classmethod
    def set_suffix(cls, suffix: str) -> None:
        """
        Set the class name suffix.
        
        :param suffix: The new suffix to use for matching class names
        """
        cls.suffix = suffix
