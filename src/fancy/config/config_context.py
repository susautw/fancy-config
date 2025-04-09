from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import BaseConfigLoader


class ConfigContext(ABC):
    """
    Abstract base class that represents a configuration context.
    
    A ConfigContext provides access to a configuration loader, allowing
    configuration data to be loaded from various sources.
    
    This class acts as a bridge between the configuration structure and
    the configuration data source.
    """
    
    @abstractmethod
    def get_loader(self) -> "BaseConfigLoader":
        """
        Get the configuration loader associated with this context.
        
        :return: The configuration loader
        :raises exc.ContextNotLoadedError: when loader does not exist.
        """
