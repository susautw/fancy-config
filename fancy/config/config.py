import inspect
import json
from abc import ABC
from typing import TYPE_CHECKING, Dict, List

from ..config import Option

if TYPE_CHECKING:
    from ..config import BaseConfigLoader


class BaseConfig(ABC):  # TODO more accurate error msg
    _name_mapping: Dict[str, str]
    _all_options: Dict[str, Option]
    _all_required_options: List[Option]

    def __init__(self, loader: 'BaseConfigLoader'):
        loader.load(self)
        for option in self.get_all_required_options():
            if not hasattr(self, option.__name__):
                raise ValueError(f'the missing option {option.name} is required.')
        self.post_load()

    def __getitem__(self, item):
        if isinstance(item, str):
            raise TypeError(f'index must be str, not {type(item)}')
        try:
            return self.__getattribute__(self.get_name_mapping()[item])
        except AttributeError:
            raise KeyError(f'not contains the config named {item}')

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f'index must be str, not {type(key)}')
        if key not in self.get_name_mapping().keys():
            raise KeyError(f'not contains the config named {key}')
        key = self.get_name_mapping()[key]
        self.__setattr__(key, value)

    def post_load(self):
        pass

    @classmethod
    def get_all_options(cls) -> Dict[str, Option]:
        if "_all_options" not in vars(cls):
            cls._all_options = {name: option for name, option in inspect.getmembers(cls) if isinstance(option, Option)}
        return cls._all_options

    @classmethod
    def get_all_required_options(cls) -> List[Option]:
        if "_all_required_options" not in vars(cls):
            cls._all_required_options = [option for option in cls.get_all_options().values() if option.required]
        return cls._all_required_options

    @classmethod
    def get_name_mapping(cls) -> Dict[str, str]:
        if "_name_mapping" not in vars(cls):
            cls._name_mapping = {option.name: attr_name for attr_name, option in cls.get_all_options().items()}
        return cls._name_mapping

    def __repr__(self):
        return str({
            option.name: getattr(self, option.__name__)
            for option in self.get_all_options().values()
            if option.is_assigned(self)
        })

    def __str__(self):
        return self.__repr__()
