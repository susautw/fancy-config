from typing import Dict, Type

from .. import config as cfg
from fancy.config import utils, exc


class ConfigLoaderFactory:
    suffix: str = "ConfigLoader"
    loaders = None

    @classmethod
    def create_loader(cls, method: str = 'yaml') -> cfg.BaseConfigLoader:
        loaders = cls.get_all_loaders()
        if method + cls.suffix in loaders:
            method += cls.suffix
        elif method.capitalize() + cls.suffix in loaders:
            method = method.capitalize() + cls.suffix
        elif method not in loaders:
            raise exc.ClassNotFoundException(method)
        return loaders[method]()

    @classmethod
    def get_all_loaders(cls) -> Dict[str, Type[cfg.BaseConfigLoader]]:
        if cls.loaders is None:
            cls.loaders = {
                loader.__name__: loader for loader in utils.reflections.find_subclasses(cfg.BaseConfigLoader)
            }
        return cls.loaders

    @classmethod
    def get_suffix(cls) -> str:
        return cls.suffix

    @classmethod
    def set_suffix(cls, suffix: str) -> None:
        cls.suffix = suffix
