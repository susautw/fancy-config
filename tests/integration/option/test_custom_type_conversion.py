import pytest
from pathlib import Path
from fancy import config as cfg
import sys


def path_converter(value):
    return Path(value)

class FileConfig(cfg.BaseConfig):
    location = cfg.Option(type=path_converter)

def test_custom_converter():
    # Test with a string path
    config = FileConfig({"location": "/tmp/file.txt"})
    
    # Verify the conversion worked
    assert isinstance(config.location, Path)
    assert str(config.location) == "/tmp/file.txt"

def test_custom_converter_with_none():
    # Test with None value
    with pytest.raises(ValueError):  # location is not nullable
        FileConfig({"location": None})

def test_custom_converter_with_invalid_input():
    # Test with a value that might cause the converter to fail
    # For the path converter, most inputs will work, but we can test with something unusual
    with pytest.raises(TypeError):  # Replace with specific exception if known
        FileConfig({"location": 123})  # Integer isn't directly convertible to Path

# Test for staticmethod converter (Python 3.10+)
@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10 or higher")
def test_staticmethod_converter():
    class StaticMethodFileConfig(cfg.BaseConfig):
        @staticmethod
        def path_converter(value):
            return Path(value)
        
        location = cfg.Option(type=path_converter)
    """Test the staticmethod converter case shown in the README"""
    # Test with a string path
    config = StaticMethodFileConfig({"location": "/tmp/file.txt"})
    
    # Verify the conversion worked
    assert isinstance(config.location, Path)
    assert str(config.location) == "/tmp/file.txt"

# Custom converter for duration in seconds
def duration_converter(value):
    if isinstance(value, str):
        if value.endswith('s'):
            return float(value[:-1])
        elif value.endswith('m'):
            return float(value[:-1]) * 60
        elif value.endswith('h'):
            return float(value[:-1]) * 3600
    return float(value)

class DurationConfig(cfg.BaseConfig):
    timeout = cfg.Option(type=duration_converter)

@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("30s", 30.0),
        ("5m", 300.0),
        ("2h", 7200.0),
        (60, 60.0),
        (1.5, 1.5),
    ]
)
def test_complex_custom_converter(input_value, expected):
    config = DurationConfig({"timeout": input_value})
    assert config.timeout == expected, f"Failed for input: {input_value}"

def test_to_dict_with_custom_types():
    config = FileConfig({"location": "/tmp/file.txt"})
    config_dict = config.to_dict()
    
    # Check how custom types are represented in dictionary
    assert isinstance(config_dict["location"], Path)
    assert str(config_dict["location"]) == "/tmp/file.txt"