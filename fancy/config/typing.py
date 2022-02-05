from typing import Union, List, Type, Callable

UnProcType = Union[List["UnProcType"], Type, Callable]  # the type may be not process though auto_process_typ
