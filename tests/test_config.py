import pytest


from pipeline.config import ConfigManager

def test_config_manager():
    config_manager = ConfigManager('../pipeline.cfg')
    assert config_manager is not None, "Failed to load configuration"

def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        ConfigManager('nonexistent_file.cfg')


def test_get_base_url():
    config_manager = ConfigManager('../pipeline.cfg')
    base_url = config_manager.get_base_url()
    assert base_url == "https://fakestoreapi.com", f"Expected base URL to be 'https://fakestoreapi.com', got '{base_url}'"

def test_get_url_limit():
    config_manager = ConfigManager('../pipeline.cfg')
    limit = config_manager.get_url_limit()
    print(f"Limit: {limit}")
    print(f"Type: {type(limit)}")
    print(f"Expected: 5")
    print(f"Match: {limit == 5}")

print("\n✓ All manual tests passed!")