from pprint import pprint

from fancy import config as cfg


# TODO write tests for accurate error messages
class MyConfigEmb(cfg.BaseConfig):
    x = cfg.Option(type=int)
    y = cfg.Option(type=int)
    i = cfg.Option(type=bool)
    parent = cfg.PlaceHolder["MyConfig"]()


class MyConfig(cfg.BaseConfig):
    _a = cfg.Option(name="a", required=True, description="hi", type=int)
    b = cfg.Option(required=False, type=float)
    c = cfg.Option(required=True, type=bool)
    li = cfg.Option(type=[[MyConfigEmb]])
    n = cfg.Option(type=int, required=True, nullable=True)

    lazy_li = cfg.Lazy(lambda c: c.li[0])
    placeholder_dict = cfg.PlaceHolder()
    child = cfg.Option(type=MyConfigEmb)

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
    pprint(c.to_dict(True), indent=1, depth=4)
