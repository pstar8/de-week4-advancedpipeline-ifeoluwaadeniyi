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
      all_products = self.make_request('/products')
      return self._paginate(all_products, self.limit)


    def _paginate(self, data: list[dict], limit: int) -> list[dict]:
        if not isinstance(limit, int):
            raise TypeError("Limit must be an Integer")

        if limit <= 0:
            raise ValueError("Limit must be greater than Zero")

        paginated_data = []
        page = 1

        for skip in range(0, len(data), limit):
            chunk = data[skip : skip + limit] #data[0 : 0+5]  data[0:5]

            # Add a logger here instead
            print(f"Processing Page {page}: {len(chunk)} items")
            paginated_data.extend(chunk)
            page += 1

        return paginated_data
