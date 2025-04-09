import pytest
from fancy import config as cfg


class MyConfig(cfg.BaseConfig):
    # Required string option
    name = cfg.Option(type=str, required=True)
    
    # Integer option with a default value
    count = cfg.Option(type=int, default=10)
    
    # Option that can be null
    description = cfg.Option(type=str, nullable=True)
    
    # Computed property (lazy evaluation)
    name_length = cfg.Lazy[int](lambda self: len(self.name))

def test_basic_config_creation():
    # Create a configuration from a dictionary
    config = MyConfig({
        "name": "Example Config",
        "description": "This is an example configuration"
    })
    
    # Verify values
    assert config.name == "Example Config"
    assert config.count == 10  # Default value
    assert config.description == "This is an example configuration"
    assert config.name_length == 14  # Computed value

def test_required_field():
    # Should raise an error when required field is missing
    with pytest.raises(ValueError):
        MyConfig({})

def test_nullable_field():
    # Test explicitly setting a nullable field to None
    config = MyConfig({
        "name": "Example Config",
        "description": None
    })
    assert config.description is None

def test_to_dict():
    config = MyConfig({
        "name": "Example Config",
        "description": "This is an example configuration"
    })
    
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert config_dict["name"] == "Example Config"
    assert config_dict["count"] == 10
    assert config_dict["description"] == "This is an example configuration"
    assert "name_length" in config_dict