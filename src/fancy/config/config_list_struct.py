from typing import Any, Callable

from . import ConfigStructure, ConfigContext, ConfigStructureVisitor
from .process import auto_process_typ, auto_process_value
from .typing import UnProcType


class ConfigListStructure(list, ConfigStructure):
    """
    A configuration structure that represents a list of configuration values.
    
    This class combines the functionality of Python's built-in list with
    the ConfigStructure interface, allowing it to be used in the configuration
    hierarchy. It is primarily used for representing arrays or lists of values
    in configuration data.
    
    Each element in the list is processed according to the specified configuration type.
    """
    _config_typ: Callable[[Any], Any]

    def __init__(self, config_typ: UnProcType):
        """
        Initialize a ConfigListStructure with a specified configuration type.
    
        :param config_typ: The type specification for elements in the list
        """
        super().__init__()
        self._config_typ = auto_process_typ(config_typ)

    @property
    def loaded(self) -> bool:
        """
        Check if the list has been loaded with configuration data.
        
        A ConfigListStructure is considered loaded if it contains at least one element.
        
        :return: True if the list contains elements, False otherwise
        """
        return len(self) > 0

    def load_by_context(self, context: ConfigContext, val):
        """
        Load a list of values from a configuration context.
        
        Each value in the input list is processed according to the
        configuration type specified during initialization.
        
        :param context: The configuration context to use
        :param val: A list of values to load
        """
        new_items = []
        for raw_value in val:
            value = auto_process_value(raw_value, self._config_typ, context)
            new_items.append(value)
        self.extend(new_items)

    def accept(self, visitor: "ConfigStructureVisitor"):
        """
        Accept a visitor for traversing and processing this list structure.
        
        This method implements the Visitor design pattern.
        
        :param visitor: The visitor to accept
        """
        visitor.visit_config_list(self)
