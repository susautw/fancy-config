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


def test_to_dict_with_filter():
    class MyConfig(cfg.BaseConfig):
        a: int = cfg.Option(default=0, type=int)
        b: float = cfg.PlaceHolder()

        def post_load(self):
            self.b = self.a * 1.2

    c = MyConfig(a=1)
    assert c.to_dict(filter=lambda p: isinstance(p, cfg.Option)) == {"a": 1}
    assert c.to_dict(filter=lambda p: p.name != "a") == {"b": 1.2}


def test_to_dict_with_hidden_placeholder():
    class MyConfig(cfg.BaseConfig):
        a: int = cfg.Option(type=int)
        _b: int = cfg.Option(name="b", type=int, hidden=True)
        _c: int = cfg.Lazy(lambda _c: 40, hidden=True)
        _d: int = cfg.PlaceHolder(hidden=True)

        def post_load(self):
            self._d = 20

    c = MyConfig(a=1, b=2)
    assert c.to_dict() == {"a": 1}
    assert c.a == 1
    assert c._b == 2
    assert c._c == 40
    assert c._d == 20
