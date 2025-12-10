import sys
import pytest

from fancy import config as cfg


# Only test generic syntax on Python 3.12+, which supports PEP 695
@pytest.mark.skipif(sys.version_info < (3, 12), reason="Generic syntax requires Python 3.12+")
def test_generic_baseconfig_subclass():
    """Test that generic subclassing of BaseConfig works correctly.
    
    This test ensures that the __init_subclass__ workaround for CPython bug
    python/cpython#114326 is in place. Without calling super().__init_subclass__,
    CPython fails to set __parameters__ on generic classes.
    """
    # Define a generic config class using PEP 695 syntax
    namespace = {'cfg': cfg}
    exec("""
class GenericConfig[T](cfg.BaseConfig):
    value = cfg.Option(type=int, default=42)
""", namespace)
    
    config_cls = namespace['GenericConfig']
    
    # This should not raise AttributeError: __parameters__
    instance = config_cls[int]()
    
    # Verify the instance works correctly
    assert instance.value == 42
    assert instance.to_dict() == {'value': 42}


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Generic syntax requires Python 3.12+")
def test_generic_baseconfig_with_options():
    """Test that generic BaseConfig subclass with options works correctly."""
    namespace = {'cfg': cfg}
    exec("""
class GenericConfigWithOptions[T](cfg.BaseConfig):
    item = cfg.Option(type=int, required=True)
    default_val = cfg.Option(type=str, default="default")
""", namespace)
    
    config_cls = namespace['GenericConfigWithOptions']
    
    # Create an instance with a type parameter
    instance = config_cls[str](item=100, default_val="custom")
    
    assert instance.item == 100
    assert instance.default_val == "custom"
    assert instance.to_dict() == {'item': 100, 'default_val': 'custom'}


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Generic syntax requires Python 3.12+")
def test_generic_nested_config():
    """Test that generic BaseConfig works with inheritance."""
    namespace = {'cfg': cfg}
    exec("""
class BaseGenericConfig[T](cfg.BaseConfig):
    base_value = cfg.Option(type=int, default=10)

class DerivedGenericConfig[T](BaseGenericConfig[T]):
    derived_value = cfg.Option(type=int, default=20)
""", namespace)
    
    config_cls = namespace['DerivedGenericConfig']
    
    # Create an instance with a type parameter
    instance = config_cls[str]()
    
    assert instance.base_value == 10
    assert instance.derived_value == 20
    assert instance.to_dict() == {
        'base_value': 10,
        'derived_value': 20
    }
