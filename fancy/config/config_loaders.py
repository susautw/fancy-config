from argparse import Namespace
from pathlib import Path
from typing import Dict, TYPE_CHECKING

import yaml
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..config import BaseConfig


class BaseConfigLoader(ABC):
    @abstractmethod
    def load(self, config: 'BaseConfig') -> 'BaseConfig':
        pass


class DictBasedConfigLoader(BaseConfigLoader):

    @abstractmethod
    def get_dict(self) -> Dict:
        pass

    def load(self, config: 'BaseConfig'):
        for key, value in self.get_dict().items():
            config[key] = value


class PathBasedConfigLoader(BaseConfigLoader, ABC):
    _path: Path

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

    def __init__(self, _dict: Dict):
        self._dict = _dict

    def get_dict(self) -> Dict:
        return self._dict


class NamespaceConfigLoader(DictBasedConfigLoader):
    _args: Namespace

    def __init__(self, args: Namespace):
        self._args = args

    def get_dict(self) -> Dict:
        return vars(self._args)
