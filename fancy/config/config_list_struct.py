from typing import Any, Callable

from . import ConfigStructure, ConfigContext, ConfigStructureVisitor
from .process import auto_process_typ
from .typing import UnProcType


class ConfigListStructure(list, ConfigStructure):
    _config_typ: Callable[[Any], Any]

    def __init__(self, config_typ: UnProcType):
        super().__init__()
        self._config_typ = auto_process_typ(config_typ)

    def load_by_context(self, context: ConfigContext, val):
        new_items = []
        for raw_cfg in val:
            cfg = self._config_typ(raw_cfg)
            if isinstance(cfg, ConfigStructure):
                cfg.load_by_context(context, raw_cfg)
            new_items.append(cfg)
        self.extend(new_items)

    def accept(self, visitor: "ConfigStructureVisitor"):
        visitor.visit_config_list(self)
