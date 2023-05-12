from fancy import config as cfg


class SubConfig(cfg.BaseConfig):
    a: int = cfg.Option(type=int)


class MyConfig(cfg.BaseConfig):
    sub: SubConfig = cfg.Option(type=SubConfig)


class MyListConfig(cfg.BaseConfig):
    subs: list = cfg.Option(type=[SubConfig])


def test_option__assigning_config_instance():
    expected_dict = {'sub': {'a': 1}}

    sub_config = SubConfig(a=1)
    config = MyConfig(sub=sub_config)

    assert MyConfig(sub={'a': 1}).to_dict() == expected_dict
    assert config.to_dict() == expected_dict
    assert config.sub is sub_config


def test_loading_list_of_config_instances():
    expected_dict = {'subs': [{'a': 1}, {'a': 2}, {'a': 3}]}

    sub_config = SubConfig(a=2)
    config = MyListConfig(subs=[{'a': 1}, sub_config, {'a': 3}])

    assert config.to_dict() == expected_dict
    assert config.subs[0] is not sub_config
    assert config.subs[1] is sub_config
    assert config.subs[2] is not sub_config
