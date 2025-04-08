from fancy import config as cfg


def test_config_to_dict_with_default_values():
    class MySubConfig(cfg.BaseConfig):
        x = cfg.Option(default=True, type=bool)
        y = cfg.Option(nullable=True, type=float)

    class MyConfig(cfg.BaseConfig):
        a = cfg.Option(type=int)
        b = cfg.Option(default=5.1, type=float)
        sub = cfg.Option(default={}, type=MySubConfig)

    assert MyConfig(a=1).to_dict() == {
        'a': 1,
        'b': 5.1,
        'sub': {'x': True, 'y': None}
    }


def test_to_dict_with_lazy_placeholder():
    class SubConfig(cfg.BaseConfig):
        x = cfg.Option(type=int)
        y = cfg.Lazy[bool](lambda c: c.x == 0)

    class MyConfig(cfg.BaseConfig):
        a = cfg.Option(type=int)
        b = cfg.Lazy[float](lambda c: c.a / 2)
        sub = cfg.Option(default={}, type=SubConfig)
        sub_list = cfg.Option(default=[], type=[SubConfig])

    assert MyConfig(
        a=1, sub=dict(x=1), sub_list=[dict(x=0), dict(x=1)]
    ).to_dict() == {
        'a': 1, 'b': 0.5,
        'sub': {'x': 1, 'y': False},
        'sub_list': [{'x': 0, 'y': True}, {'x': 1, 'y': False}]
    }


def test_to_dict_with_filter():
    class MyConfig(cfg.BaseConfig):
        a = cfg.Option(default=0, type=int)
        b = cfg.PlaceHolder[float]()

        def post_load(self):
            self.b = self.a * 1.2

    c = MyConfig(a=1)
    assert c.to_dict(filter=lambda p: isinstance(p, cfg.Option)) == {"a": 1}
    assert c.to_dict(filter=lambda p: p.name != "a") == {"b": 1.2}


def test_to_dict_with_hidden_placeholder():
    class MyConfig(cfg.BaseConfig):
        a = cfg.Option(type=int)
        _b = cfg.Option(name="b", type=int, hidden=True)
        _c = cfg.Lazy[int](lambda _c: 40, hidden=True)
        _d = cfg.PlaceHolder[int](hidden=True)

        def post_load(self):
            self._d = 20

    c = MyConfig(a=1, b=2)
    assert c.to_dict() == {"a": 1}
    assert c.a == 1
    assert c._b == 2
    assert c._c == 40
    assert c._d == 20
