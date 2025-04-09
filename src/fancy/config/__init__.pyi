"""
Typing Support for config module
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

from collections.abc import Callable, Sequence
from typing import Any, Literal, NoReturn, overload

from . import attribute_setters

from . import process
from .process import config_list, make_boolean, identical

from .config_context import ConfigContext
from .config_structure import ConfigStructure
from .config_structure_visitor import ConfigStructureVisitor
from .placeholder import PlaceHolder

# from .lazy import Lazy
# from .option import Option
from .config_list_struct import ConfigListStructure
from .config_loaders import (
    BaseConfigLoader,
    DictBasedConfigLoader,
    PathBasedConfigLoader,
    YamlConfigLoader,
    DictConfigLoader,
)
from .base_config import BaseConfig

from .config_loader_factory import ConfigLoaderFactory
from .config_factory import ConfigFactory
from .consts import IGNORED_NAME

class Lazy[GV](PlaceHolder[GV]):
    def __init__(
        self,
        fn: Callable[[Any], GV],
        name: str | None = None,
        description: str | None = None,
        hidden: bool = False,
    ) -> None: ...
    def __set__(self, instance: BaseConfig, raw_value: Any) -> NoReturn: ...

type _Nested[SV, GV] = list[_Nested[SV, GV]] | list[Callable[[SV], GV]]
type _NestedValue[V] = Sequence[_NestedValue[V]] | V
type Never = NoReturn  # TODO: use real Never type when available

class Option[GV, SV, N](PlaceHolder[GV | N]):
    @overload
    def __init__[_GV, _SV](
        self: Option[_GV, _SV, Never],
        *,
        required: bool = False,
        nullable: Literal[False] = False,
        default: _SV | None = None,
        type: Callable[[_SV], GV] = identical,
        name: str | None = None,
        description: str | None = None,
        hidden: bool = False,
    ) -> None: ...
    @overload
    def __init__[_GV, _SV](
        self: Option[_NestedValue[_GV], _NestedValue[_SV], Never],
        *,
        required: bool = False,
        nullable: Literal[False] = False,
        type: _Nested[_SV, _GV],
        default: Sequence | None = None,
        name: str | None = None,
        description: str | None = None,
        hidden: bool = False,
    ) -> None: ...
    @overload
    def __init__[_GV, _SV](
        self: Option[_GV, _SV, None],
        *,
        required: bool = False,
        nullable: Literal[True],
        default: _SV | None = None,
        type: Callable[[_SV], GV] = identical,
        name: str | None = None,
        description: str | None = None,
        hidden: bool = False,
    ) -> None: ...
    @overload
    def __init__[_GV, _SV](
        self: Option[_NestedValue[_GV], _NestedValue[_SV], None],
        *,
        required: bool = False,
        default: _SV | None = None,
        name: str | None = None,
        description: str | None = None,
        hidden: bool = False,
    ) -> None: ...
    def __set__(self, instance: BaseConfig, raw_value: SV | None) -> None: ...
    @property
    def required(self) -> bool: ...
