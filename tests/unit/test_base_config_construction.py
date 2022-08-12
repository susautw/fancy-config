import pytest

from fancy import config as cfg
from fancy.config.utils import DispatcherError


class MyConfig(cfg.BaseConfig):
    a: int = cfg.Option(type=int)
    b: float = cfg.Option(type=float)
    c: int = cfg.Option(default=2, type=int)


DATA_WITH_DEFAULT = {"a": 1, "b": 2}
RESULT_DATA_WITH_DEFAULT = {"a": 1, "b": 2.0, "c": 2}
DATA = {"a": 1, "b": 2, "c": 3}


def test_loader_construction():
    assert MyConfig(cfg.DictConfigLoader(DATA_WITH_DEFAULT)).to_dict() == RESULT_DATA_WITH_DEFAULT
    assert MyConfig(cfg.DictConfigLoader(DATA)).to_dict() == DATA


def test_dict_construction():
    assert MyConfig(DATA_WITH_DEFAULT).to_dict() == RESULT_DATA_WITH_DEFAULT
    assert MyConfig(DATA).to_dict() == DATA


def test_kwarg_construction():
    assert MyConfig(**DATA_WITH_DEFAULT).to_dict() == RESULT_DATA_WITH_DEFAULT
    assert MyConfig(**DATA).to_dict() == DATA


def test_dispatch():
    with pytest.raises(DispatcherError):
        MyConfig(loader=1)
    with pytest.raises(DispatcherError):
        # noinspection PyTypeChecker
        MyConfig(1)
    with pytest.raises(DispatcherError):
        MyConfig(1, a=1, b=2)
