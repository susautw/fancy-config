"""
Factory for creating configuration objects dynamically by name.

This module provides a factory class for creating configuration objects from their
class names, with support for automatic suffix matching.
"""

from typing import Dict, Type, TYPE_CHECKING

from . import BaseConfig, utils
from .exc import ClassNotFoundException


if TYPE_CHECKING:
    from . import BaseConfigLoader


# TODO: As mentioned in `ConfigLoaderFactory`, we can simplify the logic for suffix matching
# TODO: Consider to remove loader parameter from create_config method since the config instance
#       can be created without it and the loader can be set later.


class ConfigFactory:
    """
    Factory for dynamically creating configuration objects by name.
    
    This class provides functionality to instantiate configuration objects
    from their class names, with automatic handling of naming conventions.
    It automatically discovers all subclasses of BaseConfig and can create
    instances by name with flexible matching of class names.
    """
    
    configs = None
    suffix: str = "Config"

    @classmethod
    def create_config(cls, config: str, loader: 'BaseConfigLoader') -> 'BaseConfig':
        """
        Create a configuration object by name.
        
        This method creates an instance of a configuration class based on
        its name. It supports several naming formats:
        - Exact class name
        - Class name without suffix (suffix is appended)
        - Class name without suffix and with lowercase first letter
          (first letter is capitalized and suffix is appended)
        
        :param config: The name of the configuration class to instantiate
        :param loader: The configuration loader to use for initialization
        :return: An instance of the specified configuration class
        :raises ClassNotFoundException: If no matching configuration class is found
        """
        configs = cls._get_all_configs()
        if config + cls.suffix in configs:
            config += cls.suffix
        elif config[0].capitalize() + config[1:] + cls.suffix in configs:
            config = config[0].capitalize() + config[1:] + cls.suffix
        elif config not in configs:
            raise ClassNotFoundException(config)
        return configs[config](loader)

    @classmethod
    def _get_all_configs(cls) -> Dict[str, Type['BaseConfig']]:
        """
        Get all available configuration classes.
        
        This method discovers and caches all subclasses of BaseConfig,
        making them available for instantiation by name.
        
        :return: A dictionary mapping class names to configuration classes
        """
        if cls.configs is None:
            cls.configs = {config.__name__: config for config in utils.reflections.find_subclasses(BaseConfig)}
        return cls.configs

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
