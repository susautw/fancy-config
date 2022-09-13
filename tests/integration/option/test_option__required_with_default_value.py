import pytest

from fancy import config as cfg


class MyConfig(cfg.BaseConfig):
    x = cfg.Option(required=True, default=1)
    y = cfg.Option(required=True, nullable=True)
    z = cfg.Option(required=True, default=1, nullable=True)


@pytest.mark.parametrize("attr_name, config, expected_config", [
    # required with a default value
    ("x", dict(y=10, z=10), dict(x=1, y=10, z=10)),
    # required with a default value(None), and the value is nullable
    ("y", dict(x=10, z=10), dict(x=10, y=None, z=10)),
    # required with a default value, and the value is nullable
    ("z", dict(x=10, y=10), dict(x=10, y=10, z=1))
])
def test_required_option_with_default_value_behavior(attr_name, config, expected_config):
    c = MyConfig(config)
    assert attr_name not in vars(c)
    for k, v in expected_config.items():
        assert c[k] == v
