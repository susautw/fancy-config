from typing import List

from fancy import config as cfg


class MyConfigEmb(cfg.BaseConfig):
    x: int = cfg.Option(type=int)
    y: int = cfg.Option(type=int)
    i: bool = cfg.Option(type=bool)


class MyConfig(cfg.BaseConfig):
    _a: int = cfg.Option(name="a", required=True, description="hi", type=int)
    b: float = cfg.Option(required=False, type=float)
    c: bool = cfg.Option(required=True, type=bool)
    li: List[MyConfigEmb] = cfg.Option(type=cfg.config_list(cfg.config_list(MyConfigEmb)))

    def post_load(self):
        print(self.a)

    @property
    def a(self):
        return self._a + 1


def test_config():
    opt = {
        "a": "3",
        "b": "4.2",
        "c": "true",
        "li": [[{
            "x": 1,
            "y": 2,
            "i": "on",
            "a": "ig"
        },
            {
                "y": 3,
                "i": "off", }
        ]],
        "int_li": ["Y", "N"]
    }

    c = MyConfig(cfg.DictConfigLoader(opt, setter="strict"))
    print(c)
