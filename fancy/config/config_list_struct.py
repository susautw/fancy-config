from typing import Any, Callable, Collection

from fancy.config import ConfigStructure, ConfigContext
from fancy.config.process import auto_process_typ
from fancy.config.typing import UnProcType
from fancy.config.utils import non_config_struct_to_collection_recursive


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

    def to_collection(self, recursive: bool = True) -> Collection:
        if not recursive:
            return self
        # ConfigListStructure can process like a list
        return non_config_struct_to_collection_recursive(self)
