from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from . import ConfigContext

if TYPE_CHECKING:
    from . import ConfigStructureVisitor


class ConfigStructure(ABC):
    """
    Abstract base class that represents a configuration structure.
    
    A ConfigStructure is an entity that can be loaded with configuration data
    and can be visited by a ConfigStructureVisitor for traversal and processing.
    
    This class forms the foundation of the hierarchical configuration system,
    allowing complex nested configuration structures to be defined and processed.
    """
    
    @property
    @abstractmethod
    def loaded(self) -> bool:
        """
        Check if the structure has been loaded with configuration data.
        
        :return: True if the structure has been loaded, False otherwise
        """

    @abstractmethod
    def load_by_context(self, context: ConfigContext, val) -> None:
        """
        Load the structure using information from a configuration context.
        
        This method uses the provided context to obtain a loader for the
        given value, then loads the structure with that loader.
        
        :param context: The configuration context to use
        :param val: The value to pass to the context's loader
        """

    @abstractmethod
    def accept(self, visitor: "ConfigStructureVisitor"):
        """
        Accept a visitor for traversing and processing this structure.
        
        This method implements the Visitor design pattern, allowing operations
        to be performed on the structure without changing its implementation.
        
        :param visitor: The visitor to accept
        """
