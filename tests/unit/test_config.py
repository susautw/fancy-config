from fancy import config as cfg


class MyConfig(cfg.BaseConfig):
    a: int = cfg.Option(required=True, description="hi", type=int)
    b: float = cfg.Option(required=False, type=float)


def test_config():
    opt = {
        "a": "3",
        "b": "4.2"
    }

    c = MyConfig(cfg.DictConfigLoader(opt))
    print(vars(c))
