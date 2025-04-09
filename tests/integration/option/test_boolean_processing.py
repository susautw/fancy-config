import pytest
from fancy import config as cfg


class FeatureConfig(cfg.BaseConfig):
    # Automatically converts various string representations to boolean
    enabled = cfg.Option(type=bool)

@pytest.mark.parametrize("value", ["true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON", "1"])
def test_boolean_conversion_true_values(value):
    # Test different string representations that should convert to True
    config = FeatureConfig({"enabled": value})
    assert config.enabled is True, f"Failed for value: {value}"

@pytest.mark.parametrize("value", ["false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF", "0"])
def test_boolean_conversion_false_values(value):
    # Test different string representations that should convert to False
    config = FeatureConfig({"enabled": value})
    assert config.enabled is False, f"Failed for value: {value}"

def test_actual_boolean_values():
    # Test with actual boolean values
    config_true = FeatureConfig({"enabled": True})
    assert config_true.enabled is True
    
    config_false = FeatureConfig({"enabled": False})
    assert config_false.enabled is False

@pytest.mark.parametrize("value", ["maybe", "unknown", "2", "other"])
def test_invalid_boolean_values(value):
    # Test with values that can't be converted to boolean
    with pytest.raises(ValueError):  # Specific exception type
        FeatureConfig({"enabled": value})

def test_to_dict_boolean():
    config = FeatureConfig({"enabled": "yes"})
    config_dict = config.to_dict()
    
    assert config_dict["enabled"] is True