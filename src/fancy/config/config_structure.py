from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from . import ConfigContext

if TYPE_CHECKING:
    from . import ConfigStructureVisitor


class ConfigStructure(ABC):
    @property
    @abstractmethod
    def loaded(self) -> bool:
        """
        Whether the structure has been loaded.
        """

    @abstractmethod
    def load_by_context(self, context: ConfigContext, val) -> None:
        """
        Load the value using the information in the context.
        """

    @abstractmethod
    def accept(self, visitor: "ConfigStructureVisitor"): ...
