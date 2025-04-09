from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import BaseConfig, ConfigListStructure


class ConfigStructureVisitor(ABC):
    @abstractmethod
    def visit_config(self, structure: "BaseConfig") -> None: ...

    @abstractmethod
    def visit_config_list(self, structure: "ConfigListStructure") -> None: ...
