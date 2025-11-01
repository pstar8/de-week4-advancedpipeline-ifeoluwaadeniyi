import pytest
import pandas as pd
from pipeline.data_analyzer import DataAnalyzer


@pytest.fixture
def enriched_data():
    return pd.DataFrame([
        {
            'id': 1,
            'title': 'Product 1',
            'price': 100.0,
            'userId': 1,
            'username': 'johnd',
            'email': 'john@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'revenue': 1000.0,  
            'quantity': 10
        },
        {
            'id': 2,
            'title': 'Product 2',
            'price': 50.0,
            'userId': 2,
            'username': 'janedoe',
            'email': 'jane@example.com',
            'firstname': 'Jane',
            'lastname': 'Doe',
            'revenue': 1000.0, 
            'quantity': 20
        },
        {
            'id': 3,
            'title': 'Product 3',
            'price': 75.0,
            'userId': 1,
            'username': 'johnd',
            'email': 'john@example.com',
            'firstname': 'John',
            'lastname': 'Doe',
            'revenue': 1125.0, 
            'quantity': 15
        }
    ])


def test_analyzer_initialization(enriched_data):
    analyzer = DataAnalyzer(enriched_data)
    
    assert hasattr(analyzer, 'enriched_df')
    assert isinstance(analyzer.enriched_df, pd.DataFrame)

def test_analyze_returns_correct_structure(enriched_data):
    analyzer = DataAnalyzer(enriched_data)
    result = analyzer.analyze()
    
    assert isinstance(result, dict)
    
    for username, metrics in result.items():
        assert 'total_revenue' in metrics
        assert 'product_count' in metrics
        assert 'average_price' in metrics


def test_total_revenue_calculation(enriched_data):
    analyzer = DataAnalyzer(enriched_data)
    result = analyzer.analyze()
    
    assert result['johnd']['total_revenue'] == 2125.0
    assert result['janedoe']['total_revenue'] == 1000.0


def test_product_count_calculation(enriched_data):
    analyzer = DataAnalyzer(enriched_data)
    result = analyzer.analyze()
    
    assert result['johnd']['product_count'] == 2
    assert result['janedoe']['product_count'] == 1


def test_average_price_calculation(enriched_data):
    analyzer = DataAnalyzer(enriched_data)
    result = analyzer.analyze()
    
    assert result['johnd']['average_price'] == 87.5
    assert result['janedoe']['average_price'] == 50.0


def test_single_seller(enriched_data):
    single_seller_data = enriched_data[enriched_data['username'] == 'johnd']
    
    analyzer = DataAnalyzer(single_seller_data)
    result = analyzer.analyze()
    
    assert len(result) == 1
    assert 'johnd' in result
    assert result['johnd']['total_revenue'] == 2125.0
    assert result['johnd']['product_count'] == 2
    assert result['johnd']['average_price'] == 87.5


def test_empty_dataframe():
    empty_df = pd.DataFrame(columns=['username', 'revenue', 'price'])
    
    analyzer = DataAnalyzer(empty_df)
    result = analyzer.analyze()
    
    assert isinstance(result, dict)
    assert len(result) == 0


def test_multiple_sellers():
    data = pd.DataFrame([
        {'username': 'alice', 'price': 100, 'revenue': 1000},
        {'username': 'bob', 'price': 50, 'revenue': 500},
        {'username': 'charlie', 'price': 75, 'revenue': 750},
        {'username': 'alice', 'price': 200, 'revenue': 2000},
    ])
    
    analyzer = DataAnalyzer(data)
    result = analyzer.analyze()
    
    assert len(result) == 3
    assert 'alice' in result
    assert 'bob' in result
    assert 'charlie' in result
    
    assert result['alice']['product_count'] == 2
    assert result['alice']['total_revenue'] == 3000.0
    assert result['alice']['average_price'] == 150.0