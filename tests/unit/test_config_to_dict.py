from typing import Optional, List

from fancy import config as cfg


def test_config_to_dict_with_default_values():
    class MySubConfig(cfg.BaseConfig):
        x: bool = cfg.Option(default=True, type=bool)
        y: Optional[float] = cfg.Option(nullable=True, type=float)

    class MyConfig(cfg.BaseConfig):
        a: int = cfg.Option(type=int)
        b: float = cfg.Option(default=5.1, type=float)
        sub: MySubConfig = cfg.Option(default={}, type=MySubConfig)

    assert MyConfig(a=1).to_dict() == {
        'a': 1,
        'b': 5.1,
        'sub': {'x': True, 'y': None}
    }


def test_to_dict_with_lazy_placeholder():
    class SubConfig(cfg.BaseConfig):
        x: int = cfg.Option(type=int)
        y: bool = cfg.Lazy(lambda c: c.x == 0)

    class MyConfig(cfg.BaseConfig):
        a: int = cfg.Option(type=int)
        b: float = cfg.Lazy(lambda c: c.a / 2)
        sub: SubConfig = cfg.Option(default={}, type=SubConfig)
        sub_list: List[SubConfig] = cfg.Option(default=[], type=[SubConfig])

    assert MyConfig(
        a=1, sub=dict(x=1), sub_list=[dict(x=0), dict(x=1)]
    ).to_dict() == {
        'a': 1, 'b': 0.5,
        'sub': {'x': 1, 'y': False},
        'sub_list': [{'x': 0, 'y': True}, {'x': 1, 'y': False}]
    }
