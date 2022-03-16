from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from . import ConfigContext

if TYPE_CHECKING:
    from . import ConfigStructureVisitor


class ConfigStructure(ABC):
    @abstractmethod
    def load_by_context(self, context: ConfigContext, val): ...

    @abstractmethod
    def accept(self, visitor: "ConfigStructureVisitor"): ...
