from fancy import config as cfg


class MyConfig(cfg.BaseConfig):

    _a: int = cfg.Option(name="a", required=True, description="hi", type=int)
    b: float = cfg.Option(required=False, type=float)

    def post_load(self):
        print(self.a)

    @property
    def a(self):
        return self._a + 1


def test_config():
    opt = {
        "a": "3",
        "b": "4.2"
    }

    c = MyConfig(cfg.DictConfigLoader(opt))
    print(vars(c))

