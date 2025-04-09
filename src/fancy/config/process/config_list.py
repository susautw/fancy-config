from typing import Callable

from ..typing import UnProcType


def config_list(_type: UnProcType) -> Callable:
    """
    Create a function that returns a ConfigListStructure for the specified type.
    
    This factory function creates a processor that returns a new ConfigListStructure
    instance configured to hold elements of the specified type.
    
    :param _type: The type specification for elements in the list
    :return: A function that returns a new ConfigListStructure instance
    """
    from .. import ConfigListStructure

    def _inner(_):
        return ConfigListStructure(_type)
    return _inner
