from abc import ABC, abstractmethod
from typing import Any, Callable


class BaseOptionConverter(ABC):
    @abstractmethod
    def set_name(self, name: str):
        pass

    @abstractmethod
    def set_required(self, required: bool):
        pass

    @abstractmethod
    def set_nullable(self, nullable: bool):
        pass

    @abstractmethod
    def set_default(self, default: Any):
        pass

    @abstractmethod
    def set_type(self, type: Callable[[Any], Any]):
        pass

    @abstractmethod
    def set_description(self, description: str):
        pass
