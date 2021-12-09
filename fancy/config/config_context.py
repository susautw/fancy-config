from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import BaseConfigLoader


class ConfigContext(ABC):
    @abstractmethod
    def get_loader(self) -> "BaseConfigLoader":
        """
        :raises exc.ContextNotLoadedError when loader does not exist.
        """
