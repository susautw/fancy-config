from abc import ABC, abstractmethod
from typing import Collection

from fancy.config import ConfigContext


class ConfigStructure(ABC):
    @abstractmethod
    def load_by_context(self, context: ConfigContext, val): ...

    @abstractmethod
    def to_collection(self, recursive: bool = True) -> Collection: ...
