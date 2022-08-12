from typing import Optional

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
