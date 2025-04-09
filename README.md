# fancy-config

A flexible, type-safe, and hierarchical configuration management system for Python.

[![PyPI version](https://badge.fury.io/py/fancy-config.svg)](https://badge.fury.io/py/fancy-config)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **Type-safe configuration**: Define configuration options with specific types, automatic type conversion
- **Validation**: Options can be marked as required, nullable, with default values
- **Hierarchical structure**: Support for nested configuration objects
- **Multiple data sources**: Load configuration from YAML files, dictionaries, or command-line arguments
- **Extensible**: Create custom configuration loaders for any data source
- **Advanced features**: Lazy evaluation, placeholder values, configuration lists

## 📦 Installation

```bash
pip install fancy-config
```

## 🚀 Quick Start

```python
from fancy import config as cfg

# Define a configuration class
class MyConfig(cfg.BaseConfig):
    # Required integer option
    name = cfg.Option(type=str, required=True)
    
    # Integer option with a default value
    count = cfg.Option(type=int, default=10)
    
    # Option that can be null
    description = cfg.Option(type=str, nullable=True)
    
    # Computed property (lazy evaluation)
    name_length = cfg.Lazy[int](lambda self: len(self.name))

# Create a configuration from a dictionary
config = MyConfig({
    "name": "Example Config",
    "description": "This is an example configuration"
})

# Access configuration values
print(config.name)  # "Example Config"
print(config.count)  # 10 (default value)
print(config.name_length)  # 14 (computed)

# Convert to dictionary
config_dict = config.to_dict()
```

## 📋 Hierarchical Configuration

```python
from fancy import config as cfg

# Define a sub-configuration
class DatabaseConfig(cfg.BaseConfig):
    host = cfg.Option(type=str, default="localhost")
    port = cfg.Option(type=int, default=5432)
    username = cfg.Option(type=str, required=True)
    password = cfg.Option(type=str, required=True)

# Define a main configuration that includes the sub-configuration
class AppConfig(cfg.BaseConfig):
    app_name = cfg.Option(type=str, required=True)
    debug = cfg.Option(type=bool, default=False)
    database = cfg.Option(type=DatabaseConfig, default={})

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
print(config.app_name)  # "My Application"
print(config.database.host)  # "localhost" (default value)
print(config.database.username)  # "admin"
```

## 📝 Loading from YAML Files

```python
from fancy import config as cfg
from pathlib import Path

class MyConfig(cfg.BaseConfig):
    name = cfg.Option(type=str)
    count = cfg.Option(type=int)

# Load from a YAML file
yaml_loader = cfg.YamlConfigLoader(Path("config.yaml"))
config = MyConfig(loader=yaml_loader)
```

Example YAML file:
```yaml
name: Example Config
count: 42
```

## 📋 List Configuration

```python
from fancy import config as cfg

class ServerConfig(cfg.BaseConfig):
    host = cfg.Option(type=str, required=True)
    port = cfg.Option(type=int, default=80)

class ClusterConfig(cfg.BaseConfig):
    servers = cfg.Option(type=[ServerConfig])  # List of ServerConfig objects

# Create a configuration with a list of servers
config = ClusterConfig({
    "servers": [
        {"host": "server1.example.com", "port": 8080},
        {"host": "server2.example.com"}
    ]
})

# Access list elements
print(config.servers[0].host)  # "server1.example.com"
print(config.servers[1].port)  # 80 (default value)
```

## 🧪 Advanced Features

### Boolean Processing

```python
from fancy import config as cfg

class FeatureConfig(cfg.BaseConfig):
    # Automatically converts various string representations to boolean
    enabled = cfg.Option(type=bool)

config = FeatureConfig({
    "enabled": "yes"  # Will be converted to True
})

# Other valid string values for boolean:
# "true", "on", "1" -> True
# "false", "off", "0", "no" -> False
```

### Custom Type Conversion

```python
from fancy import config as cfg
from pathlib import Path

def path_converter(value):
    return Path(value)

class FileConfig(cfg.BaseConfig):
    location = cfg.Option(type=path_converter)

config = FileConfig({"location": "/tmp/file.txt"})
print(type(config.location))  # <class 'pathlib.Path'>
```

### Lazy Computed Values

```python
from fancy import config as cfg

class ReportConfig(cfg.BaseConfig):
    width = cfg.Option(type=int, default=100)
    height = cfg.Option(type=int, default=50)
    
    # Computed only when accessed
    area = cfg.Lazy[int](lambda self: self.width * self.height)
    
    # Can depend on other computed values
    description = cfg.Lazy[str](lambda self: f"Report size: {self.area} square units")

config = ReportConfig()
print(config.area)  # 5000 (100 * 50)
print(config.description)  # "Report size: 5000 square units"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
