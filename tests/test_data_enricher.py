import pytest
import pandas as pd
from pipeline.data_enricher import DataEnricher


@pytest.fixture
def sample_products():
    return [
        {
            'id': 1,
            'title': 'Product 1',
            'price': 100.0,
            'userId': 1,
            'rating': {'rate': 4.5, 'count': 10}
        },
        {
            'id': 2,
            'title': 'Product 2',
            'price': 50.0,
            'userId': 2,
            'rating': {'rate': 3.5, 'count': 20}
        },
        {
            'id': 3,
            'title': 'Product 3',
            'price': 75.0,
            'userId': 1,
            'rating': {'rate': 4.0, 'count': 15}
        }
    ]


@pytest.fixture
def sample_users():
    return [
        {
            'id': 1,
            'username': 'johnd',
            'email': 'john@example.com',
            'name': {'firstname': 'John', 'lastname': 'Doe'}
        },
        {
            'id': 2,
            'username': 'janedoe',
            'email': 'jane@example.com',
            'name': {'firstname': 'Jane', 'lastname': 'Doe'}
        }
    ]


def test_enricher_initialization(sample_products, sample_users):
    enricher = DataEnricher(sample_products, sample_users)
    
    assert hasattr(enricher, 'products_df')
    assert hasattr(enricher, 'users_df')
    assert isinstance(enricher.products_df, pd.DataFrame)
    assert isinstance(enricher.users_df, pd.DataFrame)
    assert len(enricher.products_df) == 3
    assert len(enricher.users_df) == 2


def test_successful_join(sample_products, sample_users):
    enricher = DataEnricher(sample_products, sample_users)
    result = enricher.enrich()
    
    assert len(result) == 3
    
    assert 'username' in result.columns
    assert 'email' in result.columns
    assert 'firstname' in result.columns
    assert 'lastname' in result.columns
    
    product1 = result[result['id'] == 1].iloc[0]
    assert product1['username'] == 'johnd'
    assert product1['email'] == 'john@example.com'


def test_missing_user_edge_case(sample_products, sample_users):
    products_with_missing = sample_products + [
        {
            'id': 4,
            'title': 'Product 4',
            'price': 200.0,
            'userId': 999,  # doesn't exist!
            'rating': {'rate': 5.0, 'count': 5}
        }
    ]
    
    enricher = DataEnricher(products_with_missing, sample_users)
    result = enricher.enrich()
    
    assert len(result) == 4
    
    product4 = result[result['id'] == 4].iloc[0]
    assert pd.isna(product4['username'])
    assert pd.isna(product4['email'])


def test_revenue_calculation(sample_products, sample_users):
    enricher = DataEnricher(sample_products, sample_users)
    result = enricher.enrich()
    
    assert 'revenue' in result.columns
    

    product1 = result[result['id'] == 1].iloc[0]
    assert product1['revenue'] == 1000.0
    
    product2 = result[result['id'] == 2].iloc[0]
    assert product2['revenue'] == 1000.0
    
    product3 = result[result['id'] == 3].iloc[0]
    assert product3['revenue'] == 1125.0


def test_extract_user_fields(sample_users):
    enricher = DataEnricher([], sample_users)
    
    users_df = pd.DataFrame(sample_users)
    extracted = enricher.extract_user_fields(users_df)
    
    expected_columns = ['userId', 'username', 'email', 'firstname', 'lastname']
    assert all(col in extracted.columns for col in expected_columns)
    
    assert 'name' not in extracted.columns
    
    user1 = extracted[extracted['userId'] == 1].iloc[0]
    assert user1['firstname'] == 'John'
    assert user1['lastname'] == 'Doe'