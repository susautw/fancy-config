import pytest
from fancy import config as cfg


class ReportConfig(cfg.BaseConfig):
    width = cfg.Option(type=int, default=100)
    height = cfg.Option(type=int, default=50)
    
    # Computed only when accessed
    area = cfg.Lazy[int](lambda self: self.width * self.height)
    
    # Can depend on other computed values
    description = cfg.Lazy[str](lambda self: f"Report size: {self.area} square units")

def test_lazy_evaluation():
    config = ReportConfig()
    assert config.width == 100
    assert config.height == 50
    
    # Computed values
    assert config.area == 5000  # 100 * 50
    assert config.description == "Report size: 5000 square units"

def test_lazy_evaluation_with_custom_values():
    config = ReportConfig({"width": 200, "height": 150})
    assert config.width == 200
    assert config.height == 150
    
    # Computed values should reflect the custom values (only when first accessed)
    assert config.area == 30000  # 200 * 150
    assert config.description == "Report size: 30000 square units"
    
def test_to_dict_with_lazy_values():
    config = ReportConfig()
    config_dict = config.to_dict()
    
    assert config_dict["width"] == 100
    assert config_dict["height"] == 50
    assert config_dict["area"] == 5000
    assert config_dict["description"] == "Report size: 5000 square units"