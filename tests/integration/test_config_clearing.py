from typing import List

import pytest

from fancy import config as cfg


class MyConfig(cfg.BaseConfig):
    a: int = cfg.Option(type=int, required=True)
    b: str = cfg.Option(type=str, default="default text")
    c: List[int] = cfg.Option(type=[int])
    d: str = cfg.PlaceHolder()  # custom state marked with Placeholder
    e: int  # a custom state marking

    def post_load(self):
        self.d = str(self.a + 2)
        self.e = self.a ** 2

    def clear(self):
        super().clear()
        del self.e  # clear an unmarked custom state manually


# Test case 1: Clear a fully loaded config
def test_clear_loaded_config():
    config = MyConfig(a=1, b="a string", c=[1, 2, 3, 4])
    config.d = "custom state"
    config.clear()

    with pytest.raises(AttributeError, match="attribute 'a' of 'MyConfig' object must be assigned before accessing."):
        _ = config.a

    assert config.b == "default text"

    with pytest.raises(AttributeError, match="attribute 'c' of 'MyConfig' object must be assigned before accessing."):
        _ = config.c

    with pytest.raises(AttributeError, match="attribute 'd' of 'MyConfig' object must be assigned before accessing."):
        _ = config.d

    with pytest.raises(AttributeError, match="'MyConfig' object has no attribute 'e'"):
        _ = config.e


# Test case 2: Load config without default_values after clearing
def test_load_config_without_default_values_after_clear():
    config = MyConfig(a=1, b="a string", c=[1, 2, 3, 4])
    config.clear()
    config.load(cfg.DictConfigLoader({"a": 3, "c": [5, 6, 7, 8]}))

    assert config.a == 3
    assert config.b == "default text"
    assert config.c == [5, 6, 7, 8]
    assert config.d == '5'
    assert config.e == 9
