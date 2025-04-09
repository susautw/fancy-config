import pytest
from fancy import config as cfg


class ServerConfig(cfg.BaseConfig):
    host = cfg.Option(type=str, required=True)
    port = cfg.Option(type=int, default=80)

class ClusterConfig(cfg.BaseConfig):
    servers = cfg.Option(type=[ServerConfig])  # List of ServerConfig objects

def test_list_config_creation():
    # Create a configuration with a list of servers
    config = ClusterConfig({
        "servers": [
            {"host": "server1.example.com", "port": 8080},
            {"host": "server2.example.com"}
        ]
    })
    
    # Verify list and its elements
    assert len(config.servers) == 2
    
    # First server
    assert config.servers[0].host == "server1.example.com"
    assert config.servers[0].port == 8080
    
    # Second server (uses default port)
    assert config.servers[1].host == "server2.example.com"
    assert config.servers[1].port == 80  # Default value

def test_empty_list():
    # Test with an empty list
    config = ClusterConfig({
        "servers": []
    })
    assert isinstance(config.servers, list)
    assert len(config.servers) == 0

def test_required_fields_in_list_elements():
    # Test missing required field in list element
    with pytest.raises(ValueError):
        ClusterConfig({
            "servers": [
                {"port": 8080}  # Missing required 'host' field
            ]
        })

def test_modifying_list():
    config = ClusterConfig({
        "servers": [
            {"host": "server1.example.com"}
        ]
    })
    
    # Initial state
    assert len(config.servers) == 1
    
    # Add a new server
    new_server = ServerConfig({"host": "server2.example.com", "port": 8080})
    config.servers.append(new_server)
    
    # Verify changes
    assert len(config.servers) == 2
    assert config.servers[1].host == "server2.example.com"
    assert config.servers[1].port == 8080
    
def test_to_dict_with_list():
    config = ClusterConfig({
        "servers": [
            {"host": "server1.example.com", "port": 8080},
            {"host": "server2.example.com"}
        ]
    })
    
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert isinstance(config_dict["servers"], list)
    assert len(config_dict["servers"]) == 2
    
    # Check list elements
    assert config_dict["servers"][0]["host"] == "server1.example.com"
    assert config_dict["servers"][0]["port"] == 8080
    assert config_dict["servers"][1]["host"] == "server2.example.com"
    assert config_dict["servers"][1]["port"] == 80