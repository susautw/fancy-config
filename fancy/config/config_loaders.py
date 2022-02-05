from argparse import Namespace
from pathlib import Path
from typing import Dict, TYPE_CHECKING, Union

import yaml
from abc import ABC, abstractmethod

from . import attribute_setters

if TYPE_CHECKING:
    from ..config import BaseConfig

setter_name_map = {}

for name, x in vars(attribute_setters).items():
    if isinstance(x, type) and issubclass(x, attribute_setters.AttributeSetter):
        try:
            name = x.get_setter_name()
            setter_name_map[name] = x()
        except NotImplementedError:
            pass


class BaseConfigLoader(ABC):
    _attribute_setter: attribute_setters.AttributeSetter

    def __init__(self, setter: Union[attribute_setters.AttributeSetter, str] = None):
        setter = "strict" if setter is None else setter
        if isinstance(setter, str):
            self._attribute_setter = setter_name_map[setter]
        else:
            self._attribute_setter = setter

    @abstractmethod
    def load(self, config: 'BaseConfig'):
        ...

    @abstractmethod
    def get_sub_loader(self, val) -> "BaseConfigLoader":
        ...

    def get_setter(self) -> attribute_setters.AttributeSetter:
        return self._attribute_setter


class DictBasedConfigLoader(BaseConfigLoader, ABC):
    @abstractmethod
    def get_dict(self) -> Dict:
        pass

    def load(self, config: 'BaseConfig'):
        for key, value in self.get_dict().items():
            self.get_setter().set(config, key, value)

    def get_sub_loader(self, val) -> "BaseConfigLoader":
        return DictConfigLoader(val, self._attribute_setter)


class PathBasedConfigLoader(BaseConfigLoader, ABC):
    _path: Path

    def __init__(self, path: Union[Path, str], setter: Union[attribute_setters.AttributeSetter, str] = None):
        super().__init__(setter)
        self._path = path if isinstance(path, Path) else Path(path)

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: Path) -> None:
        self._path = path


class YamlConfigLoader(DictBasedConfigLoader, PathBasedConfigLoader):

    def get_dict(self) -> Dict:
        if not self.path.is_file():
            raise FileNotFoundError(str(self.path))
        stream = self.path.open()
        data = yaml.safe_load(stream)

        if data is None:
            data = {}

        stream.close()
        return data


class DictConfigLoader(DictBasedConfigLoader):
    _dict: Dict

    def __init__(self, _dict: Dict, setter: Union[attribute_setters.AttributeSetter, str] = None):
        super().__init__(setter)
        self._dict = _dict

    def get_dict(self) -> Dict:
        return self._dict


class NamespaceConfigLoader(DictBasedConfigLoader):
    _args: Namespace

    def __init__(self, args: Namespace, setter: Union[attribute_setters.AttributeSetter, str] = None):
        super().__init__(setter)
        self._args = args

    def get_dict(self) -> Dict:
        return vars(self._args)
