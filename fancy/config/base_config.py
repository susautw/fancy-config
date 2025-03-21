from abc import ABC
import warnings
from typing import Dict, List, overload, Any, Callable, Optional

from . import ConfigStructure, ConfigContext, exc, PlaceHolder, ConfigStructureVisitor, DictConfigLoader, consts
from . import Option
from .utils import inspect, Dispatcher, DispatcherError
from . import visitors
from ..config import BaseConfigLoader


class BaseConfig(ConfigStructure, ConfigContext, ABC):
    _name_mapping: Optional[Dict[str, str]] = None
    _all_placeholders: Optional[Dict[str, PlaceHolder]] = None
    _all_options: Optional[Dict[str, Option]] = None
    _all_required_options: Optional[List[Option]] = None
    _loader: BaseConfigLoader = None

    _method_init_ = Dispatcher(is_method=True)

    @overload
    @_method_init_.register
    def __init__(self, loader: BaseConfigLoader = None):
        if loader is not None:
            if not isinstance(loader, BaseConfigLoader):
                raise DispatcherError("loader should be a BaseConfigLoader")
            self.load(loader)

    @overload
    @_method_init_.register
    def __init__(self, options: Dict[str, Any]):
        if not isinstance(options, dict):
            raise DispatcherError("options should be dict")
        self.__init__(DictConfigLoader(options))

    @overload
    @_method_init_.register
    def __init__(self, **options: Any):
        if "loader" in options and len(options) == 1:
            raise DispatcherError("loader should be a BaseConfigLoader")
        self.__init__(options)

    @_method_init_.implement
    def __init__(self, *args, **kwargs):
        ...

    def __init_subclass__(cls, **kwargs):
        cls._name_mapping = None
        cls._all_placeholders = None
        cls._all_options = None
        cls._all_required_options = None

    def load(self, loader: 'BaseConfigLoader') -> None:
        self._loader = loader
        loader.load(self)
        self._postprocessing()
        self.post_load()

    def _postprocessing(self) -> None:
        for option in self.get_all_required_options():
            if not option.is_assigned(self):
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

    # noinspection PyShadowingBuiltins
    def to_dict(
            self,
            recursive=True,
            prevent_circular=False, *,
            load_lazies=None,
            filter: Callable[[PlaceHolder], bool] = None
    ) -> dict:
        """
        convert this config to a dictionary

        :param recursive: If true, the method will convert structures in this config recursively.
        :param prevent_circular: If true, the method will set the circular instance to ``None`` in the result.
        :param filter: a Callable to know what placeholders should be used.
        :param load_lazies: Deprecated since 0.12.0
        :return: a dict
        """
        if load_lazies is not None:
            warnings.warn(
                "the parameter 'load_lazies' is deprecated and will be removed in 1.0.0.",
                DeprecationWarning
            )
        visitor = visitors.ToCollectionVisitor(
            recursive=recursive, set_circular_to_none=prevent_circular, filter=filter
        )
        self.accept(visitor)

        # noinspection PyTypeChecker
        #  The visitor must return a dictionary
        return visitor.get_result()

    def accept(self, visitor: "ConfigStructureVisitor"):
        visitor.visit_config(self)

    def load_lazies(self) -> None:
        warnings.warn(
            "This method is deprecated and will be removed in 1.0.0."
            "And the method has no operation",
            DeprecationWarning
        )

    def clear(self) -> None:
        for placeholder in self.get_all_placeholders().values():
            placeholder.__delete__(self)

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
            name_mapping = {}
            for attr_name, placeholder in cls.get_all_placeholders().items():
                if placeholder.name == consts.IGNORED_NAME:
                    continue
                if placeholder.name in name_mapping:
                    raise exc.DuplicatedNameError()
                name_mapping[placeholder.name] = attr_name
            cls._name_mapping = name_mapping
        return cls._name_mapping
