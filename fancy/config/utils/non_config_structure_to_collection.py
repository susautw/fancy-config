from typing import Mapping, Collection

from fancy.config import ConfigStructure


def non_config_struct_to_collection_recursive(value: Collection):
    if isinstance(value, Mapping):
        result = {}
        _iter = value.items()
    else:
        result = [None] * len(value)
        _iter = enumerate(value)
    for idx, item in _iter:
        if isinstance(item, ConfigStructure):
            result[idx] = item.to_collection()
        elif isinstance(item, Collection):
            result[idx] = non_config_struct_to_collection_recursive(item)
        else:
            result[idx] = item
    return result
