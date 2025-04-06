import pytest

from fancy import config as cfg
from fancy.config import exc
from fancy.config.utils import DispatcherError


class MyConfig(cfg.BaseConfig):
    a = cfg.Option(type=int)
    b = cfg.Option(type=float)
    c = cfg.Option(default=2, type=int)


DATA_WITH_DEFAULT = {"a": 1, "b": 2}
RESULT_DATA_WITH_DEFAULT = {"a": 1, "b": 2.0, "c": 2}
DATA = {"a": 1, "b": 2, "c": 3}


def test_loader_construction():
    assert MyConfig(cfg.DictConfigLoader(DATA_WITH_DEFAULT)).to_dict() == RESULT_DATA_WITH_DEFAULT
    assert MyConfig(cfg.DictConfigLoader(DATA)).to_dict() == DATA
    unloaded_config = MyConfig(loader=None)
    assert not unloaded_config.loaded
    with pytest.raises(exc.ContextNotLoadedError):
        unloaded_config.get_loader()


def test_dict_construction():
    assert MyConfig(DATA_WITH_DEFAULT).to_dict() == RESULT_DATA_WITH_DEFAULT
    assert MyConfig(DATA).to_dict() == DATA


def test_kwarg_construction():
    assert MyConfig(**DATA_WITH_DEFAULT).to_dict() == RESULT_DATA_WITH_DEFAULT
    assert MyConfig(**DATA).to_dict() == DATA


def test_empty_construction():
    class Config(cfg.BaseConfig):
        a = cfg.Option(default=1, type=int)
        b = cfg.Option(default=2, type=int)

    assert Config().to_dict() == {'a': 1, 'b': 2}
    assert MyConfig().to_dict() == {'c': 2}  # a and b are unload


def test_dispatch():
    with pytest.raises(DispatcherError):
        MyConfig(loader=1)
    with pytest.raises(DispatcherError):
        # noinspection PyTypeChecker
        MyConfig(1) # type: ignore
    with pytest.raises(DispatcherError):
        MyConfig(1, a=1, b=2) # type: ignore
