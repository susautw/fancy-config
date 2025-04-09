from typing import Union, List, Type, Callable

UnProcType = Union[List["UnProcType"], Type, Callable]  # the type may be not process though auto_process_typ
"""
This type is used to represent types that may not be processed by `auto_process_typ`.
"""