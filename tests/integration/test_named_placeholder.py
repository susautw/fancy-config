import pytest

from fancy import config as cfg
from fancy.config.exc import DuplicatedNameError


def test_det_duplicated_placeholder_name():
    class MyConfig(cfg.BaseConfig):
        n = cfg.Option(name="s", type=int)
        s = cfg.Lazy(lambda c: 40)  # dup!!!!

    with pytest.raises(DuplicatedNameError):
        MyConfig(s=1)


def test_ignored_name():
    class MyConfig(cfg.BaseConfig):
        # This is only for assigning, it can never be loaded
        a = cfg.Option(name=cfg.IGNORED_NAME, type=int)
        b = cfg.Option(type=int)

    c = MyConfig(b=2)
    assert c.b == 2

    with pytest.raises(AttributeError):
        _ = c.a

    c.a = 1
    assert c.a == 1


def test_ignored_name_cannot_be_loaded():
    class MyConfig(cfg.BaseConfig):
        # This is only for assigning, it can never be loaded
        a = cfg.Option(name=cfg.IGNORED_NAME, type=int)
        b = cfg.Option(type=int)

    with pytest.raises(KeyError, match=r'not contains the config named a, value: 1'):
        MyConfig(a=1, b=2)


def test_ignore_name_and_to_dict():
    class MyConfig(cfg.BaseConfig):
        a = cfg.Option(type=int)
        b = cfg.Lazy(lambda c: f'n{c.a}', name=cfg.IGNORED_NAME)

    data = {'a': 1}
    c = MyConfig(data)

    assert c.a == 1
    assert c.b == 'n1'

    assert c.to_dict() == data  # to dict is not containing MyConfig.b and can load-back to MyConfig
