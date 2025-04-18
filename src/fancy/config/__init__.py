"""
Fancy Config - A flexible configuration management system for Python applications.

This package provides a robust framework for defining, loading, and managing configuration
structures in Python. It supports various sources of configuration data, type conversion,
validation, and hierarchical configuration structures.

Key components:
- BaseConfig: Base class for creating configuration classes
- Option: For defining configuration options with validation and type conversion
- PlaceHolder and Lazy: For defining computed or placeholder values
- ConfigLoaders: For loading configuration from different sources
"""

__all__ = [
    "attribute_setters",
    "process",
    "config_list",
    "make_boolean",
    "identical",
    "ConfigContext",
    "ConfigStructure",
    "ConfigStructureVisitor",
    "PlaceHolder",
    "Lazy",
    "Option",
    "ConfigListStructure",
    "BaseConfigLoader",
    "DictBasedConfigLoader",
    "PathBasedConfigLoader",
    "YamlConfigLoader",
    "DictConfigLoader",
    "BaseConfig",
    "ConfigLoaderFactory",
    "ConfigFactory",
    "IGNORED_NAME",
]


from . import attribute_setters

from . import process
from .process import (
    config_list,
    make_boolean,
    identical
)

from .config_context import ConfigContext
from .config_structure import ConfigStructure
from .config_structure_visitor import ConfigStructureVisitor
from .placeholder import PlaceHolder
from .lazy import Lazy
from .option import Option
from .config_list_struct import ConfigListStructure
from .config_loaders import (
    BaseConfigLoader,
    DictBasedConfigLoader,
    PathBasedConfigLoader,
    YamlConfigLoader,
    DictConfigLoader
)
from .base_config import BaseConfig

from .config_loader_factory import ConfigLoaderFactory
from .config_factory import ConfigFactory
from .consts import IGNORED_NAME
