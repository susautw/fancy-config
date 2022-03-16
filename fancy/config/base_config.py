from abc import ABC
from typing import TYPE_CHECKING, Dict, List, Optional

from . import ConfigStructure, ConfigContext, exc, PlaceHolder, Lazy, ConfigStructureVisitor
from . import Option
from .utils import inspect
from . import visitors

if TYPE_CHECKING:
    from ..config import BaseConfigLoader


class BaseConfig(ConfigStructure, ConfigContext, ABC):  # TODO more accurate error msg
    _name_mapping: Dict[str, str] = None
    _all_placeholders: Dict[str, PlaceHolder] = None
    _all_options: Dict[str, Option] = None
    _all_required_options: List[Option] = None
    _loader: 'BaseConfigLoader' = None

    def __init__(self, loader: Optional['BaseConfigLoader'] = None):
        if loader is not None:
            self.load(loader)

    def load(self, loader: 'BaseConfigLoader') -> None:
        self._loader = loader
        loader.load(self)
        self._postprocessing()
        self.post_load()

    def _postprocessing(self) -> None:
        for option in self.get_all_required_options():
            if not hasattr(self, option.__name__):
                raise ValueError(f'{type(self)}: the missing placeholder {option.name} is required.')

    def load_by_context(self, context: ConfigContext, val):
        self.load(context.get_loader().get_sub_loader(val))

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise TypeError(f'{type(self)}: {item} must be str, not {type(item)}')
        try:
            return self.__getattribute__(self.get_name_mapping()[item])
        except AttributeError:
            raise KeyError(f'{type(self)}: not contains the config named {item}')

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f'{type(self)}: {key} must be str, not {type(key)}')
        if key not in self.get_name_mapping():
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

    def to_dict(self, recursive=True, prevent_circular=False, *, load_lazies=False) -> dict:
        """
        convert this config to a dictionary
        :param recursive: If true, the method will convert structures in this config recursively.
        :param prevent_circular: If true, the method will set the circular instance to `None` in the result.
        :param load_lazies: If true, will load all `Lazy`s before converting.
        :return:
        """
        if load_lazies:
            self.load_lazies()

        visitor = visitors.ToCollectionVisitor(recursive=recursive, set_circular_to_none=prevent_circular)
        self.accept(visitor)

        # noinspection PyTypeChecker
        #  The visitor must return a dictionary
        return visitor.get_result()

    def accept(self, visitor: "ConfigStructureVisitor"):
        visitor.visit_config(self)

    def load_lazies(self) -> None:
        for name, placeholder in self.get_all_placeholders().items():
            if isinstance(placeholder, Lazy):
                getattr(self, name)

    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_all_placeholders(cls) -> Dict[str, PlaceHolder]:
        if cls._all_placeholders is None:
            cls._all_placeholders = {
                name: placeholder
                for name, placeholder in inspect.getmembers(
                    cls, lambda placeholder: isinstance(placeholder, PlaceHolder), sort=False
                )
            }
        return cls._all_placeholders

    @classmethod
    def get_all_options(cls) -> Dict[str, Option]:
        if cls._all_options is None:
            cls._all_options = {
                name: option
                for name, option in cls.get_all_placeholders().items() if isinstance(option, Option)
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
            cls._name_mapping = {
                placeholder.name: attr_name
                for attr_name, placeholder in cls.get_all_placeholders().items()
            }
        return cls._name_mapping
