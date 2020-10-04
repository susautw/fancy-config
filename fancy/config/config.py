from abc import ABC
from typing import TYPE_CHECKING, Dict

from ..config import Option

if TYPE_CHECKING:
    from ..config import BaseConfigLoader


class BaseConfig(ABC):

    def __init__(self, loader: 'BaseConfigLoader'):
        loader.load(self)
        required_options = [
            option for _, option in self.get_all_options().items() if option.required
        ]
        for option in required_options:
            if not hasattr(self, option.name):
                raise ValueError(f'the missing option {option.name} is required.')

    def __getitem__(self, item):
        if isinstance(item, str):
            raise TypeError(f'index must be str, not {type(item)}')
        try:
            return self.__getattribute__(item)
        except AttributeError:
            raise IndexError(f'not contains the config named {item}')

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f'index must be str, not {type(key)}')
        if key not in type(self).__dict__:
            raise IndexError(f'not contains the config named {key}')
        self.__setattr__(key, value)

    def post_load(self):
        pass

    @classmethod
    def get_all_options(cls) -> Dict[str, Option]:
        return {name: option for name, option in vars(cls).items() if isinstance(option, Option)}
