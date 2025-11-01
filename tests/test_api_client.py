import pytest
import requests
from pipeline.api_client import ApiClient
from unittest.mock import Mock, patch, MagicMock
from pipeline.api_client import ApiClient

@pytest.fixture
def api_client():
    base_url = 'https://fakestoreapi.com'
    url_limit = 5
    return ApiClient(base_url, url_limit)


@pytest.fixture
def sample_products():
    return [
        {'id': 1, 'title': 'Product 1', 'price': 10.99},
        {'id': 2, 'title': 'Product 2', 'price': 20.99},
        {'id': 3, 'title': 'Product 3', 'price': 30.99},
        {'id': 4, 'title': 'Product 4', 'price': 40.99},
        {'id': 5, 'title': 'Product 5', 'price': 50.99},
    ]


@pytest.fixture
def sample_users():
    return [
        {'id': 1, 'username': 'johnd', 'email': 'john@example.com'},
        {'id': 2, 'username': 'mor_2314', 'email': 'mor@example.com'},
    ]

@patch('requests.get')
def test_get_all_users_success(mock_get, api_client, sample_users):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_users
    mock_get.return_value = mock_response
    
    result = api_client.get_all_users()
    
    assert result == sample_users
    assert len(result) == 2
    mock_get.assert_called_once()  


@patch('requests.get')
def test_get_all_users_handles_errors(mock_get, api_client):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    with pytest.raises(Exception): 
        api_client.get_all_users()


@patch('requests.get')
def test_get_all_products_with_pagination(mock_get, api_client, sample_products):
    first_response = MagicMock()
    first_response.status_code = 200
    first_response.json.return_value = sample_products
    
    second_response = MagicMock()
    second_response.status_code = 200
    second_response.json.return_value = []
    
    mock_get.side_effect = [first_response, second_response]
    
    result = api_client.get_all_products()
    
    assert len(result) == 5  
    assert result == sample_products
    

@patch('requests.get')
def test_get_all_products_multiple_pages(mock_get, api_client):
    page1 = [{'id': i, 'title': f'Product {i}'} for i in range(1, 6)]    
    page2 = [{'id': i, 'title': f'Product {i}'} for i in range(6, 11)]   
    page3 = [{'id': i, 'title': f'Product {i}'} for i in range(11, 14)]  
    page4 = []  # Empty - stop here
    
    responses = []
    for page_data in [page1, page2, page3, page4]:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = page_data
        responses.append(mock_response)
    
    mock_get.side_effect = responses
    
    result = api_client.get_all_products()
    
    assert len(result) == 5
    

@patch('requests.get')
def test_get_all_products_single_page(mock_get, api_client):

    products = [
        {'id': 1, 'title': 'Product 1'},
        {'id': 2, 'title': 'Product 2'},
        {'id': 3, 'title': 'Product 3'},
    ]
    
    first_response = MagicMock()
    first_response.status_code = 200
    first_response.json.return_value = products
    
    second_response = MagicMock()
    second_response.status_code = 200
    second_response.json.return_value = []
    
    mock_get.side_effect = [first_response, second_response]
    
    result = api_client.get_all_products()
    
    assert len(result) == 3
    assert result == products


@patch('requests.get')
def test_get_all_products_handles_errors(mock_get, api_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    
    with pytest.raises(Exception):
        api_client.get_all_products()

@patch('requests.get')
def test_make_request_success(mock_get, api_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'test': 'data'}
    mock_get.return_value = mock_response
    
    result = api_client.make_request('/test')
    
    assert result == {'test': 'data'}
    mock_get.assert_called_once_with('https://fakestoreapi.com/test')


@patch('requests.get')
def test_make_request_network_error(mock_get, api_client):
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    
    with pytest.raises(Exception):
        api_client.make_request('/test')