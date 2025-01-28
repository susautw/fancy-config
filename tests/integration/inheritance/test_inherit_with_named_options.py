from fancy import config as cfg


def test_inherit_with_named_options():
    class SuperConfig(cfg.BaseConfig):
        a: str = cfg.Option(name="A")

    class SubConfig(SuperConfig):
        b: str = cfg.Option(name="B")

    super_data = {"A": '1'}
    sc = SuperConfig(super_data)
    assert sc.a == '1'  # load super config before sub config

    sub_data = {"A": '1', 'B': '2'}
    c = SubConfig(sub_data)
    assert c.a == '1'
    assert c.b == '2'
