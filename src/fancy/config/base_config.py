from abc import ABC
import typing
import warnings
from typing import Dict, List, overload, Any, Callable, Optional

from . import (
    ConfigStructure,
    ConfigContext,
    exc,
    PlaceHolder,
    ConfigStructureVisitor,
    DictConfigLoader,
    consts,
)
from . import Option
from .utils import inspect, Dispatcher, DispatcherError
from . import visitors
from ..config import BaseConfigLoader


class BaseConfig(ConfigStructure, ConfigContext, ABC):
    """
    Base configuration class that provides the core functionality for defining configuration structures.
    
    This class serves as the foundation for creating custom configuration classes.
    It implements mechanisms for loading, accessing, and converting configuration data.
    
    BaseConfig combines ConfigStructure and ConfigContext to provide a complete
    configuration management solution with support for hierarchical structures.
    
    Example usage:
    ```python
    class MyConfig(cfg.BaseConfig):
        a = cfg.Option(type=int, required=True)
        b = cfg.Option(type=str, default="default text")
        
        def post_load(self):
            # Custom processing after configuration loading
            pass
    
    config = MyConfig(a=1, b="custom text")
    ```
    """
    _name_mapping: Optional[Dict[str, str]] = None
    _all_placeholders: Optional[Dict[str, PlaceHolder]] = None
    _all_options: Optional[Dict[str, Option]] = None
    _all_required_options: Optional[List[Option]] = None
    _loader: Optional[BaseConfigLoader] = None

    _method_init_ = Dispatcher(is_method=True)

    @overload
    @_method_init_.register
    def __init__(self, loader: Optional[BaseConfigLoader] = None):
        """
        Initialize the configuration with a loader.
        
        :param loader: A configuration loader that loads data into this configuration
        """
        if loader is not None:
            if not isinstance(loader, BaseConfigLoader):
                raise DispatcherError("loader should be a BaseConfigLoader")
            self.load(loader)

    @overload
    @_method_init_.register
    def __init__(self, options: Dict[str, Any]):
        """
        Initialize the configuration with a dictionary of options.
        
        :param options: A dictionary containing configuration values
        """
        if not isinstance(options, dict):
            raise DispatcherError("options should be dict")
        self.__init__(DictConfigLoader(options))

    @overload
    @_method_init_.register
    def __init__(self, **options: Any):
        """
        Initialize the configuration with keyword arguments.
        
        :param options: Keyword arguments containing configuration values
        """
        if "loader" in options and len(options) == 1:
            raise DispatcherError("loader should be a BaseConfigLoader")
        self.__init__(options)

    # TODO: @final
    @_method_init_.implement
    def __init__(self, *args, **kwargs): ...

    def __init_subclass__(cls, **kwargs):
        cls._name_mapping = None
        cls._all_placeholders = None
        cls._all_options = None
        cls._all_required_options = None

    def load(self, loader: "BaseConfigLoader") -> None:
        """
        Load configuration data from the provided loader.
        
        This method uses the loader to populate the configuration values,
        then runs post-processing and custom post-load logic.
        
        :param loader: A configuration loader
        """
        self._loader = loader
        loader.load(self)
        self._postprocessing()
        self.post_load()

    def _postprocessing(self) -> None:
        """
        Run internal post-processing after loading configuration data.
        
        This method validates that all required options are set.
        """
        for option in self.get_all_required_options():
            if not option.is_assigned(self):
                raise ValueError(
                    f"{type(self)}: the missing placeholder {option.name} is required."
                )

    def load_by_context(self, context: ConfigContext, val):
        """
        Load configuration using another context's loader.
        
        :param context: The context to get the loader from
        :param val: The value to pass to the sub loader
        """
        self.load(context.get_loader().get_sub_loader(val))

    def __getitem__(self, item):
        """
        Access configuration values by dictionary-like notation.
        
        :param item: The name of the configuration option to access
        :return: The value of the specified configuration option
        :raises KeyError: If the configuration option doesn't exist
        :raises TypeError: If the item name is not a string
        """
        if not isinstance(item, str):
            raise TypeError(f"{type(self)}: {item} must be str, not {type(item)}")
        try:
            return self.__getattribute__(self.get_name_mapping()[item])
        except AttributeError:
            raise KeyError(f"{type(self)}: not contains the config named {item}")

    def __setitem__(self, key, value):
        """
        Set configuration values by dictionary-like notation.
        
        :param key: The name of the configuration option to set
        :param value: The value to set
        :raises KeyError: If the configuration option doesn't exist
        :raises TypeError: If the key is not a string
        """
        if not isinstance(key, str):
            raise TypeError(f"{type(self)}: {key} must be str, not {type(key)}")
        if key not in self.get_name_mapping():
            raise KeyError(
                f"{type(self)}: not contains the config named {key}, value: {repr(value)}"
            )
        key = self.get_name_mapping()[key]
        self.__setattr__(key, value)

    def get_loader(self) -> "BaseConfigLoader":
        """
        Get the loader used to populate this configuration.
        
        :return: The loader instance
        :raises exc.ContextNotLoadedError: If the configuration hasn't been loaded
        """
        if self._loader is None:
            raise exc.ContextNotLoadedError(self)
        return self._loader

    @property
    def loaded(self) -> bool:
        """
        Check if the configuration has been loaded.
        
        :return: True if the configuration has been loaded, False otherwise
        """
        return self._loader is not None

    def post_load(self):
        """
        Custom processing hook that runs after loading configuration data.
        
        Override this method in subclasses to implement custom post-load behavior.
        """
        pass

    # noinspection PyShadowingBuiltins
    def to_dict(
        self,
        recursive=True,
        prevent_circular=False,
        *,
        load_lazies=None,
        filter: Optional[Callable[[PlaceHolder], bool]] = None,
    ) -> dict:
        """
        Convert this configuration to a dictionary.
        
        :param recursive: If true, convert structures in this config recursively
        :param prevent_circular: If true, set circular instance to None in the result
        :param filter: A callable to determine which placeholders should be included
        :param load_lazies: Deprecated since 0.12.0
        :return: A dictionary representation of this configuration
        """
        if load_lazies is not None:
            warnings.warn(
                "the parameter 'load_lazies' is deprecated and will be removed in 1.0.0.",
                DeprecationWarning,
            )
        visitor = visitors.ToCollectionVisitor(
            recursive=recursive, set_circular_to_none=prevent_circular, filter=filter
        )
        self.accept(visitor)

        #! The visitor must return a dictionary
        return typing.cast(dict, visitor.get_result())

    def accept(self, visitor: "ConfigStructureVisitor"):
        """
        Accept a visitor for the visitor pattern implementation.
        
        :param visitor: The visitor instance
        """
        visitor.visit_config(self)

    def load_lazies(self) -> None:
        """
        Load lazy values.
        
        Deprecated since 0.12.0 and will be removed in 1.0.0.
        """
        warnings.warn(
            "This method is deprecated and will be removed in 1.0.0."
            "And the method has no operation",
            DeprecationWarning,
        )

    def clear(self) -> None:
        """
        Clear all placeholder values in this configuration.
        
        This removes all assigned values, returning the configuration to an unloaded state.
        """
        for placeholder in self.get_all_placeholders().values():
            placeholder.__delete__(self)

    def __repr__(self):
        """
        Get a string representation of this configuration.
        
        :return: A string representation of the configuration's dictionary form
        """
        return str(self.to_dict())

    def __str__(self):
        """
        Get a string representation of this configuration.
        
        :return: A string representation of the configuration's dictionary form
        """
        return self.__repr__()

    @classmethod
    def get_all_placeholders(cls) -> Dict[str, PlaceHolder]:
        """
        Get all placeholders defined in this configuration class.
        
        :return: A dictionary mapping attribute names to placeholders
        """
        if cls._all_placeholders is None:
            cls._all_placeholders = {
                name: placeholder
                for name, placeholder in inspect.getmembers(
                    cls,
                    lambda placeholder: isinstance(placeholder, PlaceHolder),
                    sort=False,
                )
            }
        return cls._all_placeholders

    @classmethod
    def get_all_options(cls) -> Dict[str, Option]:
        """
        Get all options defined in this configuration class.
        
        :return: A dictionary mapping attribute names to options
        """
        if cls._all_options is None:
            cls._all_options = {
                name: option
                for name, option in cls.get_all_placeholders().items()
                if isinstance(option, Option)
            }
        return cls._all_options

    @classmethod
    def get_all_required_options(cls) -> List[Option]:
        """
        Get all required options defined in this configuration class.
        
        :return: A list of required options
        """
        if cls._all_required_options is None:
            cls._all_required_options = [
                option for option in cls.get_all_options().values() if option.required
            ]
        return cls._all_required_options

    @classmethod
    def get_name_mapping(cls) -> Dict[str, str]:
        """
        Get the mapping between configuration names and attribute names.
        
        :return: A dictionary mapping configuration names to attribute names
        :raises exc.DuplicatedNameError: If there are duplicate configuration names
        """
        if cls._name_mapping is None:
            name_mapping = {}
            for attr_name, placeholder in cls.get_all_placeholders().items():
                if placeholder.name == consts.IGNORED_NAME:
                    continue
                if placeholder.name in name_mapping:
                    raise exc.DuplicatedNameError()
                name_mapping[placeholder.name] = attr_name
            cls._name_mapping = name_mapping
        return cls._name_mapping
