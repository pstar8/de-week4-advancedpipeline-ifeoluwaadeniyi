import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from pipeline.pipeline import Pipeline


@pytest.fixture
def mock_config():
    config = Mock()
    config.get_base_url.return_value = 'https://fakestoreapi.com'
    config.get_url_limit.return_value = 5
    return config


@pytest.fixture
def sample_products():
    """Sample products data"""
    return [
        {'id': 1, 'title': 'Product 1', 'price': 100.0, 'rating': {'rate': 4.5, 'count': 10}},
        {'id': 2, 'title': 'Product 2', 'price': 50.0, 'rating': {'rate': 3.5, 'count': 20}},
    ]


@pytest.fixture
def sample_users():
    """Sample users data"""
    return [
        {
            'id': 1,
            'username': 'johnd',
            'email': 'john@example.com',
            'name': {'firstname': 'John', 'lastname': 'Doe'}
        }
    ]


def test_pipeline_initialization():
    pipeline = Pipeline('test_config.cfg')
    
    assert hasattr(pipeline, 'config_file')
    assert pipeline.config_file == 'test_config.cfg'


@patch('pipeline.pipeline.DataAnalyzer')
@patch('pipeline.pipeline.DataEnricher')
@patch('pipeline.pipeline.ApiClient')
@patch('pipeline.pipeline.ConfigManager')

def test_pipeline_run_integration(mock_config_class, mock_client_class, 
                                  mock_enricher_class, mock_analyzer_class,
                                  sample_products, sample_users):
    
    mock_config = Mock()
    mock_config.get_base_url.return_value = 'https://fakestoreapi.com'
    mock_config.get_url_limit.return_value = 5
    mock_config_class.return_value = mock_config
    
    mock_client = Mock()
    mock_client.get_all_products.return_value = sample_products
    mock_client.get_all_users.return_value = sample_users
    mock_client_class.return_value = mock_client
    
    mock_enricher = Mock()
    import pandas as pd
    enriched_df = pd.DataFrame([
        {
            'id': 1,
            'title': 'Product 1',
            'price': 100.0,
            'userId': 1,
            'username': 'johnd',
            'email': 'john@example.com',
            'revenue': 1000.0
        }
    ])
    mock_enricher.enrich.return_value = enriched_df
    mock_enricher_class.return_value = mock_enricher
    
    mock_analyzer = Mock()
    analysis_result = {
        'johnd': {
            'total_revenue': 1000.0,
            'product_count': 1,
            'average_price': 100.0
        }
    }
    mock_analyzer.analyze.return_value = analysis_result
    mock_analyzer_class.return_value = mock_analyzer
    
    pipeline = Pipeline('test_config.cfg')
    
    with patch.object(pipeline, 'save_results'):
        result = pipeline.run()
    
    mock_config_class.assert_called_once_with('test_config.cfg')
    mock_client_class.assert_called_once_with('https://fakestoreapi.com', 5)
    mock_client.get_all_products.assert_called_once()
    mock_client.get_all_users.assert_called_once()
    mock_enricher_class.assert_called_once()
    mock_analyzer_class.assert_called_once()
    
    assert result == analysis_result


def test_save_results(tmp_path):
    pipeline = Pipeline()
    
    test_results = {
        'johnd': {
            'total_revenue': 1000.0,
            'product_count': 1,
            'average_price': 100.0
        }
    }
    
    output_file = tmp_path / "test_output.json"
    pipeline.save_results(test_results, str(output_file))
    
    assert output_file.exists()
    
    with open(output_file, 'r') as f:
        saved_data = json.load(f)
    
    assert saved_data == test_results