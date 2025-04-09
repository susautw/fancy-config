import pytest
from fancy import config as cfg


class DatabaseConfig(cfg.BaseConfig):
    host = cfg.Option(type=str, default="localhost")
    port = cfg.Option(type=int, default=5432)
    username = cfg.Option(type=str, required=True)
    password = cfg.Option(type=str, required=True)

    def post_load(self):
        return print(f"DatabaseConfig loaded with host: {self.host}, port: {self.port}")

class AppConfig(cfg.BaseConfig):
    app_name = cfg.Option(type=str, required=True)
    debug = cfg.Option(type=bool, default=False)
    database = cfg.Option(type=DatabaseConfig, default={}, required=True)

def test_hierarchical_config_creation():
    # Create a configuration with nested values
    config = AppConfig({
        "app_name": "My Application",
        "debug": True,
        "database": {
            "username": "admin",
            "password": "secret"
        }
    })
    
    # Access nested configuration
    assert config.app_name == "My Application"
    assert config.debug is True
    assert config.database.host == "localhost"  # Default value
    assert config.database.port == 5432  # Default value
    assert config.database.username == "admin"
    assert config.database.password == "secret"

def test_required_fields_in_nested_config():
    # Create config with empty database config
    with pytest.raises(ValueError):
        AppConfig({
            "app_name": "My Application",
            "database": {}  # Missing required username and password
        })

def test_default_empty_nested_config():
    # When database is not provided, it should raise for missing required fields
    with pytest.raises(ValueError):
        AppConfig({
            "app_name": "My Application",
        })
    
def test_to_dict_with_nested_config():
    config = AppConfig({
        "app_name": "My Application",
        "debug": True,
        "database": {
            "username": "admin",
            "password": "secret"
        }
    })
    
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert config_dict["app_name"] == "My Application"
    assert config_dict["debug"] is True
    
    # Check nested dictionary
    assert isinstance(config_dict["database"], dict)
    assert config_dict["database"]["host"] == "localhost"
    assert config_dict["database"]["port"] == 5432
    assert config_dict["database"]["username"] == "admin"
    assert config_dict["database"]["password"] == "secret"