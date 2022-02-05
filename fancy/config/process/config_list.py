from typing import Callable

from ..typing import UnProcType


def config_list(_type: UnProcType) -> Callable:
    from .. import ConfigListStructure

    def _inner(_):
        return ConfigListStructure(_type)
    return _inner
