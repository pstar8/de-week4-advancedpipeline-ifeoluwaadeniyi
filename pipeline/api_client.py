import requests


class ApiClient:
    def __init__(self, base_url, url_limit):
        self.base_url = base_url
        self.limit = url_limit
    
    def make_request(self, endpoint):
        url = self.base_url + endpoint
        
        try:
            response = requests.get(url)
            
            if response.status_code != 200:
                raise Exception(f"Error: Received status code {response.status_code} for URL {url}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error occurred: {e}")    
    
    def get_all_users(self):
        return self.make_request('/users')
    
    def get_all_products(self):
        products_dict = []

        while True:
            endpoint = f'/products?limit={self.limit}'
            products = self.make_request(endpoint)

            if not products:
                break
            
            products_dict.extend(products)
        
        return products_dict