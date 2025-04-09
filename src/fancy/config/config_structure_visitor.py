from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import BaseConfig, ConfigListStructure


class ConfigStructureVisitor(ABC):
    """
    Abstract base class for visitors that traverse and process configuration structures.
    
    This class implements the Visitor design pattern, allowing operations to be
    performed on a configuration structure hierarchy without modifying the classes.
    
    Subclasses should implement the visit_* methods to provide specific functionality
    for each type of configuration structure.
    """
    
    @abstractmethod
    def visit_config(self, structure: "BaseConfig") -> None:
        """
        Visit a BaseConfig structure.
        
        :param structure: The BaseConfig structure to visit
        """
        ...

    @abstractmethod
    def visit_config_list(self, structure: "ConfigListStructure") -> None:
        """
        Visit a ConfigListStructure structure.
        
        :param structure: The ConfigListStructure to visit
        """
        ...
