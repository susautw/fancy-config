from typing import Dict, Type, TYPE_CHECKING

from . import BaseConfig, utils
from .exc import ClassNotFoundException


if TYPE_CHECKING:
    from . import BaseConfigLoader


class ConfigFactory:
    configs = None
    suffix: str = "Config"

    @classmethod
    def create_config(cls, config: str, loader: 'BaseConfigLoader') -> 'BaseConfig':
        configs = cls._get_all_configs()
        if config + cls.suffix in configs:
            config += cls.suffix
        elif config[0].capitalize() + config[1:] + cls.suffix in configs:
            config = config[0].capitalize() + config[1:] + cls.suffix
        elif config not in configs:
            raise ClassNotFoundException(config)
        return configs[config](loader)

    @classmethod
    def _get_all_configs(cls) -> Dict[str, Type['BaseConfig']]:
        if cls.configs is None:
            cls.configs = {config.__name__: config for config in utils.reflections.find_subclasses(BaseConfig)}
        return cls.configs

    @classmethod
    def get_suffix(cls) -> str:
        return cls.suffix

    @classmethod
    def set_suffix(cls, suffix: str) -> None:
        cls.suffix = suffix
