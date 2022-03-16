from pprint import pprint
from typing import List, Dict, Optional

from fancy import config as cfg


# TODO write tests for accurate error messages
class MyConfigEmb(cfg.BaseConfig):
    x: int = cfg.Option(type=int)
    y: int = cfg.Option(type=int)
    i: bool = cfg.Option(type=bool)
    parent: "MyConfig" = cfg.PlaceHolder()


class MyConfig(cfg.BaseConfig):
    _a: int = cfg.Option(name="a", required=True, description="hi", type=int)
    b: float = cfg.Option(required=False, type=float)
    c: bool = cfg.Option(required=True, type=bool)
    li: List[List[MyConfigEmb]] = cfg.Option(type=[[MyConfigEmb]])
    n: Optional[int] = cfg.Option(type=int, required=True, nullable=True)

    lazy_li: List[MyConfigEmb] = cfg.Lazy(lambda c: c.li[0])
    placeholder_dict: Dict[int, MyConfigEmb] = cfg.PlaceHolder()
    child: MyConfigEmb = cfg.Option(type=MyConfigEmb)

    def post_load(self):
        self.placeholder_dict = {self._a: self.lazy_li[0]}

    @property
    def a(self):
        return self._a + 1


def test_config():
    opt = {
        "a": "3",
        "b": "4.2",
        "c": "true",
        'n': None,
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
        "int_li": ["Y", "N"],
        "child": {
            "x": 4,
            "y": 5,
            "i": "off",
            "a": "ig"
        }
    }

    c = MyConfig(cfg.DictConfigLoader(opt, setter="ignore"))
    c.child.parent = c
    print(c)
    print(c.placeholder_dict)
    pprint(c.to_dict(True, load_lazies=True), indent=1, depth=4)
