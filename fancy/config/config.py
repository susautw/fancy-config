from abc import ABC
from typing import TYPE_CHECKING

from ..config import Option

if TYPE_CHECKING:
    from ..config import BaseConfigLoader


class BaseConfig(ABC):

    def __init__(self, loader: 'BaseConfigLoader'):
        loader.load(self)
        required_options = [
            value for key, value in type(self).__dict__.items() if isinstance(value, Option) if value.required
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
