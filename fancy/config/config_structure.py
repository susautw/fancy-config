from abc import ABC, abstractmethod

from fancy.config import ConfigContext


class ConfigStructure(ABC):
    @abstractmethod
    def load_by_context(self, context: ConfigContext, val): ...
