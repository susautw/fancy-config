from abc import ABC
from typing import TYPE_CHECKING, Dict, List, Optional

from . import ConfigStructure, ConfigContext, exc
from . import Option
from .utils import inspect

if TYPE_CHECKING:
    from ..config import BaseConfigLoader


class BaseConfig(ConfigStructure, ConfigContext, ABC):  # TODO more accurate error msg
    _name_mapping: Dict[str, str] = None
    _all_options: Dict[str, Option] = None
    _all_required_options: List[Option] = None
    _loader: 'BaseConfigLoader' = None

    def __init__(self, loader: Optional['BaseConfigLoader'] = None):
        if loader is not None:
            self.load(loader)

    def load(self, loader: 'BaseConfigLoader') -> None:
        self._loader = loader
        loader.load(self)
        for option in self.get_all_required_options():
            if not hasattr(self, option.__name__):
                raise ValueError(f'{type(self)}: the missing option {option.name} is required.')
        self.post_load()

    def load_by_context(self, context: ConfigContext, val):
        self.load(context.get_loader().get_sub_loader(val))

    def __getitem__(self, item):
        if isinstance(item, str):
            raise TypeError(f'{type(self)}: {item} must be str, not {type(item)}')
        try:
            return self.__getattribute__(self.get_name_mapping()[item])
        except AttributeError:
            raise KeyError(f'{type(self)}: not contains the config named {item}')

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f'{type(self)}: {key} must be str, not {type(key)}')
        if key not in self.get_name_mapping().keys():
            raise KeyError(f'{type(self)}: not contains the config named {key}, value: {repr(value)}')
        key = self.get_name_mapping()[key]
        self.__setattr__(key, value)

    def get_loader(self) -> 'BaseConfigLoader':
        if self._loader is None:
            raise exc.ContextNotLoadedError(self)
        return self._loader

    @property
    def loaded(self) -> bool:
        return self._loader is not None

    def post_load(self):
        pass

    @classmethod
    def get_all_options(cls) -> Dict[str, Option]:
        if cls._all_options is None:
            cls._all_options = {
                name: option
                for name, option in inspect.getmembers(cls, lambda option: isinstance(option, Option), sort=False)
            }
        return cls._all_options

    @classmethod
    def get_all_required_options(cls) -> List[Option]:
        if cls._all_required_options is None:
            cls._all_required_options = [option for option in cls.get_all_options().values() if option.required]
        return cls._all_required_options

    @classmethod
    def get_name_mapping(cls) -> Dict[str, str]:
        if cls._name_mapping is None:
            cls._name_mapping = {option.name: attr_name for attr_name, option in cls.get_all_options().items()}
        return cls._name_mapping

    def to_dict(self) -> dict:
        return {
            option.name: getattr(self, option.__name__)
            for option in self.get_all_options().values()
            if option.is_assigned(self)
        }

    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        return self.__repr__()
