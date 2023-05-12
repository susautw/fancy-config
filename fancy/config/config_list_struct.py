from typing import Any, Callable

from . import ConfigStructure, ConfigContext, ConfigStructureVisitor
from .process import auto_process_typ, auto_process_value
from .typing import UnProcType


class ConfigListStructure(list, ConfigStructure):
    _config_typ: Callable[[Any], Any]

    def __init__(self, config_typ: UnProcType):
        super().__init__()
        self._config_typ = auto_process_typ(config_typ)

    @property
    def loaded(self) -> bool:
        return len(self) > 0

    def load_by_context(self, context: ConfigContext, val):
        new_items = []
        for raw_value in val:
            value = auto_process_value(raw_value, self._config_typ, context)
            new_items.append(value)
        self.extend(new_items)

    def accept(self, visitor: "ConfigStructureVisitor"):
        visitor.visit_config_list(self)
