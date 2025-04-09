from argparse import Namespace
from pathlib import Path
from typing import Dict, TYPE_CHECKING, Optional, Union

import yaml
from abc import ABC, abstractmethod

from . import attribute_setters

if TYPE_CHECKING:
    from ..config import BaseConfig

setter_name_map = {}

for name, x in vars(attribute_setters).items():
    if isinstance(x, type) and issubclass(x, attribute_setters.AttributeSetter):
        try:
            name = x.get_setter_name()
            setter_name_map[name] = x()
        except NotImplementedError:
            pass


SetterName = Union[str, attribute_setters.AttributeSetter]


class BaseConfigLoader(ABC):
    """
    Abstract base class for configuration loaders.
    
    Configuration loaders are responsible for loading data into configuration
    objects. They provide the bridge between configuration data sources and
    configuration objects.
    """
    _attribute_setter: attribute_setters.AttributeSetter

    def __init__(self, setter: Optional[SetterName] = None):
        """
        Initialize the loader with an optional attribute setter.

        :param setter: How to handle setting attributes (e.g., 'strict', 'ignore').
                    Can be a string name or an AttributeSetter instance.
        """
        setter = "strict" if setter is None else setter
        if isinstance(setter, str):
            self._attribute_setter = setter_name_map[setter]
        else:
            self._attribute_setter = setter

    @abstractmethod
    def load(self, config: "BaseConfig"):
        """
        Load configuration data into the given configuration object.
        
        :param config: The configuration object to load data into
        """
        ...

    @abstractmethod
    def get_sub_loader(self, val) -> "BaseConfigLoader":
        """
        Get a loader for a sub-configuration.
        
        This is used for loading nested configuration structures.
        
        :param val: The value to create a sub-loader for
        :return: A new loader instance for the sub-configuration
        """
        ...

    def get_setter(self) -> attribute_setters.AttributeSetter:
        """
        Get the attribute setter used by this loader.
        
        :return: The attribute setter instance
        """
        return self._attribute_setter


# TODO: consider to use `Mapping` instead of `Dict`
class DictBasedConfigLoader(BaseConfigLoader, ABC):
    """
    Abstract base class for dictionary-based configuration loaders.
    
    These loaders obtain configuration data as dictionaries, then load
    the dictionary data into configuration objects.
    """
    
    @abstractmethod
    def get_dict(self) -> Dict:
        """
        Get the dictionary containing configuration data.
        
        :return: The configuration data dictionary
        """
        pass

    def load(self, config: "BaseConfig"):
        """
        Load configuration data into the given configuration object.
        
        This implementation iterates through the dictionary from get_dict()
        and uses the attribute setter to set each value on the config object.
        
        :param config: The configuration object to load data into
        """
        for key, value in self.get_dict().items():
            self.get_setter().set(config, key, value)

    def get_sub_loader(self, val) -> "BaseConfigLoader":
        """
        Get a loader for a sub-configuration.
        
        :param val: The value to create a sub-loader for
        :return: A new DictConfigLoader for the sub-configuration
        """
        return DictConfigLoader(val, self._attribute_setter)


class PathBasedConfigLoader(BaseConfigLoader, ABC):
    """
    Abstract base class for file-based configuration loaders.
    
    These loaders obtain configuration data from files specified by paths.
    """
    _path: Path

    def __init__(
        self,
        path: Union[Path, str],
        setter: Optional[SetterName] = None,
    ):
        """
        Initialize the loader with a path and an optional attribute setter.
        
        :param path: The path to the configuration file
        :param setter: How to handle setting attributes
        """

        super().__init__(setter)
        self._path = path if isinstance(path, Path) else Path(path)

    @property
    def path(self) -> Path:
        """
        Get the path to the configuration file.
        
        :return: The path as a Path object
        """
        return self._path

    @path.setter
    def path(self, path: Path) -> None:
        """
        Set the path to the configuration file.
        
        :param path: The new path
        """
        self._path = path


class YamlConfigLoader(DictBasedConfigLoader, PathBasedConfigLoader):
    """
    Configuration loader that loads data from YAML files.
    
    This loader combines the capabilities of dictionary-based and path-based
    loaders to load configuration data from YAML files.
    """
    
    def get_dict(self) -> Dict:
        """
        Load and parse the YAML file, returning its contents as a dictionary.
        
        :return: The configuration data dictionary from the YAML file
        :raises FileNotFoundError: If the YAML file doesn't exist
        """
        if not self.path.is_file():
            raise FileNotFoundError(str(self.path))
        stream = self.path.open()
        data = yaml.safe_load(stream)

        if data is None:
            data = {}

        stream.close()
        return data


class DictConfigLoader(DictBasedConfigLoader):
    """
    Configuration loader that loads data from a Python dictionary.
    
    This is the simplest loader, taking a dictionary directly.
    """
    _dict: Dict

    def __init__(self, _dict: Dict, setter: Optional[SetterName] = None):
        """
        Initialize the loader with a dictionary and an optional attribute setter.
        
        :param _dict: The dictionary containing configuration data
        :param setter: How to handle setting attributes
        """
        super().__init__(setter)
        self._dict = _dict

    def get_dict(self) -> Dict:
        """
        Return the dictionary containing configuration data.
        
        :return: The configuration data dictionary
        """
        return self._dict


class NamespaceConfigLoader(DictBasedConfigLoader):
    """
    Configuration loader that loads data from an argparse Namespace object.
    
    This loader is useful for loading configuration from command-line arguments.
    """
    _args: Namespace

    def __init__(
        self,
        args: Namespace,
        setter: Optional[SetterName] = None,
    ):
        """
        Initialize the loader with an argparse Namespace and an optional attribute setter.
    
        :param args: The Namespace object containing configuration data
        :param setter: How to handle setting attributes
        """
        super().__init__(setter)
        self._args = args

    def get_dict(self) -> Dict:
        """
        Convert the Namespace to a dictionary containing configuration data.
        
        :return: The configuration data dictionary
        """
        return vars(self._args)
