import pytest

from fancy import config as cfg


class MyConfig(cfg.BaseConfig):
    x = cfg.Option(required=True, default=1)
    y = cfg.Option(required=True, nullable=True)
    z = cfg.Option(required=True, default=1, nullable=True)


@pytest.mark.parametrize("config, expected_config", [
    # required and has a default value
    (dict(y=10, z=10), dict(x=1, y=10, z=10)),
    # required and has a default value with None, and the value is nullable
    (dict(x=10, z=10), dict(x=10, y=None, z=10)),
    # required and has a default value, and the value is nullable
    (dict(x=10, y=10), dict(x=10, y=10, z=1))
])
def test_option_required_behavior(config, expected_config):
    c = MyConfig(config)
    for k, v in expected_config.items():
        assert c[k] == v
