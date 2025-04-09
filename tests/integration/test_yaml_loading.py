import os
import pytest
import tempfile
from pathlib import Path
from fancy import config as cfg



class MyConfig(cfg.BaseConfig):
    name = cfg.Option(type=str)
    count = cfg.Option(type=int)

def test_yaml_loading():
    # Create a temporary YAML file for testing
    yaml_content = """
name: Example Config
count: 42
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
        temp_file.write(yaml_content)
        temp_path = Path(temp_file.name)
    
    try:
        # Load from the YAML file
        yaml_loader = cfg.YamlConfigLoader(temp_path)
        config = MyConfig(loader=yaml_loader)
        
        # Verify values
        assert config.name == "Example Config"
        assert config.count == 42
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)

def test_yaml_loading_missing_file():
    # Test loading from a non-existent file
    non_existent_path = Path("/non/existent/path/config.yaml")
    yaml_loader = cfg.YamlConfigLoader(non_existent_path)
    
    # Should raise an appropriate error
    with pytest.raises(Exception):  # Replace with specific exception if known
        MyConfig(loader=yaml_loader)

def test_yaml_loading_with_missing_fields():
    # Create a YAML file missing the count field
    yaml_content = "name: Example Config"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as temp_file:
        temp_file.write(yaml_content)
        temp_file.flush()
        temp_file.seek(0)
        temp_path = Path(temp_file.name)
    
        yaml_loader = cfg.YamlConfigLoader(temp_path)
        config = MyConfig(yaml_loader)
        
        # 'count' is not nullable, should raise an error
        assert config.name == "Example Config"
        
        assert MyConfig.count.is_assigned(config) == False
        with pytest.raises(AttributeError):
            _ = config.count