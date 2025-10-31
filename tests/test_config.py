import pytest
from pipeline.config import ConfigManager

@pytest.fixture
def temp_config_file(tmp_path):
    config_file = tmp_path / "test_pipeline.cfg" 
    
    config_content = """[API]
                    base_url = https://fakestoreapi.com
                    url_limit = 5
                    """
    config_file.write_text(config_content)  

    return str(config_file)

def test_config_manager(temp_config_file):
    config_manager = ConfigManager(temp_config_file)
    assert config_manager.get_base_url() == 'https://fakestoreapi.com'  
    assert config_manager.get_url_limit() == 5
    assert config_manager is not None, "Failed to load configuration"

def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        ConfigManager('nonexistent_file.cfg')


def test_get_base_url(temp_config_file):
    config_manager = ConfigManager(temp_config_file)
    
    assert config_manager.get_base_url() == 'https://fakestoreapi.com'

def test_get_limit(temp_config_file):
    config_manager = ConfigManager(temp_config_file)
    
    limit = config_manager.get_url_limit()
    assert limit == 5, f"/nExpected limit to be 5, got '{limit}'"
    assert isinstance(limit, int) 

print("\n✓ All manual tests passed!")