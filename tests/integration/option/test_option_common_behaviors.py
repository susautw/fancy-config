import pytest

from fancy import config as cfg


def test_required_option():
    class MyConfig(cfg.BaseConfig):
        x = cfg.Option(required=True)
        y = cfg.Option()

    with pytest.raises(ValueError, match=f'{str(MyConfig)}: the missing placeholder x is required.'):
        MyConfig({})
    c = MyConfig(x=1)  # y is not required, this statement shouldn't raise exceptions
    assert c.x == 1
    with pytest.raises(AttributeError, match="attribute must assign the value before access it."):
        # noinspection PyStatementEffect
        c.y
